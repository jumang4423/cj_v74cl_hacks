const int N_READPIN = 3;
const int N_WRITEPIN = 4;

int writePins[N_WRITEPIN] = {5, 6, 7, 8};
int readPins[N_READPIN] = {2, 3, 4};

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
  static char buffer[N_READPIN * N_WRITEPIN * 2 + 1]; // Buffer to store the read values
  char* p = buffer; // Pointer to the current position in the buffer

  for (int i = 0; i < N_WRITEPIN; i++)
  {
    digitalWrite(writePins[i], LOW);
    
    for (int j = 0; j < N_READPIN; j++)
    {
      *p++ = '0' + digitalRead(readPins[j]); // Store the read value in the buffer
      *p++ = ','; // Add a comma separator
    }
    digitalWrite(writePins[i],HIGH);
  }
  p[-1] = '\n'; // Replace the last comma with a newline
  *p = '\0'; // Null-terminate the string
  Serial.print(buffer); // Print the entire buffer at once
  delay(16);
}
