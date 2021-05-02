import shutil

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from UI import Ui_MainWindow
from pop import popWindow
from scipy.io import wavfile
import numpy as np
import sys
import os
from scipy.fftpack import fft
#from funcations import funcation as f
import wave
import struct
from scipy import signal
from playsound import playsound
from PDF import PDF
from fpdf import FPDF
from PDF import PDF
import pyqtgraph.exporters   #for taking image then take an pdf
from collections import OrderedDict
from scipy.io import wavfile



class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)









#<<<<<<<<<<<<<<<<<        ############    actions         >>>>>>>>>>>>>>>>>>>>>>>>>>
        self.ui.new_window.clicked.connect(lambda: self.pop())
        self.ui.pdf.clicked.connect(lambda: self.create_pdf())
        self.ui.spectro_reset.clicked.connect(lambda: self.spectro_reset())
        self.ui.actionopen_signal.triggered.connect(lambda: self.load_audio_feil())
        self.ui.zoomout.clicked.connect(lambda: self.zoom(0.5))  #######
        self.ui.zoomin.clicked.connect(lambda: self.zoom(2))
        self.ui.o_play.clicked.connect(lambda: self.play_audio())
        self.ui.m_play.clicked.connect(lambda: self.play2())
        self.ui.high_freq_slider.valueChanged.connect(lambda: self.draw_the_new_signal_and_spectrogram())
        self.ui.low_freq_slider.valueChanged.connect(lambda: self.draw_the_new_signal_and_spectrogram())

        self.slider=[self.ui.verticalSlider,
                    self.ui.verticalSlider_2,
                    self.ui.verticalSlider_3,
                    self.ui.verticalSlider_4,
                    self.ui.verticalSlider_5,
                    self.ui.verticalSlider_6,
                    self.ui.verticalSlider_7,
                    self.ui.verticalSlider_8,
                    self.ui.verticalSlider_9,
                    self.ui.verticalSlider_10
                    ]



        for iteration in range(0,10):
            self.slider[iteration].valueChanged.connect(lambda: self.draw_the_new_signal_and_spectrogram())



# <<<<<<<<<<<<<<<<<        ############    poping          >>>>>>>>>>>>>>>>>>>>>>>>>>


    def pop(self):
        self.pop_window = popWindow()
        self.pop_window.show()




# <<<<<<<<<<<<<<<<<        ############    pdf         >>>>>>>>>>>>>>>>>>>>>>>>>>

    def create_pdf(self):   ##take pdf to spectrogram of chaneel 1
        PLOT_DIR = 'pdf_plots'
        PDF_DIR = 'pdf_pdf'

        try:
            shutil.rmtree(PDF_DIR)
            shutil.rmtree(PLOT_DIR)
            os.mkdir(PLOT_DIR)
            os.mkdir(PDF_DIR)
        except FileNotFoundError:
            os.mkdir(PDF_DIR)
            os.mkdir(PLOT_DIR)

        exporter = pg.exporters.ImageExporter(
                    self.ui.o_signal.scene())
        exporter.export(f'{PLOT_DIR}/0.jpg')

        exporter = pg.exporters.ImageExporter(
                    self.ui.m_signal.scene())
        exporter.export(f'{PLOT_DIR}/1.jpg')

        exporter = pg.exporters.ImageExporter(
                    self.ui.o_spect.scene())
        exporter.export(f'{PLOT_DIR}/2.jpg')

        exporter = pg.exporters.ImageExporter(
                    self.ui.m_spect.scene())
        exporter.export(f'{PLOT_DIR}/3.jpg')

        pdf = PDF()
        images = pdf.construct(PLOT_DIR)
        print (images[0:])
        pdf.print_page(images, PLOT_DIR)
        pdf.output(f'{PDF_DIR}/pdf.pdf', 'F')




#<<<<<<<<<<<<<<<<<        ############    zooming         >>>>>>>>>>>>>>>>>>>>>>>>>>>


    def zoom(self,x):
            self.ui.o_signal.plotItem.getViewBox().scaleBy((x, x))
            self.ui.m_signal.plotItem.getViewBox().scaleBy((x, x))
            self.ui.o_spect.plotItem.getViewBox().scaleBy((x, x))
            self.ui.m_spect.plotItem.getViewBox().scaleBy((x, x))



 # <<<<<<<<<<<<<<<<<        ############    orignal file          >>>>>>>>>>>>>>>>>>>>>>>>>>


    def load_audio_feil(self):
        self.fname1 = QtGui.QFileDialog.getOpenFileName(None, 'Open only wav', os.getenv('HOME'),
                                                        "wav(*.wav)")  ##open to for browsing
        path = self.fname1[0]  # get fiel path
        self.infile = path
        self.sampling_rate,data=wavfile.read(self.infile)
        self.num_samples=len(data)
        wav_file = wave.open(self.infile, 'r')  # open the  file
        data = wav_file.readframes(self.num_samples)  # data is an arry have the signal with hexa
        wav_file.close()
        data = struct.unpack('{n}h'.format(n=self.num_samples), data)  # convert every elemnt from hexa to decimle
        self.data = np.array(data)

        self.time = np.arange(0, (self.num_samples/self.sampling_rate), 1 / (
            self.sampling_rate))  ######### time array for x axes ==> [0,1/sampling_rate,2/sampling_rate,...........................,7]sec

        #######

        self.data_fft = np.fft.rfft(data)  # array to convert the wave data sample to fourer ==> x+yj
        print(self.data_fft)

        self.frequencies = np.abs(self.data_fft)  # array to get the absolute of every componant ==> sqer(x.x+y.y)
        print(
            "The frequency is {} Hz".format(np.argmax(self.frequencies)))  # this will get the maximum maximum freqency
        self.ui.o_signal.plot(self.time[:1000], data[:1000])
        self.ui.o_signal.plotItem.setLimits(xMin=0, xMax=(1/self.sampling_rate)*self.num_samples ,yMin=min(self.data),yMax=max(self.data))
        self.draw_spectrogram_of_channel_1()

    ############

# <<<<<<<<<<<<<<<<<        ############    orignal spectrogram         >>>>>>>>>>>>>>>>>>>>>>>>>>

    def draw_spectrogram_of_channel_1(self):

        self.ui.o_spect.clear()
        
        f, t, Sxx = signal.spectrogram(self.data, self.sampling_rate)

    # Interpret image data as row-major instead of col-major
        pg.setConfigOptions(imageAxisOrder='row-major')

        pg.mkQApp()
        win = self.ui.o_spect
    # A plot area (ViewBox + axes) for displaying the image
        p1 = win.addPlot()

    # Item for displaying image data
        img = pg.ImageItem()
        p1.addItem(img)
    # Add a histogram with which to control the gradient of the image
        hist = pg.HistogramLUTItem()
    # Link the histogram to the image
        hist.setImageItem(img)
    # If you don't add the histogram to the window, it stays invisible, but I find it useful.
        win.addItem(hist)
    # Show the window
        win.show()
    # Fit the min and max levels of the histogram to the data available
        hist.setLevels(np.min(Sxx), np.max(Sxx))
    # This gradient is roughly comparable to the gradient used by Matplotlib
    # You can adjust it and then save it using hist.gradient.saveState()
    # Sxx contains the amplitude for each pixel
        img.setImage(Sxx)
    # Scale the X and Y Axis to time and frequency (standard is pixels)
        img.scale(t[-1]/np.size(Sxx, axis=1),
                  f[-1]/np.size(Sxx, axis=0))
    # Limit panning/zooming to the spectrogram
        p1.setLimits(xMin=0, xMax=t[-1], yMin=0, yMax=f[-1])
    # Add labels to the axis
        p1.setLabel('bottom', "Time", units='s')
    # If you include the units, Pyqtgraph automatically scales the axis and adjusts the SI prefix (in this case kHz)
        p1.setLabel('left', "Frequency", units='Hz')


    ########################################################################################################################
        self.color_pallets()
        hist.gradient.restoreState(self.Gradients[self.text])
        ##############



# <<<<<<<<<<<<<<<<<        ############    play orignal signal         >>>>>>>>>>>>>>>>>>>>>>>>>>

    def play_audio(self):
        playsound(self.infile)  # for play the audio    def play_audio(self):



# <<<<<<<<<<<<<<<<<        ############    draw modified signal         >>>>>>>>>>>>>>>>>>>>>>>>>>

    def draw_the_new_signal_and_spectrogram(self):
        self.frequencies = np.abs(self.data_fft)  # array to get the absolute of every componant ==> sqer(x.x+y.y)

        self.new_freqencyes=np.array([])

            
        slider_valeuse=[

        ]

        for x in range(0,10):
            slider_valeuse.append(self.slider[x].value())




        band=2000




        if(self.ui.high_freq_slider.value()==0 and self.ui.low_freq_slider.value()==0): ##for multiplying hight and low freqency by zero 

            self.new_freqencyes=self.frequencies[:]*0

        elif (self.ui.high_freq_slider.value()==0):####for multiplying hight  freqency by zero 
            for x in range(1,6):
                if x==5:
                    self.new_freqencyes = np.concatenate((self.new_freqencyes,self.frequencies[(x-1)*band:]*0 ),axis=0)
                else:
                    self.new_freqencyes = np.concatenate((self.new_freqencyes,self.frequencies[(x-1)*band:band*x]*slider_valeuse[x-1] ),axis=0)

            print(len(self.new_freqencyes))










        elif (self.ui.low_freq_slider.value()==0): ####for multiplying low  freqency by zero 
            print("saeed")

            for x in range(1,11): 
                if x<=5:
                    self.new_freqencyes = np.concatenate((self.new_freqencyes,self.frequencies[(x-1)*band:band*x]*0 ),axis=0)


                elif x==10:
                    self.new_freqencyes = np.concatenate((self.new_freqencyes,self.frequencies[(x-1)*band:]*slider_valeuse[x-1] ),axis=0)

                else:
                    self.new_freqencyes = np.concatenate((self.new_freqencyes,self.frequencies[(x-1)*band:band*x]*slider_valeuse[x-1] ),axis=0)

            print(len(self.new_freqencyes))










        else:


            for x in range(1,11):####for multiplying every band of freqency by his gain     
                if x==10:
                    self.new_freqencyes = np.concatenate((self.new_freqencyes,self.frequencies[(x-1)*band:]*slider_valeuse[x-1] ),axis=0)
                else:
                    self.new_freqencyes = np.concatenate((self.new_freqencyes,self.frequencies[(x-1)*band:band*x]*slider_valeuse[x-1] ),axis=0)





                







        phase = np.angle(self.data_fft)  # get the phase

        self.new_signal_after_add_gain_and_phase = np.multiply(self.new_freqencyes, np.exp(
            1j * phase))  # new_signal_after_add_gain_and_phase==>gain*(x+yj)

        self.new_signal = np.real(
            np.fft.irfft(self.new_signal_after_add_gain_and_phase))  ### convrt the signal to the time domain
         ########## limits




        self.ui.m_signal.plotItem.setLimits(xMin=0, xMax=(1/self.sampling_rate)*self.num_samples ,yMin=min(self.new_signal),yMax=max(self.new_signal))
        self.ui.m_signal.clear()
        self.ui.m_signal.plot(self.time[:1000], self.new_signal[:1000])
        self.draw_the_spectrogram_of_modified_signal()







# <<<<<<<<<<<<<<<<<        ############    modified spectrogram         >>>>>>>>>>>>>>>>>>>>>>>>>>

    def draw_the_spectrogram_of_modified_signal(self):
        self.ui.m_spect.clear()
        
        f, t, Sxx = signal.spectrogram(self.new_signal, self.sampling_rate)

    # Interpret image data as row-major instead of col-major
        pg.setConfigOptions(imageAxisOrder='row-major')

        pg.mkQApp()
        win = self.ui.m_spect
    # A plot area (ViewBox + axes) for displaying the image
        p1 = win.addPlot()

    # Item for displaying image data
        img = pg.ImageItem()
        p1.addItem(img)
    # Add a histogram with which to control the gradient of the image
        hist = pg.HistogramLUTItem()
    # Link the histogram to the image
        hist.setImageItem(img)
    # If you don't add the histogram to the window, it stays invisible, but I find it useful.
        win.addItem(hist)
    # Show the window
        win.show()
    # Fit the min and max levels of the histogram to the data available
        hist.setLevels(np.min(Sxx), np.max(Sxx))
    # This gradient is roughly comparable to the gradient used by Matplotlib
    # You can adjust it and then save it using hist.gradient.saveState()
    # Sxx contains the amplitude for each pixel
        img.setImage(Sxx)
    # Scale the X and Y Axis to time and frequency (standard is pixels)
        img.scale(t[-1]/np.size(Sxx, axis=1),
                  f[-1]/np.size(Sxx, axis=0))
    # Limit panning/zooming to the spectrogram
        p1.setLimits(xMin=0, xMax=t[-1], yMin=0, yMax=f[-1])
    # Add labels to the axis
        p1.setLabel('bottom', "Time", units='s')
    # If you include the units, Pyqtgraph automatically scales the axis and adjusts the SI prefix (in this case kHz)
        p1.setLabel('left', "Frequency", units='Hz')


    ########################################################################################################################
        self.color_pallets()
        hist.gradient.restoreState(self.Gradients[self.text])
        ##############





# <<<<<<<<<<<<<<<<<        ############    play modified signal        >>>>>>>>>>>>>>>>>>>>>>>>>>

    def play_the_modified_signal(self):
        file = "modified_signal.wav"
        wav_file = wave.open(file, 'w')
        comptype = "NONE"
        compname = "not compressed"
        nchannels = 1
        sampwidth = 2
        wav_file.setparams((nchannels, sampwidth, int(self.sampling_rate), self.num_samples, comptype,
                            compname))  ###make awav file with this specifications


        for s in self.new_signal:  #####take every sample then put it in the file we just created
            wav_file.writeframes(struct.pack('q', int(s)))


    def play2(self):
        self.play_the_modified_signal()
        playsound("modified_signal.wav")  # for play the audio









# <<<<<<<<<<<<<<<<<        ############    color pallets          >>>>>>>>>>>>>>>>>>>>>>>>>>

    def color_pallets(self):
        self.Gradients = OrderedDict([
            ('magma', {'ticks': [(0.0, (0, 0, 3, 255)), (0.25, (80, 18, 123, 255)), (0.5, (182, 54, 121, 255)),
                                 (0.75, (251, 136, 97, 255)), (1.0, (251, 252, 191, 255))], 'mode': 'rgb'}),

            ('yellowy', {'ticks': [(0.0, (0, 0, 0, 255)), (0.2328863796753704, (32, 0, 129, 255)),
                                   (0.8362738179251941, (255, 255, 0, 255)), (0.5257586450247, (115, 15, 255, 255)),
                                   (1.0, (255, 255, 255, 255))], 'mode': 'rgb'}),
            ('spectrum', {'ticks': [(1.0, (255, 0, 255, 255)), (0.0, (255, 0, 0, 255))], 'mode': 'hsv'}),
            ('greyclip',
             {'ticks': [(0.0, (0, 0, 0, 255)), (0.99, (255, 255, 255, 255)), (1.0, (255, 0, 0, 255))], 'mode': 'rgb'}),

            ('grey', {'ticks': [(0.0, (0,255,255,255)), (1, (255, 255, 0,255 )), (0.5, (0, 0, 0, 255)),
                                 (0.25, (0, 0, 255, 255)), (0.75, (255, 0, 0, 255))], 'mode': 'rgb'})
        ])

        self.text = self.ui.color_pallets.currentText()

    def spectro_reset(self):
        self.draw_the_new_signal_and_spectrogram()
        self.draw_spectrogram_of_channel_1()
        # self.draw_the_spectrogram_of_modified_signal()





# <<<<<<<<<<<<<<<<<        ############    end         >>>>>>>>>>>>>>>>>>>>>>>>>>




def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()


