# K10 Box Hardware Map

## Hardware boundaries

The K10 board and the K10 experiment box share a physical I2C bus but are not
the same hardware layer.

| Layer | Device | Address or pin | Purpose |
| --- | --- | --- | --- |
| K10 native | AHT20 | `0x38` | Temperature and humidity |
| K10 native | LTR303 | `0x29` | Ambient light |
| K10 native | SC7A20H | `0x19` | Native accelerometer; may be absent on some box assemblies |
| K10 native | Microphone/speaker | I2S | Audio input and output |
| K10 native | A/B buttons | P5/P11 | UI input |
| K10 native | LCD/RGB | board devices | Display and three RGB LEDs |
| K10 Box | IO controller | `0x20` | Inputs, motors, buzzer, red/yellow/green LEDs |
| K10 Box | Line tracker | `0x30` | Five line channels and thresholds |
| K10 Box | QMI8658 | `0x6B` | Box accelerometer and gyroscope |
| K10 Box | I2C bus | SDA 47, SCL 48 | Shared box connection |

Box GPIO inputs used by the driver:

| Input | Pin | Active state |
| --- | --- | --- |
| Left key | P8 | Low |
| Right key | P9 | Low |
| Conductance | P10 | Project-specific digital state |
| Infrared obstacle | P13 | Low |

## Box sensor API

```cpp
uint16_t getSoundVolume();
uint16_t getKnobValue();
uint32_t getIRValue();
uint16_t getSR04Value();            // 0xFFFF means no valid distance.

String getLinePatrolValueAll();
String getLinePatrolThresholdAll();
String getLinePatrolStatusAll();

uint8_t readQMI8658CID();           // Expected: 0x05.
void initQMI8658C();
void getQMI8658xyz();
```

Convert one QMI8658 raw sample after successful initialization:

```cpp
box.getQMI8658xyz();
float accXmg = static_cast<float>(box.accX) * 1000.0F / box.ssvtA;
float accYmg = static_cast<float>(box.accY) * 1000.0F / box.ssvtA;
float accZmg = static_cast<float>(box.accZ) * 1000.0F / box.ssvtA;
float gyroXdps = static_cast<float>(box.gyroX) / box.ssvtG;
float gyroYdps = static_cast<float>(box.gyroY) / box.ssvtG;
float gyroZdps = static_cast<float>(box.gyroZ) / box.ssvtG;
```

Never use these divisors before initialization. If chip ID is not `0x05`, show
`N/A` and keep the raw conversion path disabled.

## Box actuator API

```cpp
void setMotor1Run(uint8_t direction, uint8_t speed);
void setMotor2Run(uint8_t direction, uint8_t speed);
void setBothMotorsRun(uint8_t dir1, uint8_t speed1,
                      uint8_t dir2, uint8_t speed2);

void setBuzzer(uint16_t frequencyHz);
void stopBuzzer();

void red_analog(uint8_t brightness);
void yellow_analog(uint8_t brightness);
void green_analog(uint8_t brightness);
void red_digital(uint8_t state);
void yellow_digital(uint8_t state);
void green_digital(uint8_t state);
```

Directions are `0` and `1`; the driver compensates for M2's reversed physical
wiring. Speed is `0..255`. The official hardware test uses `255`; short pulses
near `90` may not overcome geared-motor starting friction.

The driver contains no servo method. Do not claim that the experiment box can
drive a servo through this API.

## Safe presence probes

```cpp
Wire.beginTransmission(IO_Device_addr);
bool boxIoAvailable = Wire.endTransmission() == 0;

Wire.beginTransmission(LINE_PATROL_ADDR);
bool lineTrackerAvailable = Wire.endTransmission() == 0;

uint8_t qmiChipId = box.readQMI8658CID();
bool boxImuAvailable = qmiChipId == 0x05;
```

Do not enable motors, LEDs, or the box buzzer unless IO controller `0x20` is
present.
