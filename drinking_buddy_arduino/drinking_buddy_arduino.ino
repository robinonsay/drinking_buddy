
typedef enum{
  pump1 = 9,
  pump2 = 10,
  pump3 = 11
} Pump;
const int BUFFER_SIZE = 3;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.flush();
}

void loop() {
  // put your main code here, to run repeatedly:
  char motorCmdBuffer[] = {0, 0, 0};
  Pump p1 = pump1;
  Pump p2 = pump2;
  Pump p3 = pump3;
  while (Serial.available() < 3);
  int bytesRead = Serial.readBytes(motorCmdBuffer, BUFFER_SIZE);
  runPump(p3, motorCmdBuffer[2]);
  runPump(p1, motorCmdBuffer[0]);
  runPump(p2, motorCmdBuffer[1]);
}

void runPump(Pump p, int duration){
  /*
   * p: Pump to run
   * duration: Time to run pump in seconds
   */
  analogWrite(p, 0xff);
  delay(duration*1000);
  analogWrite(p, 0);
}



