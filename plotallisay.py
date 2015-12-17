#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Erwan Pannier

Plot the last number you said in your microphone, versus time

# NOTE: this example requires PyAudio because it uses the Microphone class

Run this program with ipython -i plotallisay.py to have access to xdata, ydata
at the end



"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from warnings import warn

import speech_recognition as sr
import time

# %% Init Plot
fig, ax = plt.subplots()
line, = ax.plot([], [], 'o', lw=2)
ax.set_ylim(-1.1, 1.1)
ax.set_xlim(0, 5)
ax.grid()
ax.set_xlabel('Time (s)')
ax.set_ylabel('Value')
xdata, ydata = [], []
ax.grid(True)

INPUTVAL = None


# %% Init audio

def convert(value):
    ''' Convert an audio recognized text value in float '''

    def accept(out,change,value):
        if not change: 
            out = value
            change = True
        else:
            warn("Rejected instruction {0} because one was already given".format(v))
        return out, change
        
    change = False
    out = "" 
    
    w = value.split(' ')  
    w = map(str.lower,w)
    for v in w:
        
        if v in ['zero']:
            out, change = accept(out,change,0)
            
        if v in ['hundred']:
            out, change = accept(out,change,100)
            
        elif v in ['stop','over','pause']:
            out, change = accept(out,change,None)
            
        else:
            try: 
                v = float(v)
                if type(v) == float:
                    out = v
            except:
                pass
            
    return out
    

# this is called from the background thread
def callback(recognizer, audio):
    global INPUTVAL
    # received audio data, now we'll recognize it using Google Speech Recognition
    
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        value = recognizer.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + value)
        
        value = convert(value)
        if value != "": INPUTVAL = value

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

r = sr.Recognizer()
m = sr.Microphone()

with m as source:
    r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening

# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)

# %% Start
    
try:

    def data_gen():
        global INPUTVAL 
        cnt = 0
        while True:
            cnt+=1
    #        t += 0.05
    #        print(t,signal)
            signal = INPUTVAL
            
            t = time.time()-data_gen.t0
            yield t, signal
            
    
    def run(data):
        # update the data
        t,y = data
        xdata.append(t)
        
        if y is None:
            ydata.append(np.nan)
            return line, # Not started yet
        
        ydata.append(y)
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
    
        if t >= xmax:
            ax.set_xlim(xmin, 1.5*xmax)
    #        ax.figure.canvas.draw()
            plt.draw()
            

        if y >= ymax:
            ax.set_ylim(ymin, max(ymax,1.5*y))
            plt.draw()
        elif y <= ymin:
            ax.set_ylim(min(ymin,y-abs(y)), ymax)
            plt.draw()
            
        
        line.set_data(xdata, ydata)
    
        return line,
    
    # Adjust interval to change the animation speed
    print('Say a number to plot it')
    print('Start talking whenever you want')
    print("Pause with 'stop', 'pause' or 'over'")
    print("Close the plot window to stop the program")
    print('Use python -i plotallisay.py to access the data at the end (xdata, ydata,mean,telapsed)')
    data_gen.t0 = time.time()
    
#    try:
    ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=100,
        repeat=False)
    plt.show()
    
    stop_listening()

except KeyboardInterrupt:
    stop_listening() # calling this function requests that the background listener stop listening
    print('Stopped listening')
    
    pass
       
       
# Print final statistics
xdata, ydata = map(np.array,[xdata,ydata])
b = np.isfinite(ydata)
if b.sum()>0:
    mean = ydata[b].mean()
    telapsed = np.sum(np.hstack([np.diff(xdata)[0],np.diff(xdata)])[b])
    print('\n')
    print("   Average value: {0}".format(mean))
    print("   Time elapsed*: {0:.2f}s".format(telapsed))
    print('\n')
    print('*time counted for valid values only')
