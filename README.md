# Mason_Gain
This code is used to calculate Transfer Function between any two nodes of a Signal Flow Graph upto 4 non-touching loops.
# Code is seen as Follows:
1. BFS path planning algorithm to calculate Forward Paths and Closed Loops.
2. Travellling Sales Man problem for closed loops paths.
3. Removal of Duplicate Loops based on commutative property.
4. Forced iteration method for non-touching loops pairing.

# Conditions for using Code:
This code works for problems involving upto 4 non-touching loops between any 2 nodes across which transfer function needs to be calculated.
This code does not work for weights between two nodes as variable however user can allot random weights and see the console for all the paths.

# System Requirement:
1. Opencv installation is required ( otherwise comment out its import and show_sfg() function. This disables SFG visualization)
2. Numpy installation is required.
3. PIL installation is required.
