#!/usr/bin/env python3
"""
IMU data reader for quadruped robots.

This script reads and processes IMU data from sensors.
"""

import serial
import struct
import time
import math
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class IMUData:
    """IMU data structure."""
    accel: tuple[float, float, float]  # Acceleration in m/s²
    gyro: tuple[float, float, float]   # Angular velocity in rad/s
    quaternion: tuple[float, float, float, float]  # Quaternion [x, y, z, w]
    temperature: float  # Temperature in °C
    timestamp: float  # Unix timestamp


class IMU:
    """IMU sensor interface."""

    def __init__(self, port: str = '/dev/ttyUSB1', baudrate: int = 921600):
        """
        Initialize IMU connection.

        Args:
            port: Serial port device path
            baudrate: Communication baud rate (default: 921600)
        """
        self.port = port
        self.baudrate = baudrate
        self.ser = None

    def connect(self) -> bool:
        """
        Connect to IMU sensor.

        Returns:
            True if connection successful
        """
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=0.01)
            time.sleep(0.1)
            print(f"IMU: Connected to {self.port}")
            return True
        except serial.SerialException as e:
            print(f"IMU connection error: {e}")
            return False

    def read(self) -> Optional[IMUData]:
        """
        Read IMU data packet.

        Returns:
            IMUData object with sensor readings
        """
        if not self.ser:
            raise RuntimeError("IMU not connected")

        # Request IMU data
        cmd = struct.pack('!BB', 0xFF, 0x01)
        self.ser.write(cmd)
        time.sleep(0.01)

        # Read response (43 bytes)
        if self.ser.in_waiting >= 43:
            data = self.ser.read(43)

            # Parse headers
            header1, header2, packet_type = struct.unpack('!BBB', data[:3])

            # Check for valid IMU packet
            if header1 != 0x55 or header2 != 0xAA:
                return None

            # Unpack data fields
            accel_x, accel_y, accel_z = struct.unpack('!fff', data[3:12])
            gyro_x, gyro_y, gyro_z = struct.unpack('!fff', data[12:21])
            quat_x, quat_y, quat_z, quat_w = struct.unpack('!ffff', data[21:37])
            temperature = struct.unpack('!f', data[37:41])[0]
            timestamp = struct.unpack('!I', data[41:45])[0]
            checksum = struct.unpack('!B', data[45:46])[0]

            # Validate checksum (simple XOR)
            calculated_checksum = 0
            for i in range(45):
                calculated_checksum ^= data[i]

            if checksum != calculated_checksum:
                print("Warning: IMU checksum mismatch")
                return None

            return IMUData(
                accel=(accel_x, accel_y, accel_z),
                gyro=(gyro_x, gyro_y, gyro_z),
                quaternion=(quat_x, quat_y, quat_z, quat_w),
                temperature=temperature,
                timestamp=timestamp
            )

        return None

    def read_stable(self, samples: int = 10, wait_time: float = 0.1) -> Optional[IMUData]:
        """
        Read and average multiple samples for stability.

        Args:
            samples: Number of samples to average
            wait_time: Time between samples in seconds

        Returns:
            Average IMUData
        """
        accel_sum = [0.0, 0.0, 0.0]
        gyro_sum = [0.0, 0.0, 0.0]
        quat_sum = [0.0, 0.0, 0.0, 0.0]
        temp_sum = 0.0

        for _ in range(samples):
            imu_data = self.read()
            if imu_data:
                accel_sum[0] += imu_data.accel[0]
                accel_sum[1] += imu_data.accel[1]
                accel_sum[2] += imu_data.accel[2]
                gyro_sum[0] += imu_data.gyro[0]
                gyro_sum[1] += imu_data.gyro[1]
                gyro_sum[2] += imu_data.gyro[2]
                quat_sum[0] += imu_data.quaternion[0]
                quat_sum[1] += imu_data.quaternion[1]
                quat_sum[2] += imu_data.quaternion[2]
                quat_sum[3] += imu_data.quaternion[3]
                temp_sum += imu_data.temperature
                time.sleep(wait_time)

        if samples > 0:
            return IMUData(
                accel=(
                    accel_sum[0] / samples,
                    accel_sum[1] / samples,
                    accel_sum[2] / samples
                ),
                gyro=(
                    gyro_sum[0] / samples,
                    gyro_sum[1] / samples,
                    gyro_sum[2] / samples
                ),
                quaternion=(
                    quat_sum[0] / samples,
                    quat_sum[1] / samples,
                    quat_sum[2] / samples,
                    quat_sum[3] / samples
                ),
                temperature=temp_sum / samples,
                timestamp=time.time()
            )

        return None

    def disconnect(self):
        """Disconnect from IMU."""
        if self.ser:
            self.ser.close()
            print("IMU: Disconnected")


class IMUMonitor:
    """Monitor and display IMU data in real-time."""

    def __init__(self, imu: IMU, sample_rate: float = 100.0):
        """
        Initialize IMU monitor.

        Args:
            imu: IMU instance
            sample_rate: Sample rate in Hz
        """
        self.imu = imu
        self.sample_rate = sample_rate
        self.running = False

    def start(self):
        """Start monitoring loop."""
        if not self.imu.ser:
            raise RuntimeError("IMU not connected")

        self.running = True
        print("IMU Monitor: Started (Ctrl+C to stop)")

        try:
            while self.running:
                imu_data = self.imu.read_stable(samples=5, wait_time=0.05)

                if imu_data:
                    print(f"\rAccel: [{imu_data.accel[0]:6.2f}, {imu_data.accel[1]:6.2f}, {imu_data.accel[2]:6.2f}] "
                          f"m/s²  "
                          f"Gyro: [{imu_data.gyro[0]:6.2f}, {imu_data.gyro[1]:6.2f}, {imu_data.gyro[2]:6.2f}] rad/s  "
                          f"Temp: {imu_data.temperature:.1f}°C",
                          end='', flush=True)

                time.sleep(1.0 / self.sample_rate)

        except KeyboardInterrupt:
            print("\nIMU Monitor: Stopped")
        finally:
            self.running = False

    def stop(self):
        """Stop monitoring."""
        self.running = False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='IMU data reader')
    parser.add_argument('--monitor', action='store_true', help='Real-time monitoring')
    parser.add_argument('--port', type=str, default='/dev/ttyUSB1', help='Serial port')
    parser.add_argument('--baudrate', type=int, default=921600, help='Baud rate')

    args = parser.parse_args()

    imu = IMU(port=args.port, baudrate=args.baudrate)

    if args.monitor:
        imu.connect()
        monitor = IMUMonitor(imu, sample_rate=100.0)
        monitor.start()
    else:
        imu.connect()

        # Read single sample
        print("Reading single sample...")
        imu_data = imu.read()
        if imu_data:
            print("\nIMU Data:")
            print(f"  Acceleration: {imu_data.accel} m/s²")
            print(f"  Gyro: {imu_data.gyro} rad/s")
            print(f"  Quaternion: [{imu_data.quaternion[0]:.3f}, {imu_data.quaternion[1]:.3f}, "
                  f"{imu_data.quaternion[2]:.3f}, {imu_data.quaternion[3]:.3f}]")
            print(f"  Temperature: {imu_data.temperature:.2f}°C")
            print(f"  Timestamp: {imu_data.timestamp}")
        else:
            print("Failed to read IMU data")

        imu.disconnect()
