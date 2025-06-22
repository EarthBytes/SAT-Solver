# Question 6:

import os
os.chdir(os.path.dirname(__file__))

def load_dimacs(filename):
    clauses = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('p cnf'):
                continue
            clause = list(map(int, line.strip().split()))
            if clause and clause[-1] == 0:
                clause.pop()
            clauses.append(clause)
    return clauses
clauses = load_dimacs("sat.txt")
print(clauses)

# Question 7:

import itertools
def simple_sat_solve(clauses):
    variables = {abs(literal) for clause in clauses for
literal in clause}
    for assignment in itertools.product([True, False],
repeat=len(variables)):
        truth_assignment = dict(zip(variables, assignment))
        if all(any(truth_assignment[abs(literal)] if literal >
0 else not truth_assignment[abs(literal)] for literal in
clause) for clause in clauses):
            return [literal if truth_assignment[abs(literal)]
else -literal for literal in variables]
    return False
clauses = [[1, -2], [-1, 3]]
result = simple_sat_solve(clauses)
print(result)

 # Question 8:

def branching_sat_solve(clauses, partial_assignment):
    if all(is_clause_satisfied(clause, partial_assignment) for
clause in clauses):
        return partial_assignment
    unassigned_vars = get_unassigned_variables(clauses,
partial_assignment)
    if not unassigned_vars:
        return False
    var = unassigned_vars[0]
    result_true = branching_sat_solve(clauses,
partial_assignment + [var])
    if result_true:
        return result_true
    result_false = branching_sat_solve(clauses,
partial_assignment + [-var])
    if result_false:
        return result_false
    return False
def is_clause_satisfied(clause, partial_assignment):
    return any(literal in partial_assignment for literal in
clause)
def get_unassigned_variables(clauses, partial_assignment):
    assigned_vars = {abs(lit) for lit in partial_assignment}
    return list({abs(literal) for clause in clauses for
literal in clause if abs(literal) not in assigned_vars})
clause_set = [[1, -2], [-1, 2, 3], [-3, 2]]
partial_assignment = []
solution = branching_sat_solve(clause_set, partial_assignment)
if solution:
    print("Valid assignment exists:", solution)
else:
    print("No valid assignment exists")

 # Question 9:

def unit_propagate(clauses):
    while True:
        unit_clauses = [clause for clause in clauses if sum(1
for lit in clause if lit != 0) == 1]
        if not unit_clauses:
            break
        for unit_clause in unit_clauses:
            unit_literal = unit_clause[0]
            clauses = apply_unit_propagation(clauses,
unit_literal)
    return clauses

def apply_unit_propagation(clauses, literal):
    new_clauses = []
    for clause in clauses:
        if literal in clause:
            continue
        reduced_clause = [lit for lit in clause if lit != -literal]
        new_clauses.append(reduced_clause)
    return new_clauses

clause_set = [[1, -2], [-1, 2, 3], [-3, 2]]
updated_clauses = unit_propagate(clause_set)
print("Clause set after unit propagation:", updated_clauses)

# Question 10:

def dpll_sat_solve(clauses, partial_assignment, all_vars):
    clauses = unit_propagate(clauses)

    if not clauses:
        assigned_vars = {abs(lit) for lit in partial_assignment}
        remaining_vars = all_vars - assigned_vars
        return partial_assignment + list(remaining_vars)

    if any(len(clause) == 0 for clause in clauses):
        return False

    unassigned_vars = get_unassigned_variables(clauses, partial_assignment)
    if not unassigned_vars:
        assigned_vars = {abs(lit) for lit in partial_assignment}
        remaining_vars = all_vars - assigned_vars
        return partial_assignment + list(remaining_vars)

    var = unassigned_vars[0]

    result_true = dpll_sat_solve(
        unit_propagate_with_assignment(clauses, var),
        partial_assignment + [var],
        all_vars
    )
    if result_true:
        return result_true

    result_false = dpll_sat_solve(
        unit_propagate_with_assignment(clauses, -var),
        partial_assignment + [-var],
        all_vars
    )
    if result_false:
        return result_false

    return False

def unit_propagate(clauses):
    while True:
        unit_clauses = [c for c in clauses if len(c) == 1]
        if not unit_clauses:
            break
        for unit_clause in unit_clauses:
            unit_literal = unit_clause[0]
            clauses = apply_unit_propagation(clauses, unit_literal)
    return clauses

def unit_propagate_with_assignment(clauses, literal):
    return apply_unit_propagation(clauses, literal)

def apply_unit_propagation(clauses, literal):
    new_clauses = []
    for clause in clauses:
        if literal in clause:
            continue
        new_clause = [lit for lit in clause if lit != -literal]
        new_clauses.append(new_clause)
    return new_clauses

def get_unassigned_variables(clauses, partial_assignment):
    assigned_vars = {abs(lit) for lit in partial_assignment}
    vars_in_clauses = {abs(lit) for clause in clauses for lit in clause}
    return list(vars_in_clauses - assigned_vars)

clauses = [[1, -2], [-1, 2, 3], [-3, 2]]
partial_assignment = []
all_vars = {abs(lit) for clause in clauses for lit in clause}

solution = dpll_sat_solve(clauses, partial_assignment, all_vars)

if solution:
    print("Satisfying assignment found:", sorted(solution, key=abs))
else:
    print("No satisfying assignment found")


# Tests:
def test():
    print("Conducting Tests")
    
    print("Testing load_dimacs()") 
    try:
        dimacs = load_dimacs("sat.txt")
        if not dimacs:
            print("No clauses were loaded. Check the format of the DIMACs file.")
        else:
            print(f"Clauses loaded: {dimacs}")
        assert dimacs == [[1], [1, -1], [-1, -2]]
        print("Loaded DIMACS file")
    except Exception as e:
        print(f"Failed to load DIMACS file: {e}")
    
    print("Conducting test on simple_sat_solve()")
    try:
 
        sat1 = [[1], [1, -1], [-1, -2]]
        check = simple_sat_solve(sat1)
        print(f"simple_sat_solve result: {check}")
        assert check == [1, -2] or check == [-2, 1]
        print("Test for (SAT) was successful") 
    except Exception as e:
        print(f"simple_sat_solve for (SAT) was unsuccessful: {e}")
    
    try:
        unsat1 = [[1, -2], [-1, 2], [-1, -2], [1, 2]]
        check = simple_sat_solve(unsat1)
        print(f"simple_sat_solve result: {check}")
        assert not check
        print("Test for (UNSAT) was successful")
    except Exception as e:
        print(f"simple_sat_solve for (UNSAT) was unsuccessful): {e}")
    print("Conducting test on branching_sat_solve()")
    
    try:
        sat1 = [[1], [1, -1], [-1, -2]]
        check = branching_sat_solve(sat1, [])
        print(f"branching_sat_solve result: {check}")
        assert check == [1, -2] or check == [-2, 1]
        print("Test for (SAT) was successful")
    except Exception as e:
        print(f"branching_sat_solve for (SAT) was unsuccessful: {e}")
    
    try:
        unsat1 = [[1, -2], [-1, 2], [-1, -2], [1, 2]]
        check = branching_sat_solve(unsat1, [])
        print(f"branching_sat_solve result: {check}")
        assert not check
        print("Test for (UNSAT) was successful")
    except Exception as e:
        print(f"branching_sat_solve for (UNSAT) was unsuccessful): {e}")
    
    print("Conducting test for unit_propagate()")
    
    try:
        clauses = [[1], [-1, 2]]
        check = unit_propagate(clauses)
        print(f"unit_propagate result: {check}")
        assert check == []
        print("Test was successful")
    except Exception as e:
        print(f"unit_propagate was unsuccessful: {e}")
 
print("Conducting test for DPLL")
problem_names = ["sat.txt", "unsat.txt"]
for problem in problem_names:
    try:
        print(f"Testing with problem: {problem}")
        clauses = load_dimacs(problem)
        all_vars = {abs(lit) for clause in clauses for lit in clause}
        check = dpll_sat_solve(clauses, [], all_vars)
        print(f"DPLL result for {problem}: {check}")
        if problem == problem_names[1]:
            assert check is False
            print("Test for (UNSAT) was successful")
        else:
            assert check != False
            print("Test for (SAT) was successful")
    except Exception as e:
        print(f"Could not solve {problem}: {e}")

print("All tests have been conducted")

test()