# CS 170 Project Fall 2021
Instructions on how to run the code:
1. Make sure the following file folders exist before running the code:
outputs/small, outputs/medium, outputs/large
2. Make sure the input files exist on the same directory: in the directory solver.py is in, make sure inputs/small/..., inputs/medium/..., and inputs/large/... exist and all the corresponding inputs to run are within. This is the same file structure as the inputs provided.
3. To change the intervals used to generate dummy tasks in the dynamic programming solution, change the numbers in the dummy_intervals array in the file solver_s.py. Some explanation of the intervals will be in the project reflection. Different intervals were used to generate different outputs, so the outputs from the included set of intervals may differ from the results submitted to the leaderboard.
4. To generate outputs, run solver.py. Make sure the imports on this file are working. No non-standard libraries are used.
It takes around 1 min to process 4 small inputs, 2 medium inputs, or 1 large input. 

Requirements: Python 3.7. Everything in this file uses Python 3.7.

Files:
- `parse.py`: functions to read/write inputs and outputs
- `solver.py`: main file to run to generate outputs as above, contains Ben's algorithm
- `solver_s.py`: second solver to run to generate outputs as above, contains the DP algorithm
- `solver_ddl.py`: third solver to run to generate outputs. It has poor performance so it exists but is not used.
- `Task.py`: contains a class that is useful for processing inputs
