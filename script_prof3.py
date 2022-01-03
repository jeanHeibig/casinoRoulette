#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 15:19:46 2021

@author: reymard
"""
import numpy as np
import matplotlib.pyplot as plt
from random import random

n = 10000

u_ini = 4. #richesse initiale
t_final = 5.
lambdaa = 1.
mu = 1.
c = 1. #montant des primes d'assurances

survie = 0
for _ in range(n):
    
    u = u_ini
    T = -np.log(random())/lambdaa
    t = T
    while t<t_final and u>=0:
        
        S = -np.log(random())/mu
        u += c*T-S
        T = -np.log(random())/lambdaa 
        t += T
    if u>=0.:
        survie += 1

print (survie/n)
        
        
    