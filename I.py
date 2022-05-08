import localsolver

with localsolver.LocalSolver() as ls:
    model = ls.model
    f = open("Lab01_simple_medium_01.dat", "r")
    input = f.read()
    input = input.split(";")
    for i in range(len(input)):
        input[i] = input[i].split("=")
    for i in range(1, len(input) - 1):
        print(input[i][1])
    f.close()
    # mai verific daca e ok
    # parca sunt ceva spatii ramase si in afara parantezelor
    d = 2
    r = 3
    SC = [80, 57]
    D = [96, 22, 14]
    C = [[81, 51, 31],
         [82, 47, 54]]
    X = [[model.int(0, max(SC)) for i in range(r)] for j in range(d)]
    #  observatie: cu X = [[model etc] * r for i in range(d)] apar probleme, parca nu creeaza cate un element
    #  distinct pt fiecare loc din lista
    for k in range(r):
        model.constraint(model.sum(X[j][k] for j in range(d)) == D[k])
    for j in range(d):
        model.constraint(model.sum(X[j][k] for k in range(r)) <= SC[j])
    transport_cost = model.sum(model.sum(X[j][k] * C[j][k] for k in range(r)) for j in range(d))
    # poate facut alte verificari pt a vedea daca expresia de la transport_cost e buna; eventual
    # vazut ceva de genul daca apar erori la anumite modificari in expresie
    model.minimize(transport_cost)
    model.close()
    ls.param.time_limit = 10
    ls.solve()
    for i in range(d):
        for j in range(r):
            print(X[i][j].value, end=" ")
        print()
    print(transport_cost.value)
    # cu model.constraint cred ca se vor scrie restrictiile mentionate pe kb la pb clasica de transport.
    # Ce am scris pana acum cu constraint: model.constraint(model.sum(X[j][k] for i in range())).
    # E pentru prima din restrictiile mentionate pe kb si nu reprezinta complet acea restrictie.
    # Vezi exemple de programe cu localsolver pentru a putea finaliza tema.
