---
name: quadruped
description: Comprehensive quadruped robot development skill covering motor control, sensor data processing, locomotion patterns, and debugging workflows. Use when working with legged robots (e.g., Unitree Go1, ANYmal, custom four-legged designs) for tasks like: motor control commands, IMU/encoder data handling, motion planning, walking/running gaits, sensor fusion, system diagnostics, or protocol communication (CAN bus, UART, EtherCAT).
---

# Quadruped Robot Development

## Overview

This skill provides tools and guidance for developing quadruped robots, including motor control, sensor data processing, locomotion patterns, and debugging workflows. Target platforms include Unitree Go1, ANYmal, and custom four-legged robots.

**机器人名称**: 太玄照业 - The virtual quadruped robot you're controlling

## Core Capabilities

### 1. Motor Control

Control individual motors or coordinated multi-motor commands for gait generation.

**Typical operations:**
- Set motor position/velocity/force
- Read motor telemetry (temperature, voltage, errors)
- Configure motor parameters (PID gains, limits)
- Emergency stop and safety protocols

### 2. Sensor Data Processing

Handle sensor inputs from IMUs, joint encoders, and environmental sensors.

**Typical operations:**
- Read IMU data (acceleration, gyro, orientation)
- Process encoder data for joint position/velocity
- Temperature and voltage monitoring
- Sensor fusion for state estimation

### 3. Locomotion Patterns

Implement and tune walking, running, and other gaits.

**Typical operations:**
- Stance phase planning
- Swing phase kinematics
- High-speed running stabilization
- Gait transition logic

### 4. Debugging & Diagnostics

Monitor system health and debug communication issues.

**Typical operations:**
- Real-time motor telemetry display
- IMU data visualization
- Communication protocol debugging
- System status reports

## Quick Start

### Basic Motor Control

```python
# Example: Initialize and control a motor
from quadruped import Motor, Quadruped

# Initialize robot (adjust port/ID based on your setup)
robot = Quadruped(port='/dev/ttyUSB0', baudrate=1000000)

# Enable motors
for motor_id in range(1, 13):
    robot.motor[motor_id].enable()

# Set target position (degrees)
robot.motor[1].set_position(45.0)
robot.motor[2].set_position(45.0)

# Read motor status
status = robot.motor[1].get_status()
print(f"Position: {status.position:.2f}°, Temperature: {status.temperature:.1f}°C")
```

### IMU Data Reading

```python
# Example: Read IMU data
imu_data = robot.imu.read()
print(f"Accel: {imu_data.accel} m/s²")
print(f"Gyro: {imu_data.gyro} rad/s")
print(f"Quaternion: {imu_data.quaternion}")
```

### Walking Gait

```python
# Example: Simple forward walking
robot.gait.walk(forward_steps=10, step_length=0.3, frequency=1.5)

# Wait for completion
robot.gait.wait()

# Stop
robot.stop()
```

### Virtual Robot Control

Use the simulator to test code before hardware connection:

```python
from sim_state import QuadrupedSimulator
from sim_control import QuadrupedController
from gait_generator import QuadrupedGaitGenerator, GaitType

# Create simulator
sim = QuadrupedSimulator()
controller = QuadrupedController(sim, dt=0.01)

# Set initial pose
controller.set_static_pose()
time.sleep(0.5)

# Run walking gait
controller.set_gait_walk(step_length=0.1, frequency=1.0)

# Monitor real-time
controller.monitor(interval=0.1)

# Or run pre-programmed animation
controller.run_animation(duration=5.0)

# Get current state
state = sim.get_state_dict()
print(f"Position: ({state['global']['x']:.2f}, {state['global']['y']:.2f})")
print(f"IMU: {state['imu']['accel']}")

### Generate Custom Gaits

Use the gait generator for custom locomotion patterns:

```python
from gait_generator import QuadrupedGaitGenerator, GaitType

generator = QuadrupedGaitGenerator()

# Generate trot gait
positions, freq = generator.create_gait_profile(
    GaitType.TROT,
    amplitude=25,
    frequency=1.2
)

# Generate run gait with flight phase
positions, freq = generator.create_gait_profile(
    GaitType.RUN,
    amplitude=45,
    frequency=2.0,
    flight_phase=0.2
)

# Generate gallop gait
positions, freq = generator.create_gait_profile(
    GaitType.GALLOP,
    amplitude=40,
    frequency=2.5
)

# Export to JSON for robot execution
from motion_export import MotionExporter
exporter = MotionExporter(generator)
json_path = exporter.export_to_json(
    positions,
    gait_type='trot',
    frequency=freq,
    metadata={'author': 'user', 'notes': 'Custom trot pattern'}
)

print(f"Motion exported to: {json_path}")
```

### Create Motion Sequences

Combine multiple gait patterns:

```python
from motion_export import MotionExporter

exporter = MotionExporter()

# Create sequence: stand → walk → run → stand
sequence = [
    {
        'gait_type': 'static',
        'duration': 1.0,
        'amplitude': 0
    },
    {
        'gait_type': 'walk',
        'duration': 2.0,
        'frequency': 1.0,
        'amplitude': 30
    },
    {
        'gait_type': 'run',
        'duration': 2.0,
        'frequency': 2.0,
        'amplitude': 45
    },
    {
        'gait_type': 'static',
        'duration': 1.0,
        'amplitude': 0
    }
]

# Generate and export
all_positions = exporter.create_motion_sequence(sequence)
json_path = exporter.export_to_json(
    all_positions,
    gait_type='sequence',
    frequency=1.0,
    output_path='motion_sequence.json'
)
```

## Resource Structure

### scripts/
Motor control utilities and sensor reading scripts.

**Available scripts:**
- `motor_control.py` - Motor initialization, control, and status reading
- `imu_reader.py` - IMU data acquisition and formatting
- `sim_state.py` - Virtual robot state simulation
- `sim_control.py` - Virtual robot interactive control
- `gait_generator.py` - Quadruped gait pattern generation
- `motion_export.py` - Motion trajectory export (JSON, CSV)
- `encoder_reader.py` - Joint encoder data processing (预留)
- `telemetry_monitor.py` - Real-time system monitoring dashboard (预留)

### references/
Technical documentation for sensor data formats, motion models, and protocol details.

**Available references:**
- `motor_protocol.md` - Motor command protocol specification
- `imu_format.md` - IMU data format and coordinate frames
- `motion_kinematics.md` - Inverse kinematics for leg movements

## Best Practices

### Communication Protocol

Always check connection status before sending commands. Use timeout values appropriate for your hardware.

```python
# Example: Safe motor command pattern
try:
    robot.connect()
    if not robot.is_connected():
        raise ConnectionError("Robot not connected")

    robot.motor[1].set_position(45.0)
    status = robot.motor[1].get_status()
except Exception as e:
    print(f"Error: {e}")
    robot.emergency_stop()
finally:
    robot.disconnect()
```

### Safety First

- Always enable motors before attempting motion
- Set safe position limits before running gaits
- Monitor temperature and error states during operation
- Implement emergency stop capability

### Debugging Tips

1. **Communication Issues**: Check baud rate and cable connections first
2. **Motor Errors**: Check for overheating, overcurrent, or cable breaks
3. **Poor Gait Performance**: Check sensor calibration and PID tuning
4. **Unexpected Motion**: Verify gait parameters and ensure motors are enabled

## Common Tasks

### Task 1: Calibrate Sensors

```bash
# Use the calibration script
python scripts/motor_control.py --calibrate
```

### Task 2: Test Motor Control

```bash
# Move individual motors in test mode
python scripts/motor_control.py --test --motor 1
```

### Task 3: Monitor System Telemetry

```bash
# Real-time monitoring (requires Python GUI or serial console)
python scripts/telemetry_monitor.py
```

### Task 4: Generate Motion Patterns

```bash
# Create and save a motion profile
python scripts/motion_planner.py --gait walk --steps 20
```

### Task 5: Virtual Robot Simulation

Before connecting to real hardware, test with the virtual simulator:

```bash
# Interactive control (press keys to change gaits)
python scripts/sim_control.py

# Run automatic animation
python scripts/sim_control.py --animation 5

# Custom simulation parameters
python scripts/sim_control.py --dt 0.01 --port 921600
```

**Virtual robot commands:**
- `g` - Walk gait
- `r` - Run gait
- `t` - Trot gait
- `c` - Crawl gait
- `s` - Static pose
- `S` - Stretch pose
- `q` - Quit

### Task 6: Generate Motion Patterns

Create and export gait patterns for real robot execution:

```bash
# Generate walking gait and export to JSON
python scripts/gait_generator.py --gait walk --amplitude 30 --frequency 1.0

# Export to CSV format
python scripts/motion_export.py --format csv

# Generate and save motion sequence
python scripts/motion_export.py --sequence demo --output motions/
```

**Available gaits:**
- `walk` - Sine wave walking
- `run` - Fast running with flight phase
- `trot` - Diagonal pair coordination
- `crawl` - Smooth slow locomotion
- `gallop` - Fast efficient running
- `pace` - Lateral pair coordination

## Troubleshooting

**Motor not responding:**
- Check cable connections and power supply
- Verify baud rate matches robot configuration
- Ensure motors are enabled (not in error state)

**Unstable gait:**
- Check sensor calibration
- Tune PID gains (start with conservative values)
- Verify IMU and encoder synchronization

**Connection drops:**
- Check for USB/electrical interference
- Try different USB cable or port
- Reduce baud rate if communication errors occur

---

For platform-specific details (Unitree, ANYmal, custom), consult the appropriate reference documentation or hardware datasheet.
