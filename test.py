
import numpy as np
 
import wave
 
import struct
 
import matplotlib.pyplot as plt

from scipy import signal
from scipy.fft import fftshift
import matplotlib.pyplot as plt
from scipy.io import wavfile


# frequency is the number of times a wave repeats a second
 
sampling_rate,data=wavfile.read("C:\\xampp\\mysql\\bin\\test.wav")
num_samples=len(data)
wav_file = wave.open("C:\\xampp\\mysql\\bin\\test.wav", 'r')  # open the  file
data = wav_file.readframes(num_samples)  # data is an arry have the signal with hexa
wav_file.close()
data = struct.unpack('{n}h'.format(n=num_samples), data)  # convert every elemnt from hexa to decimle
data = np.array(data)

time = np.arange(0, num_samples/sampling_rate, 1 / (sampling_rate)) 
######### time array for x axes ==> [0,1/sampling_rate,2/sampling_rate,...........................,7]sec
data_fft = np.fft.rfft(data)
print(len(data_fft))
print(num_samples)

frequencies = np.abs(data_fft)







new_freq=np.array(frequencies)
new_freq[4999:5001]=0
recover_sig=np.real(np.fft.ifft(new_freq))



##########spectrogram
f, t, Sxx = signal.spectrogram(recover_sig, sampling_rate)
plt.pcolormesh(t, f, Sxx, shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()