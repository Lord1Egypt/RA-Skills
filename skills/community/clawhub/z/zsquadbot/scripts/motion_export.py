#!/usr/bin/env python3
"""
Motion trajectory export for quadruped robots.

Export gait patterns to various formats for real robot execution.
"""

import json
import csv
import numpy as np
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path
from gait_generator import QuadrupedGaitGenerator, GaitType


class MotionExporter:
    """Export motion trajectories to various formats."""

    def __init__(self, gait_generator: QuadrupedGaitGenerator = None):
        """
        Initialize exporter.

        Args:
            gait_generator: Gait generator instance
        """
        self.generator = gait_generator or QuadrupedGaitGenerator()

    def export_to_dict(
        self,
        positions: List[float],
        gait_type: str,
        frequency: float,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Export positions to dictionary format.

        Args:
            positions: List of joint positions
            gait_type: Type of gait
            frequency: Gait frequency in Hz
            metadata: Additional metadata

        Returns:
            Dictionary with motion data
        """
        if metadata is None:
            metadata = {}

        data = {
            'timestamp': datetime.now().isoformat(),
            'gait_type': gait_type,
            'frequency': frequency,
            'num_joints': len(positions),
            'num_legs': 4,
            'joints_per_leg': 3,
            'positions': positions,
            'metadata': metadata
        }

        return data

    def export_to_json(
        self,
        positions: List[float],
        gait_type: str,
        frequency: float,
        output_path: str = None,
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        Export positions to JSON file.

        Args:
            positions: List of joint positions
            gait_type: Type of gait
            frequency: Gait frequency in Hz
            output_path: Output file path (default: timestamped)
            metadata: Additional metadata

        Returns:
            Output file path
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"motion_{timestamp}_{gait_type}.json"

        data = self.export_to_dict(positions, gait_type, frequency, metadata)

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

        return output_path

    def export_to_csv(
        self,
        positions: List[float],
        gait_type: str,
        frequency: float,
        output_path: str = None,
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        Export positions to CSV file.

        Args:
            positions: List of joint positions
            gait_type: Type of gait
            frequency: Gait frequency in Hz
            output_path: Output file path (default: timestamped)
            metadata: Additional metadata

        Returns:
            Output file path
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"motion_{timestamp}_{gait_type}.csv"

        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)

            # Write header
            writer.writerow(['time', 'leg', 'joint', 'position_deg'])

            # Write data
            for step, pos in enumerate(positions):
                leg = step // 3
                joint = step % 3
                writer.writerow([step, leg, joint, pos])

        return output_path

    def export_to_robot_format(
        self,
        positions: List[float],
        gait_type: str,
        frequency: float,
        output_path: str = None,
        format: str = 'json'
    ) -> str:
        """
        Export to robot-specific format.

        Args:
            positions: List of joint positions
            gait_type: Type of gait
            frequency: Gait frequency in Hz
            output_path: Output file path (default: timestamped)
            format: Output format ('json', 'csv', 'robot')

        Returns:
            Output file path
        """
        if format == 'json':
            return self.export_to_json(positions, gait_type, frequency, output_path)
        elif format == 'csv':
            return self.export_to_csv(positions, gait_type, frequency, output_path)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def create_motion_sequence(
        self,
        sequence: List[Dict[str, Any]]
    ) -> List[List[float]]:
        """
        Create a sequence of motion segments.

        Args:
            sequence: List of segments, each with gait_type, duration, etc.

        Returns:
            Combined positions list
        """
        all_positions = []
        total_duration = 0.0

        for segment in sequence:
            gait_type = segment.get('gait_type', GaitType.WALK.value)
            duration = segment.get('duration', 2.0)

            # Generate gait
            positions, freq = self.generator.create_gait_profile(
                GaitType(gait_type),
                duration=duration,
                **segment.get('params', {})
            )

            all_positions.extend(positions)
            total_duration += duration

        return all_positions

    def generate_demo_sequence(
        self,
        duration: float = 5.0
    ) -> List[List[float]]:
        """
        Generate a demo motion sequence.

        Args:
            duration: Total duration in seconds

        Returns:
            List of motion segments
        """
        segments = []

        # Standing
        positions, _ = self.generator.create_gait_profile(
            GaitType, duration=1.0, amplitude=0
        )
        segments.append({
            'gait_type': GaitType.STATIC.value,
            'duration': 1.0,
            'positions': positions
        })

        # Walking
        positions, freq = self.generator.create_gait_profile(
            GaitType.WALK, duration=1.5, amplitude=30, frequency=1.0
        )
        segments.append({
            'gait_type': GaitType.WALK.value,
            'duration': 1.5,
            'frequency': freq,
            'amplitude': 30
        })

        # Running
        positions, freq = self.generator.create_gait_profile(
            GaitType.RUN, duration=1.5, amplitude=45, frequency=2.0
        )
        segments.append({
            'gait_type': GaitType.RUN.value,
            'duration': 1.5,
            'frequency': freq,
            'amplitude': 45
        })

        # Return to standing
        positions, _ = self.generator.create_gait_profile(
            GaitType, duration=0.5, amplitude=0
        )
        segments.append({
            'gait_type': GaitType.STATIC.value,
            'duration': 0.5,
            'positions': positions
        })

        return segments

    def simulate_trajectory(
        self,
        positions: List[float],
        frequency: float,
        dt: float = 0.01
    ) -> List[Dict[str, Any]]:
        """
        Simulate trajectory with timing information.

        Args:
            positions: List of joint positions
            frequency: Gait frequency in Hz
            dt: Time step in seconds

        Returns:
            List of frame data with timestamps
        """
        frames = []
        total_time = len(positions) / frequency

        for i, pos in enumerate(positions):
            frame = {
                'time': i * dt,
                'step': i,
                'positions': pos,
                'frequency': frequency
            }
            frames.append(frame)

        return frames

    def generate_velocities(
        self,
        positions: List[float],
        dt: float = 0.01
    ) -> List[float]:
        """
        Calculate velocities from position data.

        Args:
            positions: List of joint positions
            dt: Time step in seconds

        Returns:
            List of velocities in deg/s
        """
        velocities = []
        for i in range(1, len(positions)):
            vel = (positions[i] - positions[i-1]) / dt
            velocities.append(vel)
        return velocities


if __name__ == "__main__":
    # Test motion exporter
    generator = QuadrupedGaitGenerator()
    exporter = MotionExporter(generator)

    print("=== 运动轨迹导出器测试 ===\n")

    # Test gait generation
    gait_type = GaitType.WALK
    positions, frequency = generator.create_gait_profile(
        gait_type, duration=5.0, amplitude=30, frequency=1.0
    )

    print(f"步态类型: {gait_type.value}")
    print(f"频率: {frequency} Hz")
    print(f"总帧数: {len(positions)}")
    print(f"步态时长: {len(positions)/frequency:.2f} s")
    print(f"\n前5帧:")
    for i in range(5):
        print(f"  Step {i}: {positions[i]:.2f}°")

    # Test export to JSON
    json_path = exporter.export_to_json(
        positions, gait_type.value, frequency,
        metadata={'source': 'demo', 'author': 'quadruped-skill'}
    )
    print(f"\n✅ 已导出到: {json_path}")

    # Test export to CSV
    csv_path = exporter.export_to_csv(
        positions, gait_type.value, frequency
    )
    print(f"✅ 已导出到: {csv_path}")

    # Test motion sequence
    print("\n=== 测试运动序列 ===")
    sequence = exporter.generate_demo_sequence(duration=6.0)
    for seg in sequence:
        print(f"  {seg['gait_type']}: {seg['duration']}s")

    # Test trajectory simulation
    print("\n=== 测试轨迹模拟 ===")
    frames = exporter.simulate_trajectory(positions, frequency)
    print(f"  总帧数: {len(frames)}")
    print(f"  总时长: {frames[-1]['time']:.2f}s")
    print(f"  首帧时间: {frames[0]['time']:.3f}s")
    print(f"  末帧时间: {frames[-1]['time']:.3f}s")

    print("\n=== 测试完成 ===")
