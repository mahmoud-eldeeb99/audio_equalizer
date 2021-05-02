import numpy as np
 
import wave
 
import struct
 
import matplotlib.pyplot as plt


#####
#for spect

from scipy import signal
from scipy.fft import fftshift
import matplotlib.pyplot as plt



##########
 
#range of possibles frequencies
import numpy as np
import random
import matplotlib.pyplot as plt
import wave
import struct
import random





frame_rate = 48000.0 #didint know his function
infile = "WaveTest.wav"
num_samples = 44100
wav_file = wave.open(infile, 'r')
data = wav_file.readframes(num_samples) #data is an arry have the signal with hxa 
wav_file.close()
data = struct.unpack('{n}h'.format(n=num_samples), data)  #convert every elemnt from hxa to binary
data = np.array(data)
data_fft = np.fft.fft(data) #convert the sin wave samle to fourer x+yj
frequencies = np.abs(data_fft) #get the absolute of every componant  sqer(x.x+y.y)
print(frequencies[1000])


print("The frequency is {} Hz".format(np.argmax(frequencies))) #this will get the maximum maximum freqency 

plt.subplot(2,1,1)
 
plt.plot(data[:300])
 
plt.title("Original audio wave")
 
plt.subplot(2,1,2)
 
plt.plot(frequencies)
 
plt.title("Frequencies found")
 
plt.xlim(0,10000)
 
plt.show()


#########
#spectro

f, t, Sxx = signal.spectrogram(data,sampling_rate)
plt.pcolormesh(t, f, Sxx, shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()



###########