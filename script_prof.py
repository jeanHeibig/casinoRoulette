from math import exp
import matplotlib.pyplot as plt

N = 1200
deltau = .02
c = 1.
deltat = deltau/c
phi = [1. for _ in range(N)]
lambd = 1.
lambdt = lambd*deltat
X = [i*deltau for i in range(N)]
mu = 1.
dF = [lambdt*( exp(-mu*X[i]) - exp(-mu*X[i+1])) for i in range(N-1)]


tfinal = 5.

t = 0.

while t<tfinal:
    t+= deltat
    phin = phi.copy()
    for i in range(N-1):
        phi[i] = phin[i+1] - lambdt*phin[i] + sum([phin[i-j-1]*dF[j] for j in range(i)])
    plt.plot(X,phi)
    
iini = int(4./deltau)

print(" survie ",phi[iini])
    
plt.show()
        
    