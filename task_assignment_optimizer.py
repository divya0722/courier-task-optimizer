"""
Courier Task Assignment Optimizer
Author: Divya Rajagopal
Description: A simple optimization model using Google OR-Tools to assign delivery tasks to couriers based on travel time.
"""

from ortools.linear_solver import pywraplp

# Couriers and Tasks
couriers = ['Courier A', 'Courier B', 'Courier C', 'Courier D', 'Courier E']
tasks = ['Task 1', 'Task 2', 'Task 3', 'Task 4', 'Task 5', 'Task 6', 'Task 7', 'Task 8', 'Task 9', 'Task 10']

# Simulated travel time (5x10)
travel_time = [
    [22, 18, 35, 20, 25, 30, 40, 28, 33, 21],
    [30, 25, 15, 22, 18, 26, 33, 29, 27, 24],
    [28, 22, 32, 21, 29, 34, 39, 30, 31, 26],
    [25, 19, 30, 24, 23, 28, 36, 27, 29, 22],
    [20, 16, 33, 18, 21, 26, 35, 24, 28, 19]
]

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')

x = []
for i in range(len(couriers)):
    x.append([])
    for j in range(len(tasks)):
        x[i].append(solver.IntVar(0, 1, f'x[{i},{j}]'))

# Constraints
for j in range(len(tasks)):
    solver.Add(solver.Sum([x[i][j] for i in range(len(couriers))]) == 1)
for i in range(len(couriers)):
    solver.Add(solver.Sum([x[i][j] for j in range(len(tasks))]) <= 2)

# Objective
objective_terms = []
for i in range(len(couriers)):
    for j in range(len(tasks)):
        objective_terms.append(travel_time[i][j] * x[i][j])
solver.Minimize(solver.Sum(objective_terms))

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
    print("Optimal Assignment Found:")
    for i in range(len(couriers)):
        assigned = [tasks[j] for j in range(len(tasks)) if x[i][j].solution_value() == 1]
        print(f"{couriers[i]} is assigned to: {', '.join(assigned)}")
else:
    print("No optimal solution found.")
