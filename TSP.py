import math
import random
from matplotlib import pyplot as plt
import Simulated_Annealing
import networkx as nx

class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

def TSP_Initial_point():
    x = [0, 5,8,10,8,10,0,5,2,2,0,5,9,4,0]
    y = [0,5,2,0,8,10,10,8,8,5,6,3,5,1,2]
    cities = []
    for i in range(15):
        cities.append(City(i, x[i], y[i]))
    random.shuffle(cities)
    return cities


def TSP_neighbor(points):
    rnd1 = random.choice(range(len(points)))
    rnd2 = random.choice(range(len(points)))
    temp = points[rnd1]
    points[rnd1] = points[rnd2]
    points[rnd2] = temp
    return points

def TSP(points: list):
    result = 0
    for j in range(1, len(points)):
        result += math.sqrt((points[j].x - points[j - 1].x) ** 2 + (points[j].y - points[j - 1].y) ** 2)
    return result + math.sqrt((points[- 1].x - points[0].x) ** 2 + (points[- 1].y - points[0].y) ** 2)


sa = Simulated_Annealing.SimulatedAnnealing(start_temperature=5000, stop_temperature=0, alpha=0.95, iterations_number=10000, print_xn=False)
c, xi = sa.start_annealing(15, TSP, TSP_neighbor, TSP_Initial_point)
g = nx.Graph()
for i in range(1, len(xi)):
    g.add_node(xi[i - 1].name, pos=(xi[i - 1].x, xi[i - 1].y))
    g.add_node(xi[i].name, pos=(xi[i].x, xi[i].y))
    g.add_edge(xi[i].name, xi[i - 1].name)
g.add_edge(xi[-1].name, xi[0].name)
nx.draw(g, nx.get_node_attributes(g, 'pos'), with_labels=True, node_size=150)
plt.show()