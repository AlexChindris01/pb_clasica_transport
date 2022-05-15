from ortools.sat.python import cp_model


model = cp_model.CpModel()
d = 2
r = 3
SC = [80, 57]
D = [96, 22, 14]
C = [[81, 51, 31],
     [82, 47, 54]]
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
    print()
print(solver.Value(transport_cost))
