# UAV-Simulation
## Introduction
The aim of this task is to create a simple feedback control algorithm for position stabilisation of an Unmanned Aerial System (UAS). Processing measurements from sensors, such as GPS location, to generate actuation commands that achieve a specific vehicle state (position), is a fundamental building block of robotics systems. Many advanced guidance and navigation methods depend on the fundamental ability of a robotic system to move to a designated 'point'.

The code defines a PID controller for controlling a Unmanned Aerial Vehicle (UAV). This controller manages the position and attitude of the drone through a cascade control method, with position control as the outer loop and attitude control as the inner loop.By precisely adjusting the PID parameters, the UAV can efficiently reach the specified position and maintain a stable flight attitude. This control method is particularly important in the dynamic environment of UAVs and can effectively deal with external interference.

## Steps
1.Installation library（Linux）：

```
pip install numpy
pip install pygame_gui
pip install pygame
```
2.To launch the simulation enter the following command:
```
python run.py
```
## Results
[![Watch the video](https://img.youtube.com/vi/Fey6LxFukqU/0.jpg)](https://www.youtube.com/watch?v=Fey6LxFukqU)
- 

