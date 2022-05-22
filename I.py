from ortools.sat.python import cp_model
import ast
import time
from os import listdir
import os
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

        status = solver.Solve(model)
        sheet.write(current_row, 0, instance_name)
        t2 = time.time()
        sheet.write(current_row, 2, float(format(t2 - t1, ".3f")))
        g = open("results/" + instance_name + ".txt", "w")
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            sheet.write(current_row, 1, solver.Value(transport_cost))
            sheet.write(current_row, 3, "Solved")
            g.write("Xjk=    [")
            for i in range(d):
                g.write("[")
                for j in range(r):
                    g.write(str(solver.Value(X[i][j])))
                    if j < r - 1:
                        g.write(" ")
                g.write("]")
                if i < d - 1:
                    g.write("\n\t\t")
            g.write("]\n")
        else:
            sheet.write(current_row, 3, "Not solved")
        current_row += 1
        g.write("Dk=\t\t\t\t" + instance[4][1].replace(",", "") + "\n")
        if status == cp_model.OPTIMAL:
            g.write("Optim\t\t= " + str(solver.Value(transport_cost)) + "\n")
        g.write("Cost\tD2R = " + str(solver.Value(transport_cost)) + "\n")
        g.close()
    if os.path.exists("results.xls"):
        os.remove("results.xls")
    wb.save('results.xls')

