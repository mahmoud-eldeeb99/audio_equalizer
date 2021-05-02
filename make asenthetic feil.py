
import numpy as np
 
import wave
 
import struct
 
import matplotlib.pyplot as plt
 
# frequency is the number of times a wave repeats a second
 
frequency1 = 1000
frequency2 = 3000
frequency3 = 5000
frequency4 = 7000
frequency5 = 9000
frequency6 = 11000
frequency7 = 13000
frequency8 = 15000

 
num_samples = 48000
 
# The sampling rate of the analog to digital convert
 
sampling_rate = 48000.0
 
amplitude = 1000
 
file = "senthetic feil.wav"


sine_wave1 = [np.sin(2 * np.pi * frequency1 * x1 / sampling_rate) for x1 in range(num_samples)]
sine_wave2 = [np.sin(2 * np.pi * frequency2 * x1 / sampling_rate) for x1 in range(num_samples)]
sine_wave3 = [np.sin(2 * np.pi * frequency3 * x1 / sampling_rate) for x1 in range(num_samples)]
sine_wave4 = [np.sin(2 * np.pi * frequency4 * x1 / sampling_rate) for x1 in range(num_samples)]
sine_wave5 = [np.sin(2 * np.pi * frequency5 * x1 / sampling_rate) for x1 in range(num_samples)]
sine_wave6 = [np.sin(2 * np.pi * frequency6 * x1 / sampling_rate) for x1 in range(num_samples)]
sine_wave7 = [np.sin(2 * np.pi * frequency7 * x1 / sampling_rate) for x1 in range(num_samples)]
sine_wave8 = [np.sin(2 * np.pi * frequency8 * x1 / sampling_rate) for x1 in range(num_samples)]
 

sine_wave1 = np.array(sine_wave1)
sine_wave2 = np.array(sine_wave2)
sine_wave3 = np.array(sine_wave3)
sine_wave4 = np.array(sine_wave4)
sine_wave5 = np.array(sine_wave5)
sine_wave6 = np.array(sine_wave6)
sine_wave7 = np.array(sine_wave7)
sine_wave8 = np.array(sine_wave8)
 

combined_signal = sine_wave1 +  sine_wave2 +  sine_wave3 + sine_wave4 +  sine_wave5 + sine_wave6 +  sine_wave7 +  sine_wave8 



nframes=num_samples
 
comptype="NONE"
 
compname="not compressed"
 
nchannels=1
 
sampwidth=2

wav_file=wave.open(file, 'w')
 
wav_file.setparams((nchannels, sampwidth, int(sampling_rate), nframes, comptype, compname))

for s in combined_signal:
   wav_file.writeframes(struct.pack('h', int(s*amplitude)))