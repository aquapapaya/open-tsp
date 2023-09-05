import numpy as np

from concorde.tsp import TSPSolver

import time
import os
scaling = 10000000

def load_problem(problemIndex, numCity):
    problemDir = os.path.join('./testData' + str(numCity) +'.txt')
    with open(problemDir, 'rt') as fin:
        for idx, data in enumerate(fin):
            if idx == problemIndex:
                problemData = data
                break
    
    nodes_coord = []
    coordSet_with_ans = problemData.split()
    for i in range(numCity):
        xi = float(coordSet_with_ans.pop(0))
        yi = float(coordSet_with_ans.pop(0))
        nodes_coord.append([xi, yi])

    edge_weight = np.zeros((numCity + 1, numCity + 1), dtype= np.float64)
    for i in range(numCity):
        from_x = nodes_coord[i][0]
        from_y = nodes_coord[i][1]
        for j in range(numCity):
            to_x = nodes_coord[j][0]
            to_y = nodes_coord[j][1]
            edge_weight[i + 1, j + 1] = np.sqrt(
                np.square(from_x - to_x) + 
                np.square(from_y - to_y)
            )
    data_tsp = os.path.join('data.tsp')
    with open(data_tsp, 'w') as fp:
        fp.write("NAME: {}\n".format(numCity))
        fp.write("TYPE: TSP\n")
        fp.write("DIMENSION: {}\n".format(numCity + 1))
        fp.write("EDGE_WEIGHT_TYPE: {}\n".format("EXPLICIT"))
        fp.write("EDGE_WEIGHT_FORMAT: {}\n".format("FULL_MATRIX"))
        fp.write("EDGE_WEIGHT_SECTION:\n")
        for i in range(numCity + 1):
            for j in range(numCity + 1):
                fp.write("{} ".format(int(edge_weight[i][j] * scaling)))
            fp.write("\n")
        fp.write("EOF\n")
    
    return np.array(nodes_coord), edge_weight

def create_distance_matrix(city_x_y, numCity):
    global distance_matrix
    distance_matrix = np.zeros((numCity, numCity), dtype= np.float64)
    for i in range(numCity):
        for j in range(numCity):
            distance_matrix[i, j] = np.sqrt(
                np.square(city_x_y[i, 0] - city_x_y[j, 0]) +
                np.square(city_x_y[i, 1] - city_x_y[j, 1])
            )

def calculate_route_distance(permutation):
    return sum([distance_matrix[x1, x2] for (x1, x2) in 
        zip(permutation[0:-1], permutation[1:])])

def solve_by_pyconcorde(problemIndex, numCity):
    city_x_y, edge_weight = load_problem(problemIndex, numCity)
    create_distance_matrix(city_x_y, numCity)
    
    solver = TSPSolver.from_tspfile('./data.tsp')
    timeStart = time.time()
    tour_data = solver.solve()
    timeEnd = time.time()
    runtime = timeEnd - timeStart
    
    concorde_tour = tour_data.tour
    concorde_tour = concorde_tour - 1 
    concorde_tour = tuple(concorde_tour[1:])
    
    concorde_dist = calculate_route_distance(concorde_tour)
    print("concorde_tour:", concorde_tour)
    print("concorde_dist:", concorde_dist)
    return concorde_tour, concorde_dist, runtime

solve_by_pyconcorde(2, 10)


