/* #include <math.h>
#include <ESP32Servo.h>

Servo sortServo;
//port: COM4 (Elecrow CrowPanel 7.0P)

const int trigPin = 2;
const int echoPin = 4;
const int pirPin = 16;
const int buttonPin = 21;

float duration, distance;
double averageUltraReading;
int count = 0;
int counterTimeoutUltrasonic = 0;
int counterTimeoutPIR = 0;
int garbageCount = 0;
int recyclingCount = 0;
int previousPIRstate = 0;
int servoRotationState = 0;
int incomingByte;

void setup()
{
  sortServo.attach(23);
  sortServo.write(90);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(pirPin, INPUT); 
  pinMode(buttonPin, INPUT);
  
  Serial.begin(115200);
  
}

void loop()
{
  if(Serial.available() > 0){
    incomingByte = Serial.read();
    Serial.println(incomingByte);
    if(incomingByte == 65){ //2, 50
      sortServo.write(150);
      delay(2000);
      sortServo.write(90);
      delay(2000);
    }
    
    if(incomingByte == 66){ //3, 51
      sortServo.write(30);
      delay(2000);
      sortServo.write(90);  
      delay(2000);      
    }
  }
  
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(5);
  
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);
  
  distance = (duration * .0343)/2;

  if(count <= 10){
    averageUltraReading = ((averageUltraReading * count) + distance)/(count+1);
    count++;
    counterTimeoutUltrasonic++;
  }else if(count > 10){
    if(fabs(averageUltraReading - distance) < 5){
      averageUltraReading = ((averageUltraReading * count) + distance)/(count+1);
      if(count < 20){
        count++;        
      }
      counterTimeoutUltrasonic++;
//      if(sortServo.read() != 90){
//        sortServo.write(90);
//      }
    }else{
      if(counterTimeoutUltrasonic > 10){
        garbageCount++;
        Serial.println("garbage");
        counterTimeoutUltrasonic = 0;
      }
//      Serial.print("Detected Garbage, Garbage count: ");
//      Serial.println(garbageCount);
      
//      if(sortServo.read() != 180){
//        sortServo.write(180);
//      }

//      if(servoRotationState < 10){
//        Serial.println("Tilting servo left");
//        sortServo.write(180);
//        servoRotationState++;
//      }else if(servoRotationState <= 50){
//        servoRotationState++;
//      }else if(servoRotationState > 50){
//        Serial.println("Tilting servo middle");
//        sortServo.write(90);
//      }

    }
  }

  int pirRead = digitalRead(pirPin);
//  Serial.println(pirRead);

  if(pirRead == 0){
    counterTimeoutPIR++;
    previousPIRstate = 0;
//    if(sortServo.read() != 90){
//      sortServo.write(90);
//    }
  }else if (previousPIRstate == 0 && pirRead == 1){
    previousPIRstate = 1;
    if(counterTimeoutPIR > 10){
      Serial.println("recycling");
      recyclingCount++;
      counterTimeoutPIR = 0;
    }
  
//    Serial.print("Detected Recycling, Recycling count: ");
//    Serial.println(recyclingCount);
//    if(sortServo.read() != 0){
//      sortServo.write(0);
//    }
  }
  
//  Serial.print(distance);
//  Serial.println(averageUltraReading);

//  Serial.println(digitalRead(buttonPin));

  delay(100);
} */