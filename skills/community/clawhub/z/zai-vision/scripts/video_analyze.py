#!/usr/bin/env python3
"""
Z.AI Video Analysis Script
Analyzes videos using Z.AI's GLM-4.6V vision model
Usage: python3 video_analyze.py <video_path> <prompt> [options]

Note: Video analysis uses vision model with frame extraction. For actual video generation,
use Z.AI's video generation API (cogvideox-3 model).

Options:
    --model <model>          Vision model to use (default: glm-4.6v)
    --max-tokens <number>     Maximum response tokens (default: 2000)
    --temperature <number>     Temperature (default: 0.5)
    --json                    Output as JSON
"""

import sys
import os
import base64
import json
import argparse
from pathlib import Path

# Check if zai-sdk is installed
try:
    from zai import ZaiClient
except ImportError:
    print("❌ zai-sdk not installed. Install with: pip install zai-sdk")
    sys.exit(1)


def encode_video(video_path):
    """
    Encode video to base64 format
    Note: Z.AI vision model processes videos frame by frame. For actual video
    generation/analysis, consider using the video generation API.
    """
    try:
        with open(video_path, 'rb') as video_file:
            video_data = video_file.read()

            # Check file size (Z.AI typically limits to 8MB for vision)
            size_mb = len(video_data) / (1024 * 1024)
            if size_mb > 8:
                print(f"⚠️  Warning: Video is {size_mb:.2f}MB (exceeds 8MB recommended limit)")
                print("   Vision analysis may have limited results for large videos.")
                print("   For full video generation, use Z.AI's video generation API.")

            return base64.b64encode(video_data).decode('utf-8')
    except FileNotFoundError:
        print(f"❌ Video file not found: {video_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error encoding video: {e}")
        sys.exit(1)


def analyze_video(video_path, prompt, model="glm-4.6v", max_tokens=2000, temperature=0.5, json_output=False):
    """
    Analyze a video using Z.AI's vision model

    Note: This uses the vision model which can process videos frame-by-frame.
    For dedicated video generation/transformation, use client.videos.generations()

    Args:
        video_path: Path to the video file
        prompt: Text prompt to send with the video
        model: Model to use (default: glm-4.6v)
        max_tokens: Maximum tokens in response
        temperature: Temperature for generation
        json_output: Return raw JSON response

    Returns:
        Analysis result text or JSON object
    """
    # Get API key from environment or use default
    api_key = os.getenv("ZAI_API_KEY")

    if not api_key:
        print("❌ ZAI_API_KEY environment variable not set")
        print("Set it with: export ZAI_API_KEY='your-api-key'")
        sys.exit(1)

    try:
        # Initialize client
        client = ZaiClient(api_key=api_key)

        # Encode video
        base64_video = encode_video(video_path)

        # Determine MIME type based on file extension
        ext = Path(video_path).suffix.lower()
        mime_types = {
            '.mp4': 'video/mp4',
            '.mov': 'video/quicktime',
            '.m4v': 'video/mp4',
            '.avi': 'video/x-msvideo',
            '.mkv': 'video/x-matroska'
        }
        mime_type = mime_types.get(ext, 'video/mp4')

        # Create multimodal chat request with video
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    'role': 'user',
                    'content': [
                        {'type': 'text', 'text': prompt},
                        {
                            'type': 'image_url',
                            'image_url': {
                                'url': f'data:{mime_type};base64,{base64_video}'
                            }
                        },
                    ],
                }
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        # Extract response
        result = response.choices[0].message.content

        if json_output:
            return {
                "video_path": video_path,
                "prompt": prompt,
                "model": model,
                "response": result
            }

        return result

    except Exception as e:
        print(f"❌ Error analyzing video: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Analyze videos with Z.AI Vision')
    parser.add_argument('video_path', help='Path to video file (MP4/MOV/M4V)')
    parser.add_argument('prompt', help='Text prompt for analysis')
    parser.add_argument('--model', default='glm-4.6v', help='Vision model (default: glm-4.6v)')
    parser.add_argument('--max-tokens', type=int, default=2000, help='Max response tokens (default: 2000)')
    parser.add_argument('--temperature', type=float, default=0.5, help='Temperature (default: 0.5)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    # Validate video path
    if not Path(args.video_path).exists():
        print(f"❌ Video not found: {args.video_path}")
        sys.exit(1)

    # Analyze video
    result = analyze_video(
        video_path=args.video_path,
        prompt=args.prompt,
        model=args.model,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        json_output=args.json
    )

    # Output result
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result)


if __name__ == "__main__":
    main()
