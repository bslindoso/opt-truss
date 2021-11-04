import numpy as np

def meshtruss (p1,p2,nx,ny):
    nodes = []
    bars = []
    xx = np.linspace(p1[0],p2[0],nx+1)
    yy = np.linspace(p1[1],p2[1],ny+1)
    for y in yy:
        for x in xx:
            nodes.append([x,y])
    for j in range(ny):
        for i in range(nx):
            n1 = i + j* (nx+1)
            n2 = n1 + 1
            n3 = n1 + nx + 1
            n4 = n3 + 1
            bars.extend([[n1,n2],[n1,n3],[n1,n4],[n2,n3]])
        bars.append([n2,n4])
    index = ny* (nx+1) + 1
    for j in range(nx):
        bars.append([index+j-1,index+j])
    return np.array(nodes) , np.array(bars)