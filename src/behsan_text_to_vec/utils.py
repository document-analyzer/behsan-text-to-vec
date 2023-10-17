import numpy as np


def normalizer(vec):
    a = np.linalg.norm(vec)
    if a == 0:
        return vec
    else:
        return vec / a


def cosine_similarity(a, b):
    return np.dot(a, b)/(np.linalg.norm(a) * np.linalg.norm(b))
