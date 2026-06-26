#!/usr/bin/env python3
"""
Motor control utilities for quadruped robots.

This script provides functions for motor initialization, control, and status reading.
"""

import serial
import struct
import time
from typing import Optional, Dict, Any


class Motor:
    """Motor control class for individual motor operations."""

    def __init__(self, port: str = '/dev/ttyUSB0', baudrate: int = 1000000):
        """
        Initialize motor connection.

        Args:
            port: Serial port device path
            baudrate: Communication baud rate (default: 1,000,000)
        """
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.motor_id = None

    def connect(self, motor_id: int) -> bool:
        """
        Connect to motor and initialize.

        Args:
            motor_id: Motor ID for communication

        Returns:
            True if connection successful
        """
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=0.1)
            self.motor_id = motor_id
            time.sleep(0.1)  # Allow connection to stabilize
            return True
        except serial.SerialException as e:
            print(f"Connection error: {e}")
            return False

    def enable(self):
        """Enable motor output."""
        if not self.ser:
            raise RuntimeError("Motor not connected")

        cmd = struct.pack('!BBB', 0xFF, 0xAA, self.motor_id)
        cmd += struct.pack('!f', 0.0)  # Position 0
        cmd += struct.pack('!f', 0.0)  # Velocity 0
        cmd += struct.pack('!f', 0.0)  # Force 0

        self.ser.write(cmd)
        print(f"Motor {self.motor_id}: Enabled")

    def set_position(self, position: float, velocity: float = 0.0, force: float = 0.0):
        """
        Set motor target position.

        Args:
            position: Target position in degrees
            velocity: Target velocity in rad/s
            force: Force limit in N (optional)
        """
        if not self.ser:
            raise RuntimeError("Motor not connected")

        cmd = struct.pack('!BBB', 0xFF, 0xAA, self.motor_id)
        cmd += struct.pack('!f', position)
        cmd += struct.pack('!f', velocity)
        cmd += struct.pack('!f', force)

        self.ser.write(cmd)

    def get_status(self) -> Dict[str, float]:
        """
        Read motor status and telemetry.

        Returns:
            Dictionary with position, velocity, temperature, voltage, and errors
        """
        if not self.ser:
            raise RuntimeError("Motor not connected")

        # Request status
        status_cmd = struct.pack('!BB', 0xFF, self.motor_id)
        self.ser.write(status_cmd)
        time.sleep(0.05)

        # Read response (12 bytes)
        if self.ser.in_waiting >= 12:
            data = self.ser.read(12)
            unpacked = struct.unpack('!fffiiii', data)

            return {
                'position': unpacked[0],  # degrees
                'velocity': unpacked[1],  # rad/s
                'force': unpacked[2],     # N
                'temperature': unpacked[3] / 10.0,  # °C (scaled)
                'voltage': unpacked[4] / 1000.0,    # V
                'error_flags': unpacked[5:7]         # error codes
            }

        return {}

    def disconnect(self):
        """Disconnect motor."""
        if self.ser:
            self.ser.close()
            print(f"Motor {self.motor_id}: Disconnected")


class Quadruped:
    """High-level robot control for quadruped platforms."""

    def __init__(self, port: str = '/dev/ttyUSB0', baudrate: int = 1000000):
        """
        Initialize robot connection.

        Args:
            port: Serial port device path
            baudrate: Communication baud rate
        """
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.motors: Dict[int, Motor] = {}
        self.imu = None  # Would be a separate IMU class

    def connect(self):
        """Connect to all motors."""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=0.1)
            time.sleep(0.1)

            # Initialize motors (adjust IDs based on your robot)
            for motor_id in range(1, 13):
                motor = Motor(self.port, self.baudrate)
                motor.connect(motor_id)
                motor.enable()
                self.motors[motor_id] = motor

            print("Robot: Connected and motors enabled")
            return True
        except serial.SerialException as e:
            print(f"Connection error: {e}")
            return False

    def disconnect(self):
        """Disconnect from robot."""
        for motor in self.motors.values():
            motor.disconnect()
        if self.ser:
            self.ser.close()
        print("Robot: Disconnected")

    def get_motor_status(self, motor_id: int) -> Dict[str, float]:
        """Get status of specific motor."""
        if motor_id in self.motors:
            return self.motors[motor_id].get_status()
        return {}

    def emergency_stop(self):
        """Emergency stop all motors."""
        for motor in self.motors.values():
            try:
                motor.set_position(0.0, 0.0, 0.0)
                print(f"Motor {motor.motor_id}: Emergency stop")
            except Exception as e:
                print(f"Motor {motor.motor_id}: Stop error: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Motor control utilities')
    parser.add_argument('--test', action='store_true', help='Test motor movement')
    parser.add_argument('--motor', type=int, help='Motor ID for test')
    parser.add_argument('--calibrate', action='store_true', help='Calibrate motors')

    args = parser.parse_args()

    robot = Quadruped()

    if args.calibrate:
        print("Calibrating motors...")
        robot.connect()
        # Calibration code here
        robot.disconnect()

    elif args.test and args.motor:
        print(f"Testing motor {args.motor}")
        robot.connect()

        # Test position sweep
        for pos in [0, 45, 90, 45, 0]:
            robot.get_motor_status(args.motor)
            robot.motors[args.motor].set_position(pos)
            time.sleep(1.0)

        robot.disconnect()

    else:
        # Interactive mode
        print("Interactive motor control (Ctrl+C to exit)")
        robot.connect()

        try:
            while True:
                motor_id = input("Motor ID (1-12, 'q' to quit): ")
                if motor_id.lower() == 'q':
                    break

                try:
                    mid = int(motor_id)
                    if mid < 1 or mid > 12:
                        print("Motor ID must be 1-12")
                        continue

                    robot.get_motor_status(mid)

                    cmd = input(f"Command (pos/vel/force, 's' for status, 'q' to quit): ")
                    if cmd.lower() == 'q':
                        break
                    elif cmd.lower() == 's':
                        status = robot.get_motor_status(mid)
                        print(f"Position: {status.get('position', 0):.2f}°")
                        print(f"Velocity: {status.get('velocity', 0):.2f} rad/s")
                        print(f"Temperature: {status.get('temperature', 0):.1f}°C")
                    elif cmd.startswith('pos'):
                        pos = float(cmd.split()[1])
                        robot.motors[mid].set_position(pos)
                    elif cmd.startswith('vel'):
                        vel = float(cmd.split()[1])
                        robot.motors[mid].set_position(0.0, vel)
                    elif cmd.startswith('force'):
                        force = float(cmd.split()[1])
                        robot.motors[mid].set_position(0.0, 0.0, force)

                except ValueError as e:
                    print(f"Invalid input: {e}")
                except Exception as e:
                    print(f"Error: {e}")

        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            robot.disconnect()
