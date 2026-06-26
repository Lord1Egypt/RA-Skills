#!/usr/bin/env python3
"""
generate_shot_images.py
Generates images for each shot using MiniMax T2I API.
Handles async polling for task completion.
First shot has no previous image, subsequent shots pass previous image URL
as `referenced_image_urls` for visual continuity (character/setting consistency).

API flow:
  POST /v1/image_generation  → { id: task_id }
  GET  /v1/image_generation/{id}  → { status, data: { image_url } }

Note: referenced_image_urls for continuity is based on MiniMax i2i capability;
verify it against latest API docs if images appear inconsistent.
"""

import os
import json
import time
import requests
import uuid
from pathlib import Path
from typing import List, Dict, Any

# Configuration
API_ENDPOINT = os.environ.get("MINIMAX_IMAGE_URL", "https://api.minimaxi.com/v1/image_generation")
MODEL = "image-01"

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds
POLL_INTERVAL = 3  # seconds
POLL_TIMEOUT = 300  # seconds per image

# Output directories
OUTPUT_DIR = Path("./output")
FRAMES_DIR = OUTPUT_DIR / "frames"


def get_api_key() -> str:
    """Get API key from environment."""
    api_key = os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("MINIMAX_API_KEY environment variable not set")
    return api_key


def load_shots(input_path: str) -> List[Dict[str, Any]]:
    """Load shots from JSON file."""
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Shots file not found: {input_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, dict) and "shots" in data:
        return data["shots"]
    elif isinstance(data, list):
        return data
    else:
        raise ValueError(f"Unexpected JSON structure in {input_path}")


def generate_image(
    prompt: str,
    api_key: str,
    timeout: int = 120
) -> Dict[str, Any]:
    """
    Generate image synchronously using MiniMax T2I API.
    Returns dict with image_url and local_path on success.
    NOTE: No polling needed — result returned in initial response.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "parameters": {"aspect_ratio": "16:9"}
    }
    
    response = requests.post(
        API_ENDPOINT,
        headers=headers,
        json=payload,
        timeout=timeout
    )
    response.raise_for_status()
    result = response.json()
    
    # Check for API error
    base_resp = result.get("base_resp", {})
    if base_resp.get("status_code") != 0:
        raise RuntimeError(f"API error {base_resp.get('status_code')}: {base_resp.get('status_msg')}")
    
    # Extract image URL — correct path: data.image_urls[0]
    image_urls = result.get("data", {}).get("image_urls", [])
    if not image_urls:
        raise RuntimeError(f"No image_urls in response: {result}")
    
    return {"image_url": image_urls[0], "result": result}


def poll_task_status(task_id: str, api_key: str, timeout: int = POLL_TIMEOUT) -> Dict[str, Any]:
    """Poll task status until completion."""
    status_endpoint = f"https://api.minimaxi.com/v1/image_generation/{task_id}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    start_time = time.time()
    last_status = "processing"
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(status_endpoint, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            status = result.get("status", result.get("task_status", ""))
            last_status = status
            
            if status == "success" or status == "completed":
                return {"success": True, "data": result}
            elif status == "failed" or status == "error":
                error_msg = result.get("error", {}).get("message", "Unknown error")
                return {"success": False, "error": error_msg}
            
            print(f"    Status: {status}, waiting...")
            time.sleep(POLL_INTERVAL)
            
        except requests.exceptions.RequestException as e:
            print(f"    Poll error: {e}, retrying...")
            time.sleep(POLL_INTERVAL)
    
    return {"success": False, "error": f"Timeout after {timeout}s (last status: {last_status})"}


def download_image(url: str, output_path: Path, timeout: int = 60) -> bool:
    """Download image from URL to file path."""
    try:
        response = requests.get(url, timeout=timeout, stream=True)
        response.raise_for_status()
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True
    except Exception as e:
        print(f"    Download failed: {e}")
        return False


def generate_shot_image(
    shot: Dict[str, Any],
    shot_index: int,
    total_shots: int,
    api_key: str
) -> Dict[str, Any]:
    """Generate image for a single shot with retry logic."""
    shot_num = shot.get("shot_number", shot_index + 1)
    visual_desc = shot.get("visual_description", shot.get("description", ""))
    
    print(f"\n[Shot {shot_num} ({shot_index + 1}/{total_shots})]")
    print(f"  Description: {shot.get('description', 'N/A')[:60]}...")
    print(f"  Visual: {visual_desc[:80]}...")
    
    # Build enhanced prompt
    enhanced_prompt = f"{visual_desc}. Cinematic, photorealistic, 4K quality, professional film production."
    
    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            print(f"  [Attempt {attempt + 1}/{MAX_RETRIES}] Generating...")
            
            # Generate synchronously (no polling needed)
            result = generate_image(enhanced_prompt, api_key)
            image_url = result["image_url"]
            
            print(f"  Image URL: {image_url[:60]}...")
            
            # Download image
            output_filename = f"shot_{shot_num:03d}.png"
            output_path = FRAMES_DIR / output_filename
            
            print(f"  Downloading to {output_path}...")
            if download_image(image_url, output_path):
                return {
                    "success": True,
                    "shot_number": shot_num,
                    "image_url": image_url,
                    "local_path": str(output_path)
                }
            else:
                last_error = "Image download failed"
            
        except requests.exceptions.RequestException as e:
            last_error = f"Request error: {e}"
            print(f"  {last_error}")
        except Exception as e:
            last_error = f"Unexpected error: {e}"
            print(f"  {last_error}")
        
        if attempt < MAX_RETRIES - 1:
            print(f"  Retrying in {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)
    
    return {
        "success": False,
        "shot_number": shot_num,
        "error": last_error
    }


def generate_all_images(
    shots_path: str = "./output/shots.json",
    output_path: str = "./output/shot_images.json"
) -> List[Dict[str, Any]]:
    """
    Generate images for all shots.
    
    Args:
        shots_path: Path to shots JSON file
        output_path: Path to save output JSON
        
    Returns:
        List of generated image info
    """
    print("=" * 60)
    print("GENERATE SHOT IMAGES")
    print("=" * 60)
    
    # Get API key
    api_key = get_api_key()
    print(f"[OK] API key loaded")
    
    # Load shots
    shots = load_shots(shots_path)
    print(f"[OK] Loaded {len(shots)} shots")
    
    # Ensure output directory exists
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[OK] Output directory: {FRAMES_DIR}")
    
    # Results
    results = []
    successful = 0
    failed = 0
    
    for i, shot in enumerate(shots):
        result = generate_shot_image(
            shot=shot,
            shot_index=i,
            total_shots=len(shots),
            api_key=api_key
        )
        
        results.append(result)
        
        if result["success"]:
            successful += 1
            print(f"  [OK] Shot {result['shot_number']} complete")
        else:
            failed += 1
            print(f"  [FAIL] Shot {shot.get('shot_number', i+1)} failed: {result.get('error')}")
    
    # Save results
    output_data = {
        "shots": results,
        "summary": {
            "total": len(shots),
            "successful": successful,
            "failed": failed
        }
    }
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'=' * 60}")
    print(f"COMPLETE: {successful} successful, {failed} failed")
    print(f"Output saved to: {output_path}")
    print(f"{'=' * 60}")
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate images for shots")
    parser.add_argument("-i", "--input", default="./output/shots.json", help="Input shots JSON")
    parser.add_argument("-o", "--output", default="./output/shot_images.json", help="Output JSON path")
    
    args = parser.parse_args()
    
    try:
        results = generate_all_images(args.input, args.output)
        success_count = sum(1 for r in results if r.get("success"))
        print(f"\nGenerated {success_count}/{len(results)} images successfully")
    except Exception as e:
        print(f"\nERROR: {e}")
        exit(1)
