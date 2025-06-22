# SAT-Solver

This is a Python program that solves SAT problems. A SAT problem asks:  
> Can we assign True or False to variables so that a logic formula becomes True?

This project includes several different methods to try to solve SAT problems.

# What this program does

- Reads SAT problems written in DIMACS CNF
- Solves the problems using:
  - Brute-force search
  - A smarter branching method
  - The DPLL algorithm
  - Unit propagation 
- Prints the answers
- Runs built-in tests to make sure everything works

# Files included

- Sat_Solver_Final.py - Main Python program
- sat.txt - Example SAT problem (solvable) 
- unsat.txt - Example SAT problem (unsolvable)
