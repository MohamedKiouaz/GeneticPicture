from matplotlib.patches import Rectangle
import numpy as np
import matplotlib.pyplot as plt

class Rectangle:
    def __init__(self, x, y, w, h, val, shape):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.val = val
        self.validate(shape)
    
    def __str__(self):
        return "Rectangle: x={}, y={}, w={}, h={}, val={}".format(self.x, self.y, self.w, self.h, self.val)
    
    def randomize(self, shape):
        if np.random.rand() < 0.1:
            self.x += np.random.randint(-10, 10)
        if np.random.rand() < 0.1:
            self.y += np.random.randint(-10, 10)
        if np.random.rand() < 0.1:
            self.w += np.random.randint(-3, 3)
        if np.random.rand() < 0.1:
            self.h += np.random.randint(-3, 3)
        if np.random.rand() < 0.1:
            self.val += np.random.randint(-10, 10)
        self.validate(shape)

    def validate(self, shape):
        self.x = np.clip(self.x, 0, shape[0] - 25)
        self.y = np.clip(self.y, 0, shape[1] - 25)
        self.w = np.clip(self.w, 1, 25)
        self.h = np.clip(self.h, 1, 25)
        self.val = np.clip(self.val, 0, 255)

class Genom:
    def __init__(self, shape):
        self.rectangles = []
        self.shape = shape

    def array(self):
        # returns a numpy array of the image
        ret = np.zeros(self.shape, dtype=int)
        for r in self.rectangles:
            ret[r.x:r.x+r.w, r.y:r.y+r.h] = r.val
        return np.clip(ret, 0, 255)
    
    def randomize(self):
        # randomize the genom
        for r in self.rectangles:
            if np.random.rand() < .1:
                r.randomize(self.shape)
        if np.random.rand() < .1:
            n = np.random.randint(2, len(self.rectangles)-2)

            self.rectangles = self.rectangles[:n-1] + self.rectangles[n:]

        if np.random.rand() < .1:
            self.rectangles.append(Rectangle(np.random.randint(0, self.shape[0]), np.random.randint(0, self.shape[1]), np.random.randint(1, self.shape[0]), np.random.randint(1, self.shape[1]), np.random.randint(0, 255), img.shape))

    def __str__(self):
        return " ".join(str(r) for r in self.rectangles)

import copy
copy.deepcopy(Genom)    

img = plt.imread("1.jpg")
n_genoms = 100
genom = Genom(img.shape)
for i in range(n_genoms):
    x = np.random.randint(0, img.shape[0])
    y = np.random.randint(0, img.shape[1])
    w = np.random.randint(0, img.shape[0] - x)
    h = np.random.randint(0, img.shape[1] - y)
    val = np.random.randint(0, 255)
    genom.rectangles.append(Rectangle(x, y, w, h, val, img.shape))

def distance(a, b):
    # returns the distance between two images
    return np.sum(np.square(a - b), dtype=float)

n_generations = 20000
n_children = 10
len_ax = 5
fig, axs = plt.subplots(len_ax, len_ax)
axs[-1][-1].imshow(img)
for ax in axs.flatten():
    ax.axis('off')
ax_i = 0
ax_j = 0

for gen in range(n_generations):
    childs = [copy.deepcopy(genom) for i in range(n_children)]
    for child in childs:
        child.randomize() 
    childs += [genom]
    genom = min(childs, key=lambda x: distance(x.array(), img))
    if gen % (n_generations // (len_ax**2 - 1)) == 0:
        if ax_j == 5:
            ax_j = 0
            ax_i += 1
        
        print(len(genom.rectangles))
        axs[ax_i][ax_j].imshow(genom.array())
        axs[ax_i][ax_j].set_title(f"Generation: {gen}, {np.log(distance(genom.array(), img)):.2f}")
        
        plt.pause(0.1)
        
        ax_j += 1
    
plt.show()