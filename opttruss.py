import numpy as np
from openopt import NLP
from matplotlib import use
use('Agg')
from matplotlib.pyplot import figure, show, savefig


def opttruss(coord,connec,E,F,freenode,V0,plotdisp=False):
    n = connec.shape[0]
    m = coord.shape[0]
    vectors = coord[connec[:,1],:] - coord[connec[:,0],:]
    l = np.sqrt((vectors**2).sum(axis=1))
    e = vectors.T/l
    B = (e[np.newaxis] * e[:,np.newaxis]).T


    def fobj(x):
        D = E * x/l
        kx = e * D
        K = np.zeros((2*m, 2*m))
        for i in range(n):
            aux = 2*connec[i,:]
            index = np.r_[aux[0]:aux[0]+2, aux[1]:aux[1]+2]
            k0 = np.concatenate((np.concatenate((B[i],-B[i]),axis=1), \
                                 np.concatenate((-B[i],B[i]),axis=1)),axis=0)
            K[np.ix_(index,index)] = K[np.ix_(index,index)] + D[i] * k0   

        block = freenode.flatten().nonzero()[0]
        matrix = K[np.ix_(block,block)]
        rhs = F.flatten()[block]
        solution = np.linalg.solve(matrix,rhs)
        u = freenode.astype('float').flatten()
        u[block] = solution
        U = u.reshape(m,2)
        axial = ((U[connec[:,1],:] - U[connec[:,0],:]) * kx.T).sum(axis=1)
        stress = axial / x
        cost = (U * F).sum()
        dcost = -stress**2 / E * l
        return cost, dcost, U, stress

    def volume(x):
        return (x * l).sum(), l

    def drawtruss(x, factor=5, wdt=5e2):
        U, stress = fobj(x)[2:]
        newcoor = coord + factor*U
        if plotdisp:
            fig = figure(figsize=(12,6))
            ax = fig.add_subplot(121)
            bx = fig.add_subplot(122)
        else:
            fig = figure()
            ax = fig.add_subplot(111)
        for i in range(n):
            bar1 = np.concatenate( (coord[connec[i,0],:][np.newaxis],coord[connec[i,1],:][np.newaxis]),axis=0 )
            bar2 = np.concatenate( (newcoor[connec[i,0],:][np.newaxis],newcoor[connec[i,1],:][np.newaxis]),axis=0 )
            if stress[i] > 0:
                clr = 'r'
            else:
                clr = 'b'
            ax.plot(bar1[:,0],bar1[:,1], color = clr, linewidth = wdt * x[i])
            ax.axis('equal')
            ax.set_title('Stress')
            if plotdisp:
                bx.plot(bar1[:,0],bar1[:,1], 'r:')
                bx.plot(bar2[:,0],bar2[:,1], color = 'k', linewidth= wdt* x[i])
                bx.axis('equal')
                bx.set_title('Displacement')
        show()
        savefig('example1.png')

    xmin = 1e-6 * np.ones(n)
    xmax = 1e-2 * np.ones(n)
    f = lambda x: fobj(x)[0]
    derf = lambda x: fobj(x)[1]
    totalvolume = volume(xmax)[0]
    constr = lambda x: 1./totalvolume * volume(x)[0] - V0
    dconstr= lambda x: 1./totalvolume * volume(x)[1]
    x0 = 1e-4*np.ones(n)
    problem = NLP(f,x0,df=derf,c=constr,dc=dconstr, lb=xmin, ub=xmax, name='Truss', iprint=100)
    result = problem.solve('scipy_slsqp')
    #result = problem.solve('interalg')
    #result = problem.solve('ralg')
    
    drawtruss(result.xf)
