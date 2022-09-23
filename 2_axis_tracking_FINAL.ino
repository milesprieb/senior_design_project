#include<Servo.h>
#include "ServoEasing.hpp"

ServoEasing x, y;
const int SERVO_PIN = 12;

int width = 640, height = 480;  // total resolution of the video
int xpos = 90, ypos = 25;  // initial positions of both Servos
void setup() {

  pinMode(SERVO_PIN, OUTPUT);
  Serial.begin(9600);
  x.attach(10);
  y.attach(9);
  // Serial.print(width);
  //Serial.print("\t");
  //Serial.println(height);
  x.write(xpos);
  y.write(ypos);
}
const int angle = 2;   // degree of increment or decrement
int tmp = 0;
void loop() {
  if (Serial.available() > 0)
  {
    int x_mid, y_mid,servo_state;

    char message = Serial.read();
    
    if (message == 'X')
    {
      x_mid = Serial.parseInt();  // read center x-coordinate
      if (Serial.read() == 'Y'){
        y_mid = Serial.parseInt(); // read center y-coordinate
        tmp = 1;
        servo_state = HIGH;
      }
    }
    else if (message == 'F')
      {
          //Serial.print("HERE");
          xpos = 90;
          ypos = 25;
          x.easeTo(90,40);
          y.easeTo(25,40);
//          Serial.flush();
          tmp = 0;
          servo_state = LOW;
      }
      Serial.print(message);
    if (tmp == 1){
      
        /* adjust the servo within the region of interest (ROI) if the coordinates
            is outside it
        */
        if (x_mid > width / 2 + 30) // If the ROI is to the right of the current camera position, increase pan servo angle
          xpos += angle;
        if (x_mid < width / 2 - 30) // If the ROI is to the left of the current camera position, decrease pan servo angle
          xpos -= angle;
        if (y_mid < height / 2 + 30) // If the ROI is below the current camera position, decrease tilt servo angle
          ypos -= angle;
        if (y_mid > height / 2 - 30) // If the ROI is above the current camera position, increase tilt servo angle
          ypos += angle;
        x.easeTo(xpos - 5,40); // Adjust for offset of nozzle with respect to camera, in x-direction
        y.easeTo(ypos - 5,40); // Adjust for offset of nozzle with respect to camera, in y-direction
        tmp = 0;
    }

    // if the servo degree is outside its range
    /*
    if (xpos >= 180)
      xpos = 180;
    else if (xpos <= 0)
      xpos = 0;
    if (ypos >= 180)
      ypos = 180;
    else if (ypos <= 0)
      ypos = 0;
      */

    
    
    digitalWrite(13,servo_state);
    digitalWrite(SERVO_PIN, servo_state);

    // used for testing
    //Serial.print(xpos);
    //Serial.print(" ");
    //Serial.println(ypos);
    //Serial.print(" ");
    //Serial.print(servo_state);
  }
}