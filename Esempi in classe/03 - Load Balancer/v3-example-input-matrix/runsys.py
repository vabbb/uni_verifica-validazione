#! /usr/bin/env python

# Import compiler function
from pymodelica import compile_fmu
from pyfmi import load_fmu
import matplotlib.pyplot as plt
import sys
import numpy as N

def fun1(t) :
    return 1*N.sin(2*3.14*5*t)

def fun2(t) :
    return 1*N.cos(2*3.14*5*t)

fmu = compile_fmu('ClosedSystem', ['closed-system.mo', 'system.mo', 'monitor.mo', 'environment.mo', 'dictionary.mo', 'state.mo'])

model = load_fmu(fmu)
opts = model.simulate_options()
#opts['ncp'] = 1000 #Change the number of communication points
 


maxt = 10

timepoints = N.linspace(0.,maxt,1000)  # Create one hundred evenly spaced points

u1 = fun1(timepoints) #Create the first input vector

u2 = fun2(timepoints) #Create the second input vector

n = len(timepoints)
u_traj = N.zeros((n, 3))

for i in xrange(n) :
    u_traj[i][0] = timepoints[i]

for i in xrange(n) :
    u_traj[i][1] = u1[i]

for i in xrange(n) :
    u_traj[i][2] = u2[i]
       
input_object = (['failures','noise'], u_traj)

res = model.simulate(start_time=0, final_time=maxt, input=input_object, options=opts)

#sys.exit();

t = res['time']

rows = 4
cols = 2
maxy =  5 # max(res['v3']);


# col 1
fig = 1
# 1 (1,1)
plt.subplot(rows,cols,fig)
plt.plot(t, res['sys.x'])
plt.grid()
#plt.axis([0, maxt, 0, maxy])
plt.title('sys.x')
fig = fig + 1
# 2 (2, 1)
plt.subplot(rows,cols,fig)
plt.plot(t, res['sys.u'])
plt.grid()
#plt.axis([0, maxt, -2, 2])
plt.title('sys.u')
fig = fig + 1
# 3 (3, 1)
#plt.subplot(rows,cols,fig)
#plt.plot(t, res['sys.noise'])
#plt.grid()
#plt.axis([0, maxt, -1, 2])
#plt.title('sys.noise')
#fig = fig + 1
# 4 (3, 1)
plt.subplot(rows,cols,fig)
plt.plot(t, res['sys.failures'])
plt.grid()
#plt.axis([0, maxt, -1, 2])
plt.title('sys.failures')
fig = fig + 1
# 5 (1, 2)
plt.subplot(rows,cols,fig)
plt.plot(t, res['monitor.x'])
plt.grid()
#plt.axis([0, maxt, -1, 2])
plt.title('monitor.x')
fig = fig + 1
# 6 (2, 1)
plt.subplot(rows,cols,fig)
plt.plot(t, res['monitor.y'])
plt.grid()
plt.axis([0, maxt, -0.5, 1.5])
plt.title('monitor.y')
fig = fig + 1
# 7 (2, 1)
plt.subplot(rows,cols,fig)
plt.plot(t, res['env.d.noise'])
plt.grid()
plt.axis([0, maxt, -1.5, 1.5])
plt.title('env.d.noise')
# 8 (2, 1)
fig = fig + 1
plt.subplot(rows,cols,fig)
plt.plot(t, res['failures'])
plt.grid()
#plt.axis([0, maxt, -0.5, 1.5])
plt.title('failures')
fig = fig + 1
plt.subplot(rows,cols,fig)
plt.plot(t, res['noise'])
plt.grid()
#plt.axis([0, maxt, -0.5, 1.5])
plt.title('noise')
fig = fig + 1

plt.show()
