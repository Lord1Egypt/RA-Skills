#!/usr/bin/env python3
"""
Volcengine Jimeng Video Generation 3.0 Pro Script
API Flow: Submit task → Poll for results
Docs: https://www.volcengine.com/docs/85621/1777001
"""

import requests
import os
import sys
import json
import argparse
import time
from typing import Optional, List, Dict, Any
from urllib.parse import urlparse
from pathlib import Path

script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

try:
    from volcengine_signer import VolcengineSigner

    HAS_SIGNER = True
except ImportError:
    HAS_SIGNER = False
    VolcengineSigner = None


class JimengVideoGenerator:
    """Client for Volcengine Jimeng Video Generation 3.0 Pro API"""

    SUBMIT_ACTION = "CVSync2AsyncSubmitTask"
    QUERY_ACTION = "CVSync2AsyncGetResult"
    API_VERSION = "2022-08-31"

    # Video generation req_key options
    # Pro version: jimeng_high_aes (text-to-video Pro)
    # Standard: jimeng_t2v_v30 (text-to-video 3.0)
    # Image-to-video: jimeng_i2v_v30
    REQ_KEYS = {
        "t2v_pro": "jimeng_high_aes",  # Text-to-video Pro (high quality)
        "t2v_720p": "jimeng_t2v_v30",  # Text-to-video 720P
        "t2v_1080p": "jimeng_t2v_v30_1080p",  # Text-to-video 1080P
        "i2v_pro": "jimeng_i2v_pro",  # Image-to-video Pro
        "i2v_720p": "jimeng_i2v_v30",  # Image-to-video 720P
        "i2v_1080p": "jimeng_i2v_v30_1080p",  # Image-to-video 1080P
    }

    # Video duration options (in seconds)
    DURATION_OPTIONS = [4, 5, 6, 8, 10]

    # FPS options
    FPS_OPTIONS = [24, 25, 30]

    # Resolution options
    RESOLUTION_OPTIONS = {
        "720p": (1280, 720),
        "1080p": (1920, 1080),
        "pro": (1920, 1080),  # Pro uses 1080p base
    }

    def __init__(
        self,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
    ):
        self.access_key = access_key or os.environ.get("VOLC_ACCESSKEY")
        self.secret_key = secret_key or os.environ.get("VOLC_SECRETKEY")

        if not self.access_key or not self.secret_key:
            raise ValueError(
                "Access Key and Secret Key required. "
                "Set VOLC_ACCESSKEY and VOLC_SECRETKEY environment variables."
            )

        if not HAS_SIGNER:
            raise ImportError(
                "volcengine_signer module not found. "
                "Make sure volcengine_signer.py is in the same directory."
            )

        self.service = "cv"
        self.region = "cn-north-1"
        self.base_url = os.environ.get(
            "JIMENG_VIDEO_API_URL", "https://visual.volcengineapi.com"
        )
        self.timeout = int(os.environ.get("JIMENG_VIDEO_API_TIMEOUT", "300"))
        self.poll_interval = int(os.environ.get("JIMENG_VIDEO_POLL_INTERVAL", "5"))
        self.max_poll_attempts = int(
            os.environ.get("JIMENG_VIDEO_MAX_POLL_ATTEMPTS", "120")
        )

    def _make_request(
        self,
        action: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")

        parsed_url = urlparse(self.base_url)
        path = parsed_url.path or "/"

        headers = {
            "Content-Type": "application/json",
            "Host": parsed_url.netloc,
        }

        if VolcengineSigner is None:
            raise RuntimeError("VolcengineSigner not available")

        assert self.access_key is not None
        assert self.secret_key is not None

        query_params = {
            "Action": action,
            "Version": self.API_VERSION,
        }

        headers = VolcengineSigner.sign_request(
            method="POST",
            url=path,
            headers=headers,
            body=body,
            access_key=self.access_key,
            secret_key=self.secret_key,
            service=self.service,
            region=self.region,
            query_params=query_params,
        )

        try:
            response = requests.post(
                self.base_url,
                params=query_params,
                data=body,
                headers=headers,
                timeout=self.timeout,
            )
            result = response.json()
            return result
        except requests.exceptions.Timeout:
            return {
                "code": "timeout",
                "message": f"Request timed out after {self.timeout} seconds",
            }
        except requests.exceptions.RequestException as e:
            return {
                "code": "request_failed",
                "message": str(e),
            }
        except json.JSONDecodeError as e:
            return {
                "code": "json_error",
                "message": f"Failed to parse response: {e}",
            }

    def submit_task(
        self,
        prompt: str,
        req_key: str = "jimeng_high_aes",
        video_duration: int = 5,
        fps: int = 24,
        input_image: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Submit a video generation task"""
        payload: Dict[str, Any] = {
            "req_key": req_key,
            "prompt": prompt,
        }

        # Video duration (default 5 seconds)
        if video_duration in self.DURATION_OPTIONS:
            payload["video_duration"] = video_duration
        else:
            payload["video_duration"] = 5

        # FPS setting
        if fps in self.FPS_OPTIONS:
            payload["fps"] = fps

        # Input image for image-to-video
        if input_image:
            payload["image_url"] = input_image

        # Random seed for reproducibility
        if seed is not None:
            payload["seed"] = seed

        result = self._make_request(self.SUBMIT_ACTION, payload)

        if result.get("code") != 10000:
            return {
                "success": False,
                "error": {
                    "code": result.get("code", "unknown"),
                    "message": result.get("message", str(result)),
                },
            }

        return {
            "success": True,
            "task_id": result.get("data", {}).get("task_id"),
        }

    def query_task(
        self,
        task_id: str,
        req_key: str = "jimeng_high_aes",
    ) -> Dict[str, Any]:
        """Query the status of a video generation task"""
        payload: Dict[str, Any] = {
            "req_key": req_key,
            "task_id": task_id,
        }

        return self._make_request(self.QUERY_ACTION, payload)

    def generate(
        self,
        prompt: str,
        mode: str = "t2v_720p",
        video_duration: int = 5,
        fps: int = 24,
        input_image: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Generate a video from text or image"""
        # Determine req_key based on mode
        req_key = self.REQ_KEYS.get(mode, "jimeng_high_aes")

        submit_result = self.submit_task(
            prompt=prompt,
            req_key=req_key,
            video_duration=video_duration,
            fps=fps,
            input_image=input_image,
            seed=seed,
        )

        if not submit_result.get("success"):
            return submit_result

        task_id = submit_result.get("task_id")
        if not task_id:
            return {
                "success": False,
                "error": {
                    "code": "no_task_id",
                    "message": "No task_id returned from submit",
                },
            }
        print(f"Task submitted: {task_id}", file=sys.stderr)

        for attempt in range(self.max_poll_attempts):
            result = self.query_task(task_id, req_key=req_key)

            if result.get("code") != 10000:
                return {
                    "success": False,
                    "error": {
                        "code": result.get("code", "unknown"),
                        "message": result.get("message", str(result)),
                    },
                    "task_id": task_id,
                }

            status = result.get("data", {}).get("status", "")

            if status == "done":
                video_url = result.get("data", {}).get("video_url")
                return {
                    "success": True,
                    "task_id": task_id,
                    "video_url": video_url,
                    "data": result.get("data", {}),
                }
            elif status in ["not_found", "expired"]:
                return {
                    "success": False,
                    "error": {
                        "code": status,
                        "message": f"Task {status}",
                    },
                    "task_id": task_id,
                }

            # Show progress
            if attempt % 12 == 0:  # Every minute (at 5s intervals)
                elapsed = attempt * self.poll_interval
                print(f"Still processing... ({elapsed}s elapsed)", file=sys.stderr)

            time.sleep(self.poll_interval)

        return {
            "success": False,
            "error": {
                "code": "timeout",
                "message": f"Polling timed out after {self.max_poll_attempts} attempts",
            },
            "task_id": task_id,
        }

    def download_video(self, url: str, output_path: str) -> bool:
        """Download generated video to local file"""
        try:
            response = requests.get(url, timeout=120, stream=True)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return True
        except Exception as e:
            print(f"Failed to download video: {e}", file=sys.stderr)
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate videos using Volcengine Jimeng 3.0 Pro API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text-to-video (Pro quality)
  %(prog)s "一只可爱的柴犬在樱花树下奔跑，阳光温暖，治愈系风格"

  # Specify duration and FPS
  %(prog)s "A serene lake at sunset" --duration 10 --fps 30

  # Image-to-video
  %(prog)s "The character starts walking forward" --image https://example.com/character.png

  # Use 720P mode
  %(prog)s "A beautiful sunset" --mode t2v_720p

  # Save to file
  %(prog)s "Mountain landscape timelapse" --output video.mp4

Modes:
  t2v_pro     - Text-to-video Pro (highest quality)
  t2v_720p    - Text-to-video 720P (default)
  t2v_1080p   - Text-to-video 1080P
  i2v_pro     - Image-to-video Pro
  i2v_720p    - Image-to-video 720P
  i2v_1080p   - Image-to-video 1080P

Environment Variables:
  VOLC_ACCESSKEY           Volcengine Access Key ID (required)
  VOLC_SECRETKEY           Volcengine Secret Access Key (required)
  JIMENG_VIDEO_API_URL     API endpoint (default: https://visual.volcengineapi.com)
  JIMENG_VIDEO_API_TIMEOUT Request timeout seconds (default: 300)
  JIMENG_VIDEO_POLL_INTERVAL Polling interval seconds (default: 5)
  JIMENG_VIDEO_MAX_POLL_ATTEMPTS Max polling attempts (default: 120)
        """,
    )

    parser.add_argument("prompt", help="Text prompt for video generation")
    parser.add_argument(
        "--mode",
        default="t2v_720p",
        choices=list(JimengVideoGenerator.REQ_KEYS.keys()),
        help="Generation mode (default: default)",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=5,
        choices=JimengVideoGenerator.DURATION_OPTIONS,
        help="Video duration in seconds (default: 5)",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=24,
        choices=JimengVideoGenerator.FPS_OPTIONS,
        help="Frames per second (default: 24)",
    )
    parser.add_argument(
        "--image",
        help="Input image URL for image-to-video generation",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducibility",
    )
    parser.add_argument("--output", "-o", help="Download video to specified file path")
    parser.add_argument("--json", action="store_true", help="Output raw JSON response")

    args = parser.parse_args()

    try:
        client = JimengVideoGenerator()

        print(f"Generating video with prompt: {args.prompt}", file=sys.stderr)
        print(
            f"Mode: {args.mode}, Duration: {args.duration}s, FPS: {args.fps}",
            file=sys.stderr,
        )

        result = client.generate(
            prompt=args.prompt,
            mode=args.mode,
            video_duration=args.duration,
            fps=args.fps,
            input_image=args.image,
            seed=args.seed,
        )

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return

        if result.get("success"):
            video_url = result.get("video_url")
            task_id = result.get("task_id")

            print(f"✓ Generated video [task: {task_id}]")
            if video_url:
                print(f"  URL: {video_url}")

            if args.output and video_url:
                print(f"  Downloading to: {args.output}...", file=sys.stderr)
                if client.download_video(video_url, args.output):
                    print(f"  Saved to: {args.output}")
        else:
            error = result.get("error", {})
            print(
                f"✗ Error [{error.get('code')}]: {error.get('message')}",
                file=sys.stderr,
            )
            sys.exit(1)

    except ValueError as e:
        print(f"✗ Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n✗ Interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
