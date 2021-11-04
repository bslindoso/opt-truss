def remove_bar (connec ,n1 ,n2):
    bars = connec.tolist()
    for bar in bars[:]:
        if (bar[0] == n1 and bar[1] == n2) or (bar[0] == n2 and bar[1] ==n1):
            bars.remove(bar)
            return np.array(bars)
    else:
        print('There is no such bar')
        return connec

def remove_node(connec, n1):
    bars = connec.tolist()
    for bar in bars[:]:
        if bar[0] == n1 or bar[1] == n1:
            bars.remove(bar)
    return np.array(bars)