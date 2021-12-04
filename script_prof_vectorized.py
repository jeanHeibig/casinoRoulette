import matplotlib.pyplot as plt
import numpy as np


N = 1000
delta_u = 1e-2
c = 1
delta_t = c * delta_u
phi = np.ones(N)
_lambda = 1
X = delta_u * np.arange(N)
mu = 1
e_mu_X = np.exp(-mu * X)
dF = _lambda * delta_t * (e_mu_X[: -1] - e_mu_X[1:])
T = 1
t = 0
p = lambda phi: np.vectorize(lambda i: np.dot(phi[i-N-1:-N-1:-1], dF[:i]))
while t < T:
    t += delta_t
    phi[:-1] = phi[1:] - _lambda * delta_t * phi[:-1] + p(phi)(np.arange(N-1))
    plt.plot(X,phi)
plt.show()