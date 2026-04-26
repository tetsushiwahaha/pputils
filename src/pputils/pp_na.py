import sys
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from pputils import pptools

def main():
    data = pptools.init()
    time = 0.0

    duration = 2.0 * np.pi * data.n_period
    tspan = np.arange(0, duration, data.tick)
    
    while True:
        sol = solve_ivp(pptools.fun, (0, duration), data.x0, 
            t_eval=tspan, rtol = 1e-9, method = 'RK45', args=(data,))

        if data.visible_orbit == True:
            plt.plot(sol.y[0, :], sol.y[1, :],
                lw = 3, c = 'k', ls = "-", alpha = data.alpha)

        plt.plot(sol.y[0, -1], sol.y[1, -1], 'o', 
            ms = 5, c = "k", alpha = data.alpha)

        if data.fd_file is not None:
            pptools.dump_data(time, sol, data)

        data.x0 = data.p_x0 = sol.y[:, -1] 

        time += sol.t[-1]

        if pptools.window_closed(data.ax) == True:
            sys.exit()

        plt.pause(0.001) 

if __name__ == '__main__':
    main()

