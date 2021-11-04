from opttruss import*
from meshtruss import*

coord, connec = meshtruss((0,0), (0.6,0.4), 6, 4)
E0=1e+7
E = E0*np.ones(connec.shape[0])
loads = np.zeros_like(coord)
loads[20,1] = -100.
free = np.ones_like(coord).astype('int')
free[::7,:]=0
opttruss(coord,connec,E,loads,free,0.11,True)
