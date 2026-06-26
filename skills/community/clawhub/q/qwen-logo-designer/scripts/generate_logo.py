#!/usr/bin/env python3
"""
Logo Designer - Generate professional business logos using Alibaba Cloud Bailian API
Uses Qwen-Image-2.0-Pro model for high-quality image generation
"""

import argparse
import hashlib
import json
import os
import sys
import subprocess
import tempfile
from pathlib import Path


# API Configuration
API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
DEFAULT_MODEL = "qwen-image-2.0-pro"

# Default negative prompt for logo quality
DEFAULT_NEGATIVE_PROMPT = "低分辨率，低画质，模糊，噪点，变形，扭曲，构图混乱，文字错误，拼写错误，水印，签名，边框，复杂背景，过度饱和，过度曝光，欠曝，色偏，AI生成感，不专业"


def get_output_dir() -> str:
    """Get output directory from env var or default to workspace."""
    output_dir = os.environ.get("LOGO_OUTPUT_DIR", os.environ.get("WORKSPACE", os.getcwd()))
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def calculate_md5(filepath: str) -> str:
    """Calculate MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def generate_logo(
    prompt: str,
    api_key: str,
    negative_prompt: str = DEFAULT_NEGATIVE_PROMPT,
    size: str = "1024*1024",
    watermark: bool = False,
    prompt_extend: bool = True,
    output: str = None,
) -> dict:
    """
    Generate a logo using Alibaba Cloud Bailian API.
    """
    payload = {
        "model": DEFAULT_MODEL,
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        },
        "parameters": {
            "negative_prompt": negative_prompt,
            "prompt_extend": prompt_extend,
            "watermark": watermark,
            "size": size,
        }
    }

    try:
        # Use curl for reliable connection handling
        result = subprocess.run([
            "curl", "-s", "--max-time", "120",
            API_URL,
            "-H", "Content-Type: application/json",
            "-H", f"Authorization: Bearer {api_key}",
            "-d", json.dumps(payload, ensure_ascii=False)
        ], capture_output=True, text=True, timeout=150)

        if result.returncode != 0:
            return {
                "success": False,
                "error": f"curl failed: {result.stderr}",
                "response": None
            }

        response = json.loads(result.stdout)

        # Extract image URL from response
        image_url = None

        if "output" in response:
            # Format: output.choices[].message.content[].image
            if "choices" in response["output"]:
                for choice in response["output"]["choices"]:
                    if "message" in choice and "content" in choice["message"]:
                        for content in choice["message"]["content"]:
                            if "image" in content:
                                image_url = content["image"]
                                break
            # Legacy format: output.results[].url
            elif "results" in response["output"]:
                for img_result in response["output"]["results"]:
                    if "url" in img_result:
                        image_url = img_result["url"]
                        break

        if image_url:
            # Download and save with MD5 filename
            save_result = download_and_save_with_md5(image_url, output)
            
            return {
                "success": True,
                "image_url": image_url,
                "saved_path": save_result.get("path"),
                "md5": save_result.get("md5"),
                "response": response
            }

        if "code" in response and "message" in response:
            return {
                "success": False,
                "error": f"API Error {response['code']}: {response['message']}",
                "response": response
            }

        return {
            "success": False,
            "error": "No image URL in response",
            "response": response
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Request timeout (120s)",
            "response": None
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Invalid JSON response: {e}",
            "response": result.stdout if 'result' in dir() else None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response": None
        }


def download_and_save_with_md5(url: str, output_path: str = None) -> dict:
    """
    Download image from URL and save with MD5 filename.
    Sets proper permissions (644 for files, 755 for dirs) for nginx access.
    """
    output_dir = get_output_dir()
    
    # Download to temp file first
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        # Download using curl
        result = subprocess.run([
            "curl", "-s", "--max-time", "60",
            "-o", tmp_path,
            url
        ], capture_output=True, timeout=90)
        
        if result.returncode != 0:
            return {"success": False, "error": f"curl download failed (code {result.returncode}): {result.stderr}"}
        
        # Check if file was downloaded
        if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) == 0:
            return {"success": False, "error": "Downloaded file is empty or missing"}
        
        # Calculate MD5
        md5_hash = calculate_md5(tmp_path)
        
        # Determine final output path
        if output_path:
            final_path = output_path
        else:
            final_path = os.path.join(output_dir, f"{md5_hash}.png")
        
        # Ensure directory exists
        dir_path = os.path.dirname(final_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        else:
            dir_path = output_dir
        
        # If file already exists with same MD5, just remove temp
        if os.path.exists(final_path):
            os.remove(tmp_path)
            return {"success": True, "path": final_path, "md5": md5_hash, "existed": True}
        
        # Move temp to final
        os.rename(tmp_path, final_path)
        
        # Set file permissions for nginx access (644: rw-r--r--)
        os.chmod(final_path, 0o644)
        
        # Ensure directory is accessible (755: rwxr-xr-x)
        os.chmod(dir_path, 0o755)
        
        return {"success": True, "path": final_path, "md5": md5_hash, "existed": False}
        
    except Exception as e:
        # Cleanup temp file on error
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="Generate professional business logos using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  DASHSCOPE_API_KEY  DashScope API key (required)
  LOGO_OUTPUT_DIR    Output directory for generated logos (default: current directory)
  WORKSPACE          Fallback output directory if LOGO_OUTPUT_DIR not set

Examples:
  # Basic usage (auto-saves to LOGO_OUTPUT_DIR with MD5 filename)
  export DASHSCOPE_API_KEY="your-key"
  export LOGO_OUTPUT_DIR="~/logos"
  python generate_logo.py --prompt "Modern minimalist tech logo, blue gradient"
  
  # Custom size and no watermark
  python generate_logo.py -p "Vintage coffee shop logo" -s "2048*2048" --no-watermark
  
  # Save to specific file
  python generate_logo.py -p "Restaurant logo" -o mylogo.png
  
  # JSON output for scripting
  python generate_logo.py -p "Tech startup logo" --json
        """
    )

    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Logo design description"
    )
    parser.add_argument(
        "--api-key", "-k",
        required=False,
        default=os.environ.get("DASHSCOPE_API_KEY"),
        help="DashScope API key (or set DASHSCOPE_API_KEY env var)"
    )
    parser.add_argument(
        "--negative-prompt", "-n",
        default=DEFAULT_NEGATIVE_PROMPT,
        help="Negative prompt to avoid unwanted elements"
    )
    parser.add_argument(
        "--size", "-s",
        default="1024*1024",
        choices=["512*512", "720*720", "1024*1024", "1280*1280", "2048*2048"],
        help="Output image size (default: 1024*1024)"
    )
    parser.add_argument(
        "--no-watermark",
        action="store_true",
        help="Remove watermark from generated image"
    )
    parser.add_argument(
        "--no-prompt-extend",
        action="store_true",
        help="Disable automatic prompt extension"
    )
    parser.add_argument(
        "--output", "-o",
        help="Local path to save the generated image (default: LOGO_OUTPUT_DIR/MD5.png)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON response"
    )

    args = parser.parse_args()

    if not args.api_key:
        print("❌ Error: API key required.")
        print("   Set DASHSCOPE_API_KEY environment variable")
        print("   Or use --api-key / -k option")
        sys.exit(1)

    output_dir = get_output_dir()
    
    print(f"🎨 Generating logo...")
    print(f"   Prompt: {args.prompt[:60]}..." if len(args.prompt) > 60 else f"   Prompt: {args.prompt}")
    print(f"   Size: {args.size}")
    print(f"   Output dir: {output_dir}")
    print()

    result = generate_logo(
        prompt=args.prompt,
        api_key=args.api_key,
        negative_prompt=args.negative_prompt,
        size=args.size,
        watermark=not args.no_watermark,
        prompt_extend=not args.no_prompt_extend,
        output=args.output,
    )

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result["success"]:
            print(f"✅ Logo generated successfully!")
            print(f"🖼️  Image URL: {result['image_url']}")
            if result.get("saved_path"):
                existed = result.get("existed", False)
                if existed:
                    print(f"📁 File already exists: {result['saved_path']}")
                else:
                    print(f"📁 Saved to: {result['saved_path']}")
                print(f"🔑 MD5: {result.get('md5', 'N/A')}")
            print(f"\n💡 Tip: URLs expire in ~2 hours. Images are auto-saved with MD5 filenames.")
        else:
            print(f"❌ Error: {result['error']}")
            if result.get("response"):
                print(f"   Response: {json.dumps(result['response'], indent=4, ensure_ascii=False)[:200]}")
            sys.exit(1)


if __name__ == "__main__":
    main()
