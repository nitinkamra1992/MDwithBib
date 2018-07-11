# MDwithBib

This tool allows working with Bibtex-style bibliographies for Markdown files. It requires two inputs: (i) a markdown file which supports a custom syntax (described below) to include bibtex references, and (ii) a bibtex-style bibliography file.  
It generates another markdown file as output, which has all the custom syntax replaced appropriately using references from the bibliography. This output markdown file can then be directly rendered or converted to other formats (say with [pandoc](https://pandoc.org/)).

## Compatibility

The tool has been written for Ubuntu and tested on Python v3.5 and above but is also compatible with previous and newer versions of python3.

## Dependencies

Requires python3, the `re` and `argparse` packages from Python Standard Library and the `bibtexparser` package (available via pip):

```
pip install bibtexparser
```

## Usage

This tool has been written primarily for the purpose of maintaining academic reading lists in Github Flavored Markdown (GFM). The tool can be run as a Python script, e.g.:
```bash
python3 md_with_bib.py <infile> -b <bibfile> -o <outfile>
```

It accepts the following command-line arguments:
```
infile: Path of input markdown file.
-b, --bibfile: Path of bibtex-style bibliography file. Default: 'biblio.bib'.
-o, --outfile: Path of output markdown file. Default: 'result.md'.
```

To refer attributes of a bibtex reference, the following syntax can be used anywhere in the input markdown file:
```
[@<bib_ref_ID>:<bib_ref_cmd>]
```
where `<bib_ref_ID>` is the unique bibtex ID of the reference and `<bib_ref_cmd>` is the command to be executed for the reference.

Currently the following commands are supported for `<bib_ref_cmd>`:

  - `title`: Display `title` attribute of the reference (see **Note 1** below).
  - `subtitle`: Display `subtitle` attribute of the reference (for bibentries of type `book`).
  - `journal`: Display `journal` attribute of the reference (for bibentries of type `article`).
  - `author`: Display `author` attribute of the reference (in *et al.* format; see **Note 2** below).
  - `authors`: Display full list of authors for the reference (see **Note 2** below).
  - `cite`: Displays a label for the reference in <Author *et al.*, year> format and inserts the full citation for that reference in the reference list at the bottom of the output markdown file (see **Note3** below).
  - `booktitle`: Display the `booktitle` attribute of the reference (for bibentries of type `inproceedings`).
  - `series`: Display the `series` attribute of the reference.
  - `month`: Display the `month` attribute of the reference.
  - `year`: Display the `year` attribute of the reference.
  - `citation`: Displays the full citation for the reference. Unlike the `cite` command which adds a label at the location of the custom syntax and the actual citation in the references at the bottom, the `citation` command adds the full citation at the location of the custom syntax.
  - `URL`: Display the `URL` attribute of the reference.
  - `full`: Displays the reference like a header with a title in the current line, followed by the full list of authors in the subsequent line, followed by a few other attributes and the year in the next line.

Note that even though bibtex supports citations for many entry types, this tool mostly focuses on the following entry types: `inproceedings`, `article`, `book`, `phdthesis` and `mastersthesis`. When citing other entry types it still produces a basic citation with the `author`, `title` and `year` fields (see **Note 4** below).

## Example

For a working example which uses the custom syntax with a variety of the above commands, execute the following on the command-line:
```bash
python3 md_with_bib.py example/input.md -b example/biblio.bib -o example/output.md
```
The above uses the sample input files in the example folder. A copy of the generated output file (output.md) is already present in the example folder for reference.

## Notes

#### Note 1:
The title of any reference is automatically linked to its URL (if provided for the reference in the bibtex file). This is true regardless of whether the title is refered to individually via `title` command or as a part of a citation.

#### Note 2:
For bibentries of type `book`, the `editor` attribute in `--bibfile` is checked before the `author` attribute when using `author` or `authors` command for `<bib_ref_cmd>`. Exactly one of `editor` or `author` attributes is expected for bibentry of type `book`. If both are provided, the `editor` attribute overrides `author`.

#### Note 3:
Since academic documents often require multiple citations simultaneously, the above custom syntax allows having multiple `cite` commands in a single pair of square brackets. Such references should be separated by semi-colons. Note that multiple references in a single pair of square brackets are only allowed for the `cite` command. All other commands must have a square bracket of their own. In any square bracket containing multiple commands, all commands are treated as `cite` regardless of what the actual commands are.

**Example 1** - Valid multiple `cite` commands in a single square bracket:
```
Many more advancements have been made along these lines [@zenke2014:cite; @silver2011:cite].
```

**Example 2** - Invalid multiple commands in a single square bracket:
```
Many more advancements have been made along these lines [@zenke2014:author; @silver2011:title]
```
is still treated as:
```
Many more advancements have been made along these lines [@zenke2014:cite; @silver2011:cite].
```

#### Note 4:
For citation purposes, every bibentry must have at least the following attributes: `author` (or `editor` for entry of type `book`), `title` and `year`. Additionally entries of type `inproceedings` must have a `booktitle` attribute and entries of type `article` must have a `journal` attribute.