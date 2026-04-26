import os
import sys, json
import matplotlib.pyplot as plt
import numpy as np
import argparse
from pathlib import Path

# @public

class DataStruct():
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("jsonfile")
        args = parser.parse_args()
        if not Path(args.jsonfile).is_file():
            parser.error(f"file not found: {args.jsonfile}")
        with open(args.jsonfile, 'r', encoding='utf-8') as fd:
            self.dic = json.load(fd)
        self.x0 = self.dic['x0']
        self.params = self.dic['params']
        self.dparams = self.dic['dparams']
        self.fun = self.dic['fun']
        self.p_terminal = True
        self.p_direction = 1
        self.param_ptr = 0
        self.ax =None
        self.fig =None
        self.xrange = self.dic.get('xrange', [-1, 1])
        self.yrange = self.dic.get('yrange', [-1, 1])
        self.disp_x, self.disp_y = 0, 1
        self.now_xy = [0.0, 0.0]
        self.alpha = self.dic.get('alpha', 1.0)
        self.chunk = self.dic.get('chunk', 2.0)
        self.n_period = self.dic.get('n_period', 1)
        self.tick = self.dic.get('tick', 0.01)
        self.p_index = self.dic.get('p_index', 0) 
        self.p_location = self.dic.get('p_location', 0)
        self.dump_data = bool(self.dic.get('dump_data', False))
        self.fd_file = None
        if self.dump_data:
            bn = os.path.splitext(os.path.basename(sys.argv[1]))[0] + '.dat'
            self.fd_file = open(bn, mode='w')

def init():
    data = DataStruct()
    data.fig = plt.figure(figsize=(10, 10))
    data.ax = data.fig.add_subplot(111)
    data.visible_orbit = True

    plt.rcParams['keymap.save'].remove('s')
    plt.rcParams['keymap.quit'].remove('q')
    plt.rcParams['keymap.fullscreen'].remove('f')

    plt.connect('button_press_event', 
        lambda event: on_click(event, data))
    plt.connect('key_press_event', 
        lambda event: keyin(event, data))
    redraw_frame(data)
    show_param(data)
    return data


def redraw_frame(data):
    data.ax.set_xlim(data.xrange)
    data.ax.set_ylim(data.yrange)
    data.ax.tick_params(labelsize=14)
    data.ax.set_xlabel(r'$x \longrightarrow$', fontsize=18)
    data.ax.set_ylabel(r'$y \longrightarrow$', fontsize=18)
    data.ax.grid(c='gainsboro', ls='--', zorder=9)


class jsonconvert(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(jsonconvert, self).default(obj)

def window_closed(ax):
    fig = ax.figure.canvas.manager
    mgr = plt._pylab_helpers.Gcf.figs.values()
    return fig not in mgr

def keyin(event, data):
    ptr = data.param_ptr
    dim = len(data.fun)
    if event.key == '+':
        data.disp_x += 1
        if data.disp_x >= dim:
            data.disp_x = 0
        data.disp_y = data.disp_x + 1
        if data.disp_y >= dim:
            data.disp_y = 0
    elif event.key == '-':
        data.disp_x -= 1
        if data.disp_x < 0 :
            data.disp_x = dim - 1
        data.disp_y -= 1
    elif event.key == 'q':
        plt.close('all') 
        print("quit")    
        sys.exit()
    elif event.key == 'w':
        jd = json.dumps(data.dic, cls = jsonconvert)
        #print(jd)
        with open("__ppout__.json", 'w') as fd:
            json.dump(data.dic, fd, indent=4, cls = jsonconvert)
        print("now writing...", end="")
        fname = next_filename("snapshot", "pdf")
        plt.savefig(fname)
        print(f"saved to {fname}")
        print("done.")
    elif event.key == ' ' or event.key == 'e':
        plt.cla()
        redraw_frame(data)
        show_param(data)
    elif event.key == 'f':
        plt.cla()
        redraw_frame(data)
        data.visible_orbit = not data.visible_orbit
    elif event.key == 's':
        if data.x0 is not None:
            out = {"params": data.params, "x0": data.p_x0, 
                "t_period": data.t_period}
        else:
            out = {"params": data.params, "x0": data.p_x0}
        print(json.dumps(out, cls=jsonconvert))
    elif event.key == 'p':
        data.param_ptr += 1
        if data.param_ptr >= len(data.params):
            data.param_ptr = 0
        print(f"changable parameter: {data.param_ptr}")
    elif event.key == 'P':
        data.param_ptr -= 1
        if data.param_ptr < 0:
            data.param_ptr = len(data.params)-1
        print(f"changable parameter: {data.param_ptr}")
    elif event.key == 'up':
        ptr = data.param_ptr
        data.params[ptr] += data.dparams[ptr] 
        show_param(data)
    elif event.key == 'down':
        ptr = data.param_ptr
        data.params[ptr] -= data.dparams[ptr] 
        show_param(data)
    return

def next_filename(base="snapshot", ext=".pdf"):
    i = 0
    while True:
        name = f"{base}{'' if i == 0 else i-1}.{ext.lstrip('.')}"
        path = Path(name)
        if not path.exists():
            return path
        i += 1

def show_param(data):
    out = {"params": data.params, 
        "x0": data.x0.tolist() if hasattr(data.x0, "tolist") else data.x0
    }
    print(json.dumps(out))
    out = {"params": data.params}
    plt.title(json.dumps(out), color='b', size='15')

def on_click(event, data):
    if event.xdata == None or event.ydata == None:
        return
    s0 = data.now_xy[:] 
    s0[data.disp_x] = event.xdata
    s0[data.disp_y] = event.ydata
    plt.plot(s0[data.disp_x], s0[data.disp_y], 'o', 
        markersize = 2, color="blue")
    avg = (s0[data.disp_x] + s0[data.disp_y])/2.0
    for i in np.arange(len(s0)):
        if (i != data.disp_x and i != data.disp_y):
            s0[i] = avg
    redraw_frame(data)
    data.now_xy[:] = s0
    x0 = data.x0 = s0[:]
    data.p_terminal = True
    out = {"params": data.params, "x0": x0}
    print(json.dumps(out))
    data.t_period = 0.0
    return

def dump_data(time, state, data):
    for i in np.arange(len(state.t)):
        data.fd_file.write("{0:.6f} ".format(time + state.t[i]))
        for j in np.arange(len(data.x0)):
            data.fd_file.write("{0:.6f} ".format(state.y[j,i]))
        data.fd_file.write("\n")

def fun(t, x, data):
    p = data.params
    v = []
    for i in np.arange(len(data.fun)):
        v.append(eval(data.fun[i]))
    return v

def on_p_sec(t, x, data):
    return x[data.p_index] - data.p_location
