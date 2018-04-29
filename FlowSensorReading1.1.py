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
#import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from matplotlib import pyplot as plt
#from matplotlib import style

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
ser.reset_input_buffer()
print ("Ready to use")    



class Monitor(object):
    """  This is supposed to be the class that will capture the data from
        whatever you are doing.
    """    
    def __init__(self,N):
        self._t    = linspace(0,300,N)*0.1
        self._data = self._t*0

    def captureNewDataPoint(self):
        """  The function that should be modified to capture the data
            according to your needs
        """
#        if ser.in_waiting > 0:
#        ser.reset_input_buffer()
#        ser.flushInput()
        reading = float(ser.readline().decode('utf-8').split(' ')[0].strip('\r\n'))
        print(reading, 'SLPM at %s' % datetime.now())
   #     return float(ser.readline().decode('utf-8').split(' ')[0].strip('\r\n'))
        return reading


    def updataData(self):
        while True:
            self._data[:]  = roll(self._data,-1)
            try:
                self._data[-1] = self.captureNewDataPoint()
            except ValueError:
                self._data[-1] = self._data[-2]
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
    
def flush():
    ser.reset_input_buffer()
#    print('flushed')
    
# Main
if __name__ == '__main__':
    m = Monitor(300)
    sd = StreamingDisplay()
    sd.plot(m)
    sd.set_lims((0,300*0.1),(-0.1,30))
    sd.set_labels('Time, sec', 'Flow rate, SLPM', 'Flow sensor reading')

#    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))


    scheduler = BackgroundScheduler()
    scheduler.add_job(flush, 'interval', seconds = 300)
    scheduler.start()
    
    try:
        while True:
            ani = animation.FuncAnimation(sd._fig, sd.update, m.updataData, interval=10) # interval is in ms
            plt.grid()
            plt.show()
    except(KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        ser.close()
#        pass


