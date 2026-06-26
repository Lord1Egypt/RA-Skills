#!/usr/bin/env python3
"""
generate_shot_videos.py
Generates videos from images using MiniMax I2V API.
MiniMax video generation is a 3-step async flow:
  1. POST /v1/video_generation       → { task_id }
  2. GET  /v1/video_generation/{id} → { status, file_id }
  3. GET  /v1/files/{file_id}        → video file binary
"""

import os
import json
import time
import requests
from pathlib import Path
from typing import List, Dict, Any, Optional

# ── MiniMax Video Generation Endpoints ──────────────────────────────────────
MINIMAX_BASE_V2 = os.environ.get("MINIMAX_BASE_URL", "https://api.minimaxi.com/v1")
CREATE_ENDPOINT  = f"{MINIMAX_BASE_V2}/video_generation"
QUERY_ENDPOINT   = f"{MINIMAX_BASE_V2}/query/video_generation"
FILE_ENDPOINT    = lambda file_id: f"{MINIMAX_BASE_V2}/files/{file_id}"

MODEL        = "MiniMax-Hailuo-2.3"
MODEL_FAST   = "MiniMax-Hailuo-2.3-Fast"  # cheaper/faster alternative

# ── Retry / Polling ──────────────────────────────────────────────────────────
MAX_RETRIES   = 3
RETRY_DELAY   = 5    # seconds between retries
POLL_INTERVAL = 10   # seconds between status polls
POLL_TIMEOUT  = 600  # seconds (10 min max per video)

# ── Output ────────────────────────────────────────────────────────────────────
OUTPUT_DIR   = Path("./output")
VIDEOS_DIR   = OUTPUT_DIR / "videos"


def get_api_key() -> str:
    key = os.environ.get("MINIMAX_API_KEY")
    if not key:
        raise ValueError("MINIMAX_API_KEY environment variable not set")
    return key


def load_image_data(input_path: str) -> List[Dict[str, Any]]:
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Image data file not found: {input_path}")
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, dict):
        for key in ("shots", "images"):
            if key in data:
                return data[key]
    elif isinstance(data, list):
        return data
    raise ValueError(f"Unexpected JSON structure in {input_path}")


# ── Step 1: Create video generation task ─────────────────────────────────────
def create_video_task(
    image_url: str,
    api_key: str,
    duration: int = 6,
    resolution: str = "768P",
    model: str = MODEL,
    timeout: int = 60
) -> Dict[str, Any]:
    """
    POST /v1/video_generation
    Returns { task_id: "..." } on success.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "first_frame_image": image_url,
        "duration": duration,
        "resolution": resolution
    }
    resp = requests.post(CREATE_ENDPOINT, headers=headers, json=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


# ── Step 2: Poll task status ─────────────────────────────────────────────────
def poll_video_status(
    task_id: str,
    api_key: str,
    timeout: int = POLL_TIMEOUT
) -> Dict[str, Any]:
    """
    GET /v1/query/video_generation?task_id={task_id}
    Returns { success: True, file_id: "..." } or { success: False, error: "..." }.
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    start = time.time()
    last_status = "processing"

    while time.time() - start < timeout:
        resp = requests.get(QUERY_ENDPOINT, headers=headers,
                           params={"task_id": task_id}, timeout=30)
        resp.raise_for_status()
        result = resp.json()

        status = result.get("status", result.get("task_status", ""))
        last_status = status

        if status == "Success":
            file_id = result.get("file_id")
            if not file_id:
                return {"success": False, "error": f"No file_id in success response: {result}"}
            return {"success": True, "file_id": file_id, "data": result}

        if status == "Fail":
            err = result.get("base_resp", {}).get("status_msg", "Unknown error")
            return {"success": False, "error": err}

        print(f"    Status: {status}, waiting...")
        time.sleep(POLL_INTERVAL)

    return {"success": False, "error": f"Timeout after {timeout}s (last: {last_status})"}


# ── Step 3: Download video file ──────────────────────────────────────────────
def download_video(file_id: str, api_key: str, output_path: Path, timeout: int = 300) -> bool:
    """
    GET /v1/files/{file_id}
    Saves the binary video to output_path.
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    resp = requests.get(FILE_ENDPOINT(file_id), headers=headers, timeout=timeout, stream=True)
    resp.raise_for_status()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=65536):
            f.write(chunk)
    return True


# ── Main generation function ──────────────────────────────────────────────────
def generate_shot_video(
    image_url: str,
    shot_number: int,
    shot_desc: str,
    api_key: str,
    duration: int = 6,
    resolution: str = "768P",
    model: str = MODEL,
    timeout: int = 60
) -> Dict[str, Any]:
    """Generate one video from an image URL with retry logic."""
    print(f"\n[Shot {shot_number}]")
    print(f"  Image: {image_url[:80]}...")
    print(f"  Model: {model} | Duration: {duration}s | Resolution: {resolution}")

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"  [Attempt {attempt}/{MAX_RETRIES}] Creating task...")
            create_result = create_video_task(image_url, api_key, duration, resolution, model, timeout)

            task_id = (
                create_result.get("task_id")
                or create_result.get("id")
                or create_result.get("data", {}).get("task_id")
            )
            if not task_id:
                raise ValueError(f"No task_id in create response: {create_result}")
            print(f"  Task ID: {task_id}")

            print(f"  Waiting for completion...")
            poll_result = poll_video_status(task_id, api_key)

            if not poll_result["success"]:
                last_error = poll_result["error"]
                print(f"  Poll failed: {last_error}")
                time.sleep(RETRY_DELAY)
                continue

            file_id = poll_result["file_id"]
            output_file = VIDEOS_DIR / f"video_{shot_number:03d}.mp4"
            print(f"  Downloading video to {output_file}...")
            if download_video(file_id, api_key, output_file):
                return {
                    "success": True,
                    "shot_number": shot_number,
                    "task_id": task_id,
                    "file_id": file_id,
                    "local_path": str(output_file)
                }
            else:
                last_error = "Download failed"

        except requests.exceptions.RequestException as e:
            last_error = f"Request error: {e}"
            print(f"  {last_error}")
        except Exception as e:
            last_error = f"Unexpected error: {e}"
            print(f"  {last_error}")

        if attempt < MAX_RETRIES:
            print(f"  Retrying in {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)

    return {"success": False, "shot_number": shot_number, "error": last_error}


def generate_all_videos(
    input_path: str = "./output/shot_images.json",
    output_path: str = "./output/shot_videos.json",
    duration: int = 6,
    resolution: str = "768P",
    model: str = MODEL
) -> List[Dict[str, Any]]:
    print("=" * 60)
    print("GENERATE SHOT VIDEOS  (MiniMax I2V)")
    print("=" * 60)

    api_key = get_api_key()
    print(f"[OK] API key loaded\n")

    images = load_image_data(input_path)
    print(f"[OK] Loaded {len(images)} image entries\n")

    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    success = fail = 0

    for entry in images:
        shot_number = entry.get("shot_number", 1)
        image_url = (
            entry.get("image_url")
            or entry.get("url")
            or (entry.get("data", {}).get("image_url"))
        )
        if not image_url:
            print(f"[WARN] Shot {shot_number}: no image_url, skipping")
            continue

        result = generate_shot_video(
            image_url=image_url,
            shot_number=shot_number,
            shot_desc=entry.get("description", ""),
            api_key=api_key,
            duration=duration,
            resolution=resolution,
            model=model
        )
        results.append(result)

        if result["success"]:
            success += 1
            print(f"  [OK] Shot {shot_number} → {result['local_path']}")
        else:
            fail += 1
            print(f"  [FAIL] Shot {shot_number}: {result.get('error')}")

    # Save results
    output_data = {
        "shots": results,
        "summary": {"total": len(results), "successful": success, "failed": fail}
    }
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 60}")
    print(f"COMPLETE: {success} successful, {fail} failed")
    print(f"Output saved to: {output_path}")
    print(f"{'=' * 60}")
    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate videos from images via MiniMax I2V")
    parser.add_argument("-i", "--input",  default="./output/shot_images.json", help="Input images JSON")
    parser.add_argument("-o", "--output", default="./output/shot_videos.json", help="Output JSON path")
    parser.add_argument("-d", "--duration", type=int, default=6, choices=[6, 10], help="Video duration in seconds")
    parser.add_argument("-r", "--resolution", default="768P", choices=["768P", "1080P"], help="Video resolution")
    parser.add_argument("-m", "--model", default=MODEL, help=f"Model name (default: {MODEL})")

    args = parser.parse_args()
    try:
        generate_all_videos(args.input, args.output, args.duration, args.resolution, args.model)
    except Exception as e:
        print(f"\nERROR: {e}")
        exit(1)
