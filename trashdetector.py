import cv2 as cv
import numpy as np
from serial import Serial
import time

esp32 = Serial(port='COM4', baudrate=115200, timeout=.1)

classes = ["background", "person", "bicycle", "car", "motorcycle",
  "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant",
  "unknown", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse",
  "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "unknown", "backpack",
  "umbrella", "unknown", "unknown", "handbag", "tie", "suitcase", "frisbee", "skis",
  "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
  "surfboard", "tennis racket", "bottle", "unknown", "wine glass", "cup", "fork", "knife",
  "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog",
  "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "unknown", "dining table",
  "unknown", "unknown", "toilet", "unknown", "tv", "laptop", "mouse", "remote", "keyboard",
  "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "unknown",
  "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush" ]

recycable = ["cup" , "bottle"]
trash = ["fork", "spoon", "knife"]

colors = np.random.uniform(0, 255, size=(len(classes), 3))
cam = cv.VideoCapture(0)

pb  = 'frozen_inference_graph.pb'
pbt = 'ssd_inception_v2_coco_2017_11_17.pbtxt'

cvNet = cv.dnn.readNetFromTensorflow(pb,pbt)   

recentGuess = ""
prevtime = time.time()

while True:
  data = esp32.readline().decode('utf-8').strip()
  if data != "":
    print(data)
    recentGuess = data
  
  ret_val, img = cam.read()
  rows = img.shape[0]
  cols = img.shape[1]
  cvNet.setInput(cv.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False))

  cvOut = cvNet.forward()

  for detection in cvOut[0,0,:,:]:
    score = float(detection[2])
    if score > 0.3:

      idx = int(detection[1])   # prediction class index. 

      if classes[idx] != "dining table" and classes[idx]!="person":

        left = detection[3] * cols
        top = detection[4] * rows
        right = detection[5] * cols
        bottom = detection[6] * rows
        cv.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (23, 230, 210), thickness=2)
            

        label = "{}: {:.2f}%".format(classes[idx],score * 100)
        y = top - 15 if top - 15 > 15 else top + 15
        cv.putText(img, label, (int(left), int(y)),cv.FONT_HERSHEY_SIMPLEX, 0.5, colors[idx], 2)
        if classes[idx] in recycable:
          print("Recycle")
          print(time.time() - prevtime)
          if (time.time() - prevtime) > 4:
            esp32.write('A'.encode('utf-8'))
            prevtime = time.time()
          if recentGuess == "recycle":
            print("Success")
          else:
            print("Wrong Bin")
        else:
          print("Trash")
          print(time.time() - prevtime)
          if (time.time() - prevtime) > 4:
            esp32.write('B'.encode('utf-8'))
            prevtime = time.time()
          if recentGuess == "garbage":
            print("Success")
          else:
            print("Wrong bin")
  cv.imshow('my webcam', img)
  if cv.waitKey(1) == 27: 
    break 
cam.release()
cv.destroyAllWindows()