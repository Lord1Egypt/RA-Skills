# Raspberry Pi GPIO and the 40-pin Header

## Overview

All current Raspberry Pi boards feature a 40-pin GPIO (general-purpose input/output) header with a 0.1in (2.54 mm) pin pitch.

> **Note:** The header is unpopulated (has no headers) on Zero and Pico devices that lack the "H" suffix.

| Pin | BCM GPIO | Function |
|:---:|:---:|:---|
| 1 | - | 3.3V Power |
| 2 | - | 5V Power |
| 3 | 2 | GPIO2 (SDA) |
| 4 | - | 5V Power |
| 5 | 3 | GPIO3 (SCL) |
| 6 | - | GND |
| 7 | 4 | GPIO4 (GPCLK0) |
| 8 | 14 | GPIO14 (TXD0) |
| 9 | - | GND |
| 10 | 15 | GPIO15 (RXD0) |
| 11 | 17 | GPIO17 |
| 12 | 18 | GPIO18 (PCM_CLK) |
| 13 | 27 | GPIO27 |
| 14 | - | GND |
| 15 | 22 | GPIO22 |
| 16 | 23 | GPIO23 |
| 17 | - | 3.3V Power |
| 18 | 24 | GPIO24 |
| 19 | 10 | GPIO10 (MOSI) |
| 20 | - | GND |
| 21 | 9 | GPIO9 (MISO) |
| 22 | 25 | GPIO25 |
| 23 | 11 | GPIO11 (SCLK) |
| 24 | 8 | GPIO8 (CE0) |
| 25 | - | GND |
| 26 | 7 | GPIO7 (CE1) |
| 27 | 0 | GPIO0 (ID_SD) |
| 28 | 1 | GPIO1 (ID_SC) |
| 29 | 5 | GPIO5 |
| 30 | - | GND |
| 31 | 6 | GPIO6 |
| 32 | 12 | GPIO12 (PWM0) |
| 33 | 13 | GPIO13 (PWM1) |
| 34 | - | GND |
| 35 | 19 | GPIO19 (PCM_FS) |
| 36 | 16 | GPIO16 (CE2) |
| 37 | 26 | GPIO26 |
| 38 | 20 | GPIO20 (PCM_DIN) |
| 39 | - | GND |
| 40 | 21 | GPIO21 (PCM_DOUT) |

## GPIO Pin Functions

General Purpose I/O (GPIO) pins can be configured as:
- General-purpose input
- General-purpose output
- One of up to six special alternate settings (functions are pin-dependent)

> **Note:** The GPIO pin numbering scheme is not in numerical order. GPIO pins 0 and 1 are present on the board (physical pins 27 and 28), but are reserved for advanced use.

## Outputs

A GPIO pin designated as an output pin can be set to:
- **High:** 3.3V
- **Low:** 0V

## Inputs

A GPIO pin designated as an input pin can be read as:
- **High:** 3.3V
- **Low:** 0V

This is made easier with the use of internal pull-up or pull-down resistors:
- Pins **GPIO2** and **GPIO3** have fixed pull-up resistors
- For other pins, pull-up/pull-down can be configured in software

## View GPIO Pinout

A GPIO reference can be accessed on your Raspberry Pi by opening a terminal window and running the command:

```bash
pinout
```

This tool is provided by the [GPIO Zero](https://gpiozero.readthedocs.io/) Python library, which is installed by default in Raspberry Pi OS.

> **Warning:** While connecting simple components to GPIO pins is safe, be careful how you wire things up:
> - LEDs should have resistors to limit the current passing through them
> - Do not use 5V for 3.3V components
> - Do not connect motors directly to the GPIO pins; instead use an [H-bridge circuit or a motor controller board](https://projects.raspberrypi.org/en/projects/physical-computing/14)

## Permissions

To use the GPIO ports, your user must be a member of the `gpio` group. The default user account is a member by default, but you must add other users manually:

```bash
sudo usermod -a -G gpio <username>
```

## GPIO Pads

The GPIO connections on the BCM2835 package are sometimes referred to as "pads" -- a semiconductor design term meaning "chip connection to outside world".

The pads are configurable CMOS push-pull output drivers/input buffers with register-based control settings for:
- Internal pull-up / pull-down enable/disable
- Output drive strength
- Input Schmitt-trigger filtering

### Power-on States

All GPIO pins revert to general-purpose inputs on power-on reset. The default pull states are also applied (detailed in the alternate function table in the Arm peripherals datasheet). Most GPIOs have a default pull applied.

## Interrupts

Each GPIO pin, when configured as a general-purpose input, can be configured as an interrupt source to the Arm. Several interrupt generation sources are configurable:

| Interrupt Type | Description |
|----------------|-------------|
| Level-sensitive | High/low level detection |
| Rising/falling edge | Edge detection with synchronization |
| Asynchronous rising/falling edge | Edge detection without synchronization |

- **Level interrupts:** Maintain the interrupt status until the level has been cleared by system software
- **Rising/falling edge detection:** Has a small amount of synchronization built into the detection. The pin is sampled at the system clock frequency with criteria for generation of an interrupt being a stable transition within a three-cycle window (record of 1 0 0 or 0 1 1)
- **Asynchronous detection:** Bypasses synchronization to enable detection of very narrow events

## Alternative Functions

Almost all GPIO pins have alternative functions. Peripheral blocks internal to the SoC can be selected to appear on one or more of a set of GPIO pins.

### PWM (Pulse-Width Modulation)

| Type | Available Pins |
|------|----------------|
| Software PWM | All pins |
| Hardware PWM | GPIO12, GPIO13, GPIO18, GPIO19 |

### SPI

| SPI Bus | Pins |
|---------|------|
| **SPI0** | MOSI (GPIO10), MISO (GPIO9), SCLK (GPIO11), CE0 (GPIO8), CE1 (GPIO7) |
| **SPI1** | MOSI (GPIO20), MISO (GPIO19), SCLK (GPIO21), CE0 (GPIO18), CE1 (GPIO17), CE2 (GPIO16) |

### I2C

| Function | Pin |
|----------|-----|
| Data | GPIO2 |
| Clock | GPIO3 |
| EEPROM Data | GPIO0 |
| EEPROM Clock | GPIO1 |

### Serial (UART)

| Function | Pin |
|----------|-----|
| TX | GPIO14 |
| RX | GPIO15 |

> **Note:** Pad control settings such as drive strength or Schmitt filtering still apply when the pin is configured as an alternate function.

## Voltage Specifications

Two 5V pins and two 3.3V pins are present on the board, as well as a number of ground pins (GND), which cannot be reconfigured. The remaining pins are all general-purpose 3.3V pins:
- **Outputs:** Set to 3.3V
- **Inputs:** 3.3V-tolerant

### BCM2835, BCM2836, BCM2837 and RP3A0-based Products

Applies to: Raspberry Pi Zero, Raspberry Pi 3+, etc.

| Symbol | Parameter | Conditions | Min | Typical | Max | Unit |
|--------|-----------|------------|-----|---------|-----|------|
| V_IL | Input Low Voltage | - | - | - | 0.9 | V |
| V_IH | Input High Voltage | Hysteresis enabled | 1.6 | - | - | V |
| I_IL | Input Leakage Current | TA = +85°C | - | - | 5 | µA |
| C_IN | Input Capacitance | - | - | 5 | - | pF |
| V_OL | Output Low Voltage | IOL = -2mA (Default drive: 8mA) | - | - | 0.14 | V |
| V_OH | Output High Voltage | IOH = 2mA (Default drive: 8mA) | 3.0 | - | - | V |
| I_OL | Output Low Current | VO = 0.4V (Max drive: 16mA) | 18 | - | - | mA |
| I_OH | Output High Current | VO = 2.3V (Max drive: 16mA) | 17 | - | - | mA |
| R_PU | Pull-up Resistor | - | 50 | - | 65 | kΩ |
| R_PD | Pull-down Resistor | - | 50 | - | 65 | kΩ |

### BCM2711-based Products (4-series devices)

Applies to: Raspberry Pi 4 series

| Symbol | Parameter | Conditions | Min | Typical | Max | Unit |
|--------|-----------|------------|-----|---------|-----|------|
| V_IL | Input Low Voltage | - | - | - | 0.8 | V |
| V_IH | Input High Voltage | Hysteresis enabled | 2.0 | - | - | V |
| I_IL | Input Leakage Current | TA = +85°C | - | - | 10 | µA |
| V_OL | Output Low Voltage | IOL = -4mA (Default drive: 4mA) | - | - | 0.4 | V |
| V_OH | Output High Voltage | IOH = 4mA (Default drive: 4mA) | 2.6 | - | - | V |
| I_OL | Output Low Current | VO = 0.4V (Max drive: 8mA) | 7 | - | - | mA |
| I_OH | Output High Current | VO = 2.6V (Max drive: 8mA) | 7 | - | - | mA |
| R_PU | Pull-up Resistor | - | 33 | - | 73 | kΩ |
| R_PD | Pull-down Resistor | - | 33 | - | 73 | kΩ |