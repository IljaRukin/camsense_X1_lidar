# camsense-X1-lidar

chinese lidar "camsense X1" outputs data over serial (GND, VCC +5V, TX).<br>
this python script reads the data and visualizes it using matplotlib.<br>
There are two infinite loops, one imports the data and the other plots it.<br>
to run the script "lidar.py" type:<br>

python lidar.py COM12

with the according com port name<br>
the included "lidar.bat" file just runs this script with windows cmd for COM12.<br>
some info and comments ar included in the python notebook "lidar.ipynb".<br>
The serial connection and data packet format is described at:<br>
https://github.com/Vidicon/camsense-X1<br>
and the visualization script "lidar.py" is heavily inspired by:<br>
https://memotut.com/try-using-cheap-lidar-(camsense-x1)-819ac/<br>

here are some images:<br>
<img src="/img/plot.jpg">
<img src="/img/lidar1.jpg">
<img src="/img/lidar2.jpg">
<img src="/img/lidar3.jpg">