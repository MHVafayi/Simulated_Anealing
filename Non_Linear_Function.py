import math
import random

import numpy as np
from matplotlib import pyplot as plt

import Simulated_Annealing


def find_neighbor(point):
    upper_bound = 1
    lower_bound = 0
    distance = random.random() * 0.105
    new_point = []

    for i in range(len(point)):
        upper_neighbor = point[i] + distance
        if upper_neighbor > upper_bound:
            upper_neighbor = upper_bound
        else:
            upper_neighbor = upper_neighbor

        lower_neighbor = point[i] - distance
        if lower_neighbor < lower_bound:
            lower_neighbor = lower_bound
        else:
            lower_neighbor = lower_neighbor
        neighbor = random.uniform(lower_neighbor, upper_neighbor)
        new_point.append(neighbor)
    return new_point


def random_initial():
    lower_bound = 1
    upper_bound = 0
    point = []
    for i in range(2):
        point.append(random.uniform(lower_bound, upper_bound))
    return point


def function(points):
    return (-1)*(16*points[0]*(1-points[0])*points[1]*(1-points[1])*math.sin(9*math.pi*points[0])*math.sin(9*math.pi*points[1]))**2



sa = Simulated_Annealing.SimulatedAnnealing(start_temperature=5000, stop_temperature=0, alpha=0.95, iterations_number=10000, temperature_method='exponential')
h,a = sa.start_annealing(2, function, find_neighbor, random_initial)
print(f"the minimum: {function([0.5, 0.5])}")

x = np.linspace(0, 1, 1000)
y = np.linspace(0, 1, 1000)
X, Y = np.meshgrid(x, y)
z=[]
for i in x :
    val_array = []
    for j in y :
        val = function([i, j])
        val_array.append(val)
    z.append(val_array)
Z= np.array(z).transpose()
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_wireframe(X, Y, Z, color='green')
plt.show()
