# Specialization: Embedded / IoT System

Apply this guidance for firmware, MCU systems, RTOS-based designs, hardware abstraction layers, and IoT edge devices.

## Phase 3 — Embedded Architecture Patterns

| Pattern | When to choose |
|---------|---------------|
| Bare-metal (super loop) | Simple device, deterministic timing, no OS needed |
| RTOS task-based | Multiple concurrent behaviors, timing constraints |
| Hardware Abstraction Layer (HAL) | Portability across hardware variants required |
| Edge + Cloud hybrid | Local processing + cloud sync; offline-capable |
| Firmware OTA | Field-deployed devices requiring remote update |

Mandatory layer for any embedded system with hardware variants:

```
Application Logic
      ↓
Hardware Abstraction Layer (HAL)
      ↓
Board Support Package (BSP) / Drivers
      ↓
Physical Hardware
```

## Phase 5 — Critical Flows for Embedded Systems

1. **Boot / initialization flow**: power-on → hardware init → self-test → main loop
2. **Interrupt service flow**: hardware event → ISR → flag/queue → task handler
3. **Communication protocol flow**: frame receive → parse → validate → dispatch → respond
4. **OTA update flow**: check version → download → verify checksum → apply → reboot
5. **Fault / error handling flow**: detect → log → safe state → notify

## Phase 6 — Storage in Embedded

| Data type | Storage option | Notes |
|-----------|---------------|-------|
| Firmware image | Internal flash | Dual-bank for safe OTA |
| Configuration | EEPROM or flash with wear leveling | |
| Runtime logs | SRAM ring buffer → external flash | Circular overwrite |
| Calibration data | Non-volatile (FRAM / EEPROM) | |
| Streaming sensor data | FIFO buffer → UART/SPI to host | |

## Phase 7 — Embedded-Specific Decision Points

| Decision | Options | Key constraint |
|----------|---------|---------------|
| RTOS vs bare-metal | FreeRTOS, Zephyr vs super-loop | Determinism and task count |
| Communication bus | UART, SPI, I2C, CAN, USB, Ethernet | Speed, distance, node count |
| Memory allocation | Static only vs dynamic | Safety-critical → static only |
| Bootloader | Custom vs MCUboot | OTA needed → use standard bootloader |
| HAL approach | Custom HAL vs vendor SDK HAL | Portability requirement |

## Phase 8 — Interface Design for Embedded

Define these communication contracts:

- **Hardware interface**: pin mapping, voltage levels, timing diagrams, protocol (CAN frame format, UART baud rate, SPI mode)
- **Host / cloud interface**: protocol (MQTT, CoAP, HTTP), message schema, QoS, reconnect behavior
- **Debug interface**: UART log format, JTAG/SWD access, remote shell commands
- **OTA interface**: package format, signature verification, rollback mechanism

## Phase 9 — Deployment for Embedded

| Artifact | Notes |
|----------|-------|
| Firmware binary | Checksum + version metadata embedded |
| Programming tool | Specify flasher tool + config (J-Link, OpenOCD, etc.) |
| Factory programming | Jig procedure, test coverage, pass/fail criteria |
| Field update | OTA mechanism, fallback image, minimum power requirement |
| CI/CD | Cross-compile toolchain, unit tests on host (mocking HAL), HIL tests |

## Phase 10 — Embedded NFR

- **Timing constraints**: define hard real-time (missed deadline = failure) vs soft real-time; specify worst-case execution time for critical ISRs
- **Memory budget**: document RAM and flash usage per module; set hard limits
- **Power budget**: define sleep modes, wake sources, maximum current draw per state
- **Watchdog**: hardware watchdog must be enabled and kicked by application, never in ISR
- **Fail-safe state**: define what the device does on any unhandled error (safe outputs, halt, reboot)
- **EMC / environmental**: note operating temperature range, vibration, humidity, CE/FCC compliance requirements
