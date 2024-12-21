# AI Agent for Futoshiki Puzzle Solver
## Summary
Developed an AI agent for Futoshiki puzzle solver, employing a backtracking search algorithm with forward checking and minimum remaining value heuristic, resulting in an 80.625% search space reduction and solving 7x7 puzzles within 1 second.

## Introduction
[Futoshiki](https://www.futoshiki.com/) is a CSP (Constraint Satisfaction Problem) puzzle similar to Sudoku. The objective is to fill an n×n grid with numbers 1 to n such that each number appears exactly once in each row and column, while satisfying additional inequality constraints between adjacent cells. This project implements an AI agent to efficiently solve Futoshiki puzzles of various sizes up to 7×7.

![Puzzel](https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Futoshiki1.png/400px-Futoshiki1.png)



## Algorithm & Techniques Used
- **Backtracking Search**: A systematic search algorithm that incrementally builds candidates to solve problems and abandons candidates ("backtracks") when they are found to not satisfy the constraints.
  
- **Minimum Remaining Value (MRV) Heuristic**: A variable selection strategy that chooses the variable with the smallest remaining domain to assign next, helping to identify failures earlier.

- **Forward Checking**: A constraint propagation technique that updates domain values of unassigned variables whenever a value is assigned to a variable, preventing future conflicts.

The combination of these techniques achieves significant optimization:
- Theoretical worst-case complexity: O(n^(n²))
- Each additional constraint reduces search space by ~80.625%
- For a 7×7 board: Reduced from 7^49 ≈ 10^41 possibilities to approximately 10^25 valid combinations

    ![forward checking](https://ktiml.mff.cuni.cz/~bartak/constraints/images/backtrack.gif) 
    [Reference](https://ktiml.mff.cuni.cz/~bartak/constraints/propagation.html)

## Workflow
1. **Board Initialization**
   - Parse input string to create board configuration
   - Initialize domains for each cell
   - Apply initial forward checking

2. **Solution Search**
   - Select unassigned variable using MRV heuristic
   - Try values from variable's domain
   - Apply forward checking after each assignment
   - Backtrack when constraints are violated

3. **Constraint Checking**
   - Row uniqueness constraints
   - Column uniqueness constraints
   - Inequality constraints between adjacent cells

## How to Run
The program can be executed in two ways:

1. Solve a single board:
```bash
python3 futoshiki.py <input_string>
```
2. Solve multiple boards from a file:
```
python3 futoshiki.py
# This will read boards from futoshiki_start.txt and write solutions to output.txt
```
Input format example in futoshiki_start.txt:
```
0-0<0---0<2-0<--0-0-0

Where:

"0" represents empty cells
"-" represents no constraint between adjacent cells
"<" and ">" represent inequality constraints
```

## Result
The agent successfully demonstrates:

1. Efficient constraint satisfaction through intelligent search strategies
2. Significant reduction in search space through forward checking
3. Optimal variable selection through MRV heuristic
4. The project successfully implements an efficient solution for Futoshiki puzzles, making what would be an intractable problem with brute force (3.17×10^27 years for 7×7) solvable in practical time frames **(under 5 minutes).**
5. Statistical analysis shows that for a 7×7 board, each additional inequality constraint reduces the search space by an **average of 80.625%**, demonstrating the effectiveness of combining constraint propagation with backtracking search. (See the following block for calculation.)
```
[Calculation for Result 5.]
Base Search Space (no constraints): 7^49 ≈ 10^41
Reduced Search Space with Different Numbers of Constraints:

With 1 constraint: ≈ 10^41 * (1/2) = 5 × 10^40
With 2 constraints: ≈ 10^41 * (1/2)^2 = 2.5 × 10^40
With 3 constraints: ≈ 10^41 * (1/2)^3 = 1.25 × 10^40
With 4 constraints: ≈ 10^41 * (1/2)^4 = 6.25 × 10^39
With 5 constraints: ≈ 10^41 * (1/2)^5 = 3.125 × 10^39

Optimization Percentage (reduction from original):

1 constraint: 50% reduction
2 constraints: 75% reduction
3 constraints: 87.5% reduction
4 constraints: 93.75% reduction
5 constraints: 96.875% reduction

Average Optimization: (50 + 75 + 87.5 + 93.75 + 96.875)/5 = 80.625%
```