const int N_READPIN = 3;
const int N_WRITEPIN = 4;
/**
 * #PHONE BUTTON#
 * 1 2 3
 * 4 5 6
 * 7 8 9
 * * 0 #
 *
 * |phone | write | read  |
 * | ---- | ----  | ----- |
 * | 1    |  18   |  8    |
 * | 2    |  19   |  8    |
 * | 3    |  20   |       |
 */
int writePins[N_WRITEPIN] = {5, 6, 7, 8}; // 8,10,11,22
int readPins[N_READPIN] = {2, 3, 4};      // 18,19,21




void setup()
{
  Serial.begin(9600);
  for (int i = 0; i < N_READPIN; i++)
  {
    pinMode(readPins[i],INPUT_PULLUP);
  }
  for (int i = 0; i < N_WRITEPIN; i++)
  {
    pinMode(writePins[i], OUTPUT);
    digitalWrite(writePins[i], HIGH);
  }



}

void loop()
{
  for (int i = 0; i < N_WRITEPIN; i++)
  {
    digitalWrite(writePins[i], LOW);
    for (int j = 0; j < N_READPIN; j++)
    {

      Serial.print(digitalRead(readPins[j]));
      if(i==(N_WRITEPIN-1) && j==(N_READPIN-1)){
          Serial.println();
      }else{
        Serial.print(",");
      }
        
    }
    digitalWrite(writePins[i],HIGH);
  }
  delay(16);
}
