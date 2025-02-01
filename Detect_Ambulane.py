from ultralytics import YOLO
import cv2
import numpy as np
import serial
import time
model_path = 'C:\\Users\\yolei\\Desktop\\amb_v8\\runs\\detect\\train3\\weights\\best.pt'
video_paths = [
    "C:/Users/*****/Downloads/cam1.mp4",  #add path to your videos
    "C:/Users/*****/Downloads/cam2.mp4",  
    "C:/Users/*****/Downloads/cam3.mp4",  
    "C:/Users/*****/Downloads/cam4.mp4"   
]

model = YOLO(model_path)
confidence_threshold = 0.82
class_names = model.names
caps = [cv2.VideoCapture(video_path) for video_path in video_paths]
for i, cap in enumerate(caps):
    if not cap.isOpened():
        print(f"Error: Could not open video {video_paths[i]}.")
        exit()
ser = serial.Serial('COM3', 9600)  
time.sleep(2)
initial_module = 1  
ser.write(f'{initial_module}'.encode())  
time.sleep(5)  
def process_videos():
    global initial_module  
    frame_skip = 8  
    frame_count = [0] * len(caps)  
    output_frames = [None] * len(caps)  
    video_ended = [False] * len(caps)  
    last_signal_times = [0] * len(caps)  
    signal_count = [0] * len(caps)  
    signal_sent = [False] * len(caps)  
    signal_duration = 10  
    last_display_update = time.time()  
    display_interval = 0.5  
    while True:
        current_time = time.time()  
        for i, cap in enumerate(caps):
            if video_ended[i]:
                continue  
            ret, frame = cap.read()
            if not ret:
                video_ended[i] = True  
                continue  
            if frame_count[i] % frame_skip == 0:
                resized_frame = cv2.resize(frame, (320, 240))
                results = model.predict(source=resized_frame, save=False, show=False, verbose=False)
                ambulance_detected = False
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()  
                        conf = box.conf[0].cpu().numpy() 
                        cls = int(box.cls[0].cpu().numpy())  
                        if conf >= confidence_threshold:  
                            class_name = class_names[cls]  
                            if class_name == 'ambulance':  
                                ambulance_detected = True
                                print(f"Ambulance detected on road {i + 1}. Sending command to Arduino: {i + 1}")
                                if signal_count[i] < 2:  
                                    if not signal_sent[i]:  
                                        ser.write(f'{i + 1}'.encode())  
                                        last_signal_times[i] = current_time  
                                        signal_count[i] += 1 
                                        signal_sent[i] = True  
                                cv2.rectangle(resized_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                                cv2.putText(resized_frame, 'Ambulance', (int(x1), int(y1) - 10),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                if current_time - last_signal_times[i] >= signal_duration:
                    if signal_count[i] < 2:
                        signal_sent[i] = False  
                if current_time - last_signal_times[i] >= signal_duration and signal_count[i] >= 2:
                    ser.write(f'{initial_module}'.encode()) 
                    initial_module = (initial_module % 4) + 1  
                    signal_count[i] = 0 
                cv2.putText(resized_frame, f'Road {i + 1}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 255), 2, cv2.LINE_AA)
                output_frames[i] = cv2.resize(resized_frame, (640, 360)) 
                frame_count[i] += 1
        if time.time() - last_display_update > display_interval:
            valid_frames = [frame for frame in output_frames if frame is not None]
            if len(valid_frames) == 4: 
                top_row = np.hstack((valid_frames[0], valid_frames[1]))
                bottom_row = np.hstack((valid_frames[2], valid_frames[3]))
                grid_frame = np.vstack((top_row, bottom_row))
                cv2.imshow('Video Detection Grid', grid_frame)
            elif valid_frames:  
                grid_frame = np.hstack(valid_frames)  
                cv2.imshow('Video Detection Grid', grid_frame)
            last_display_update = time.time() 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    for cap in caps:
        cap.release()
    cv2.destroyAllWindows()
process_videos()
