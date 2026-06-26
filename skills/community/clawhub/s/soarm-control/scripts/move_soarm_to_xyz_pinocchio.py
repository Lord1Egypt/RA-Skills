#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pinocchio as pin

from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
URDF_PATH = SKILL_DIR / "references" / "so101_new_calib.urdf"
EE_FRAME = "gripper_frame_link"
ARM_JOINTS = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll"]
ALL_JOINTS = ARM_JOINTS + ["gripper"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Move the SOARM 101 end effector to target x y z using Pinocchio inverse kinematics."
    )
    parser.add_argument("x", type=float, help="Target x in meters, relative to base_link.")
    parser.add_argument("y", type=float, help="Target y in meters, relative to base_link.")
    parser.add_argument("z", type=float, help="Target z in meters, relative to base_link.")
    parser.add_argument("--port", help="Serial port, e.g. /dev/ttyACM0. Required unless --dry-run is used.")
    parser.add_argument("--id", default="openclaw_soarm", help="Robot calibration id used by lerobot.")
    parser.add_argument("--sleep", type=float, default=1.0, help="Seconds to wait after sending the command.")
    parser.add_argument("--skip-calibration", action="store_true", help="Skip calibration on connect.")
    parser.add_argument("--dry-run", action="store_true", help="Solve IK only and do not connect to the robot.")
    parser.add_argument("--max-iters", type=int, default=300, help="Maximum IK iterations.")
    parser.add_argument("--tol", type=float, default=1e-3, help="Position tolerance in meters.")
    parser.add_argument("--step-size", type=float, default=0.6, help="IK integration step size.")
    parser.add_argument("--damping", type=float, default=1e-4, help="Damping for least-squares IK.")
    return parser.parse_args()


def build_robot(args: argparse.Namespace) -> SO101Follower:
    config = SO101FollowerConfig(
        port=args.port,
        id=args.id,
        disable_torque_on_disconnect=True,
        use_degrees=True,
    )
    return SO101Follower(config)


def build_model() -> tuple[pin.Model, pin.Data, int]:
    model = pin.buildModelFromUrdf(str(URDF_PATH))
    data = model.createData()
    frame_id = model.getFrameId(EE_FRAME)
    return model, data, frame_id


def fk_position(model: pin.Model, data: pin.Data, frame_id: int, q: np.ndarray) -> np.ndarray:
    pin.forwardKinematics(model, data, q)
    pin.updateFramePlacements(model, data)
    return data.oMf[frame_id].translation.copy()


def gripper_pct_to_rad(model: pin.Model, gripper_pct: float) -> float:
    lower = model.lowerPositionLimit[5]
    upper = model.upperPositionLimit[5]
    return lower + (gripper_pct / 100.0) * (upper - lower)


def observation_to_q(model: pin.Model, observation: dict[str, float]) -> np.ndarray:
    q = np.zeros(model.nq)
    for i, joint in enumerate(ARM_JOINTS):
        q[i] = np.deg2rad(observation[f"{joint}.pos"])
    q[5] = gripper_pct_to_rad(model, observation["gripper.pos"])
    return np.clip(q, model.lowerPositionLimit, model.upperPositionLimit)


def q_to_action(q: np.ndarray, gripper_pct: float) -> dict[str, float]:
    action = {f"{joint}.pos": float(np.rad2deg(q[i])) for i, joint in enumerate(ARM_JOINTS)}
    action["gripper.pos"] = float(gripper_pct)
    return action


def solve_ik(
    model: pin.Model,
    data: pin.Data,
    frame_id: int,
    q0: np.ndarray,
    target_xyz: np.ndarray,
    max_iters: int,
    tol: float,
    step_size: float,
    damping: float,
) -> tuple[np.ndarray, float, int]:
    q = q0.copy()
    fixed_gripper = q0[5]

    for iteration in range(max_iters):
        current_xyz = fk_position(model, data, frame_id, q)
        error = target_xyz - current_xyz
        error_norm = float(np.linalg.norm(error))
        if error_norm < tol:
            return q, error_norm, iteration

        jacobian = pin.computeFrameJacobian(
            model,
            data,
            q,
            frame_id,
            pin.ReferenceFrame.LOCAL_WORLD_ALIGNED,
        )[:3, :5]

        lhs = jacobian @ jacobian.T + damping * np.eye(3)
        dq_arm = step_size * jacobian.T @ np.linalg.solve(lhs, error)

        dq = np.zeros(model.nv)
        dq[:5] = dq_arm
        q = pin.integrate(model, q, dq)
        q = np.clip(q, model.lowerPositionLimit, model.upperPositionLimit)
        q[5] = fixed_gripper

    final_error = float(np.linalg.norm(target_xyz - fk_position(model, data, frame_id, q)))
    return q, final_error, max_iters


def print_xyz(label: str, xyz: np.ndarray) -> None:
    print(f"{label}: x={xyz[0]:.4f}  y={xyz[1]:.4f}  z={xyz[2]:.4f} m")


def main() -> int:
    args = parse_args()
    if not args.dry_run and not args.port:
        raise ValueError("--port is required unless --dry-run is used.")

    target_xyz = np.array([args.x, args.y, args.z], dtype=float)
    model, data, frame_id = build_model()

    robot = None
    current_gripper_pct = 50.0
    q0 = pin.neutral(model)

    try:
        if not args.dry_run:
            robot = build_robot(args)
            robot.connect(calibrate=not args.skip_calibration)
            observation = robot.get_observation()
            q0 = observation_to_q(model, observation)
            current_gripper_pct = float(observation["gripper.pos"])

        current_xyz = fk_position(model, data, frame_id, q0)
        print_xyz("Current end-effector position", current_xyz)
        print_xyz("Target end-effector position ", target_xyz)

        q_sol, final_error, iterations = solve_ik(
            model=model,
            data=data,
            frame_id=frame_id,
            q0=q0,
            target_xyz=target_xyz,
            max_iters=args.max_iters,
            tol=args.tol,
            step_size=args.step_size,
            damping=args.damping,
        )

        solved_xyz = fk_position(model, data, frame_id, q_sol)
        print_xyz("Solved end-effector position", solved_xyz)
        print(f"IK iterations: {iterations}")
        print(f"Final position error: {final_error:.6f} m")

        if final_error >= args.tol:
            raise RuntimeError("IK did not converge within tolerance. Try a closer target or tune the IK parameters.")

        print("\nSolved arm joints:")
        for i, joint in enumerate(ARM_JOINTS):
            print(f"{joint:14s}: {np.rad2deg(q_sol[i]):8.3f} deg")

        if args.dry_run:
            return 0

        action = q_to_action(q_sol, current_gripper_pct)
        robot.send_action(action)

        if args.sleep > 0:
            time.sleep(args.sleep)

        final_observation = robot.get_observation()
        final_q = observation_to_q(model, final_observation)
        final_xyz_after_move = fk_position(model, data, frame_id, final_q)
        print_xyz("\nMeasured end-effector position", final_xyz_after_move)
        return 0
    finally:
        if robot is not None and robot.is_connected:
            robot.disconnect()


if __name__ == "__main__":
    raise SystemExit(main())
