# Script utlizzato per laciare i modelli
# Autore: Cristian Di Pietrantonio


# import necessari
from pymodelica import compile_fmu
from pyfmi import load_fmu
import matplotlib.pyplot as plt
import sys
import os

#funzione per plottare i dati
def plottaDati(rows, cols, arraydict, vals):
    # col 1
    fig = 1
    t = res['time']
    xend = max(t)
    for i in range(0, len(arraydict)):
        plt.subplot(rows,cols, fig)
        currentRange = vals[arraydict[i]]
        plt.plot(t, currentRange)
        plt.grid()
        plt.axis([0,xend,min(currentRange) - 1, max(currentRange) + 1])
        plt.title(arraydict[i])
        fig = fig + 1
    plt.show()


model_name="ClosedSystem"

#sono caricati tutti i file ".mo" nella cartella
model_files = [f for f in os.listdir(".") if ".mo" in f]

#input_object = (['noise', 'failures'], input_function)

model_comp = compile_fmu(model_name, model_files)
model = load_fmu(model_comp)
maxt = 20
opts = model.simulate_options()
#opts['CVode_options']['maxh'] = 1.0e-4
res = model.simulate(start_time=0, final_time=maxt, options=opts)

plottaDati(3, 2, ['proc1.myState', 'proc2.myState', 'mem.reset1', 'mem.reset2', 'mem.kr'], res)
