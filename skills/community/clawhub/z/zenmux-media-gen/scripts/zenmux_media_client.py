#!/usr/bin/env python3
"""
ZenMux Media Generation Client
Generate images and videos using ZenMux API
"""

import os
import sys
import json
import argparse
import time
import base64
import requests
from pathlib import Path

ZENMUX_API_KEY = os.environ.get("ZENMUX_API_KEY")
ZENMUX_BASE_URL = "https://api.zenmux.ai/v1"

DEFAULT_IMAGE_MODEL = "google/gemini-3-pro-image-preview"
DEFAULT_VIDEO_MODEL = "google/veo-3.1-generate-001"


def generate_image(model: str, prompt: str, out: str = None) -> str:
    """Generate image using ZenMux API"""
    if not ZENMUX_API_KEY:
        print("Error: ZENMUX_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    
    url = f"{ZENMUX_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {ZENMUX_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image"]
    }
    
    print(f"Generating image with model: {model}")
    print(f"Prompt: {prompt}")
    
    response = requests.post(url, headers=headers, json=data, timeout=120)
    response.raise_for_status()
    
    result = response.json()
    
    # Extract image from response
    if "choices" in result and len(result["choices"]) > 0:
        choice = result["choices"][0]
        if "message" in choice and "content" in choice["message"]:
            content = choice["message"]["content"]
            if isinstance(content, list):
                for item in content:
                    if item.get("type") == "image":
                        image_data = item.get("image", {})
                        if "url" in image_data:
                            # Download from URL
                            img_response = requests.get(image_data["url"], timeout=30)
                            img_data = img_response.content
                        elif "base64" in image_data:
                            img_data = base64.b64decode(image_data["base64"])
                        else:
                            print(f"Unknown image format: {image_data}", file=sys.stderr)
                            sys.exit(1)
                        
                        if out:
                            with open(out, "wb") as f:
                                f.write(img_data)
                            print(f"Image saved to: {out}")
                            return out
                        else:
                            # Save to default file
                            default_out = "output.png"
                            with open(default_out, "wb") as f:
                                f.write(img_data)
                            print(f"Image saved to: {default_out}")
                            return default_out
    
    print(f"Response: {json.dumps(result, indent=2)}", file=sys.stderr)
    print("Warning: No image in response", file=sys.stderr)
    return None


def create_video_task(model: str, prompt: str, duration: int = 5, 
                      img_url: str = None, resolution: str = "720p") -> str:
    """Create video generation task"""
    if not ZENMUX_API_KEY:
        print("Error: ZENMUX_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    
    url = f"{ZENMUX_BASE_URL}/images/generations"
    headers = {
        "Authorization": f"Bearer {ZENMUX_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "prompt": prompt,
        "parameters": {
            "duration": duration,
            "resolution": resolution
        }
    }
    
    if img_url:
        data["parameters"]["image_url"] = img_url
    
    print(f"Creating video task with model: {model}")
    print(f"Prompt: {prompt}")
    print(f"Duration: {duration}s, Resolution: {resolution}")
    
    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()
    
    result = response.json()
    
    if "id" in result:
        task_id = result["id"]
        print(f"Task created: {task_id}")
        return task_id
    else:
        print(f"Response: {json.dumps(result, indent=2)}", file=sys.stderr)
        print("Error: No task ID in response", file=sys.stderr)
        sys.exit(1)


def get_video_status(task_id: str) -> dict:
    """Get video generation task status"""
    if not ZENMUX_API_KEY:
        print("Error: ZENMUX_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    
    url = f"{ZENMUX_BASE_URL}/images/generations/{task_id}"
    headers = {
        "Authorization": f"Bearer {ZENMUX_API_KEY}"
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    return response.json()


def wait_for_video(task_id: str, poll_interval: int = 5, timeout: int = 600,
                   download: bool = False, out: str = None) -> str:
    """Wait for video generation to complete"""
    print(f"Waiting for task {task_id} to complete...")
    start_time = time.time()
    
    while True:
        if time.time() - start_time > timeout:
            print("Error: Timeout waiting for video", file=sys.stderr)
            sys.exit(1)
        
        status = get_video_status(task_id)
        state = status.get("status", "unknown")
        
        print(f"Status: {state}")
        
        if state == "completed":
            if download:
                # Download video
                if "output" in status and "url" in status["output"]:
                    video_url = status["output"]["url"]
                    print(f"Downloading from: {video_url}")
                    
                    response = requests.get(video_url, timeout=300)
                    response.raise_for_status()
                    
                    if out is None:
                        out = f"{task_id}.mp4"
                    
                    with open(out, "wb") as f:
                        f.write(response.content)
                    
                    print(f"Video saved to: {out}")
                    return out
            elif "output" in status and "url" in status["output"]:
                print(f"Video URL: {status['output']['url']}")
                return status["output"]["url"]
            return None
        
        elif state == "failed":
            error = status.get("error", "Unknown error")
            print(f"Error: Video generation failed - {error}", file=sys.stderr)
            sys.exit(1)
        
        time.sleep(poll_interval)


def main():
    parser = argparse.ArgumentParser(description="ZenMux Media Generation Client")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Image command
    img_parser = subparsers.add_parser("image", help="Generate image")
    img_parser.add_argument("--model", default=DEFAULT_IMAGE_MODEL, help="Image model ID")
    img_parser.add_argument("--prompt", required=True, help="Image prompt")
    img_parser.add_argument("--out", help="Output file path")
    
    # Video create command
    video_create_parser = subparsers.add_parser("video-create", help="Create video task")
    video_create_parser.add_argument("--model", default=DEFAULT_VIDEO_MODEL, help="Video model ID")
    video_create_parser.add_argument("--prompt", required=True, help="Video prompt")
    video_create_parser.add_argument("--duration", type=int, default=5, help="Video duration in seconds")
    video_create_parser.add_argument("--img-url", help="Reference image URL for video")
    video_create_parser.add_argument("--resolution", default="720p", help="Video resolution")
    
    # Video status command
    video_status_parser = subparsers.add_parser("video-status", help="Get video task status")
    video_status_parser.add_argument("--task-id", required=True, help="Task ID")
    
    # Video wait command
    video_wait_parser = subparsers.add_parser("video-wait", help="Wait for video completion")
    video_wait_parser.add_argument("--task-id", required=True, help="Task ID")
    video_wait_parser.add_argument("--poll", type=int, default=5, help="Poll interval in seconds")
    video_wait_parser.add_argument("--timeout", type=int, default=600, help="Timeout in seconds")
    video_wait_parser.add_argument("--download", action="store_true", help="Download video when ready")
    video_wait_parser.add_argument("--out", help="Output file path")
    
    args = parser.parse_args()
    
    if args.command == "image":
        generate_image(args.model, args.prompt, args.out)
    elif args.command == "video-create":
        create_video_task(args.model, args.prompt, args.duration, args.img_url, args.resolution)
    elif args.command == "video-status":
        status = get_video_status(args.task_id)
        print(json.dumps(status, indent=2))
    elif args.command == "video-wait":
        wait_for_video(args.task_id, args.poll, args.timeout, args.download, args.out)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
