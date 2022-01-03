from math import exp
import matplotlib.pyplot as plt

deltau = .025
c = 1.
tfinal = 5.
uini = 4.
iini = int(uini/deltau)
deltat = deltau/c
N = iini+ int( tfinal/deltat)+2

u = [0. for _ in range(N)]

u[iini] = 1./deltau

lambd = 1.
lambdt = lambd*deltat
uplambdt = 1./(1. + lambdt )
X = [i*deltau for i in range(N+2)]
mu = 1.
dF = [lambdt*( exp(-mu*X[i]) - exp(-mu*X[i+1])) for i in range(N+1)]

Xplot = X[0:N]

t = 0.
Nmax = iini+1

while t<tfinal:
    t+= deltat
    Nmax +=1
    un = u.copy()
    i=0
    u[i] = uplambdt * sum([un[i+j]*dF[j] for j in range(Nmax-i)])
    for i in range(Nmax):
        u[i] = uplambdt * (un[i-1]  + sum([un[i+j]*dF[j] for j in range(Nmax-i)]))
    
plt.plot(Xplot,u)
print(" survie ",sum(u)*deltau)
    
plt.show()
        
    