#!/usr/bin/env python3
"""
Light Sensor Module
"""

import serial
import time
import re


class Sensor:
    """USB Light Sensor Class"""

    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, timeout=1, filter_size=5):
        """
        Initialize Light Sensor

        Args:
            port: Serial port, default '/dev/ttyUSB0'
            baudrate: Baud rate, default 9600
            timeout: Timeout in seconds, default 1
            filter_size: Moving average filter window size, default 5
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.filter_size = filter_size
        self.serial = None
        self.latest_lux = None
        self.lux_history = []

    def connect(self):
        """
        Connect to Sensor

        Returns:
            bool: True if connection successful
        """
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            print(f"Connected to light sensor: {self.port}")
            # Warm up sensor
            self._warmup()
            return True
        except serial.SerialException as e:
            print(f"Failed to connect to sensor: {e}")
            return False

    def _warmup(self):
        """Warm up sensor"""
        print("  Warming up sensor...")
        time.sleep(1)
        count = 0
        while count < 20:
            if self.serial.in_waiting > 0:
                self.serial.readline()
                count += 1
            time.sleep(0.05)

    def disconnect(self):
        """Disconnect from Sensor"""
        if self.serial and self.serial.is_open:
            self.serial.close()

    def read_lux(self):
        """
        Read Light Intensity (lux) - with moving average filter

        Returns:
            float: Light intensity value, None if read failed
        """
        if not self.serial or not self.serial.is_open:
            return self.latest_lux

        try:
            if self.serial.in_waiting > 0:
                line = self.serial.readline().decode('utf-8', errors='ignore').strip()
                match = re.search(r'brightness:\s*([\d.]+)\s*Lux', line, re.IGNORECASE)
                if match:
                    lux = float(match.group(1))
                    # Add to history
                    self.lux_history.append(lux)
                    if len(self.lux_history) > self.filter_size:
                        self.lux_history.pop(0)
                    # Return moving average
                    self.latest_lux = sum(self.lux_history) / len(self.lux_history)
                    return self.latest_lux
            return self.latest_lux

        except Exception as e:
            print(f"Failed to read sensor data: {e}")
            return None

    def read_raw(self):
        """
        Read Raw Light Intensity (no filter)

        Returns:
            float: Raw light intensity value, None if read failed
        """
        if not self.serial or not self.serial.is_open:
            return None

        try:
            if self.serial.in_waiting > 0:
                line = self.serial.readline().decode('utf-8', errors='ignore').strip()
                match = re.search(r'brightness:\s*([\d.]+)\s*Lux', line, re.IGNORECASE)
                if match:
                    return float(match.group(1))
            return None

        except Exception as e:
            print(f"Failed to read sensor data: {e}")
            return None

    def get_lux(self):
        """
        Get Latest Light Intensity Value

        Returns:
            float: Light intensity value
        """
        return self.latest_lux

    def is_dark(self, threshold=100):
        """
        Check if Environment is Dark

        Args:
            threshold: Threshold below which is considered dark, default 100 lux

        Returns:
            bool: True if dark
        """
        if self.latest_lux is None:
            return False
        return self.latest_lux < threshold

    def is_bright(self, threshold=500):
        """
        Check if Environment is Bright

        Args:
            threshold: Threshold above which is considered bright, default 500 lux

        Returns:
            bool: True if bright
        """
        if self.latest_lux is None:
            return False
        return self.latest_lux > threshold


if __name__ == "__main__":
    # Test example
    sensor = Sensor()

    if sensor.connect():
        print("Sensor initialized")

        print("\nReading 10 light intensity values:")
        for i in range(10):
            lux = sensor.read_lux()
            if lux:
                print(f"  {lux:.2f} lux")
            time.sleep(0.5)

        print(f"\nCurrent light intensity: {sensor.get_lux():.2f} lux")
        print(f"Is dark (<100 lux): {sensor.is_dark()}")
        print(f"Is bright (>500 lux): {sensor.is_bright()}")

        sensor.disconnect()
        print("\nSensor disconnected")
