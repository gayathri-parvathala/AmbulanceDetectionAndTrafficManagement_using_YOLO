# Ambulance Detection and Traffic Management System
This project uses YOLOv8 for ambulance detection and controls traffic light signals through an Arduino setup to ensure the fast movement of ambulances through traffic. The system processes multiple video feeds from cameras placed at different roads, detects ambulances in real-time, and then sends control signals to the Arduino to change traffic light signals accordingly.

- **Key Components:**

**YOLOv8 Model:** Used to detect ambulances in real-time from video feeds.

**Arduino:** Manages traffic light signals based on the detection of ambulances.

**Python Script:** Controls the detection process and interfaces with Arduino via serial communication.

**Video Feeds:** The system processes four video feeds corresponding to four different roads.
*Requirements*

- **Hardware:**

Arduino (connected via COM port to the computer).
Traffic light setup with LEDs connected to Arduino pins.
Cameras providing video feeds of roads.

- **Software:**

Python (version 3.8+).

- **Required Python libraries:**

opencv-python for video processing.

numpy for handling array manipulations.

ultralytics for YOLOv8 model inference.

pyserial for communication with the Arduino.

- **Install Dependencies:**

Install Python 3.8 or higher.

Install required Python libraries using pip:

pip install opencv-python numpy pyserial (terminal)

Install YOLOv8: To use the YOLOv8 model, clone the ultralytics repository from GitHub:


git clone https://github.com/ultralytics/ultralytics.git (in terminal)

cd ultralytics

pip install -U -r requirements.txt

This will install YOLOv8 and its dependencies.

- **YOLOv8 Model:**

Download or train a YOLOv8 model for ambulance detection and save it as best.pt in the yolov8_model/ folder.
If you are training your own model, refer to the YOLOv8 documentation for training instructions and dataset preparation.
Arduino Setup:

Upload the traffic_management.ino Arduino sketch to the Arduino board. This code will control the traffic light signals.
Connect the LEDs for the traffic lights to the corresponding pins defined in the sketch (for example, pins 4, 2 for road 1, etc.).
The Arduino communicates with the Python script via the COM port to receive commands.

Start the Python Script:

Run the python script to begin processing the video feeds and detect ambulances:

python (your_python_scrpit_file).py (terminal)

*The script will:*

Open the video feeds from the specified paths (cam1.mp4, cam2.mp4, etc.).
Process each video frame using the YOLOv8 model to detect ambulances.
If an ambulance is detected in any road, the Python script sends a command to the Arduino to turn the green light for the respective road, allowing the ambulance to pass.
The traffic lights cycle every 5 seconds by default unless an ambulance is detected, in which case it holds the green light for the corresponding road for 10 seconds.

*Arduino Logic:*

The Arduino will cycle through the four roads, setting each road's green light for 5 seconds by default.
When the Python script sends a signal indicating an ambulance, the Arduino switches the green light for the road where the ambulance is detected and holds it for 10 seconds.
After 10 seconds, the Arduino switches back to the default cycling pattern.
Code Breakdown
*Python Script (detect.py):*

Loads the YOLOv8 model and processes video frames to detect ambulances.
Sends commands to the Arduino via serial communication to control the traffic lights based on ambulance detection.
Arduino Sketch (traffic_management.ino):

Controls the traffic lights for four roads, with the ability to override the default cycle when an ambulance is detected.
YOLOv8 Model Training
If you wish to train your own YOLOv8 model for ambulance detection, ensure that your dataset is organized in the following way:

new_data/

├── images/

    │   ├── train/

        │   ├── val/

        │   └── test/

    ├── labels/

        │   ├── train/

        │   ├── val/

        │   └── test/


- **Notes**

The system processes video feeds in real-time and may require a powerful machine depending on the resolution and number of video feeds.
Make sure the Arduino is properly connected to the computer via the specified COM port.
