#!/usr/bin/env python3
"""
Volcengine Jimeng (Seedream) 4.0 Image Generation Script
API Flow: Submit task → Poll for results
Docs: https://www.volcengine.com/docs/85621/1817045
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


class JimengImageGenerator:
    """Client for Volcengine Jimeng (Seedream) 4.0 API"""

    SUBMIT_ACTION = "CVSync2AsyncSubmitTask"
    QUERY_ACTION = "CVSync2AsyncGetResult"
    API_VERSION = "2022-08-31"
    REQ_KEY = "jimeng_t2i_v40"

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
            "JIMENG_API_URL", "https://visual.volcengineapi.com"
        )
        self.timeout = int(os.environ.get("JIMENG_API_TIMEOUT", "120"))
        self.poll_interval = int(os.environ.get("JIMENG_POLL_INTERVAL", "2"))
        self.max_poll_attempts = int(os.environ.get("JIMENG_MAX_POLL_ATTEMPTS", "60"))

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
        size: str = "2K",
        images: Optional[List[str]] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        scale: float = 0.5,
        force_single: bool = False,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "req_key": self.REQ_KEY,
            "prompt": prompt,
            "scale": scale,
        }

        if images:
            payload["image_urls"] = images

        if width and height:
            payload["width"] = width
            payload["height"] = height
        elif size:
            size_map = {"1K": 1048576, "2K": 4194304, "4K": 16777216}
            if size in size_map:
                payload["size"] = size_map[size]
            elif "x" in size.lower():
                w, h = size.lower().split("x")
                payload["width"] = int(w)
                payload["height"] = int(h)

        if force_single:
            payload["force_single"] = True

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
        return_url: bool = True,
        watermark: bool = False,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "req_key": self.REQ_KEY,
            "task_id": task_id,
        }

        req_json: Dict[str, Any] = {"return_url": return_url}
        if watermark:
            req_json["logo_info"] = {
                "add_logo": True,
                "position": 0,
                "language": 0,
                "opacity": 1,
            }
        payload["req_json"] = json.dumps(req_json)

        return self._make_request(self.QUERY_ACTION, payload)

    def generate(
        self,
        prompt: str,
        size: str = "2K",
        images: Optional[List[str]] = None,
        watermark: bool = False,
        width: Optional[int] = None,
        height: Optional[int] = None,
        scale: float = 0.5,
        force_single: bool = False,
    ) -> Dict[str, Any]:
        submit_result = self.submit_task(
            prompt=prompt,
            size=size,
            images=images,
            width=width,
            height=height,
            scale=scale,
            force_single=force_single,
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
            result = self.query_task(task_id, return_url=True, watermark=watermark)

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
                image_urls = result.get("data", {}).get("image_urls", [])
                return {
                    "success": True,
                    "task_id": task_id,
                    "images": image_urls,
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

            time.sleep(self.poll_interval)

        return {
            "success": False,
            "error": {
                "code": "timeout",
                "message": f"Polling timed out after {self.max_poll_attempts} attempts",
            },
            "task_id": task_id,
        }

    def download_image(self, url: str, output_path: str) -> bool:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                f.write(response.content)

            return True
        except Exception as e:
            print(f"Failed to download image: {e}", file=sys.stderr)
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Volcengine Jimeng (Seedream) 4.0 API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text-to-image
  %(prog)s "一只白色暹罗猫，坐在窗台上，阳光照进来" --size 2K

  # Image-to-image editing
  %(prog)s "Change to watercolor style" --images https://example.com/input.jpg

  # Specify exact dimensions
  %(prog)s "Beautiful landscape" --width 2048 --height 1440

  # Save to file
  %(prog)s "Mountain sunset" --output sunset.jpg

Environment Variables:
  VOLC_ACCESSKEY       Volcengine Access Key ID (required)
  VOLC_SECRETKEY       Volcengine Secret Access Key (required)
  JIMENG_API_URL       API endpoint (default: https://visual.volcengineapi.com)
  JIMENG_API_TIMEOUT   Request timeout in seconds (default: 120)
  JIMENG_POLL_INTERVAL Polling interval in seconds (default: 2)
  JIMENG_MAX_POLL_ATTEMPTS Max polling attempts (default: 60)
        """,
    )

    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument(
        "--size",
        default="2K",
        help="Image size: 1K, 2K, 4K or exact dimensions like 2048x2048 (default: 2K)",
    )
    parser.add_argument(
        "--width",
        type=int,
        help="Exact image width (requires --height)",
    )
    parser.add_argument(
        "--height",
        type=int,
        help="Exact image height (requires --width)",
    )
    parser.add_argument(
        "--images",
        nargs="+",
        help="Input image URLs for image-to-image editing",
    )
    parser.add_argument(
        "--watermark", action="store_true", help='Add "AI生成" watermark'
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=0.5,
        help="Text influence scale 0-1 (default: 0.5)",
    )
    parser.add_argument(
        "--force-single",
        action="store_true",
        help="Force single image output",
    )
    parser.add_argument("--output", "-o", help="Download image to specified file path")
    parser.add_argument("--json", action="store_true", help="Output raw JSON response")

    args = parser.parse_args()

    try:
        client = JimengImageGenerator()

        print(f"Generating image with prompt: {args.prompt}", file=sys.stderr)

        result = client.generate(
            prompt=args.prompt,
            size=args.size,
            images=args.images,
            watermark=args.watermark,
            width=args.width,
            height=args.height,
            scale=args.scale,
            force_single=args.force_single,
        )

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return

        if result.get("success"):
            images = result.get("images", [])
            task_id = result.get("task_id")

            print(f"✓ Generated {len(images)} image(s) [task: {task_id}]")
            for i, url in enumerate(images, 1):
                print(f"  [{i}] {url}")

                if args.output:
                    output_path = (
                        args.output if len(images) == 1 else f"{args.output}.{i}.png"
                    )
                    if client.download_image(url, output_path):
                        print(f"      Saved to: {output_path}")
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
