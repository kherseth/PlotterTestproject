# -*- coding: utf-8 -*-
"""
Created on Sun Mar 08 12:57:41 2015

@author: kim
"""

import sys
import numpy
from PyQt4 import QtGui, QtCore, uic, Qt
import matplotlib.pyplot as plt
import PyQt4.Qwt5 as Qwt
import serial
from threading import Thread
import time
 
numPoints=1000
xs=numpy.arange(numPoints)
ys=numpy.sin(3.14159*xs*10/numPoints)
ys2=numpy.sin(3.14159*xs*10/numPoints)
t = numpy.arange(256)
 
global connected
global win

class TestApp(QtGui.QMainWindow):
       # DataTimer = QtCore.QTimer()
        pen = Qt.QPen()
        pen.setColor(Qt.Qt.red)
        pen.setWidth(1)
        ser = serial.Serial("COM4", 38400)
        ser.setTimeout(0.2)
        DataTimer = QtCore.QTimer()
        c=Qwt.QwtPlotCurve()  #make a curve
        c2=Qwt.QwtPlotCurve()
        c2.setPen(pen)        
        
        def __init__(self):
            QtGui.QMainWindow.__init__(self)
            self.ui = uic.loadUi('plot.ui')        
            self.ui.show()                 
            self.connect(self.ui.okButton, QtCore.SIGNAL("clicked()"), buttonFn)
            self.connect(self.ui.OpenCom, QtCore.SIGNAL("clicked()"), OpenComClicked)
            self.connect(self.ui.CloseCom, QtCore.SIGNAL("clicked()"), CloseComClicked)            
            self.connect(self.DataTimer, QtCore.SIGNAL("timeout()"), self.UpdatePlot)            
            self.DataTimer.singleShot = False
            self.DataTimer.start(2)
            self.ui.qwtPlot.setAutoReplot(True)
            self.c.attach(self.ui.qwtPlot) #attach it to the qwtPlot object
            self.c2.attach(self.ui.qwtPlot) #attach it to the qwtPlot object
            
        def UpdatePlot(self):
            global ys
            global ys2
            global xs
            
            ys=numpy.roll(ys,-1)
            ys2=numpy.roll(ys2,-1)
            
            temp = self.ser.readline()
            tempsplit = temp.split(';')
            ys[0] = int(tempsplit[0])
            ys2[0] = int(tempsplit[1])
            self.c.setData(xs, ys)
            self.c2.setData(xs, ys2)
            
            self.ui.label_4.setText(str(len(tempsplit)))

def buttonFn():
    print("button clicked")
    
class WorkThread(QtCore.QThread):
 def __init__(self):
  QtCore.QThread.__init__(self)

 def __del__(self):
  self.wait()
   
def OpenComClicked():

    print("button clicked")

    
def CloseComClicked():
    print("button clicked")
    
def main():
    global app
    global win
    app = QtGui.QApplication(sys.argv)
    win = TestApp()
    sys.exit(app.exec_())
    print("Exited")
    
if __name__ == "__main__":
        
    main()
    
    
 