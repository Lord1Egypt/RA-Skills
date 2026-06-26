#!/usr/bin/env python3
"""
Video Generation Script using Doubao Seedance API
Supports: text-to-video, image-to-video, audio-video modes
"""
import os
import sys
import json
import time
import base64
import httpx
from pathlib import Path

API_KEY = os.environ.get("VIDEO_GEN_API_KEY", "")
BASE_URL = os.environ.get("VIDEO_GEN_API_KEY", "https://ark.cn-beijing.volces.com/api/v3")

def create_video_task(
    prompt: str,
    model: str = "doubao-seedance-1.5",
    mode: str = "text_to_video",
    first_frame: str = None,  # base64 or URL
    last_frame: str = None,   # base64 or URL
    reference_image: str = None,  # for seedance-lite
    audio_enabled: bool = False,
    aspect_ratio: str = "16:9",
    duration: int = 5,
) -> dict:
    """Create video generation task"""
    
    if not API_KEY:
        print("ERROR: VIDEO_GEN_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    
    url = f"{BASE_URL}/video/generations"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    
    payload = {
        "model": model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "duration": duration,
    }
    
    # Handle different modes
    if mode == "image_to_video" and first_frame:
        payload["first_frame"] = first_frame
    elif mode == "image_to_video_base64" and first_frame:
        # Assume first_frame is file path, encode to base64
        if os.path.exists(first_frame):
            with open(first_frame, "rb") as f:
                payload["first_frame"] = base64.b64encode(f.read()).decode()
        else:
            payload["first_frame"] = first_frame  # already base64
    elif mode == "audio_video_first_frame" and first_frame:
        payload["first_frame"] = first_frame
        payload["audio_enabled"] = True
    elif mode == "audio_video_first_last_frame" and first_frame and last_frame:
        payload["first_frame"] = first_frame
        payload["last_frame"] = last_frame
        payload["audio_enabled"] = True
    elif mode == "seedance_lite_reference" and reference_image:
        payload["reference_image"] = reference_image
        payload["model"] = "seedance-lite"
    
    print(f"Creating video task: model={model}, mode={mode}", file=sys.stderr)
    
    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
    except Exception as e:
        print(f"ERROR: API call failed: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    
    return result


def query_video_task(task_id: str) -> dict:
    """Query video generation task status"""
    
    url = f"{BASE_URL}/video/generations/{task_id}"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
    }
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"ERROR: Query failed: {e}", file=sys.stderr)
        sys.exit(1)


def wait_for_completion(task_id: str, timeout: int = 600, poll_interval: int = 10) -> dict:
    """Wait for video generation to complete"""
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        result = query_video_task(task_id)
        status = result.get("status", "unknown")
        
        print(f"Task {task_id}: status={status}", file=sys.stderr)
        
        if status == "completed":
            return result
        elif status == "failed":
            print(f"ERROR: Task failed: {result}", file=sys.stderr)
            sys.exit(1)
        
        time.sleep(poll_interval)
    
    print(f"ERROR: Timeout waiting for task {task_id}", file=sys.stderr)
    sys.exit(1)


def download_video(video_url: str, output_path: str) -> str:
    """Download generated video"""
    
    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.get(video_url)
            response.raise_for_status()
            
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            print(f"Video downloaded to: {output_path}", file=sys.stderr)
            return output_path
    except Exception as e:
        print(f"ERROR: Download failed: {e}", file=sys.stderr)
        sys.exit(1)


def generate_video(
    prompt: str,
    mode: str = "text_to_video",
    model: str = "doubao-seedance-1.5",
    first_frame: str = None,
    last_frame: str = None,
    reference_image: str = None,
    audio_enabled: bool = False,
    output: str = None,
    wait: bool = True,
) -> str:
    """Main video generation function"""
    
    # Create task
    task = create_video_task(
        prompt=prompt,
        model=model,
        mode=mode,
        first_frame=first_frame,
        last_frame=last_frame,
        reference_image=reference_image,
        audio_enabled=audio_enabled,
    )
    
    task_id = task.get("id") or task.get("task_id")
    print(f"Task created: {task_id}", file=sys.stderr)
    
    if not wait:
        return json.dumps({"task_id": task_id, "status": "pending"})
    
    # Wait for completion
    result = wait_for_completion(task_id)
    
    # Get video URL
    video_url = result.get("video_url") or result.get("output", {}).get("video_url")
    
    if not video_url:
        print(f"ERROR: No video URL in result: {result}", file=sys.stderr)
        sys.exit(1)
    
    # Download video
    if output:
        output_path = output
    else:
        output_path = str(Path.cwd() / f"video_{task_id}.mp4")
    
    download_video(video_url, output_path)
    
    return output_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate video with Doubao Seedance")
    parser.add_argument("prompt", help="Text prompt for video generation")
    parser.add_argument("--mode", "-m", default="text_to_video", 
                        choices=["text_to_video", "image_to_video", "image_to_video_base64",
                                 "audio_video_first_frame", "audio_video_first_last_frame",
                                 "seedance_lite_reference"],
                        help="Generation mode")
    parser.add_argument("--model", default="doubao-seedance-1.5", help="Model name")
    parser.add_argument("--first-frame", help="First frame image (URL or base64 or file path)")
    parser.add_argument("--last-frame", help="Last frame image (URL or base64 or file path)")
    parser.add_argument("--reference-image", help="Reference image for seedance-lite")
    parser.add_argument("--audio", action="store_true", help="Enable audio")
    parser.add_argument("--output", "-o", help="Output video file path")
    parser.add_argument("--no-wait", action="store_true", help="Don't wait for completion")
    args = parser.parse_args()
    
    result = generate_video(
        prompt=args.prompt,
        mode=args.mode,
        model=args.model,
        first_frame=args.first_frame,
        last_frame=args.last_frame,
        reference_image=args.reference_image,
        audio_enabled=args.audio,
        output=args.output,
        wait=not args.no_wait,
    )
    
    print(result)
