from matrix import Matrix
from vector import Vector

a = Vector([1, 2, 3])
b = Vector([4, 5, 6])

print(f"a + b = {a + b}")
print(f"a · b = {a.dot(b)}")
print(f"|a| = {a.magnitude():.4f}")
print(f"cosine similarity = {a.cosine_similarity(b):.4f}")


rotation_90 = Matrix([[0, -1], [1, 0]])
point = Vector([3, 1])

rotated = rotation_90 @ point
print(f"Original: {point}")
print(f"Rotated 90°: {rotated}")



#same thing with numpy

import numpy as np
a = np.array([1, 2, 3], dtype = float)
b = np.array([4, 5, 6], dtype = float)
print("========With numpy==========")
print(f"a + b = {a + b}")
print(f"a · b = {np.dot(a, b)}")
print(f"|a| = {np.linalg.norm(a):.4f}")
print(f"cosine = {np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)):.4f}")

W = np.random.randn(2, 3) * 0.1
x = np.array([1.0, 0.5, -0.3], dtype = float)
print(f"Wx = {W @ x}")

#Rank, Projection, and QR with NumPy

A = np.array([[1,2], [2,4]])
print(f"rank={np.linalg.matrix_rank(A)}")

print(W)