## Introduction
An intelligent agent designed to find optimal solutions for the Rush Hour puzzle game using various search algorithms. The study examines and compares the properties and efficiency of each algorithm in searching for solutions.
<br><br>
Search algorithms implemented include:
- Breadth-first search (BFS)
- Iterative deepening depth-limited search (IDDLS)
- A* search (Heuristic approach)
- Hill climbing search (Random restart & greedy search)

## Technologies Used
- Language: Python

## Search Algorithms
### Breadth-First Search (BFS)
BFS is a startegy in which the root node is expanded first, followed by its successors of the root node before proceesing to their succesors, and so on. The nodes in the same depth are expanded and explored before any nodes at the next level are visited. In short, the shallowest unexpanded node is chosen for expansion first.

### Iterative Deepening Depth-Limited Search (IDDLS)
Depth-limited search is basically depth-first search with depth limit. It assumes that the nodes at depth 'l' have no successors and immediately stop the search once all the nodes in depth 'l' are explored. Iterative deepening search is an algorithm that repeatedly applies depth-limited search with increasing limits. It terminates when a solution is found or when no solution is found after all the deepest nodes are expanded, returning a failure.

### A* Search
This is a stategy that finds the cheapest path by avoiding the algorithm from expanding paths that are already expensive even before reaching the goal state. A* uses an evaluation function to estimate the total path cost, as shown below:
```
f(n) = g(n) + h(n), where

f(n) = Estimated total path cost through n to goal
g(n) = Actual cost from the starting point to n
h(n) = Estimated path cost from n to goal
```
*Note that h(n) is an admissible heuristic, meaning that h(n) never overestimates the actual total path cost. h(n) is always smaller or equal to h*(n), the true cost from n to goal.*

### Hill Climbing Search
Hill climbing search chooses the best neighbour state in its neighbourhood to expand. This process is repeated until a local maximum(solution) is found. Stochastic hill climbing and random restart hill climbing are implented in this algorithm.


## Output
### Output Text File
The solutions generated by each algorithm are printed to an output text file.

### Console
For each problem, these will be printed on the console:
1. Problem number and its game level
2. Initial state
3. Game board of initial state
4. Given solution
5. For BFS, IDDLS and A* search,
    - Solution found
    - Execution time
    - Path cost(Depth)
    - Difference of length between given solution and found solution
    - Number of explored nodes
6. For hill climbing search,
    - Local solution or actual solution
    - Execution time
    - Path cost(Depth)
    - Difference of length between given solution and found solution
    - Number of explored node
    - Game board of final state

### Output Example
```
Problem 9 (Beginner)
Initial State: .ABBCC.A.DEEXX.DOFPQQQOFP.G.OHP.G..H
+-------------+
| . A B B C C |
| . A . D E E |
| X X . D O F  ==>
| P Q Q Q O F |
| P . G . O H |
| P . G . . H |
+-------------+
Given Solution: OD1 XR1 PU3 QL1 DD2 XR2 AD1 EL1 BL1 CL1 FU2 XR3
A*
Solution Found: OD1 XR1 PU3 QL1 DD2 EL1 XR1 AD1 BL1 CL1 FU2 XR2 
CPU Time: 502.23 Path Cost: 12 Diff: 0 Explored: 20687
```

## Developer
Loo<br>
loo.workspace@gmail.com