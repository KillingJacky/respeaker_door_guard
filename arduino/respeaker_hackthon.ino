
#include "SPI.h"
#include "respeaker.h"
#include <Adafruit_NeoPixel.h>

#define PIXELS_PIN      11
#define PIXELS_NUM      12
#define PIXELS_SPACE    128

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(PIXELS_NUM, PIXELS_PIN, NEO_GRB + NEO_KHZ800);

void touch_event(uint8_t id, uint8_t event) {
  
}

void spi_event(uint8_t addr, uint8_t *data, uint8_t len)
{

}

int pin = 17;

void setup() {
  pixels.begin();
  for (int i = 0; i < PIXELS_NUM; i++) {
    pixels.setPixelColor(i, 0, 0, 32);
  }
  pixels.show();

  respeaker.begin(1,1,0);
  respeaker.attach_touch_isr(touch_event);
  respeaker.attach_spi_isr(spi_event);

  //hackthon
  pinMode(pin, OUTPUT);
  digitalWrite(pin, 0);

  delay(1000);
  pixels.clear();
  pixels.show();
}

uint32_t last_time = 0;

void loop() {
  static uint32_t t = 0;
  for (int i = 0; i < PIXELS_NUM; i++) {
    pixels.setPixelColor(i, triangular_color((t + i * PIXELS_SPACE) % (PIXELS_SPACE * PIXELS_NUM)));
  }
  pixels.show();

  t++;
  if (t >= (PIXELS_SPACE * PIXELS_NUM)) {
    t = 0;
  }


  //hackthon

  uint32_t now = millis();
  if (now - last_time > 5000)
  {
    last_time = now;
    digitalWrite(pin, 1);
    delay(1);
    digitalWrite(pin, 0);
  }
}

uint32_t triangular_color(uint32_t t)
{
  uint32_t c;

  if (t < 256) {
    c = pixels.Color(0, t, 0);
  } else if (t < 512) {
    c = pixels.Color(0, 511 - t, 0);
  }

  return c;
}
