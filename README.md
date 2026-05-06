# `pputils` --- a simulator for dynamical systems

## Overview
This repository gives a visual simulation tool for
an ordinary differential equation (ODE),  
or a difference equation in any dimension.
This simulator allows: 
* no time limit computation
* real-time parameter change
* attemping various initial values by clicking a pointer
* taking a snapshot anytime
* reporting current state, parameter values, period information

This repository contains three types of simulators: `pp_na.py` for a
non-autonomous ODE, `pp_a.py` for an automonous ODE, and `pp_map.py`
for a defference equation. The settings are decribed in a JSON file. 

The left hand side of the equation 
can be written in this setting file, that is, 
you do not need to edit `pp*.py` every time you test a  
different dynamical system.

## Requirements
* python 3.8 later
* numpy, scipy
* matplotlib

## How to install

You should change current directory to an appropriate directory, and do
    % git clone https://github.com/tetsushiwahaha/pputils.git
    % cd pputils
	% python -m pip install -e .

After this installation, you can use `pp*.py` at any location 
by a declaration:
`from pputils import pptools`

There are three sample simulators in for non-autonomous ODE `pp_na`, 
autonomous ODE `pp_a`, and discrete map `pp_map`.


## pp_na --- for non-autonomous systems

<img src="figs/duffing.png" width="300">

Display a phase portrait of the given nonautonomous ODE. 

### Files
* pp_na.py: a simulator 
* duffing.json: a sample setup file for Duffing equation

### To exec

    % python pp_na.py duffing.json

### Setup file configuration

* `fun`: a list of the right hand side of the ODE.
* `x0`:	an initial value vector
* `params`:	a list of parameter values
* `dparams`: a list of incremental values corresponding to the parameters
* `xrange`, yrange: $x$ and $y$ ranges of the graph
* `tick`: a time step for drawing a curve
* `alpha`:  transparency value, zero to one.

### variables and parameters in fun()

* `x[0]`, `x[1]`, ...: state variables
* `p[0]`, `p[1]`, ...: parameters 

### How to use
#### mouse operation 

- A new initial values is given by clicking on the appropriate location
in the graph.
 
#### key operation

- `s`: print the current status
- `f`: show/hide trajectory (toggle)
- `w`: print the dictionary and dump it to `__ppout__.json` and taking a snapshot into `snapshot*.pdf` 
- `p`: change the active parameter index (default: 0, toggle)
- up and down arrows: increase/decrease the active parameter value
- `space` or `e`: clear transitions
- `q`: quit 


## pp_a.py --- for autonomous systems

<img src="figs/ebvp.png" width="300">

Display a phase portrait of the given autonomous ODE. 

### Files
* `pp_a.py`: an simulator 
* `ebvp.json`: a sample setup file for the extended BVP equation (3rd order ODE)

### To exec

    % python pp_a.py ebvp.json

or, if you could add an excutable permission to `pp.py`, 

    % ./pp.py in.json

### Setup file configuration

* `fun`: a definition of the right hand of the ODE.
* `x0`:	an initial value vector
* `params`:	a list of parameter values
* `dparams`: a list of incremental values corresponding to the parameters
* `tick`: a time step for drawing a curve
* `p_index`, `p_location`: Poincare section definition. x[p_index] - p_location = 0
* `xrange`, `yrange`: $x$ and $y$ ranges of the graph
* `dump_data`: `false` write nothing, `true` write data to a file.
* `alpha`:  transparency value, 0 < alpha < 1

### How to use
#### mouse operation

- A new initial value can be given by clicking on the appropriate location
in the graph.

#### key operation

- `s`: print the current status
- `f`: show/hide trajectory (toggle). Poincare mapping points remain.
- `w`: print the dictionary into `__ppout__.json` and save `snapshot.pdf`
- `p`: change the active parameter index (default: 0, toggle)
- up and down arrows: increase/decrease the active parameter value
- `space` or `e`: clear transitions
- `+`, `-`: change the coordinate system, $(x, y) \rightarrow (y, z) \rightarrow (z, x)$, toggle.
- `q`: quit

## pp_map --- for discrete maps

<img src="figs/quadmap.png" width="300">

Display a phase portrait of the given discrete map. 

### Files

* pp_map.py: a visualizer
* quadmap.json: a sample setup file for a quadratic map

### To exec

    % python pp_map quadmap.json

### Setup file configuration

* `fun`: a list of the right hand side of the discrete map
* `x0`:	an initial value vector
* `params`:	a list of parameter values
* `dparams`: a list of incremental values corresponding to the parameters
* `xrange`, yrange: $x$ and $y$ ranges of the graph
* `tick`: a time step for drawing a curve
* `alpha`:  transparency value, zero to one
* `break`: a number for non-interruptible iterations 

### variables and parameters in fun()

* `x[0]`, `x[1]`, ...: state variables
* `p[0]`, `p[1]`, ...: parameters 

### How to use
#### mouse operation 

- A new initial values is given by clicking on the appropriate location
in the graph.
 
#### key operation

- `s`: print the current status
- `f`: show/hide trajectory (toggle)
- `w`: print the dictionary and dump it to `__ppout__.json` and taking a snapshot into `snapshot*.pdf` 
- `p`: change the active parameter index (default: 0, toggle)
- up and down arrows: increase/decrease the active parameter value
- `space` or `e`: clear transitions
- `q`: quit 

