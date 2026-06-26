#!/usr/bin/env python3
"""
Virtual quadruped robot control interface.

This script provides interactive control of the virtual robot.
"""

import time
import math
import argparse
from typing import List
from sim_state import QuadrupedSimulator, create_default_gait


class QuadrupedController:
    """Control interface for virtual quadruped."""

    def __init__(self, simulator: QuadrupedSimulator, dt: float = 0.01):
        """
        Initialize controller.

        Args:
            simulator: QuadrupedSimulator instance
            dt: Time step for simulation
        """
        self.sim = simulator
        self.dt = dt
        self.running = False
        self.step_count = 0

    def set_static_pose(self):
        """Set robot to static standing pose."""
        positions = [0] * 12
        self.sim.set_all_joints(positions)
        print("Pose: Static standing")

    def set_stretch_pose(self):
        """Set robot to stretch pose."""
        # Front legs forward, back legs back
        positions = [
            30, -30, 0,    # Front-left: knee forward
            30, -30, 0,    # Front-right: knee forward
            -30, 30, 0,    # Back-left: knee backward
            -30, 30, 0     # Back-right: knee backward
        ]
        self.sim.set_all_joints(positions)
        print("Pose: Stretch")

    def set_gait_walk(self, step_length: float = 0.1, frequency: float = 1.0):
        """
        Set walking gait.

        Args:
            step_length: Step length in meters
            frequency: Walking frequency in Hz
        """
        amplitude = 30.0  # degrees
        for motor_id in range(1, 13):
            phase = (motor_id - 1) * 0.25  # 90° phase per leg
            position = create_default_gait(motor_id, phase, amplitude, frequency)
            self.sim.set_joint_position(motor_id, position)

        print(f"Gait: Walking (step_length={step_length}m, frequency={frequency}Hz)")

    def set_gait_run(self, frequency: float = 2.0):
        """Set running gait."""
        amplitude = 45.0
        for motor_id in range(1, 13):
            phase = (motor_id - 1) * 0.25
            position = create_default_gait(motor_id, phase, amplitude, frequency)
            self.sim.set_joint_position(motor_id, position)

        print(f"Gait: Running (frequency={frequency}Hz)")

    def set_gait_trot(self, frequency: float = 1.2):
        """Set trot gait."""
        amplitude = 25.0
        for motor_id in range(1, 13):
            phase = ((motor_id - 1) // 3) * 0.5  # 180° phase between diagonal pairs
            position = create_default_gait(motor_id, phase, amplitude, frequency)
            self.sim.set_joint_position(motor_id, position)

        print(f"Gait: Trot (frequency={frequency}Hz)")

    def set_gait_crawl(self, frequency: float = 0.8):
        """Set crawl gait."""
        amplitude = 20.0
        for motor_id in range(1, 13):
            phase = ((motor_id - 1) // 3) * 0.5
            position = create_default_gait(motor_id, phase, amplitude, frequency)
            self.sim.set_joint_position(motor_id, position)

        print(f"Gait: Crawl (frequency={frequency}Hz)")

    def monitor(self, interval: float = 0.1):
        """Monitor robot state in real-time."""
        print("\n" + "="*60)
        print("太玄照业 - Virtual Quadruped Monitor")
        print("="*60)
        print("\nControls:")
        print("  g - Walk gait")
        print("  r - Run gait")
        print("  t - Trot gait")
        print("  c - Crawl gait")
        print("  s - Static pose")
        print("  S - Stretch pose")
        print("  q - Quit")
        print("\n" + "="*60 + "\n")

        self.running = True

        try:
            while self.running:
                # Update simulation
                self.sim.update(self.dt)
                self.step_count += 1

                # Print status
                state = self.sim.get_state_dict()

                print(f"\rStep: {self.step_count:5d} | "
                      f"Pos: ({state['global']['x']:+6.3f}, {state['global']['y']:+6.3f})m | "
                      f"Yaw: {math.degrees(state['global']['yaw']):6.1f}° | "
                      f"Batt: {state['battery']:5.1f}% | "
                      f"Avg Temp: {sum(j['temperature'] for j in state['joints'].values())/12:.1f}°C  ",
                      end='', flush=True)

                # Check for input
                import sys
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    cmd = sys.stdin.readline().strip().lower()
                    if cmd == 'q':
                        self.running = False
                        print("\nStopping...")
                    elif cmd == 'g':
                        self.set_gait_walk()
                    elif cmd == 'r':
                        self.set_gait_run()
                    elif cmd == 't':
                        self.set_gait_trot()
                    elif cmd == 'c':
                        self.set_gait_crawl()
                    elif cmd == 's':
                        self.set_static_pose()
                    elif cmd == 'S':
                        self.set_stretch_pose()
                    else:
                        print(f"\nUnknown command: {cmd}")

                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n\nStopping...")
            self.running = False

    def run_animation(self, duration: float = 5.0):
        """
        Run pre-programmed animation.

        Args:
            duration: Duration in seconds
        """
        print(f"\n太玄照业运行动画: {duration} 秒...")
        self.running = True

        try:
            for i in range(int(duration / self.dt)):
                # Simple animation: alternate between walking and running
                if i < int(duration / 2):
                    self.set_gait_walk(frequency=1.0)
                else:
                    self.set_gait_run(frequency=2.0)

                # Update simulation
                self.sim.update(self.dt)
                self.step_count += 1

                if i % 100 == 0:
                    state = self.sim.get_state_dict()
                    print(f"\rAnimation: Step {i}/{int(duration/self.dt)} | "
                          f"Pos: ({state['global']['x']:+.2f}, {state['global']['y']:+.2f})m",
                          end='', flush=True)

                time.sleep(self.dt)

        except KeyboardInterrupt:
            print("\n\n动画已停止。")

        print("\n\n太玄照业动画完成。")


if __name__ == "__main__":
    import select

    parser = argparse.ArgumentParser(description='Virtual quadruped control')
    parser.add_argument('--animation', type=float, help='Run animation for N seconds')
    parser.add_argument('--port', type=int, default=921600, help='Terminal control (0=disabled)')
    parser.add_argument('--dt', type=float, default=0.01, help='Simulation time step')

    args = parser.parse_args()

    # Create simulator
    sim = QuadrupedSimulator()
    controller = QuadrupedController(sim, dt=args.dt)

    # Start in static pose
    controller.set_static_pose()
    time.sleep(0.5)

    if args.animation:
        # Run animation
        controller.run_animation(duration=args.animation)
    else:
        # Interactive control
        controller.monitor()
