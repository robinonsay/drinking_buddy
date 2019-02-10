/*
 Fading

 This example shows how to fade an LED using the analogWrite() function.

 The circuit:
 * LED attached from digital pin 9 to ground.

 Created 1 Nov 2008
 By David A. Mellis
 modified 30 Aug 2011
 By Tom Igoe

 http://www.arduino.cc/en/Tutorial/Fading

 This example code is in the public domain.

 */


int pump1 = 9;    // LED connected to digital pin 9
int pump2 = 10;    // LED connected to digital pin 9
int pump3 = 11;    // LED connected to digital pin 9

void setup() {
  // nothing happens in setup
}

void loop() {
  // fade in from min to max in increments of 5 points:
  analogWrite(pump1, 0xff);
  analogWrite(pump2, 0xff);
  analogWrite(pump3, 0xff);
  delay(5000);
  analogWrite(pump1, 0);
  analogWrite(pump2, 0);
  analogWrite(pump3, 0);
  exit(1);
}


