#! /usr/bin/python3

# System imports
import argparse
import re

# Package imports
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode, author, editor, page_double_hyphen


def customizations(record):
    """Use some functions delivered by the library

    :param record: a record
    :returns: -- customized record
    """
    record = convert_to_unicode(record)
    # record = type(record)
    record = author(record)
    record = editor(record)
    # record = journal(record) # Do not use!
    # record = keyword(record)
    # record = link(record)
    record = page_double_hyphen(record)
    # record = doi(record)
    return record


def load_bibtex(bibfile, customizer=None):
    # Open and parse the BibTeX file in `bibfile` using
    # `bibtexparser`
    with open(bibfile, 'r') as bib_file:
        bp = BibTexParser(bib_file.read(), customization=customizer)

    # Get a dictionary of dictionaries of key, value pairs from the
    # BibTeX file. The structure is
    # {ID:{authors:...},ID:{authors:...}}.
    refsdict = bp.get_entry_dict()

    return refsdict


class Processor:
    def __init__(self, refsdict):
        self.refsdict = refsdict
        # Check that all references have populated author, title and year fields
        for k, v in self.refsdict.items():
            assert 'author' in v or 'editor' in v, 'Missing field author/editor in {}'.format(k)
            assert 'title' in v, 'Missing field title in {}'.format(k)
            assert 'year' in v, 'Missing field year in {}'.format(k)

    def gen_replacement(self, match, skip_types=None):
        match_type = self.get_match_type(match.group())
        if skip_types is not None and match_type in skip_types:
            return None, None
        else:
            func = getattr(self, 'process_' + match_type, None)
            if func is not None:
                if match_type == 'multicite':
                    match_strings = [string.strip() for string in match.group()[1:-1].split(';')]
                    refIDs = [self.get_reference_ID(match_string) for match_string in match_strings]
                    for refID in refIDs:
                        assert refID in self.refsdict, 'Reference {} not found'.format(refID)
                    return func([self.refsdict[refID] for refID in refIDs])
                else:
                    refID = self.get_reference_ID(match.group())
                    assert refID in self.refsdict, 'Reference {} not found'.format(refID)
                    return func(self.refsdict[refID])
            return None, None

    def get_match_type(self, match_string):
        match_string = match_string.strip()
        if ';' in match_string and ':cite' in match_string:
            return 'multicite'
        elif ':cite' in match_string:
            return 'cite'
        else:
            assert ('@' in match_string and ':' in match_string and '[' in match_string and ']' in match_string), \
            'match_string must contain an at-symbol, a colon, a left and a right square bracket.'
            pos_colon = match_string.find(':')
            pos_rbracket = match_string.find(']')
            return match_string[pos_colon + 1 : pos_rbracket].strip()

    def get_reference_ID(self, match_string):
        match_string = match_string.strip()
        assert ('@' in match_string and ':' in match_string), \
            'match_string must contain an at-symbol and a colon.'
        pos_colon = match_string.find(':')
        pos_at = match_string.find('@')
        return match_string[pos_at + 1 : pos_colon].strip()

    def process_title(self, ref):
        if 'url' in ref:
            return '[' + ref['title'] + '](' + ref['url'] + ')', None            
        else:
            return ref['title'], None            

    def process_subtitle(self, ref):
        return ref.get('subtitle', None), None

    def process_journal(self, ref):
        return ref.get('journal', None), None

    def process_author(self, ref):
        if ref['ENTRYTYPE'].lower() == 'book' and 'editor' in ref:
            authors_list = [editor['name'] for editor in ref['editor']]
        else:
            authors_list = ref['author']
        num_authors = len(authors_list)
        if num_authors == 1:
            return authors_list[0].split(',')[0].strip(), None
        elif num_authors == 2:
            return authors_list[0].split(',')[0].strip() + \
                   ' and ' + authors_list[1].split(',')[0].strip(), None
        elif num_authors >= 3:
            return authors_list[0].split(',')[0].strip() + ' *et al.*', None

    def process_authors(self, ref):
        if ref['ENTRYTYPE'].lower() == 'book' and 'editor' in ref:
            authors_list = [editor['name'] for editor in ref['editor']]
        else:
            authors_list = ref['author']
        processed_authors_list = []
        for author in authors_list:
            a_name = author.split(',')
            a_name[0] = a_name[0].strip()
            a_name[1] = a_name[1].strip()
            processed_authors_list.append(a_name[1] + ' ' + a_name[0])
        if len(processed_authors_list) == 1:
            return processed_authors_list[0], None
        elif len(processed_authors_list) == 2:
            return processed_authors_list[0] + ' and ' + processed_authors_list[1], None
        elif len(processed_authors_list) >= 3:
            processed_authors_list[-1] = 'and ' + processed_authors_list[-1]
            return ', '.join(processed_authors_list), None

    def process_cite(self, ref):
        author = self.process_author(ref)[0]
        label = '[' + author + ', ' + ref['year'] + ']'
        citation = label + ' ' + self.process_citation(ref)[0]
        return label, citation

    def process_multicite(self, refs):
        labels = []
        citations = []
        for ref in refs:
            author = self.process_author(ref)[0]
            label = author + ', ' + ref['year']
            labels.append(label)
            citations.append('[' + label + '] ' + self.process_citation(ref)[0])
        multilabel = '[' + '; '.join(labels) + ']'
        multicitation = '\n  - '.join(citations)
        return multilabel, multicitation

    def process_booktitle(self, ref):
        return ref.get('booktitle', None), None

    def process_series(self, ref):
        return ref.get('series', None), None

    def process_month(self, ref):
        return ref.get('month', None), None

    def process_year(self, ref):
        return ref['year'], None

    def process_citation(self, ref):
        authors = self.process_authors(ref)[0]
        title = self.process_title(ref)[0]
        time = ref['year']
        if 'month' in ref:
            time = ref['month'] + ' ' + time

        if ref['ENTRYTYPE'].lower() == 'book':
            if 'subtitle' in ref:
                title = title + '. ' + ref['subtitle']
            citation = authors + '. *' + title + '*. '
            if 'publisher' in ref:
                citation = citation + ref['publisher'] + ', '

        elif 'thesis' in ref['ENTRYTYPE'].lower():
            citation = authors + '. *' + title + '*. '
            if ref['ENTRYTYPE'].lower() == 'phdthesis':
                citation = citation + 'PhD thesis, '
            elif ref['ENTRYTYPE'].lower() == 'mastersthesis':
                citation = citation + 'Masters thesis, '
            if 'school' in ref:
                citation = citation + ref['school'] + ', '

        elif ref['ENTRYTYPE'].lower() == 'inproceedings':
            citation = authors + '. ' + title + '. '
            citation = citation + 'In *' + ref['booktitle'] + '*, '
            if 'pages' in ref:
                citation = citation + 'pages ' + ref['pages'] + ', '

        elif ref['ENTRYTYPE'].lower() == 'article':
            citation = authors + '. ' + title + '. '
            citation = citation + '*' + ref['journal'] + '*, '
            if 'volume' in ref and 'number' in ref and 'pages' in ref:
                citation = citation + ref['volume'] + '(' + ref['number'] + '):' + ref['pages'] + ', '

        else:
            citation = authors + '. *' + title + '*. '

        citation = citation + time + '.'

        return citation, None

    def process_URL(self, ref):
        return ref.get('url', None), None

    def process_full(self, ref):
        authors = self.process_authors(ref)[0]
        title = self.process_title(ref)[0]
        time = ref['year']

        if 'month' in ref:
            time = ref['month'] + ' ' + time
        if ref['ENTRYTYPE'].lower() == 'book' and 'subtitle' in ref:
            title = title + '. ' + ref['subtitle'] + '.'

        citation = '**' + title + '**\n  *' + authors + '*\n  '
        if ref['ENTRYTYPE'].lower() == 'book':
            if 'publisher' in ref:
                citation = citation + ref['publisher'] + ', '
        elif 'thesis' in ref['ENTRYTYPE'].lower():
            if ref['ENTRYTYPE'].lower() == 'phdthesis':
                citation = citation + 'PhD thesis, '
            elif ref['ENTRYTYPE'].lower() == 'mastersthesis':
                citation = citation + 'Masters thesis, '
            if 'school' in ref:
                citation = citation + ref['school'] + ', '
        elif ref['ENTRYTYPE'].lower() == 'inproceedings':
            citation = citation + ref['booktitle'] + ', '            
        elif ref['ENTRYTYPE'].lower() == 'article':
            citation = citation + ref['journal'] + ', '
        citation = citation + time

        return citation, None        


def main(args):
    infile = args.infile
    bibfile = args.bibfile
    outfile = args.outfile

    refsdict = load_bibtex(bibfile, customizer=customizations)

    # Read infile
    with open(infile, 'r') as inf:
        inputs = inf.read()

    # Process locations of replacement patterns
    matches = list(re.compile('\[[\s]*@\w*:\w*[\s]*\]').finditer(inputs))
    cites = list(re.compile('\[[\w\s@:;]*@\w*:cite[\w\s@:;]*\]').finditer(inputs))

    # Generate replacement and append strings for each reference
    processor = Processor(refsdict)
    all_matches = []
    for match in matches:
        replace_str, append_str = processor.gen_replacement(match)
        all_matches.append((match, replace_str, append_str))
    for match in cites:
        replace_str, append_str = processor.gen_replacement(match, skip_types=['cite'])
        all_matches.append((match, replace_str, append_str)) # duplication from cites is fine due to skip_types

    # Sort all_matches according to start position of match
    all_matches = sorted(all_matches, key=lambda j_match: j_match[0].start())

    # Generate output string
    outputs = inputs
    offset = 0
    for j_match in all_matches:
        match = j_match[0]        
        replace_str = j_match[1]
        replace_start = offset + match.start()
        if replace_str is not None:
            outputs = outputs[:replace_start] + outputs[replace_start:].replace(match.group(), replace_str, 1)
            offset += len(replace_str) - len(match.group())

    # Append references to output string
    appends = '\n' if outputs.endswith('\n') else '\n\n'
    appends = appends + '## References\n'
    for j_match in all_matches:
        match = j_match[0]
        append_str = j_match[2]
        if append_str is not None:
            appends = appends + '\n  - ' + append_str
    outputs = outputs + appends

    # Write output to file
    with open(outfile, mode='w') as outf:
        outf.write(outputs)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Replace references in a markdown file with proper attributes from a bib file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    arg_parser.add_argument("infile",
        help="Path to the input markdown file.",
        type=str)
    arg_parser.add_argument("-b", "--bibfile",
        help="Path to the BibTeX reference file.",
        default="biblio.bib",
        type=str)
    arg_parser.add_argument("-o", "--outfile",
        help="Path for the output markdown file.",
        default="result.md",
        type=str)

    args = arg_parser.parse_args()
    main(args)
