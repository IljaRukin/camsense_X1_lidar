import serial
import struct
import time
import sys
import threading
import numpy as np
import matplotlib.pyplot as plt

class Lidar:
    def __init__(self, serialPort, dataSize = 8*64):
        self.theta = [0] * dataSize
        self.r = [0] * dataSize
        self.serial = serial.Serial(port = serialPort, baudrate = 115200)
        self.dataSize = dataSize
        self.thread = threading.Thread(target = self.getData)
        self.lock = threading.Lock()
        self.dataObtained = False
        self.L = 8
        self.N = 64

    def getData(self):
        n = 0
        distance = np.zeros(self.L)
        quality = np.zeros(self.L)
        while True:
            if int.from_bytes(self.serial.read(1),byteorder='little') == 85:
                if int.from_bytes(self.serial.read(1),byteorder='little') == 170:
                    if int.from_bytes(self.serial.read(1),byteorder='little') == 3:
                        if int.from_bytes(self.serial.read(1),byteorder='little') == 8:
                            (speed, startAngle) = struct.unpack_from("<2H", self.serial.read(4))
                            speed = speed/64
                            startAngle = (startAngle-0xa000)/64
                            for i in range(0,self.L):
                                (distance[i], quality[i]) = struct.unpack_from("<HB", self.serial.read(3))
                            (endAngle, crc) = struct.unpack_from("<2H", self.serial.read(4))
                            endAngle = (endAngle-0xa000)/64
                            ###phase manipulation
                            if endAngle<startAngle:
                                endAngle += 360
                            angle = np.linspace(startAngle,endAngle,self.L)
                            angle = angle*(2*np.pi/360)
                            angle = np.mod(angle,2*np.pi)
                            
                            self.lock.acquire()
                            self.r[self.L*n:self.L*(n+1)] = distance
                            self.theta[self.L*n:self.L*(n+1)] = angle
                            n+=1
                            if n == self.N:
                                self.dataObtained = True
                                n = 0
                            self.lock.release()

    def run(self):
        self.thread.start()

    def stop(self):
        self.thread.stop()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("You must specify serial port! \n example: " + sys.argv[0] + " COM12")
        quit()

    lidar = Lidar(sys.argv[1])
    lidar.run()

    #Generate polar graph
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')

    lidar.lock.acquire()
    im, = ax.plot(lidar.theta, lidar.r,color='blue',marker='.',ls='')
    lidar.lock.release()
    
    rmax = 3000

    while True:
        if lidar.dataObtained:

            lidar.lock.acquire()
            #print(lidar.theta)
            #print(lidar.r)
            im.set_data(lidar.theta, lidar.r)
            lidar.dataObtained = False
            lidar.lock.release()

            ax.set_theta_offset(np.pi / 2)
            ax.set_rmax(rmax)
            fig.canvas.draw()
            fig.canvas.flush_events()
            
            plt.pause(0.1)
            rmax = ax.get_rmax()

        else:
            time.sleep(0.1)
