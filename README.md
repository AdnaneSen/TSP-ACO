# TSP-ACO

-This project aims to solve the Traveling Salesman Problem (TSP) using Ant Colony Optimization (ACO). 

-The goal is to determine the optimal route for the traveler to visit all cities. The resolution method involves using ant colony stigmergy
 to find the best possible path. Each ant leaves a certain amount of pheromone on its way and follows the paths with the greatest amount of it.
 
-To implement this, the "TSP_Ant_colony.py" code uses object-oriented programming and introduces five classes: Node, Edge, Graph, Ant, and ACO,
 defining the environment and solving the TSP problem.
 
-For the purpose of visualizing the output, you can find two images. The first one shows a map of France with 10 nodes representing cities "carte.png", and 
the second one shows the optimal path marked with a red line "sol_carte.png" The Python code returns the optimal distance as well as a list of nodes to follow in order, along with their coordinates.

-The code "Interface_TSP.py" (to be placed in the same file as the previous code) is an implementation of an interface that allows the user to freely create nodes on a 500x400 frame. After creating the nodes, the user can click on the "Résoudre" (Solve) button to execute the algorithm, display the optimal distance, and draw the best path. The user can also adjust the parameters from the interface, such as the "number of ants," "number of iterations," and "pheromone evaporation rate"... There two images "interface_test.png" and "interface_test_result.png" are showing this interface as well as the results.
