#!/usr/bin/env python3
"""
Create a Vidau video generation task. Reads API key from env VIDAU_API_KEY or OpenClaw config.
Prints API JSON to stdout for the agent to parse data.taskUUID.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import api_client
from urllib.error import URLError

API_BASE = "https://api.superaiglobal.com/v1"
CREATE_TASK_URL = f"{API_BASE}/video/createTask"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a Vidau video task. Requires env VIDAU_API_KEY."
    )
    parser.add_argument("--prompt", required=True, help="Text description, up to 2000 chars")
    parser.add_argument(
        "--model",
        default="veo@3:normal",
        help="Model ID, default veo@3:normal",
    )
    parser.add_argument("--negative-prompt", default="", help="Negative prompt, up to 2000 chars")
    parser.add_argument("--image-url", default="", help="First-frame image URL")
    parser.add_argument("--last-image-url", default="", help="Last-frame image URL")
    parser.add_argument(
        "--ref-image-urls",
        nargs="*",
        default=None,
        help="Reference image URLs, space-separated",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=None,
        help="Video duration in seconds",
    )
    def _bool_arg(s: str) -> bool:
        return s.lower() in ("true", "1", "yes")

    parser.add_argument(
        "--generate-audio",
        type=_bool_arg,
        default=False,
        help="Generate audio; true/false",
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--resolution", required=True, help="Resolution, e.g. 720p")
    parser.add_argument("--ratio", default="", help="Aspect ratio, e.g. 16:9")
    parser.add_argument("--task-uuid", default="", help="Optional task UUID")
    args = parser.parse_args()

    api_key = api_client.get_api_key()
    if not api_key:
        print(
            "Error: VIDAU_API_KEY is not set. Register at https://www.superaiglobal.com/ to get an API key, then configure apiKey or env.VIDAU_API_KEY in OpenClaw skills.entries.vidau.",
            file=sys.stderr,
        )
        sys.exit(1)

    body = {
        "model": args.model,
        "prompt": args.prompt,
    }
    if args.negative_prompt:
        body["negative_prompt"] = args.negative_prompt
    if args.image_url:
        body["image_url"] = args.image_url
    if args.last_image_url:
        body["last_image_url"] = args.last_image_url
    if args.ref_image_urls:
        body["ref_image_urls"] = args.ref_image_urls
    if args.duration is not None:
        body["duration"] = args.duration
    if args.generate_audio:
        body["generate_audio"] = True
    if args.seed is not None:
        body["seed"] = args.seed
    body["resolution"] = args.resolution
    if args.ratio:
        body["ratio"] = args.ratio
    if args.task_uuid:
        body["taskUUID"] = args.task_uuid

    data = json.dumps(body).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    try:
        raw, _ = api_client.api_request(
            "POST", CREATE_TASK_URL, headers=headers, data=data, timeout=60
        )
        raw_str = raw.decode("utf-8")
        print(raw_str)
        out = json.loads(raw_str)
        if out.get("code") != "200":
            msg = out.get("message", "")
            print(
                f"API returned non-success: code={out.get('code')}, message={msg}",
                file=sys.stderr,
            )
            sys.exit(1)
    except api_client.APIError as e:
        try:
            err_json = json.loads(e.body)
            msg = err_json.get("message", e.body)
        except Exception:
            msg = e.body or str(e)
        print(f"HTTP {e.code}: {msg}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Request failed: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Response is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
