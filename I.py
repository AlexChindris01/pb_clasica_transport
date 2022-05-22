from ortools.sat.python import cp_model
import ast
import time
from os import listdir
import xlwt
from xlwt import Workbook

if __name__ == "__main__":
    instances_filenames = listdir("instances")
    wb = Workbook()
    sheet = wb.add_sheet('Sheet 1')
    current_row = 0
    for instance_filename in instances_filenames:
        model = cp_model.CpModel()
        t1 = time.time()
        f = open("instances/" + instance_filename, "r")
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

        status = solver.Solve(model)  # only need status variable for seeing if the status is optimal, feasible etc
        sheet.write(current_row, 0, instance_name)
        t2 = time.time()
        sheet.write(current_row, 2, float(format(t2 - t1, ".3f")))
        print(format(t2 - t1, ".3f"))
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            # for i in range(d):  # print solution
            #     for j in range(r):
            #         print(solver.Value(X[i][j]), end=" ")
            #         if solver.Value(X[i][j]) < 10:
            #             print(" ", end="")
            #     print()
            sheet.write(current_row, 1, solver.Value(transport_cost))
            print(solver.Value(transport_cost))
            sheet.write(current_row, 3, "Solved")
        else:
            sheet.write(current_row, 3, "Not solved")
        current_row += 1
    wb.save('results.xls')

