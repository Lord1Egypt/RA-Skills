"""Frame extraction with global index overlay."""

import uuid
from pathlib import Path
from typing import List, Optional, Union

import cv2
import numpy as np
from videoarm_lib.config import database


def extract_frames_uniform(
    video_path: Path,
    num_frames: int = 8,
    start_sec: float = 0.0,
    end_sec: Optional[float] = None
) -> List[dict]:
    """Extract frames uniformly from a time range, return as bytes."""
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise Exception(f"Failed to open video: {video_path}")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0
    
    if end_sec is None:
        end_sec = duration
    
    start_frame = int(start_sec * fps)
    end_frame = int(end_sec * fps)
    
    available = end_frame - start_frame + 1
    actual = min(num_frames, available)
    
    if actual == 1:
        indices = [start_frame]
    else:
        indices = [
            int(start_frame + (end_frame - start_frame) * i / (actual - 1))
            for i in range(actual)
        ]
    
    frames = []
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue
        
        # Encode to JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frames.append({
            "frame_index": idx,
            "timestamp": idx / fps if fps > 0 else 0,
            "image_bytes": buffer.tobytes()
        })
    
    cap.release()
    return frames


def get_cropped_frame_paths(
    video_path: Union[str, Path],
    start_frame: Optional[int],
    end_frame: Optional[int],
    num_frames: int,
    session_id: Optional[str] = None,
    target_short_side: int = 256,
) -> List[str]:
    """Uniformly sample frames with global index overlay at top-left."""
    video_path = Path(video_path)
    video_id, dataset = database.get_video_id_from_path(video_path)
    if session_id is None:
        session_id = str(uuid.uuid4())[:8]

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise Exception(f"Failed to open video: {video_path}")

    if start_frame is None or end_frame is None:
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        start_frame = start_frame or 0
        end_frame = end_frame or (total - 1)

    available = end_frame - start_frame + 1
    actual = min(num_frames, available)

    if actual == 1:
        indices = [start_frame]
    else:
        indices = [
            int(start_frame + (end_frame - start_frame) * i / (actual - 1))
            for i in range(actual)
        ]

    output_dir = database.get_temp_frames_dir(video_id, session_id, dataset)
    output_dir.mkdir(parents=True, exist_ok=True)

    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 256
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 256

    paths = []
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret or frame is None:
            frame = np.zeros((h, w, 3), dtype=np.uint8)

        cv2.putText(
            frame, str(idx), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
        )

        if target_short_side and target_short_side > 0:
            short = min(frame.shape[:2])
            if short > target_short_side:
                scale = target_short_side / float(short)
                new_w = max(1, int(round(frame.shape[1] * scale)))
                new_h = max(1, int(round(frame.shape[0] * scale)))
                frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)

        out = output_dir / f"frame_{idx:06d}.jpg"
        cv2.imwrite(str(out), frame)
        paths.append(str(out.resolve()))

    cap.release()
    return paths
