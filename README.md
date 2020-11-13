# camsense-X1-lidar

chinese lidar "camsense X1" outputs data over serial.
this python script reads the data and visualizes it using matplotlib.
There are two infinite loops, one imports data and the other plots it.
more info and ressources are mentioned in the python notebook "lidar.ipynb"
to run it type:

python lidar.py COM12

with the according com port name
the included "lidar.bat" file just runs this script with windows cmd for COM12.