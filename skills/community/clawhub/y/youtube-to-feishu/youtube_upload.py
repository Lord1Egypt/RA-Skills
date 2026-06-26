#!/usr/bin/env python3
"""YouTube to Feishu - Download audio and upload to Feishu cloud storage."""

import argparse
import json
import os
import sys
import subprocess
import tempfile
from pathlib import Path

# Try to import feishu tools (available in OpenClaw environment)
try:
    # These will be called via OpenClaw's tool system
    FEISHU_AVAILABLE = True
except ImportError:
    FEISHU_AVAILABLE = False


def print_progress(step: str, message: str):
    """Print progress message."""
    print(f"[{step}] {message}")
    sys.stdout.flush()


def download_audio(url: str, output_dir: str) -> dict:
    """Download audio from YouTube using yt-dlp."""
    print_progress("1/4", "Extracting video info...")
    
    # First, get video info
    info_cmd = [
        "yt-dlp",
        "--dump-json",
        "--no-download",
        url
    ]
    
    try:
        result = subprocess.run(info_cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            return {"error": f"Failed to get video info: {result.stderr}"}
        
        video_info = json.loads(result.stdout)
        video_title = video_info.get("title", "Unknown")
        video_duration = video_info.get("duration", 0)
        video_id = video_info.get("id", "unknown")
        
        print_progress("2/4", f"Downloading audio: {video_title[:50]}...")
    except Exception as e:
        return {"error": f"Failed to extract video info: {str(e)}"}
    
    # Download audio
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")
    download_cmd = [
        "yt-dlp",
        "-x",  # Extract audio
        "--audio-format", "mp3",
        "--audio-quality", "192K",
        "-o", output_template,
        url
    ]
    
    try:
        result = subprocess.run(download_cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            return {"error": f"Download failed: {result.stderr}"}
        
        # Find downloaded file
        downloaded_files = list(Path(output_dir).glob("*.mp3"))
        if not downloaded_files:
            return {"error": "No audio file found after download"}
        
        audio_file = downloaded_files[0]
        file_size = audio_file.stat().st_size
        file_size_mb = round(file_size / (1024 * 1024), 2)
        
        print_progress("2/4", f"Downloaded: {audio_file.name} ({file_size_mb} MB)")
        
        return {
            "success": True,
            "file_path": str(audio_file),
            "file_name": audio_file.name,
            "file_size": file_size,
            "file_size_mb": file_size_mb,
            "video_title": video_title,
            "video_id": video_id,
            "video_duration": video_duration,
            "video_url": url,
        }
        
    except subprocess.TimeoutExpired:
        return {"error": "Download timeout (5 minutes)"}
    except Exception as e:
        return {"error": f"Download failed: {str(e)}"}


def main():
    parser = argparse.ArgumentParser(description="YouTube to Feishu Audio Upload")
    parser.add_argument("--url", required=True, help="YouTube video URL")
    parser.add_argument("--title", help="Optional custom title")
    args = parser.parse_args()
    
    # Create temp directory
    temp_dir = os.path.join(os.path.dirname(__file__), "..", "..", "temp")
    os.makedirs(temp_dir, exist_ok=True)
    
    print_progress("START", f"YouTube to Feishu - {args.url}")
    
    # Step 1-2: Download audio
    result = download_audio(args.url, temp_dir)
    
    if "error" in result:
        print(f"[ERROR] {result['error']}")
        print(json.dumps({"status": "error", "message": result["error"]}))
        sys.exit(1)
    
    # Output result for OpenClaw to process
    print_progress("3/4", "Ready for Feishu upload...")
    print_progress("4/4", "Use feishu_drive_file to upload, then feishu_im_user_message to send")
    
    # Return structured result
    output = {
        "status": "success",
        "message": f"Audio downloaded: {result['file_name']} ({result['file_size_mb']} MB)",
        "video_info": {
            "title": result["video_title"],
            "id": result["video_id"],
            "duration": result["video_duration"],
            "url": result["video_url"],
        },
        "file_info": {
            "path": result["file_path"],
            "name": result["file_name"],
            "size": result["file_size"],
            "size_mb": result["file_size_mb"],
        },
        "next_steps": [
            "1. Upload to Feishu cloud: feishu_drive_file (action=upload, file_path=<path>)",
            "2. Send to user: feishu_im_user_message (msg_type=file, content={'file_key': <token>})",
        ]
    }
    
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
