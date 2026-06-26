#!/usr/bin/env python3

from __future__ import annotations

import atexit
import math
import os
import threading
import time
from pathlib import Path

import cv2
import numpy as np
import pinocchio as pin
from flask import Flask, jsonify, request
from ultralytics import YOLO

from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
URDF_PATH = SKILL_DIR / "references" / "so101_new_calib.urdf"
EE_FRAME = "gripper_frame_link"
ARM_JOINTS = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll"]
JOINTS = ARM_JOINTS + ["gripper"]
DEFAULT_SPEED = 0.2
STEP_DELAY_S = 0.05

IMG_W, IMG_H = 640, 480
IMG_CX, IMG_CY = IMG_W // 2, IMG_H // 2
SERVO_TARGET_X = 422
SERVO_TARGET_Y = 217
MAX_SERVO_STEPS = 200
LOCK_MAX_JUMP = 150
KP_PAN = 0.015
KP_LIFT = 0.01
DEAD_ZONE = 4.0
MAX_STEP = 1.0
PICK_SPEED_DEG = 20
PICK_HZ = 30

OVERHEAD_JOINTS = {
    "shoulder_pan": 0.0,
    "shoulder_lift": -50.0,
    "elbow_flex": 20.0,
    "wrist_flex": 90.0,
    "wrist_roll": -97.0,
}

HOME_JOINTS = {
    "shoulder_pan": 0.0,
    "shoulder_lift": -104.0,
    "elbow_flex": 95.0,
    "wrist_flex": 65.0,
    "wrist_roll": -95.0,
}


class DetectionManager:
    def __init__(self, weights_path: Path, source: int, conf: float):
        self.weights_path = weights_path
        self.source = source
        self.conf = conf
        self.lock = threading.Lock()
        self.state = {
            "timestamp": 0.0,
            "count": 0,
            "objects": [],
        }
        self.ready = False
        self.error: str | None = None
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()

    def start(self) -> None:
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()

    def get_state(self) -> dict:
        with self.lock:
            return dict(self.state)

    def get_detection(self, last_pos: tuple[int, int] | None = None) -> tuple[int, int] | None:
        with self.lock:
            objs = list(self.state.get("objects", []))
        if not objs:
            return None
        if last_pos is None:
            best = max(objs, key=lambda o: o["confidence"])
        else:
            lx, ly = last_pos
            best = min(
                objs,
                key=lambda o: (o["center"]["x"] - lx) ** 2 + (o["center"]["y"] - ly) ** 2,
            )
            dist = math.sqrt((best["center"]["x"] - lx) ** 2 + (best["center"]["y"] - ly) ** 2)
            if dist > LOCK_MAX_JUMP:
                return None
        return best["center"]["x"], best["center"]["y"]

    def _run(self) -> None:
        try:
            model = YOLO(str(self.weights_path))
            cap = cv2.VideoCapture(self.source)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_W)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_H)
            if not cap.isOpened():
                raise RuntimeError(f"Could not open camera source {self.source}")
            self.ready = True

            while not self._stop.is_set():
                ret, frame = cap.read()
                if not ret:
                    self.error = "Failed to read frame"
                    time.sleep(1.0)
                    continue

                objects_list = []
                results = model.predict(frame, conf=self.conf, verbose=False, stream=True)
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        cx = int((x1 + x2) / 2)
                        cy = int((y1 + y2) / 2)
                        cls_id = int(box.cls[0])
                        label = model.names[cls_id]
                        confidence = float(box.conf[0])
                        objects_list.append(
                            {
                                "label": label,
                                "confidence": float(f"{confidence:.2f}"),
                                "center": {"x": cx, "y": cy},
                                "bbox": {
                                    "x1": int(x1),
                                    "y1": int(y1),
                                    "x2": int(x2),
                                    "y2": int(y2),
                                },
                            }
                        )

                with self.lock:
                    self.state = {
                        "timestamp": time.time(),
                        "count": len(objects_list),
                        "objects": objects_list,
                    }
        except Exception as exc:
            self.error = str(exc)


class PickTaskManager:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.running = False
        self.last_result: dict | None = None

    def status(self) -> dict:
        with self.lock:
            return {"running": self.running, "last_result": self.last_result}

    def start(self, worker: callable) -> bool:
        with self.lock:
            if self.running:
                return False
            self.running = True
            self.last_result = None

        def runner() -> None:
            result = worker()
            with self.lock:
                self.running = False
                self.last_result = result

        threading.Thread(target=runner, daemon=True).start()
        return True


class SoArmController:
    def __init__(self, port: str, robot_id: str, skip_calibration: bool):
        self.lock = threading.Lock()
        self.model = pin.buildModelFromUrdf(str(URDF_PATH))
        self.data = self.model.createData()
        self.frame_id = self.model.getFrameId(EE_FRAME)
        self.robot = SO101Follower(
            SO101FollowerConfig(
                port=port,
                id=robot_id,
                disable_torque_on_disconnect=True,
                use_degrees=True,
            )
        )
        self.robot.connect(calibrate=not skip_calibration)

    def close(self) -> None:
        if self.robot.is_connected:
            self.robot.disconnect()

    def _fk_position(self, q: np.ndarray) -> np.ndarray:
        pin.forwardKinematics(self.model, self.data, q)
        pin.updateFramePlacements(self.model, self.data)
        return self.data.oMf[self.frame_id].translation.copy()

    def _gripper_pct_to_rad(self, gripper_pct: float) -> float:
        lower = self.model.lowerPositionLimit[5]
        upper = self.model.upperPositionLimit[5]
        return lower + (gripper_pct / 100.0) * (upper - lower)

    def _observation_to_q(self, observation: dict[str, float]) -> np.ndarray:
        q = np.zeros(self.model.nq)
        for i, joint in enumerate(ARM_JOINTS):
            q[i] = np.deg2rad(observation[f"{joint}.pos"])
        q[5] = self._gripper_pct_to_rad(observation["gripper.pos"])
        return np.clip(q, self.model.lowerPositionLimit, self.model.upperPositionLimit)

    def _action_from_q(self, q: np.ndarray, gripper_pct: float) -> dict[str, float]:
        action = {f"{joint}.pos": float(np.rad2deg(q[i])) for i, joint in enumerate(ARM_JOINTS)}
        action["gripper.pos"] = float(gripper_pct)
        return action

    def _solve_ik(
        self,
        q0: np.ndarray,
        target_xyz: np.ndarray,
        max_iters: int,
        tol: float,
        step_size: float,
        damping: float,
    ) -> tuple[np.ndarray, float, int, np.ndarray]:
        q = q0.copy()
        fixed_gripper = q0[5]

        for iteration in range(max_iters):
            current_xyz = self._fk_position(q)
            error = target_xyz - current_xyz
            error_norm = float(np.linalg.norm(error))
            if error_norm < tol:
                return q, error_norm, iteration, current_xyz

            jacobian = pin.computeFrameJacobian(
                self.model,
                self.data,
                q,
                self.frame_id,
                pin.ReferenceFrame.LOCAL_WORLD_ALIGNED,
            )[:3, :5]

            dq_arm = step_size * jacobian.T @ np.linalg.solve(
                jacobian @ jacobian.T + damping * np.eye(3),
                error,
            )
            dq = np.zeros(self.model.nv)
            dq[:5] = dq_arm
            q = pin.integrate(self.model, q, dq)
            q = np.clip(q, self.model.lowerPositionLimit, self.model.upperPositionLimit)
            q[5] = fixed_gripper

        final_xyz = self._fk_position(q)
        final_error = float(np.linalg.norm(target_xyz - final_xyz))
        return q, final_error, max_iters, final_xyz

    def _read_state(self) -> tuple[dict[str, float], np.ndarray]:
        observation = self.robot.get_observation()
        q = self._observation_to_q(observation)
        xyz = self._fk_position(q)
        return observation, xyz

    def _send_smooth_action(
        self, start: dict[str, float], target: dict[str, float], speed: float
    ) -> tuple[dict[str, float], int]:
        if speed <= 0:
            raise ValueError("speed must be > 0.")

        arm_delta = max(abs(target[f"{joint}.pos"] - start[f"{joint}.pos"]) for joint in ARM_JOINTS)
        gripper_delta = abs(target["gripper.pos"] - start["gripper.pos"])
        arm_step_deg = 8.0 * speed
        gripper_step_pct = 10.0 * speed
        steps = max(
            1,
            int(np.ceil(arm_delta / arm_step_deg)) if arm_step_deg > 0 else 1,
            int(np.ceil(gripper_delta / gripper_step_pct)) if gripper_step_pct > 0 else 1,
        )

        sent = target
        for i in range(1, steps + 1):
            alpha = i / steps
            action = {
                f"{joint}.pos": float(
                    start[f"{joint}.pos"] + alpha * (target[f"{joint}.pos"] - start[f"{joint}.pos"])
                )
                for joint in JOINTS
            }
            sent = self.robot.send_action(action)
            if i < steps:
                time.sleep(STEP_DELAY_S)
        return sent, steps

    def _send_pick_action(self, joints: dict[str, float], gripper: float) -> None:
        action = {f"{joint}.pos": float(joints[joint]) for joint in ARM_JOINTS}
        action["gripper.pos"] = float(gripper)
        self.robot.send_action(action)

    def _move_pick_pose(
        self,
        target: dict[str, float],
        gripper: float | None = None,
        speed: float = PICK_SPEED_DEG,
    ) -> tuple[dict[str, float], float]:
        start, cur_gripper = self._read_pick_joints()
        g_target = cur_gripper if gripper is None else gripper
        max_delta = max(abs(target[joint] - start[joint]) for joint in ARM_JOINTS)
        duration = max(1.0, max_delta / speed)
        steps = max(1, int(duration * PICK_HZ))
        for i in range(1, steps + 1):
            alpha = i / steps
            joints = {
                joint: start[joint] + (target[joint] - start[joint]) * alpha
                for joint in ARM_JOINTS
            }
            g = cur_gripper + (g_target - cur_gripper) * alpha
            self._send_pick_action(joints, g)
            time.sleep(1.0 / PICK_HZ)
        time.sleep(0.3)
        return target, g_target

    def _move_pick_gripper(
        self,
        joints: dict[str, float],
        g_start: float,
        g_target: float,
        duration: float = 0.6,
    ) -> float:
        steps = max(1, int(duration * PICK_HZ))
        for i in range(1, steps + 1):
            alpha = i / steps
            g = g_start + (g_target - g_start) * alpha
            self._send_pick_action(joints, g)
            time.sleep(1.0 / PICK_HZ)
        time.sleep(0.3)
        return g_target

    def _read_pick_joints(self) -> tuple[dict[str, float], float]:
        observation = self.robot.get_observation()
        joints = {joint: float(observation[f"{joint}.pos"]) for joint in ARM_JOINTS}
        return joints, float(observation.get("gripper.pos", 0.0))

    def status(self) -> dict:
        with self.lock:
            observation, xyz = self._read_state()
            return {
                "connected": self.robot.is_connected,
                "joints": observation,
                "xyz": xyz.tolist(),
            }

    def move_joints(self, angles: list[float], sleep_s: float, speed: float) -> dict:
        if len(angles) != 6:
            raise ValueError("angles must contain 6 values.")
        if not 0.0 <= angles[5] <= 100.0:
            raise ValueError("gripper must be in [0, 100].")

        target = {f"{joint}.pos": float(value) for joint, value in zip(JOINTS, angles, strict=True)}
        with self.lock:
            before, before_xyz = self._read_state()
            sent, steps = self._send_smooth_action(before, target, speed)
            if sleep_s > 0:
                time.sleep(sleep_s)
            after, after_xyz = self._read_state()
            return {
                "before": before,
                "before_xyz": before_xyz.tolist(),
                "sent": sent,
                "speed": speed,
                "steps": steps,
                "after": after,
                "after_xyz": after_xyz.tolist(),
            }

    def move_xyz(
        self,
        x: float,
        y: float,
        z: float,
        sleep_s: float,
        speed: float,
        max_iters: int,
        tol: float,
        step_size: float,
        damping: float,
    ) -> dict:
        target_xyz = np.array([x, y, z], dtype=float)
        with self.lock:
            before, before_xyz = self._read_state()
            q0 = self._observation_to_q(before)
            gripper_pct = float(before["gripper.pos"])

            q_sol, final_error, iterations, solved_xyz = self._solve_ik(
                q0=q0,
                target_xyz=target_xyz,
                max_iters=max_iters,
                tol=tol,
                step_size=step_size,
                damping=damping,
            )
            if final_error >= tol:
                raise RuntimeError("IK did not converge within tolerance.")

            action = self._action_from_q(q_sol, gripper_pct)
            _, steps = self._send_smooth_action(before, action, speed)
            if sleep_s > 0:
                time.sleep(sleep_s)

            after, after_xyz = self._read_state()
            return {
                "target_xyz": target_xyz.tolist(),
                "before_xyz": before_xyz.tolist(),
                "solved_xyz": solved_xyz.tolist(),
                "measured_xyz": after_xyz.tolist(),
                "final_error": final_error,
                "iterations": iterations,
                "speed": speed,
                "steps": steps,
                "solved_joints_deg": {
                    joint: float(np.rad2deg(q_sol[i])) for i, joint in enumerate(ARM_JOINTS)
                },
                "before_joints": before,
                "after_joints": after,
            }

    def run_pick_task(self, detection_manager: DetectionManager) -> dict:
        with self.lock:
            try:
                self._move_pick_pose(OVERHEAD_JOINTS)

                cur_joints, gripper = self._read_pick_joints()
                t0 = time.monotonic()
                while time.monotonic() - t0 < 1.0:
                    self._send_pick_action(cur_joints, gripper)
                    time.sleep(1.0 / PICK_HZ)

                cur_joints, gripper = self._read_pick_joints()
                initial_det = detection_manager.get_detection()
                if initial_det is None:
                    wrist_adjust = -10.0
                else:
                    cx, cy = initial_det
                    dist_from_center = math.sqrt((cx - IMG_CX) ** 2 + (cy - IMG_CY) ** 2)
                    if dist_from_center > 250:
                        wrist_adjust = -28.0
                    elif dist_from_center > 200:
                        wrist_adjust = -24.0
                    elif dist_from_center > 150:
                        wrist_adjust = -20.0
                    elif dist_from_center > 100:
                        wrist_adjust = -15.0
                    elif dist_from_center > 70:
                        wrist_adjust = -12.0
                    elif dist_from_center > 40:
                        wrist_adjust = -9.0
                    else:
                        wrist_adjust = -7.0
                pre_joints = dict(cur_joints)
                pre_joints["wrist_flex"] += wrist_adjust
                self._move_pick_pose(pre_joints)

                cur_joints, gripper = self._read_pick_joints()
                step = 0
                last_pos: tuple[int, int] | None = None

                while step < MAX_SERVO_STEPS:
                    det = detection_manager.get_detection(last_pos)
                    if det is None:
                        time.sleep(1.0 / PICK_HZ)
                        continue
                    cx, cy = det
                    last_pos = (cx, cy)
                    dx = cx - SERVO_TARGET_X
                    dy = cy - SERVO_TARGET_Y
                    err = math.sqrt(dx**2 + dy**2)
                    step += 1
                    if err < DEAD_ZONE:
                        break

                    delta_pan = float(np.clip(dx * KP_PAN, -MAX_STEP, MAX_STEP))
                    delta_lift = float(np.clip(dy * KP_LIFT, -MAX_STEP, MAX_STEP))
                    cur_joints["shoulder_pan"] += delta_pan
                    cur_joints["shoulder_lift"] += delta_lift
                    self._send_pick_action(cur_joints, gripper)
                    time.sleep(1.0 / PICK_HZ)

                gripper = self._move_pick_gripper(cur_joints, gripper, 50, duration=0.5)

                pick_joints = dict(cur_joints)
                pick_joints["shoulder_lift"] = 20.0
                pick_joints["elbow_flex"] = -5.0
                self._move_pick_pose(pick_joints, gripper=gripper, speed=15)

                gripper = self._move_pick_gripper(pick_joints, 50, 1, duration=0.8)

                lift_joints = dict(pick_joints)
                lift_joints["shoulder_lift"] -= 20.0
                lift_joints["elbow_flex"] -= 35.0
                lift_joints["wrist_flex"] += 45.0
                self._move_pick_pose(lift_joints, gripper=gripper, speed=15)

                place_joints = dict(lift_joints)
                place_joints["shoulder_pan"] = 60.0
                self._move_pick_pose(place_joints, gripper=gripper, speed=PICK_SPEED_DEG)

                self._move_pick_gripper(place_joints, 5, 50, duration=0.6)
                self._move_pick_pose(HOME_JOINTS, gripper=1, speed=PICK_SPEED_DEG)

                return {"ok": True, "message": "抓取任务完成"}
            except Exception as exc:
                return {"ok": False, "error": str(exc)}


def create_app() -> Flask:
    port = os.getenv("SOARM_PORT", "/dev/ttyACM0")
    robot_id = os.getenv("SOARM_ID", "openclaw_soarm")
    skip_calibration = os.getenv("SOARM_SKIP_CALIBRATION", "1") != "0"
    controller = SoArmController(port=port, robot_id=robot_id, skip_calibration=skip_calibration)
    atexit.register(controller.close)

    weights_path = Path(os.getenv("DETECTION_WEIGHTS", str(SCRIPT_DIR / "best.pt")))
    camera_source = int(os.getenv("DETECTION_SOURCE", "0"))
    confidence = float(os.getenv("DETECTION_CONF", "0.25"))
    detection_manager = DetectionManager(weights_path=weights_path, source=camera_source, conf=confidence)
    detection_manager.start()
    atexit.register(detection_manager.stop)

    pick_manager = PickTaskManager()

    app = Flask(__name__)
    app.config["controller"] = controller

    @app.get("/healthz")
    def healthz():
        return jsonify(
            {
                "ok": True,
                "connected": controller.robot.is_connected,
                "detection_ready": detection_manager.ready,
                "detection_error": detection_manager.error,
            }
        )

    @app.get("/joints")
    def joints():
        return jsonify(controller.status())

    @app.get("/coordinates")
    def coordinates():
        return jsonify(detection_manager.get_state())

    @app.get("/status")
    def pick_status():
        return jsonify(pick_manager.status())

    @app.post("/pick")
    def pick():
        started = pick_manager.start(lambda: controller.run_pick_task(detection_manager))
        if not started:
            return jsonify({"ok": False, "message": "任务正在运行中"}), 409
        return jsonify({"ok": True, "message": "抓取任务已启动"})

    @app.post("/move/joints")
    def move_joints():
        payload = request.get_json(force=True, silent=False) or {}
        angles = payload.get("angles")
        sleep_s = float(payload.get("sleep", 2.0))
        speed = float(payload.get("speed", DEFAULT_SPEED))
        return jsonify(controller.move_joints(angles, sleep_s, speed))

    @app.post("/move/xyz")
    def move_xyz():
        payload = request.get_json(force=True, silent=False) or {}
        return jsonify(
            controller.move_xyz(
                x=float(payload["x"]),
                y=float(payload["y"]),
                z=float(payload["z"]),
                sleep_s=float(payload.get("sleep", 2.0)),
                speed=float(payload.get("speed", DEFAULT_SPEED)),
                max_iters=int(payload.get("max_iters", 300)),
                tol=float(payload.get("tol", 1e-3)),
                step_size=float(payload.get("step_size", 0.6)),
                damping=float(payload.get("damping", 1e-4)),
            )
        )

    @app.post("/disconnect")
    def disconnect():
        controller.close()
        return jsonify({"ok": True, "connected": False})

    @app.errorhandler(Exception)
    def handle_error(exc: Exception):
        return jsonify({"ok": False, "error": str(exc)}), 400

    return app


app = create_app()


if __name__ == "__main__":
    host = os.getenv("SOARM_API_HOST", "127.0.0.1")
    port = int(os.getenv("SOARM_API_PORT", "8000"))
    app.run(host=host, port=port, threaded=True, use_reloader=False)
