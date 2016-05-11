import MLP as net
import cv2
import urllib2
import numpy as np
import serial as sp
import sys
import time
import csv

class SDC_Mode(object):
    def __init__(self,NetLayers,ip_camera_host,capture_image_size,serialport):
        self.MyNet = net.MLP(NetLayers)
        self.Host = ip_camera_host
        self.Frame = None
        self.Image = None
        self.Size = capture_image_size
        self.Port = serialport
    def Connect_Serial(self):
        self.SerialPort = sp.Serial(self.Port)
    def Send_Serial(self,data):
        if(data == 1):
            self.SerialPort.write('W')
        if(data == 2):
            self.SerialPort.write('Z')
        if(data == 3):
            self.SerialPort.write('D')
        if(data == 4):
            self.SerialPort.write('A')
        if(data == 5):
            self.SerialPort.write('S')
    def Load_Trained_MLP(self,mlp_xml_file):
        print 'Loading trained data'
        self.MyNet.Load_From(mlp_xml_file)
        print self.MyNet.Weights
    def Start_Driving(self):
        print 'Start self driving mode'
        self.Stream = urllib2.urlopen(self.Host)
        bytes=''
        self.isRunning = True
        while(self.isRunning):
            bytes+=self.Stream.read(10024)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a!=-1 and b!=-1:
                jpg = bytes[a:b+2]
                bytes= bytes[b+2:]
                self.Frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_GRAYSCALE)
                x = np.size(self.Frame)
                if(x >= self.Size[0]*self.Size[1]):
                    try:
                        self.Image = cv2.resize(self.Frame,self.Size)
                        print 'Capture Size'+str(self.Size)
                        print np.shape(np.mat(self.Image))
                        print self.Image
                        ImageArray = self.Image.reshape(-1,self.MyNet.Network_Shape[0]).astype(np.float32)
                        _TrainingData = []
                        _TestingData = []
                        _TestingData.append(1)
                        _TrainingData.append(ImageArray)
                        TestingData = [np.reshape(x, (self.MyNet.Network_Shape[0], 1)) for x in _TrainingData]
                        TestingResult = [np.reshape(x, (1, 1)) for x in _TestingData]
                        TestData = zip(TestingData,TestingResult)
                        res = self.MyNet.Evaluate(TestData)
                        print 'Learning Result: '
                        print res
                        self.Send_Serial(res[0])
                        cv2.imshow('IP Camera '+self.Host,self.Frame)
                    finally:
                        x = 0
                k = cv2.waitKey(1)
                if(k == 27):
                    break
        cv2.destroyAllWindows()

