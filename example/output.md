# Reading List

This is a reading list for literature on **multirobot task scheduling**.

## Main reading

Scheduling problems often arise in teams of robots trying to accomplish persistent tasks. For anyone trying to survey the field of multirobot task scheduling, this reading list describes some good resources to begin with.

Some early examples of persistent multirobot scheduling are the works [Smith *et al.*, 2010; Stump and Michael, 2011; Toksoz *et al.*, 2011]. Ethan Stump and Nathan Michael have designed a scheduling algorithm for persistent surveillance planning for teams of robots in their work [Multi-robot persistent surveillance planning as a Vehicle Routing Problem](https://ieeexplore.ieee.org/document/6042503/). Toksoz *et al.* have implemented automated battery swapping for multirobot systems and Smith *et al.* have studied the vehicle-routing problem for a team of two autonomous vehicles.

A more recent work by Nitin Kamra and Nora Ayanian titled [A mixed integer programming model for timed deliveries in multirobot systems](https://ieeexplore.ieee.org/document/7294146/?arnumber=7294146&tag=1) combines all the above works to design a routing planner for a persistent multirobot system which involves many worker robots providing services and being kept alive by autonomous delivery robots continuously exchanging their batteries [Kamra and Ayanian, 2015]. For a detailed introductory text on operations research solutions to multirobot path planning and vehicle routing, see the book The Vehicle Routing Problem by Toth and Vigo [Toth and Vigo, 2001].

## For further reading

For further reading also see: 

  - Jonghoe Kim and James R. Morrison. On the Concerted Design and Scheduling of Multiple Resources for Persistent UAV Operations. *Journal of Intelligent and Robotic Systems*, 74(1-2):479--498, 2014.
  - Rafael Lazimy. Mixed-integer quadratic programming. *Mathematical Programming*, 22(1):332--349, 1982.

## References

  - [Smith *et al.*, 2010] Stephen L. Smith, Marco Pavone, Francesco Bullo, and Emilio Frazzoli. Dynamic Vehicle Routing with Priority Classes of Stochastic Demands. *SIAM J. Control and Optimization*, 48(5):3224--3245, 2010.
  - [Stump and Michael, 2011] Ethan Stump and Nathan Michael. [Multi-robot persistent surveillance planning as a Vehicle Routing Problem](https://ieeexplore.ieee.org/document/6042503/). In *IEEE Conf. on Automation Science and Engineering*, pages 569--575, 2011.
  - [Toksoz *et al.*, 2011] Tuna Toksoz, Joshua Redding, Matthew Michini, Bernard Michini, Jonathan P. How, Matthew Vavrina, and John Vian. Automated Battery Swap and Recharge to Enable Persistent UAV Missions. In *AIAA Infotech@Aerospace*, Mar 2011.
  - [Kamra and Ayanian, 2015] Nitin Kamra and Nora Ayanian. [A mixed integer programming model for timed deliveries in multirobot systems](https://ieeexplore.ieee.org/document/7294146/?arnumber=7294146&tag=1). In *IEEE International Conference on Automation Science and Engineering (CASE)*, pages 612--617, August 2015.
  - [Toth and Vigo, 2001] Paolo Toth and Daniele Vigo. *The Vehicle Routing Problem*. Society for Industrial and Applied Mathematics, 2001.