# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 12:30:52 2018

@author: yxu
"""


from pylab import *
import matplotlib.animation as animation
import sys
#import io
#import threading
from matplotlib import pyplot as plt
#from matplotlib import style

#import serial
#from serial.tools.list_ports import comports
#from serial.tools import hexlify_codec
#ser = serial.Serial('COM3', 9600, timeout=0, parity=NONE, rtscts=1)
#s = ser.read(100)       # read up to one hundred bytes
                         # or as much is in the buffer
#import imaplib
import serial
from serial.tools.list_ports import comports
#from serial.tools import hexlify_codec
#import argparse

def ask_for_port():
    """\
    Show a list of ports and ask the user for a choice. To make selection
    easier on systems with long device names, also allow the input of an
    index.
    """
    sys.stderr.write('\n--- Available ports:\n')
    ports = []
    for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
        sys.stderr.write('--- {:2}: {:20} {!r}\n'.format(n, port, desc))
        ports.append(port)
    while True:
        port = input('--- Enter port index or full name: ')
        try:
            index = int(port) - 1
            if not 0 <= index < len(ports):
                sys.stderr.write('--- Invalid index!\n')
                continue
        except ValueError:
            pass
        else:
            port = ports[index]
        return port

        
#port1 = ask_for_port()

ser = serial.Serial()
ser.baudrate = 9600
ser.port = ask_for_port()
print ("Opening port")
ser.close()
ser.open()
print ("Ready to use")    
#serial.Serial.close()
#serial_port = serial.Serial.(port1)
#serial.Serial(serial_port).close()
# set plot to animated
#plt.ion() 

"""start_time = time()
timepoints = []
ydata = []
yrange = [-0.1,50]
view_time = 15 # seconds of data to view at once
"""
# ser.reset_input_buffer()

class Monitor(object):
    """  This is supposed to be the class that will capture the data from
        whatever you are doing.
    """    
    def __init__(self,N):
        self._t    = linspace(0,300,N)
        self._data = self._t*0

    def captureNewDataPoint(self):
        """  The function that should be modified to capture the data
            according to your needs
        """ 
        return float(ser.readline().decode('utf-8').split(' ')[0].strip('\r\n'))
        #return 0.01


    def updataData(self):
        while True:
            self._data[:]  = roll(self._data,-1)
            self._data[-1] = self.captureNewDataPoint()
            yield self._data

class StreamingDisplay(object):

    def __init__(self):
        self._fig = figure()
        self._ax  = self._fig.add_subplot(111)

    def set_labels(self,xlabel,ylabel,title):
        self._ax.set_xlabel(xlabel)
        self._ax.set_ylabel(ylabel)
        self._ax.set_title(title)


    def set_lims(self,xlim,ylim):
        self._ax.set_xlim(xlim)
        self._ax.set_ylim(ylim)

    def plot(self,monitor):
        self._line, = (self._ax.plot(monitor._t,monitor._data))

    def update(self,data):
        self._line.set_ydata(data)
        return self._line

# Main
if __name__ == '__main__':
    m = Monitor(300)
    sd = StreamingDisplay()
    sd.plot(m)
    sd.set_lims((0,300),(-0.1,30))
    sd.set_labels('Time, 0.1sec', 'Flow rate, SLPM', 'Flow sensor reading')
    ani = animation.FuncAnimation(sd._fig, sd.update, m.updataData, interval=10) # interval is in ms
    plt.grid()
    plt.show()
#    fig1.suptitle('live updated data', fontsize='18', fontweight='bold')
#    plt.xlabel('time, seconds', fontsize='14', fontstyle='italic')
#    plt.ylabel('potential, volts', fontsize='14', fontstyle='italic')