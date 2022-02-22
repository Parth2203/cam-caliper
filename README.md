# square-one
Auto Object Detection and Dimension Measurement with Computer Vision. 

# Introduction
This repository contains main.py which runs the following task - 
* Object detection and measuring the dimension.
* Measuring the dimension of object using extrinsic calibration method.

# Installation 
```sh
$ pip install -r requirements.txt
            or
$ pip install opencv-python
$ pip install numpy
```

# Execution
* Setup a camera which is to be used to take video feed, make sure it is aligned perpendicularly to the surface,
  so that very precise measurement can be obtained.
* Now you should have a contrasting background and ample lighting so that computer vision can distinguish between the object and background more accurately.
* To find out the camera id number, which is to be used, type in command-
```sh
$ ls -hal /dev
```
* Now search for video"num", once you get the camera id you are ready to go. 

# Starting
* In the terminal go to target directory where the project has been saved and then-
```sh
$ python3 main.py "camera_id"
```
* For example: if camera_id is 0 then
```sh
$ python3 main.py 0
```
