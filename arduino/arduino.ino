#include <Servo.h>
#include <string.h>
 
Servo servo_x;
Servo servo_y;

String data;

int indexx;
int indexy;

int pos_x = 90;
int pos_y = 90;

void setup() {
   Serial.begin(9600);
   servo_x.attach(9);
   servo_y.attach(10);
}
 
void loop(){
  if (Serial.available()){
    data = Serial.readStringUntil('\n');
    indexx = data.indexOf('x');
    indexy = data.indexOf('y');
    
    if (indexx != -1 && indexy != -1){
      pos_x = data.substring(indexx + 1, indexy - 1).toInt();
      pos_y = data.substring(indexy + 1).toInt();

      if (pos_x >= 0 && pos_x <= 180){
        servo_x.write(pos_x);
        }

      if (pos_y >= 0 && pos_y <= 180){
        servo_y.write(pos_y);
        }
    }
    
    delay(10);
    data = ""; 
  } 
}
