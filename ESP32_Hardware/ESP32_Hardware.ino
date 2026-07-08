/*
 * JARVIS Ultimate Core - ESP32 Hardware Controller
 * Author: Jimmy Hadad
 * Description: Listens to serial commands from the Python AI vision system.
 * Integrates an SSD1306 OLED display for status updates and a Servo motor for physical actuation.
 */

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <ESP32Servo.h> 

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// Initialize the OLED display on I2C address 0x3C
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

Servo myServo;
const int servoPin = 18; 

void setup() {
  Serial.begin(9600);
  
  // Initialize Servo
  myServo.attach(servoPin);
  myServo.write(0);

  // Initialize OLED Display
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }
  
  // 1.(Welcome Screen) 
  display.clearDisplay();
  display.setTextColor(WHITE);
  
  display.setTextSize(2);
  display.setCursor(28, 22);
  display.println("JARVIS");
  
  display.setTextSize(1);
  display.setCursor(4, 45);
  display.println("Waiting for vision..");
  display.display();
}

void loop() {
  // Listen for commands from the Python AI core
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    // If Python sends '1' (Cell Phone Detected)
    if (command == '1') {
      
      // 2. (Detection Screen)
      display.clearDisplay();
      
      display.setTextSize(2);
      display.setCursor(4, 20); 
      display.println("CELL PHONE");
      
      display.setCursor(10, 42); 
      display.println("DETECTED!");
      display.display();
      
      // Actuate Servo
      myServo.write(90);
      delay(3000); 
      
      // 3.(Ready Screen)
      myServo.write(0);
      display.clearDisplay();
      
      display.setTextSize(2);
      display.setCursor(28, 22); 
      display.println("JARVIS");
      
      display.setTextSize(1);
      display.setCursor(19, 45); 
      display.println("System Ready...");
      display.display();
    }
  }
}
