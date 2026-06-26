#!/usr/bin/env python3
"""
Gait generation for quadruped robots.

Provides various walking patterns and locomotion strategies.
"""

import math
from typing import List, Tuple, Optional
from enum import Enum


class GaitType(Enum):
    """Supported gait types."""
    WALK = "walk"
    RUN = "run"
    TROT = "trot"
    CRAWL = "crawl"
    GALLOP = "gallop"
    PACE = "pace"


class QuadrupedGaitGenerator:
    """Generates gait patterns for quadruped locomotion."""

    def __init__(self, num_legs: int = 4, num_joints_per_leg: int = 3):
        """
        Initialize gait generator.

        Args:
            num_legs: Number of legs (default: 4)
            num_joints_per_leg: Joints per leg (default: 3)
        """
        self.num_legs = num_legs
        self.num_joints_per_leg = num_joints_per_leg
        self.total_joints = num_legs * num_joints_per_leg

    def sine_wave_gait(
        self,
        phase_shift: float = 0.0,
        amplitude: float = 30.0,
        frequency: float = 1.0,
        joints_per_leg: Optional[List[float]] = None
    ) -> List[float]:
        """
        Generate sine wave gait (typical walking).

        Args:
            phase_shift: Phase offset in radians
            amplitude: Movement amplitude in degrees
            frequency: Gait frequency in Hz
            joints_per_leg: Relative joint amplitudes (default: 1.0 for all)

        Returns:
            List of joint positions for all joints
        """
        if joints_per_leg is None:
            joints_per_leg = [1.0] * self.num_joints_per_leg

        positions = []
        for leg in range(self.num_legs):
            for joint_idx in range(self.num_joints_per_leg):
                # Different joints have different phase relationships
                phase = phase_shift + (joint_idx * 0.5)
                pos = amplitude * math.sin(2 * math.pi * frequency * phase)
                positions.append(pos)

        return positions

    def trot_gait(
        self,
        amplitude: float = 25.0,
        frequency: float = 1.2,
        diagonal_sync: bool = True
    ) -> List[float]:
        """
        Generate trot gait (diagonal leg pairs move together).

        Args:
            amplitude: Movement amplitude in degrees
            frequency: Gait frequency in Hz
            diagonal_sync: Whether to synchronize diagonal pairs

        Returns:
            List of joint positions for all joints
        """
        positions = []
        num_steps = 20

        for step in range(num_steps):
            phase = (step / num_steps) * 2 * math.pi

            for leg in range(self.num_legs):
                # Diagonal pairs: (0,3), (1,2), (4,7), (5,6)
                if diagonal_sync:
                    diagonal_idx = leg if leg < 2 else leg - 2
                    leg_phase = phase if diagonal_idx % 2 == 0 else phase + math.pi
                else:
                    leg_phase = phase + leg * 0.5

                # Create diagonal motion
                base_pos = amplitude * math.sin(leg_phase)

                for joint_idx in range(self.num_joints_per_leg):
                    joint_phase = leg_phase + (joint_idx * 0.3)
                    pos = amplitude * math.sin(joint_phase)
                    positions.append(pos)

        return positions

    def run_gait(
        self,
        amplitude: float = 45.0,
        frequency: float = 2.0,
        flight_phase: float = 0.2
    ) -> List[float]:
        """
        Generate run gait (front and back legs alternate).

        Args:
            amplitude: Movement amplitude in degrees
            frequency: Gait frequency in Hz
            flight_phase: Flight phase proportion (0-1)

        Returns:
            List of joint positions for all joints
        """
        positions = []
        num_steps = 30

        for step in range(num_steps):
            phase = (step / num_steps) * 2 * math.pi

            for leg in range(self.num_legs):
                # Front legs and back legs alternate
                if leg < 2:  # Front legs
                    leg_phase = phase
                else:  # Back legs
                    leg_phase = phase + math.pi

                # Higher frequency for run gait
                run_phase = leg_phase * 2

                for joint_idx in range(self.num_joints_per_leg):
                    joint_phase = run_phase + (joint_idx * 0.2)
                    pos = amplitude * math.sin(joint_phase)
                    positions.append(pos)

        return positions

    def crawl_gait(
        self,
        amplitude: float = 20.0,
        frequency: float = 0.8,
        offset_steps: int = 2
    ) -> List[float]:
        """
        Generate crawl gait (smooth, slow locomotion).

        Args:
            amplitude: Movement amplitude in degrees
            frequency: Gait frequency in Hz
            offset_steps: Number of step offsets

        Returns:
            List of joint positions for all joints
        """
        positions = []
        num_steps = 40

        for step in range(num_steps):
            phase = (step / num_steps) * 2 * math.pi

            for leg in range(self.num_legs):
                # Sequential stepping pattern
                leg_phase = phase + (leg * (2 * math.pi / self.num_legs) / offset_steps)

                for joint_idx in range(self.num_joints_per_leg):
                    joint_phase = leg_phase + (joint_idx * 0.1)
                    pos = amplitude * math.sin(joint_phase)
                    positions.append(pos)

        return positions

    def gallop_gait(
        self,
        amplitude: float = 40.0,
        frequency: float = 2.5,
        extra_step: bool = False
    ) -> List[float]:
        """
        Generate gallop gait (fast, efficient running).

        Args:
            amplitude: Movement amplitude in degrees
            frequency: Gait frequency in Hz
            extra_step: Use 5-step pattern

        Returns:
            List of joint positions for all joints
        """
        positions = []
        num_steps = 40

        for step in range(num_steps):
            phase = (step / num_steps) * 2 * math.pi

            for leg in range(self.num_legs):
                # 4-1 pattern (4 legs together, 1 leg off)
                if extra_step:
                    if leg < 4:
                        leg_phase = phase
                    else:
                        leg_phase = phase + math.pi
                else:
                    # Standard gallop
                    leg_phase = phase + (leg * 0.25)

                gallop_phase = leg_phase * 2

                for joint_idx in range(self.num_joints_per_leg):
                    joint_phase = gallop_phase + (joint_idx * 0.15)
                    pos = amplitude * math.sin(joint_phase)
                    positions.append(pos)

        return positions

    def pace_gait(
        self,
        amplitude: float = 28.0,
        frequency: float = 1.0,
        lateral_sync: bool = True
    ) -> List[float]:
        """
        Generate pace gait (lateral leg pairs move together).

        Args:
            amplitude: Movement amplitude in degrees
            frequency: Gait frequency in Hz
            lateral_sync: Whether to synchronize lateral pairs

        Returns:
            List of joint positions for all joints
        """
        positions = []
        num_steps = 25

        for step in range(num_steps):
            phase = (step / num_steps) * 2 * math.pi

            for leg in range(self.num_legs):
                # Left-right pairs
                if lateral_sync:
                    if leg < 2:  # Left side
                        leg_phase = phase
                    else:  # Right side
                        leg_phase = phase + math.pi
                else:
                    leg_phase = phase + leg * 0.3

                for joint_idx in range(self.num_joints_per_leg):
                    joint_phase = leg_phase + (joint_idx * 0.25)
                    pos = amplitude * math.sin(joint_phase)
                    positions.append(pos)

        return positions

    def static_pose(self) -> List[float]:
        """
        Generate static standing pose.

        Returns:
            List of zero positions for all joints
        """
        return [0.0] * self.total_joints

    def create_gait_profile(
        self,
        gait_type: GaitType,
        duration: float = 5.0,
        **kwargs
    ) -> Tuple[List[float], float]:
        """
        Create complete gait profile.

        Args:
            gait_type: Type of gait
            duration: Duration in seconds
            **kwargs: Additional gait parameters

        Returns:
            Tuple of (positions list, frequency in Hz)
        """
        if gait_type == GaitType.WALK:
            positions = self.sine_wave_gait(**kwargs)
            frequency = kwargs.get('frequency', 1.0)
        elif gait_type == GaitType.RUN:
            positions = self.run_gait(**kwargs)
            frequency = kwargs.get('frequency', 2.0)
        elif gait_type == GaitType.TROT:
            positions = self.trot_gait(**kwargs)
            frequency = kwargs.get('frequency', 1.2)
        elif gait_type == GaitType.CRAWL:
            positions = self.crawl_gait(**kwargs)
            frequency = kwargs.get('frequency', 0.8)
        elif gait_type == GaitType.GALLOP:
            positions = self.gallop_gait(**kwargs)
            frequency = kwargs.get('frequency', 2.5)
        elif gait_type == GaitType.PACE:
            positions = self.pace_gait(**kwargs)
            frequency = kwargs.get('frequency', 1.0)
        else:
            positions = self.static_pose()
            frequency = 0.0

        return positions, frequency

    def plot_gait(self, positions: List[float], show: bool = True):
        """
        Plot gait pattern.

        Args:
            positions: List of joint positions
            show: Whether to display plot
        """
        try:
            import matplotlib.pyplot as plt

            # Organize by leg
            leg_positions = []
            for leg in range(self.num_legs):
                leg_positions.append(positions[leg * self.num_joints_per_leg:(
                    (leg + 1) * self.num_joints_per_leg
                )])

            fig, axes = plt.subplots(self.num_legs, 1, figsize=(12, 8))
            if self.num_legs == 1:
                axes = [axes]

            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

            for i, (ax, leg_data) in enumerate(zip(axes, leg_positions)):
                ax.plot(leg_data, color=colors[i], linewidth=2)
                ax.set_title(f'Leg {i+1} ({["FL", "FR", "BL", "BR"][i]})')
                ax.set_ylabel('Position (°)')
                ax.grid(True)

            axes[-1].set_xlabel('Joint Index')
            plt.tight_layout()

            if show:
                plt.show()
            else:
                plt.close()

        except ImportError:
            print("Matplotlib not available. Install with: pip install matplotlib")


if __name__ == "__main__":
    # Test gait generation
    generator = QuadrupedGaitGenerator()

    print("=== 四足机器人步态生成器测试 ===\n")

    gaits = [
        ("静态站立", GaitType, generator.static_pose(), 0.0),
        ("行走步态", GaitType.WALK, generator.sine_wave_gait(amplitude=30, frequency=1.0), 1.0),
        ("奔跑步态", GaitType.RUN, generator.run_gait(amplitude=45, frequency=2.0), 2.0),
        ("小跑步态", GaitType.TROT, generator.trot_gait(amplitude=25, frequency=1.2), 1.2),
        ("爬行步态", GaitType.CRAWL, generator.crawl_gait(amplitude=20, frequency=0.8), 0.8),
        ("快跑步态", GaitType.GALLOP, generator.gallop_gait(amplitude=40, frequency=2.5), 2.5),
    ]

    for name, gait_type, positions, freq in gaits:
        print(f"\n{name}:")
        print(f"  频率: {freq} Hz")
        print(f"  前左腿 (FL):", positions[0:3])
        print(f"  前右腿 (FR):", positions[3:6])
        print(f"  后左腿 (BL):", positions[6:9])
        print(f"  后右腿 (BR):", positions[9:12])

        # Test plotting
        if name in ["行走步态", "奔跑步态"]:
            generator.plot_gait(positions, show=False)

    print("\n=== 测试完成 ===")
