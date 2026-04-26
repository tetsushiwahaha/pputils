import sys
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from pputils import pptools

# @public
def main():
    data = pptools.init()
    t_period, time = 0.0, 0.0

    while True:
        pptools.on_p_sec.terminal = data.p_terminal
        pptools.on_p_sec.direction = data.p_direction

        sol = solve_ivp( pptools.fun, (0.0, data.chunk), data.x0, 
            method='RK45', args=(data,), events=pptools.on_p_sec, 
            max_step=data.tick, rtol=1e-9, dense_output=True)

        data.now_xy = data.x0 = sol.y[:, -1].tolist()

        if data.visible_orbit is True:
            plt.plot(sol.y[data.disp_x, :], sol.y[data.disp_y, :],
                linewidth=2, color=(0.1, 0.1, 0.3), ls='-',
                alpha=data.alpha)

        if sol.status == 1:
            p_point = sol.y_events[0][-1]
            data.dic['x0'] = data.now_xy = p_point.tolist()
            plt.plot(p_point[data.disp_x], p_point[data.disp_y], 'o', 
                markersize=3, color="red", alpha=data.alpha)
            data.p_x0 = p_point.tolist()
            data.p_duration = sol.t_events[0][-1]
            t_period += sol.t_events[0][-1]
            data.t_period = t_period
            data.p_terminal = False
            t_period = 0.0
        else:
            t_period += sol.t[-1]
            if data.p_terminal is False:
                data.p_terminal = True

        if data.fd_file is not None:
            pptools.dump_data(time, sol, data)

        time += sol.t[-1]

        if pptools.window_closed(data.ax):
            sys.exit()

        plt.pause(0.01)

if __name__ == '__main__':
    main()
