from ortools.sat.python import cp_model
import ast
import time

# init == main or whatever
model = cp_model.CpModel()
t1 = time.time()
f = open("Lab01_simple_large_01.dat", "r")
instance = f.read()
f.close()
instance = instance.split(";")
for i in range(len(instance)):
    instance[i] = instance[i].split(" = ")
instance[0][1] = instance[0][1].replace('"', '')
for i in range(1, len(instance) - 1):
    instance[i][1] = instance[i][1].replace(" ", ", ")
    instance[i][1] = instance[i][1].replace(", , ", ", ")
    instance[i][1] = instance[i][1].replace("\n", "")
instance_name = instance[0][1]
d = ast.literal_eval(instance[1][1])
r = ast.literal_eval(instance[2][1])
SC = ast.literal_eval(instance[3][1])
D = ast.literal_eval(instance[4][1])
C = ast.literal_eval(instance[5][1])
X = [[model.NewIntVar(0, max(SC), 'x') for i in range(r)] for j in range(d)]
for k in range(r):
    model.Add(cp_model.LinearExpr.Sum([X[j][k] for j in range(d)]) == D[k])
for j in range(d):
    model.Add(cp_model.LinearExpr.Sum([X[j][k] for k in range(r)]) <= SC[j])
transport_cost = cp_model.LinearExpr.Sum([cp_model.LinearExpr.Sum([X[j][k] * C[j][k] for k in range(r)]) for j in range(d)])
model.Minimize(transport_cost)

solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 10.0

status = solver.Solve(model)  # only need this line for seeing if the status is optimal, feasible etc
for i in range(d):
    for j in range(r):
        print(solver.Value(X[i][j]), end=" ")
        if solver.Value(X[i][j]) < 10:
            print(" ", end="")
    print()
print(solver.Value(transport_cost))
t2 = time.time()
print(format(t2 - t1, ".3f"))
