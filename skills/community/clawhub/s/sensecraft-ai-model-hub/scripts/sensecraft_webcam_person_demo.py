#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import cv2
import numpy as np
from ai_edge_litert.interpreter import Interpreter


DEFAULT_MODEL_ID = "60080"
DEFAULT_MODEL_NAME = "Person-Detection--Swift-YOLO"
DEFAULT_MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / f"{DEFAULT_MODEL_ID}-{DEFAULT_MODEL_NAME}.tflite"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run a local webcam person-detection demo with a SenseCraft TFLite model.")
    p.add_argument("--model", type=Path, default=DEFAULT_MODEL_PATH)
    p.add_argument("--camera", type=int, default=0, help="OpenCV camera index")
    p.add_argument("--score-threshold", type=float, default=45.0, help="Model-space score threshold for candidate filtering")
    p.add_argument("--nms-threshold", type=float, default=0.45, help="IoU threshold for NMS")
    p.add_argument("--image", type=Path, help="Run once on a still image instead of webcam")
    p.add_argument("--save", type=Path, help="Optional output path for an annotated still image")
    p.add_argument("--width", type=int, default=1280)
    p.add_argument("--height", type=int, default=720)
    p.add_argument("--debug", action="store_true", help="Print top raw candidates before NMS")
    return p.parse_args()


class PersonDetector:
    def __init__(self, model_path: Path, score_threshold: float = 45.0, nms_threshold: float = 0.45, debug: bool = False):
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")

        self.score_threshold = score_threshold
        self.nms_threshold = nms_threshold
        self.debug = debug
        self.interpreter = Interpreter(model_path=str(model_path))
        self.interpreter.allocate_tensors()

        self.input_detail = self.interpreter.get_input_details()[0]
        self.output_detail = self.interpreter.get_output_details()[0]

        _, self.input_h, self.input_w, _ = self.input_detail["shape"]
        self.input_scale, self.input_zero = self.input_detail["quantization"]
        self.output_scale, self.output_zero = self.output_detail["quantization"]

    def preprocess(self, frame_bgr: np.ndarray) -> np.ndarray:
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(rgb, (self.input_w, self.input_h), interpolation=cv2.INTER_LINEAR)
        q = np.round(resized / self.input_scale + self.input_zero).astype(np.int8)
        return np.expand_dims(q, axis=0)

    def infer(self, frame_bgr: np.ndarray) -> list[dict]:
        tensor = self.preprocess(frame_bgr)
        self.interpreter.set_tensor(self.input_detail["index"], tensor)
        self.interpreter.invoke()
        raw = self.interpreter.get_tensor(self.output_detail["index"])[0].astype(np.float32)
        raw = (raw - self.output_zero) * self.output_scale
        return self.decode(raw, frame_bgr.shape[1], frame_bgr.shape[0])

    def decode(self, raw: np.ndarray, frame_w: int, frame_h: int) -> list[dict]:
        # This specific SenseCraft Swift-YOLO export exposes a single fused output
        # tensor with shape [1, 2268, 6]. In practice, the first four values decode
        # more correctly as center-x, center-y, width, height in model-space rather
        # than plain x1,y1,x2,y2. Treating them as xyxy causes visibly wrong boxes.
        centers_and_sizes = raw[:, :4].copy()
        scores = raw[:, 4].copy()

        keep = scores >= self.score_threshold
        centers_and_sizes = centers_and_sizes[keep]
        scores = scores[keep]
        if len(centers_and_sizes) == 0:
            return []

        cx = centers_and_sizes[:, 0]
        cy = centers_and_sizes[:, 1]
        bw = centers_and_sizes[:, 2]
        bh = centers_and_sizes[:, 3]

        x1 = np.clip(cx - bw / 2.0, 0, self.input_w - 1)
        y1 = np.clip(cy - bh / 2.0, 0, self.input_h - 1)
        x2 = np.clip(cx + bw / 2.0, 0, self.input_w - 1)
        y2 = np.clip(cy + bh / 2.0, 0, self.input_h - 1)

        boxes = np.stack([x1, y1, x2, y2], axis=1)

        if self.debug:
            top = np.argsort(scores)[-8:][::-1]
            print("[debug] top candidates before NMS:")
            for rank, idx in enumerate(top, start=1):
                bx = boxes[idx]
                print(
                    f"  #{rank} score={scores[idx]:.3f} box_model=({bx[0]:.1f},{bx[1]:.1f},{bx[2]:.1f},{bx[3]:.1f}) "
                    f"raw=({centers_and_sizes[idx][0]:.3f},{centers_and_sizes[idx][1]:.3f},{centers_and_sizes[idx][2]:.3f},{centers_and_sizes[idx][3]:.3f})"
                )

        scale_x = frame_w / float(self.input_w)
        scale_y = frame_h / float(self.input_h)
        boxes[:, [0, 2]] *= scale_x
        boxes[:, [1, 3]] *= scale_y

        indices = cv2.dnn.NMSBoxes(
            bboxes=[[float(x1), float(y1), float(x2 - x1), float(y2 - y1)] for x1, y1, x2, y2 in boxes],
            scores=[float(s) for s in scores],
            score_threshold=float(self.score_threshold),
            nms_threshold=float(self.nms_threshold),
        )
        if len(indices) == 0:
            return []

        flat = np.array(indices).reshape(-1)
        detections = []
        for idx in flat:
            x1, y1, x2, y2 = boxes[idx]
            detections.append({
                "label": "person",
                "score": float(scores[idx]),
                "box": [int(x1), int(y1), int(x2), int(y2)],
            })
        return detections


def draw(frame: np.ndarray, detections: list[dict], fps: float | None = None) -> np.ndarray:
    out = frame.copy()
    for det in detections:
        x1, y1, x2, y2 = det["box"]
        cv2.rectangle(out, (x1, y1), (x2, y2), (40, 220, 90), 2)
        text = f"{det['label']} {det['score']:.1f}"
        cv2.putText(out, text, (x1, max(24, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (40, 220, 90), 2, cv2.LINE_AA)

    status = f"persons: {len(detections)}"
    if fps is not None:
        status += f" | fps: {fps:.1f}"
    cv2.rectangle(out, (10, 10), (330, 44), (0, 0, 0), -1)
    cv2.putText(out, status, (16, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    return out


def run_image(args: argparse.Namespace, detector: PersonDetector) -> int:
    frame = cv2.imread(str(args.image))
    if frame is None:
        print(f"Failed to read image: {args.image}", file=sys.stderr)
        return 2
    detections = detector.infer(frame)
    annotated = draw(frame, detections)
    if args.save:
        cv2.imwrite(str(args.save), annotated)
        print(f"Saved: {args.save}")
    print(f"detections={len(detections)}")
    for det in detections[:20]:
        print(det)
    return 0


def run_camera(args: argparse.Namespace, detector: PersonDetector) -> int:
    cap = cv2.VideoCapture(args.camera)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    if not cap.isOpened():
        print("Could not open camera. On macOS this often means camera permission is missing.", file=sys.stderr)
        return 2

    prev = time.perf_counter()
    fps = None
    win = "SenseCraft Person Detection"
    cv2.namedWindow(win, cv2.WINDOW_NORMAL)

    while True:
        ok, frame = cap.read()
        if not ok:
            print("Camera frame read failed.", file=sys.stderr)
            break

        start = time.perf_counter()
        detections = detector.infer(frame)
        infer_ms = (time.perf_counter() - start) * 1000.0

        now = time.perf_counter()
        instant_fps = 1.0 / max(now - prev, 1e-6)
        prev = now
        fps = instant_fps if fps is None else (fps * 0.9 + instant_fps * 0.1)

        annotated = draw(frame, detections, fps=fps)
        cv2.putText(annotated, f"infer: {infer_ms:.1f} ms | s: save | q: quit", (16, annotated.shape[0] - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow(win, annotated)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            captures_dir = Path(__file__).resolve().parent.parent / "captures"
            captures_dir.mkdir(parents=True, exist_ok=True)
            out_path = captures_dir / f"capture-{int(time.time())}.png"
            cv2.imwrite(str(out_path), annotated)
            print(f"Saved frame: {out_path}")
        if key in (ord('q'), 27):
            break

    cap.release()
    cv2.destroyAllWindows()
    return 0


def main() -> int:
    args = parse_args()
    detector = PersonDetector(args.model, args.score_threshold, args.nms_threshold, debug=args.debug)
    if args.image:
        return run_image(args, detector)
    return run_camera(args, detector)


if __name__ == "__main__":
    raise SystemExit(main())
