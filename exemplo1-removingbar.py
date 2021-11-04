coord, connec = meshtruss((0,0),(0.6,0.4),6,4)
connec = remove_bar(connec,16,22)
E0=1e+7
E = E0*np.ones(connec.shape[0])
loads = np.zeros_like(coord)
loads[18,1] = -100.
free = np.ones_like(coord).astype("int")
free[::7,:]=0
opttruss(coord,connec,E,loads,free,0.1)