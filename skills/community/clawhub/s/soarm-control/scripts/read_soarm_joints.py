#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig


JOINT_NAMES = [
    "shoulder_pan",
    "shoulder_lift",
    "elbow_flex",
    "wrist_flex",
    "wrist_roll",
    "gripper",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read current joint values from a SOARM 101 arm.")
    parser.add_argument("--port", required=True, help="Serial port, e.g. /dev/ttyACM0.")
    parser.add_argument("--id", default="openclaw_soarm", help="Robot calibration id used by lerobot.")
    parser.add_argument(
        "--skip-calibration",
        action="store_true",
        help="Skip automatic calibration on connect. Use this only if calibration already exists.",
    )
    return parser.parse_args()


def build_robot(args: argparse.Namespace) -> SO101Follower:
    config = SO101FollowerConfig(
        port=args.port,
        id=args.id,
        disable_torque_on_disconnect=True,
        use_degrees=True,
    )
    return SO101Follower(config)


def main() -> int:
    args = parse_args()
    robot = build_robot(args)

    try:
        robot.connect(calibrate=not args.skip_calibration)
        obs = robot.get_observation()

        print("Current joint values:")
        for joint in JOINT_NAMES:
            key = f"{joint}.pos"
            value = obs.get(key)
            if value is None:
                continue
            unit = "deg" if joint != "gripper" else "%"
            print(f"{joint:14s}: {value:8.3f} {unit}")
        return 0
    finally:
        if robot.is_connected:
            robot.disconnect()


if __name__ == "__main__":
    raise SystemExit(main())
