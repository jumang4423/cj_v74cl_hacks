#include "MIDIUSB.h"

const int N_READPIN = 3;
const int N_WRITEPIN = 4;
const int DEFAULT_CHANNEL = 0;
const int DEFAULT_VELOCITY = 64;
int buffer[N_READPIN][N_WRITEPIN];
int buffer_old[N_READPIN][N_WRITEPIN];

int writePins[N_WRITEPIN] = {5, 6, 7, 8};
int readPins[N_READPIN] = {2, 3, 4};

int notes[N_WRITEPIN][N_READPIN] = {
  {72, 73, 74},
  {68, 69, 70},
  {64, 65, 66},
  {60, 61, 62}
};

void noteOn(byte channel, byte pitch, byte velocity) {
  midiEventPacket_t noteOn = {0x09, 0x90 | channel, pitch, velocity};
  MidiUSB.sendMIDI(noteOn);
}

void noteOff(byte channel, byte pitch, byte velocity) {
  midiEventPacket_t noteOff = {0x08, 0x80 | channel, pitch, velocity};
  MidiUSB.sendMIDI(noteOff);
}

void setup()
{
  Serial.begin(115200);
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

void play_notes(int j, int i) {
  bool is_played = false;
  // noteOn
  if (buffer[j][i] == 0 && buffer_old[j][i] == 1) {
    noteOn(DEFAULT_CHANNEL, notes[i][j], DEFAULT_VELOCITY);
    is_played = true;
  }
  // noteOff
  if (buffer[j][i] == 1 && buffer_old[j][i] == 0) {
    noteOff(DEFAULT_CHANNEL, notes[i][j], DEFAULT_VELOCITY);
    is_played = true;
  }
  if (is_played) {
    MidiUSB.flush();
  }
}

void loop()
{
  for (int i = 0; i < N_WRITEPIN; i++)
  {
    digitalWrite(writePins[i], LOW);
    
    for (int j = 0; j < N_READPIN; j++)
    {
      buffer[j][i] = digitalRead(readPins[j]);
      play_notes(j, i);
    }
    digitalWrite(writePins[i],HIGH);
  }

  // sync buffers
  for (int i = 0; i < N_READPIN; i++)
  {
    for (int j = 0; j < N_WRITEPIN; j++)
    {
      buffer_old[i][j] = buffer[i][j];
    }
  }

  delay(8);
}

