import numpy as np
import sys
import sympy as sp

pop = np.zeros((2,2))

x = sp.Matrix([[1,1,1,0],[0,1,1,1],[0,0,1,1],[0,0,0,1],[0,1,0,1],[4,2,2,3]])
l = sp.zeros(8,16)
print(l)
print(x.rref())
z = np.array([[1,1,0],[1,1,1],[0,1,1],[1,1,3]])

#print(np.linalg.lstsq(z,[1,1,3]))
#b = np.array([1,2,2,2,1])
#print(pop)
#z = np.linalg.svd(x,b)
#print(z)
a, b, c, d, e = sp.symbols('a, b, c, d, e', extended_real=True)
jkl = sp.Matrix([[1,1,0,0,0],[1,1,1,0,0],[0,1,1,1,0],[0,0,1,1,1],[0,0,0,1,1],[1,2,2,2,1]])
print(sp.nonlinsolve(jkl,[a,b,c,d,e]))