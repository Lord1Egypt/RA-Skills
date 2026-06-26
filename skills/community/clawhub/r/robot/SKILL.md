---
name: Robot
slug: robot
version: 1.0.0
description: Build robots from hobby to industrial with hardware wiring, ROS2, motion planning, and safety constraints.
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## When to Use

User needs robotics help — Arduino/ESP32 wiring, ROS2 configuration, motor control, sensor integration, or industrial robot programming. Agent handles hardware selection, code generation, and debugging across hobby to professional contexts.

## Architecture

Memory lives in `~/robot/` with tiered structure. See `memory-template.md` for initial setup.

```
~/robot/
├── memory.md          # HOT: inventory + active project
├── inventory.md       # Hardware owned (boards, sensors, motors)
├── projects/          # Per-project configs and learnings
│   └── {name}.md      # Project-specific notes
├── corrections.md     # What failed + fixes found
└── archive/           # Completed project summaries
```

## Quick Reference

| Topic | File |
|-------|------|
| Memory setup | `memory-template.md` |
| Arduino, ESP32, RPi wiring | `hardware.md` |
| Sensors: wiring + code | `sensors.md` |
| Motors: types + drivers | `motors.md` |
| ROS1/ROS2, Gazebo, MoveIt | `ros.md` |
| Industrial arms (ABB, KUKA, UR) | `industrial.md` |
| Systematic troubleshooting | `debugging.md` |
| Common project templates | `projects.md` |

## Core Rules

### 1. Check Memory First
Before ANY recommendation:
1. Read ~/robot/memory.md — what hardware does user have?
2. Check ~/robot/projects/ — is there an active project?
3. Check ~/robot/corrections.md — past failures to avoid?

### 2. ASK Exact Hardware
Before ANY code: exact board model, exact sensor/motor models, voltage rails.
"Arduino" is ambiguous (Uno? Nano? ESP32-based?). Add to inventory once confirmed.

### 3. Update Memory Proactively
| Event | Action |
|-------|--------|
| User mentions hardware they own | Add to inventory.md |
| User starts new project | Create projects/{name}.md |
| Something fails → fix found | Log in corrections.md |
| Project completed | Archive to archive/ |

### 4. Version Everything
Always ask and specify:
- Arduino core version, library versions
- ROS distro (Humble, Iron, Foxy, Noetic)
- Firmware versions for industrial controllers

### 5. Simulation First for Industrial
For ABB/KUKA/Fanuc/UR code:
- Always clarify: simulation or real hardware?
- Never generate motion code without safety discussion
- Include speed limits and safety checks in ALL code

## Hardware Traps

### Board Selection
- `Servo.h` crashes on ESP32 — use `ESP32Servo.h` (different API)
- `analogWrite()` missing on ESP32 — use `ledcWrite()` + channel setup
- ESP32 GPIO 6-11 are flash pins — touching them = crash
- ESP32 GPIO 34-39 are input-only — output silently fails
- Arduino pins 0,1 are Serial — using them breaks upload

### Voltage and Current
- 5V sensor → 3.3V board without divider — burns pin permanently
- GPIO sourcing >40mA (Uno) or >12mA (ESP32) — pin damage over time
- Motor on same rail as logic — brownouts cause random resets
- No common ground between boards — erratic sensor readings

### Sensors
- HC-SR04 Echo pin 5V → 3.3V board — needs divider or level shifter
- DHT22 read interval <2s — returns stale/error values
- I2C bus >30cm without pullups — intermittent failures
- MPU6050 FIFO overflow if not read fast — readings corrupt

## ROS Traps

- Mixing `rospy` (ROS1) and `rclpy` (ROS2) — import errors
- Forgot `source install/setup.bash` — "package not found"
- QoS mismatch publisher/subscriber — messages silently dropped
- `static_transform_publisher` syntax varies by ROS2 version
- Gazebo Classic plugins ≠ Ignition/Fortress plugins

## Industrial Traps

- MoveL through singularity — joint whip, dangerous
- Wrong coordinate frame (base vs world vs tool) — unexpected position
- Omitting MoveJ before MoveL — path through obstacles
- Speed too high in shared human space — safety violation
- Bypassing SafeMove/SafetyIO signals — defeats physical safeties
