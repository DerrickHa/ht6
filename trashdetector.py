import cv2 as cv
import numpy as np
import serial
from supabase import create_client, Client
import time

#0312

SUPABASE_URL = "https://sndaxdsredktgpsakage.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNuZGF4ZHNyZWRrdGdwc2FrYWdlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyMjcxOTIyNywiZXhwIjoyMDM4Mjk1MjI3fQ.62q7Xfaifhqg26p6wapWd-bOfekg3ACHw85W4p0h8yM"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# esp32 = serial.Serial(port='COM4', baudrate=115200, timeout=.1)
esp32 = serial.Serial(port='/dev/cu.usbserial-110', baudrate=115200, timeout=.1)

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

recycable = ["cup" , "bottle", "fork"]
trash = ["spoon", "knife"]

colors = np.random.uniform(0, 255, size=(len(classes), 3))
cam = cv.VideoCapture(2)

pb  = 'frozen_inference_graph.pb'
pbt = 'ssd_inception_v2_coco_2017_11_17.pbtxt'

cvNet = cv.dnn.readNetFromTensorflow(pb,pbt)   

recentGuess = ""
prevtime = time.time()
leaderboardScore = 0 #send to database

def updateScore():
  global leaderboardScore
  response = supabase.table('leaderboard').update({"aura": leaderboardScore}).eq('id', 1).execute()
  print(response)

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

      if classes[idx] != "dining table" and classes[idx]!="person" and classes[idx] != "clock" and classes[idx] != "refrigerator" and classes[idx] != "oven" and classes[idx] != "toilet":

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
            print("Send A")
            esp32.write('A'.encode('utf-8'))
            prevtime = time.time()
            if recentGuess == "recycle":
              print("Success")
              leaderboardScore += 150
              updateScore()
              esp32.write('C'.encode('utf-8'))
            else:
              print("Wrong Bin")
              leaderboardScore -= 150
              updateScore()
              esp32.write('D'.encode('utf-8'))
        else:
          print("Trash")
          print(time.time() - prevtime)
          if (time.time() - prevtime) > 4:
            print("Send B")
            esp32.write('B'.encode('utf-8'))
            prevtime = time.time()
            if recentGuess == "garbage":
              print("Success")
              leaderboardScore += 100
              updateScore()
              esp32.write('C'.encode('utf-8'))
            else:
              print("Wrong bin")
              leaderboardScore -= 200
              updateScore()
              esp32.write('D'.encode('utf-8'))
  cv.imshow('my webcam', img)
  if cv.waitKey(1) == 27: 
    break 
cam.release()
cv.destroyAllWindows()