#!/usr/bin/env python3
"""VideoARM Extract Frames — extract frames and return image paths for agent analysis.

Returns image paths for the agent to analyze with image tool or spawn sub-agents.
"""

import argparse
import json
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np

from videoarm_lib.config import get_config
from videoarm_lib.frames import extract_frames_uniform
from videoarm_lib.logger import ToolTracer
from videoarm_lib.resolve import resolve_video


def extract_and_save_frames(video_path: Path, fps: float, frame_ranges: list, num_frames: int, tracer=None) -> dict:
    """Extract frames and save as grid image.

    Frames are distributed proportionally across ranges by range length,
    matching the source agent_pipeline logic.
    """
    # Calculate proportional frame distribution by range length
    total_range_length = sum(r["end_frame"] - r["start_frame"] for r in frame_ranges)

    all_frames = []
    range_info = []

    for i, fr in enumerate(frame_ranges):
        start_sec = fr["start_frame"] / fps
        end_sec = fr["end_frame"] / fps

        # Proportional allocation
        range_length = fr["end_frame"] - fr["start_frame"]
        if total_range_length > 0:
            range_ratio = range_length / total_range_length
            frames_for_this_range = max(1, int(num_frames * range_ratio))
        else:
            frames_for_this_range = max(1, num_frames // len(frame_ranges))

        # Last range gets the remainder to ensure exact total
        if i == len(frame_ranges) - 1:
            frames_for_this_range = num_frames - len(all_frames)
            frames_for_this_range = max(1, frames_for_this_range)

        frames = extract_frames_uniform(video_path, num_frames=frames_for_this_range, start_sec=start_sec, end_sec=end_sec)
        all_frames.extend(frames)
        range_info.append({
            "start_frame": fr["start_frame"],
            "end_frame": fr["end_frame"],
            "start_sec": round(start_sec, 2),
            "end_sec": round(end_sec, 2),
        })

    if tracer:
        tracer.log("frames_extracted", count=len(all_frames), ranges=range_info)

    # Create grid images (fixed 3x2 layout, multiple grids if needed)
    images = []
    frame_numbers = []
    for frame_data in all_frames[:num_frames]:
        arr = np.frombuffer(frame_data["image_bytes"], dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        images.append(img)
        frame_numbers.append(frame_data.get("frame_number", 0))
    
    # Fixed 3x2 grid (3 columns, 2 rows = 6 frames per grid)
    cols = 3
    rows = 2
    frames_per_grid = cols * rows
    
    # Resize frames: shorter edge = 512, add frame number overlay
    resized = []
    for idx, img in enumerate(images):
        h, w = img.shape[:2]
        if h < w:
            # Height is shorter
            new_h = 512
            new_w = int(w * (512 / h))
        else:
            # Width is shorter
            new_w = 512
            new_h = int(h * (512 / w))
        resized_img = cv2.resize(img, (new_w, new_h))
        
        # Add frame number overlay (top-left corner)
        frame_num = frame_numbers[idx]
        cv2.putText(resized_img, f"#{frame_num}", (10, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.putText(resized_img, f"#{frame_num}", (10, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2, cv2.LINE_AA)
        
        resized.append(resized_img)
    
    # Create multiple grids if needed
    grid_images = []
    for grid_idx in range(0, len(resized), frames_per_grid):
        grid_frames = resized[grid_idx:grid_idx + frames_per_grid]
        
        # Pad to 6 frames if needed
        while len(grid_frames) < frames_per_grid:
            grid_frames.append(np.zeros((512, 512, 3), dtype=np.uint8))
        
        grid_rows = []
        for r in range(rows):
            row_imgs = grid_frames[r * cols:(r + 1) * cols]
            grid_rows.append(np.hstack(row_imgs))
        grid = np.vstack(grid_rows)
        grid_images.append(grid)
    
    # Save all grid images to workspace temp directory
    workspace_tmp = Path.home() / ".openclaw" / "workspace" / "tmp"
    workspace_tmp.mkdir(parents=True, exist_ok=True)
    
    image_paths = []
    for i, grid in enumerate(grid_images):
        tmp = tempfile.NamedTemporaryFile(suffix=f"_grid{i}.jpg", delete=False, dir=str(workspace_tmp))
        cv2.imwrite(tmp.name, grid)
        tmp.close()
        image_paths.append(tmp.name)

    if tracer:
        tracer.log("grids_saved", paths=image_paths, grid_count=len(grid_images), total_frames=len(images))

    return {
        "image_paths": image_paths,  # Multiple grid images
        "frame_ranges": range_info,
        "num_frames_extracted": len(all_frames),
    }


def main():
    parser = argparse.ArgumentParser(description="Extract frames and save as grid image")
    parser.add_argument("--video", required=True, help="Video file path or URL")
    parser.add_argument("--ranges", required=True, help='JSON array: [{"start_frame":0,"end_frame":100}]')
    parser.add_argument("--num-frames", type=int, default=30, choices=[30, 60, 90, 150])
    args = parser.parse_args()

    try:
        frame_ranges = json.loads(args.ranges)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in --ranges: {e}", file=sys.stderr)
        sys.exit(1)

    config = get_config()

    with ToolTracer("extract-frames", video=args.video, ranges=frame_ranges, num_frames=args.num_frames) as t:
        video_path, meta = resolve_video(args.video, tracer=t)
        fps = meta["fps"]

        result = extract_and_save_frames(video_path, fps, frame_ranges, args.num_frames, tracer=t)
        result["video"] = str(video_path)
        result["meta"] = meta
        t.set_result(result)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
