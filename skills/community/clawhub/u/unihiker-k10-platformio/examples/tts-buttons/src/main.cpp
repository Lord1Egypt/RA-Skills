#include <Arduino.h>
#include "asr.h"
#include "unihiker_k10.h"

UNIHIKER_K10 k10;
ASR asr;

void onButtonAPressed();
void onButtonBPressed();

void setup() {
  k10.begin();
  asr.setAsrSpeed(2);
  k10.buttonA->setPressedCallback(onButtonAPressed);
  k10.buttonB->setPressedCallback(onButtonBPressed);
  asr.speak("你好");
}

void loop() {}

void onButtonAPressed() {
  asr.speak("我是行空板");
}

void onButtonBPressed() {
  asr.speak("语音合成");
}
