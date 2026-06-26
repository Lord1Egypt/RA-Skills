#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
import time
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
    parser = argparse.ArgumentParser(
        description=(
            "Control a SOARM 101 arm by sending target joint values. "
            "The first 5 values are degrees. The 6th value is gripper opening in [0, 100]."
        )
    )
    parser.add_argument("--port", required=True, help="Serial port, e.g. /dev/ttyACM0.")
    parser.add_argument(
        "--angles",
        nargs=6,
        type=float,
        metavar=(
            "SHOULDER_PAN",
            "SHOULDER_LIFT",
            "ELBOW_FLEX",
            "WRIST_FLEX",
            "WRIST_ROLL",
            "GRIPPER",
        ),
        help="Six target values. First 5 joints use degrees, gripper uses 0-100.",
    )
    parser.add_argument("--id", default="openclaw_soarm", help="Robot calibration id used by lerobot.")
    parser.add_argument(
        "--sleep",
        type=float,
        default=2.0,
        help="Seconds to wait after sending the command before reading back the position.",
    )
    parser.add_argument(
        "--skip-calibration",
        action="store_true",
        help="Skip automatic calibration on connect. Use this only if calibration already exists.",
    )
    return parser.parse_args()


def prompt_for_angles() -> list[float]:
    prompts = [
        "shoulder_pan (deg)",
        "shoulder_lift (deg)",
        "elbow_flex (deg)",
        "wrist_flex (deg)",
        "wrist_roll (deg)",
        "gripper (0-100)",
    ]
    values: list[float] = []
    for prompt in prompts:
        raw = input(f"Input target for {prompt}: ").strip()
        values.append(float(raw))
    return values


def build_robot(args: argparse.Namespace) -> SO101Follower:
    config = SO101FollowerConfig(
        port=args.port,
        id=args.id,
        disable_torque_on_disconnect=True,
        use_degrees=True,
    )
    return SO101Follower(config)


def print_joint_dict(title: str, obs: dict[str, float]) -> None:
    print(title)
    for joint in JOINT_NAMES:
        key = f"{joint}.pos"
        if key in obs:
            print(f"  {joint:14s}: {obs[key]:8.3f}")


def main() -> int:
    args = parse_args()
    values = args.angles if args.angles is not None else prompt_for_angles()

    if len(values) != 6:
        raise ValueError("Exactly 6 target values are required.")
    if not 0.0 <= values[5] <= 100.0:
        raise ValueError("Gripper target must be in [0, 100].")

    action = {f"{joint}.pos": value for joint, value in zip(JOINT_NAMES, values, strict=True)}
    robot = build_robot(args)

    try:
        robot.connect(calibrate=not args.skip_calibration)

        current = robot.get_observation()
        print_joint_dict("Current joint positions:", current)

        print("\nSending action:")
        for joint, value in zip(JOINT_NAMES, values, strict=True):
            unit = "deg" if joint != "gripper" else "%"
            print(f"  {joint:14s}: {value:8.3f} {unit}")

        sent = robot.send_action(action)
        print_joint_dict("\nCommand sent:", sent)

        if args.sleep > 0:
            time.sleep(args.sleep)

        final_obs = robot.get_observation()
        print_joint_dict("\nJoint positions after motion:", final_obs)
        return 0
    finally:
        if robot.is_connected:
            robot.disconnect()


if __name__ == "__main__":
    raise SystemExit(main())
