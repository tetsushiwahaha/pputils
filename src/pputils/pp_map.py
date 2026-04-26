#!/usr/bin/env python
import sys, json
import numpy as np
import matplotlib.pyplot as plt

from pputils import pptools

def main():
    data = pptools.init()
    x = np.array(data.x0, dtype=float)
    buffer = []
    cnt = 0
    while True:
        x = np.array(pptools.fun(0, x, data))
        buffer.append(x.copy())
        cnt += 1
        if cnt > data.dic['break']:
            arr = np.array(buffer)
            plt.plot( arr[:, data.disp_x], arr[:, data.disp_y], 'o',
                markersize=1, color="black", alpha=data.alpha)
            data.now = data.p_x0 = x.copy()
            buffer.clear()
            cnt = 0
            plt.pause(0.01)
            if pptools.window_closed(data.ax):
                sys.exit()

if __name__ == '__main__':
	main()
