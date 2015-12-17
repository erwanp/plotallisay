# PlotAllISay

Plot the last number you said in your microphone, versus time

I happened to need to record numbers and time while conducting an experiment. 
I built this small script on top of the SpeechRecognition library to help me
do that. 

## Use

In the console call:

```
    python -i plotallisay.py
```

Then:

- Say a number to plot it

- Start talking whenever you want

- Pause with 'stop', 'pause' or 'over'"

- Close the plot window to stop the program

The script will then output the time-averaged mean of all the values you 
dictated, as well as the total elapsed time. 


## Required

This module is built on top of the SpeechRecognition library by Anthony Zhang. 
You'll also need pyaudio to use the microphone

```
    pip install SpeechRecognition
	pip install pyaudio
```

