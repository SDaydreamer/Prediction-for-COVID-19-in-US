import numpy as np

def sigmoid(x, k=1, t=0, m=1):
    return k/(1+np.exp(-(x-t)/m))
