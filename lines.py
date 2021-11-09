from matplotlib.patches import Rectangle
import numpy as np
import matplotlib.pyplot as plt
from numpy.core.function_base import linspace
import os
from tqdm import trange

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)
    
    def randomize(self, shape):
        self.x += np.random.randint(-10, 10)
        self.y += np.random.randint(-10, 10)
        self.x = np.clip(self.x, 0, shape[0] - 1)
        self.y = np.clip(self.y, 0, shape[1] - 1)

    def distance(self, other):
        return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return "({}, {})".format(self.a, self.b)

    def lenght(self):
        return self.a.distance(self.b)
    
    def randomize(self, shape):
        self.a.randomize(shape)
        self.b.randomize(shape)

class Genom:
    def __init__(self, shape):
        self.lines = []
        self.shape = shape

    def array(self):
        ret = np.ones(self.shape, dtype=float)
        for line in self.lines:
            d = line.lenght()
            for a in np.linspace(0, 1, int(d)):
                x = int(a * (line.a.x - line.b.x) + line.b.x)
                y = int(a * (line.a.y - line.b.y) + line.b.y)
                ret[x, y] = 255
        
        return np.clip(ret - 1, 0, 255).astype(int)
    
    def randomize(self):
        for line in self.lines:
            if np.random.rand() < 0.1:
                line.randomize(self.shape)

        if np.random.rand() < .1:
            n = np.random.randint(2, len(self.lines)-2)

            self.lines = self.lines[:n-1] + self.lines[n:]
        
        if np.random.rand() < .1:
            self.add_random_line()

    def add_random_line(self):
        x1 = np.random.randint(0, self.shape[0])
        y1 = np.random.randint(0, self.shape[1])
        x2 = np.random.randint(0, self.shape[0])
        y2 = np.random.randint(0, self.shape[1])
        self.lines.append(Line(Point(x1, y1), Point(x2, y2)))

import copy
copy.deepcopy(Genom)    

if not os.path.exists("plots"):
    os.mkdir("plots")

img = plt.imread("1.jpg")
n_genoms = 100
genom = Genom(img.shape)
for i in range(n_genoms):
    genom.add_random_line()

def distance(a, b):
    return np.sum(np.square(a - b), dtype=float)

n_generations = 2000
n_children = 10
len_ax = 5
fig, axs = plt.subplots(len_ax, len_ax)
axs[-1][-1].imshow(img)
for ax in axs.flatten():
    ax.axis('off')
ax_i = 0
ax_j = 0
best = 1e100
for gen in range(n_generations):
    childs = [copy.deepcopy(genom) for i in range(n_children)]
    for child in childs:
        child.randomize() 
    childs += [genom]
    genom = min(childs, key=lambda x: distance(x.array(), img))
    array = genom.array()
    d = distance(array, img)
    if d < best * .99:
        change = (d / best - 1) * 100
        print(f"{gen} {change:.2f}%")
        best = d
        fig.savefig(f"plots/{gen}.png")
    
    if gen % (n_generations // (len_ax**2 - 1)) == 0:
        if ax_j == 5:
            ax_j = 0
            ax_i += 1

        print(len(genom.lines))
        axs[ax_i][ax_j].imshow(array)
        axs[ax_i][ax_j].set_title(f"Generation: {gen}, {np.log(distance(genom.array(), img)):.2f}")
        
        plt.pause(0.1)
        
        ax_j += 1
    
plt.show()
