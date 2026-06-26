#!/usr/bin/env python3
"""
Virtual quadruped robot state simulation.

This module simulates a quadruped robot with joint positions, IMU data, and motion.
"""

import time
import math
from typing import Dict, List, Tuple
from dataclasses import dataclass, field
import random


@dataclass
class JointState:
    """Joint position and velocity state."""
    id: int
    position: float  # degrees
    velocity: float  # deg/s
    temperature: float = 25.0  # Celsius
    voltage: float = 12.0  # Volts
    error_code: int = 0


@dataclass
class IMUState:
    """IMU sensor state."""
    accel_x: float = 0.0  # m/s²
    accel_y: float = 0.0
    accel_z: float = 9.81
    gyro_x: float = 0.0   # rad/s
    gyro_y: float = 0.0
    gyro_z: float = 0.0
    quat_x: float = 0.0
    quat_y: float = 0.0
    quat_z: float = 0.0
    quat_w: float = 1.0
    temperature: float = 25.0
    timestamp: float = 0.0


@dataclass
class RobotState:
    """Complete robot state."""
    joints: Dict[int, JointState] = field(default_factory=dict)
    imu: IMUState = field(default_factory=IMUState)
    x: float = 0.0  # Global X position (m)
    y: float = 0.0  # Global Y position (m)
    yaw: float = 0.0  # Global yaw angle (radians)
    linear_velocity: float = 0.0  # m/s
    angular_velocity: float = 0.0  # rad/s
    battery_level: float = 100.0  # percentage
    is_moving: bool = False
    timestamp: float = 0.0


class QuadrupedSimulator:
    """Virtual quadruped robot simulator."""

    # Leg configuration (4 legs, 3 joints each = 12 motors)
    # Front-left: motors 1-3, Front-right: motors 4-6, Back-left: motors 7-9, Back-right: motors 10-12

    def __init__(self, dt: float = 0.01):
        """Initialize simulator with default state.

        Args:
            dt: Time step for simulation
        """
        self.dt = dt
        self.state = RobotState()

        # Initialize joints with home position
        for motor_id in range(1, 13):
            self.state.joints[motor_id] = JointState(
                id=motor_id,
                position=0.0,  # Home position
                velocity=0.0
            )

        self.time = 0.0

    def set_joint_position(self, motor_id: int, position: float, velocity: float = 0.0):
        """
        Set target joint position (instant for simulation).

        Args:
            motor_id: Motor ID (1-12)
            position: Target position in degrees
            velocity: Target velocity in deg/s
        """
        if motor_id not in self.state.joints:
            raise ValueError(f"Invalid motor ID: {motor_id}")

        joint = self.state.joints[motor_id]
        joint.position = position
        joint.velocity = velocity

    def set_all_joints(self, positions: List[float]):
        """
        Set positions for all 12 joints.

        Args:
            positions: List of 12 positions in degrees (FL1-FL3, FR1-FR3, BL1-BL3, BR1-BR3)
        """
        if len(positions) != 12:
            raise ValueError(f"Expected 12 positions, got {len(positions)}")

        for i in range(12):
            self.set_joint_position(i + 1, positions[i])

    def update(self, dt: float):
        """
        Update simulation by time step dt.

        Args:
            dt: Time step in seconds
        """
        self.time += dt

        # Update joint velocities based on position changes
        for joint in self.state.joints.values():
            joint.velocity = (joint.position - joint.velocity) * 0.1  # Simple velocity smoothing

        # Update IMU with simulated motion
        self._update_imu()

        # Update global position (simplified)
        self._update_position()

        # Update temperature
        self._update_temperature()

        self.state.timestamp = self.time

    def _update_imu(self):
        """Simulate IMU readings based on joint motion."""
        # Calculate approximate body acceleration based on joint movement
        accel_magnitude = sum(abs(j.position) for j in self.state.joints.values()) / 12.0
        accel_magnitude = min(accel_magnitude, 5.0)  # Cap at 5 m/s²

        # Add random noise
        noise = 0.1
        accel_x = (math.sin(self.time) * 0.1 + random.uniform(-noise, noise)) * accel_magnitude
        accel_y = (math.cos(self.time) * 0.1 + random.uniform(-noise, noise)) * accel_magnitude
        accel_z = 9.81 + random.uniform(-noise, noise) * accel_magnitude

        # Calculate angular velocity from joint movements
        gyro_sum = sum(abs(j.velocity) for j in self.state.joints.values()) / 12.0
        gyro_x = (random.uniform(-noise, noise) + math.sin(self.time * 0.5) * gyro_sum * 0.1) / 10.0
        gyro_y = (random.uniform(-noise, noise) + math.cos(self.time * 0.5) * gyro_sum * 0.1) / 10.0
        gyro_z = random.uniform(-noise, noise)

        # Update quaternion based on rotation
        yaw_rate = gyro_z * self.dt
        yaw = self.state.yaw + yaw_rate

        # Small incremental rotation
        dq = yaw_rate * self.dt / 2.0
        qx = self.state.imu.quat_x + (self.state.imu.quat_w * gyro_x - self.state.imu.quat_y * gyro_z + self.state.imu.quat_z * gyro_y) * dq
        qy = self.state.imu.quat_y + (self.state.imu.quat_w * gyro_y - self.state.imu.quat_z * gyro_x + self.state.imu.quat_x * gyro_z) * dq
        qz = self.state.imu.quat_z + (self.state.imu.quat_w * gyro_z - self.state.imu.quat_x * gyro_y + self.state.imu.quat_y * gyro_x) * dq
        qw = self.state.imu.quat_w - (self.state.imu.quat_x * gyro_x + self.state.imu.quat_y * gyro_y + self.state.imu.quat_z * gyro_z) * dq

        # Normalize quaternion
        norm = math.sqrt(qx*qx + qy*qy + qz*qz + qw*qw)
        if norm > 0:
            qx /= norm
            qy /= norm
            qz /= norm
            qw /= norm

        self.state.imu.accel_x = accel_x
        self.state.imu.accel_y = accel_y
        self.state.imu.accel_z = accel_z
        self.state.imu.gyro_x = gyro_x
        self.state.imu.gyro_y = gyro_y
        self.state.imu.gyro_z = gyro_z
        self.state.imu.quat_x = qx
        self.state.imu.quat_y = qy
        self.state.imu.quat_z = qz
        self.state.imu.quat_w = qw
        self.state.imu.temperature = 25.0 + accel_magnitude * 0.5

    def _update_position(self):
        """Update global position based on motion."""
        # Simple model: x = ∫ v dt, y = ∫ v dt
        # In reality, this depends on foot placement and gait
        base_velocity = sum(abs(j.velocity) for j in self.state.joints.values()) / 12.0 * 0.01
        self.state.x += base_velocity * math.cos(self.state.yaw)
        self.state.y += base_velocity * math.sin(self.state.yaw)

    def _update_temperature(self):
        """Update motor temperatures."""
        active_joints = sum(1 for j in self.state.joints.values() if abs(j.position) > 1.0)
        temp_increase = active_joints * 0.01

        for joint in self.state.joints.values():
            target_temp = 25.0 + temp_increase
            joint.temperature += (target_temp - joint.temperature) * 0.05

    def get_state_dict(self) -> Dict:
        """Get current state as dictionary."""
        return {
            'joints': {k: {
                'position': v.position,
                'velocity': v.velocity,
                'temperature': v.temperature
            } for k, v in self.state.joints.items()},
            'imu': {
                'accel': [self.state.imu.accel_x, self.state.imu.accel_y, self.state.imu.accel_z],
                'gyro': [self.state.imu.gyro_x, self.state.imu.gyro_y, self.state.imu.gyro_z],
                'quaternion': [self.state.imu.quat_x, self.state.imu.quat_y, self.state.imu.quat_z, self.state.imu.quat_w],
                'temperature': self.state.imu.temperature
            },
            'global': {
                'x': self.state.x,
                'y': self.state.y,
                'yaw': self.state.yaw
            },
            'battery': self.state.battery_level,
            'moving': self.state.is_moving
        }

    def get_joint_state(self, motor_id: int) -> JointState:
        """Get state of specific joint."""
        return self.state.joints.get(motor_id)

    def get_imu_state(self) -> IMUState:
        """Get current IMU state."""
        return self.state.imu


def create_default_gait(motor_id: int, phase: float, amplitude: float = 30.0, frequency: float = 1.0) -> float:
    """
    Generate sinusoidal joint position for gait.

    Args:
        motor_id: Motor ID
        phase: Phase offset (0-1)
        amplitude: Movement amplitude in degrees
        frequency: Gait frequency in Hz

    Returns:
        Position in degrees
    """
    return amplitude * math.sin(2 * math.pi * frequency * phase + motor_id * 0.5)


if __name__ == "__main__":
    # Test simulator
    sim = QuadrupedSimulator()

    # Set initial gait (simple walking)
    print("Setting up simple walking gait...")
    for motor_id in range(1, 13):
        sim.set_joint_position(motor_id, create_default_gait(motor_id, phase=0.0))

    # Run simulation
    print("Running simulation for 5 seconds...")
    for i in range(500):
        sim.update(dt=0.01)
        if i % 100 == 0:
            state = sim.get_state_dict()
            print(f"Step {i}: X={state['global']['x']:.3f}m, Y={state['global']['y']:.3f}m, "
                  f"Avg Temp={sum(j['temperature'] for j in state['joints'].values())/12:.1f}°C")

    print("\nFinal state:")
    state = sim.get_state_dict()
    print(f"  Position: ({state['global']['x']:.2f}, {state['global']['y']:.2f}) m")
    print(f"  IMU: {state['imu']['accel']}")
