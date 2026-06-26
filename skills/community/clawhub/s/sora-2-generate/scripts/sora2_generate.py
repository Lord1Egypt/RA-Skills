#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Optional

GENERATE_URL = "https://nanophoto.ai/api/sora-2/generate"
STATUS_URL = "https://nanophoto.ai/api/sora-2/check-status"
VALID_MODES = {"textToVideo", "imageToVideo"}
VALID_MODEL_TIERS = {"sora2", "sora2-pro-standard", "sora2-pro-high"}
VALID_ASPECT_RATIOS = {"portrait", "landscape"}
VALID_DURATIONS = {"10", "15"}
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
DEFAULT_INITIAL_STATUS_DELAY = 120
DEFAULT_STATUS_CHECK_INTERVAL = 20
DEFAULT_MAX_WAIT = 1200
DEFAULT_OPENCLAW_CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
SKILL_NAME = "sora-2-generate"
ENV_KEY_NAME = "NANOPHOTO_API_KEY"


def fail(message: str, code: int = 1) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


def post_json(url: str, api_key: str, payload: dict, timeout: int, user_agent: str) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": user_agent,
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://nanophoto.ai",
            "Referer": "https://nanophoto.ai/",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            text = response.read().decode("utf-8", "replace")
            return json.loads(text)
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", "replace")
        fail(f"HTTP {exc.code}: {error_body}")
    except urllib.error.URLError as exc:
        fail(f"Request failed: {exc}")
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON response: {exc}")


def emit(stage: str, response: dict, json_only: bool) -> None:
    if json_only:
        print(json.dumps(response, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"stage": stage, "response": response}, ensure_ascii=False, indent=2), flush=True)


def load_api_key_from_openclaw_config(config_path: str = DEFAULT_OPENCLAW_CONFIG_PATH) -> Optional[str]:
    try:
        with open(config_path, "r", encoding="utf-8") as fh:
            config = json.load(fh)
    except FileNotFoundError:
        return None
    except (OSError, json.JSONDecodeError):
        return None

    return (
        config.get("skills", {})
        .get("entries", {})
        .get(SKILL_NAME, {})
        .get("env", {})
        .get(ENV_KEY_NAME)
    )


def resolve_api_key(explicit_api_key: Optional[str]) -> Optional[str]:
    return explicit_api_key or os.environ.get(ENV_KEY_NAME) or load_api_key_from_openclaw_config()


def validate_timing(initial_status_delay: int, status_check_interval: int, max_wait: int) -> None:
    if initial_status_delay < 0:
        fail("--initial-status-delay must be >= 0")
    if status_check_interval <= 0:
        fail("--status-check-interval must be > 0")
    if max_wait <= 0:
        fail("--max-wait must be > 0")


def build_generate_payload(args: argparse.Namespace) -> dict:
    payload = {
        "prompt": args.prompt,
        "mode": args.mode,
        "modelTier": args.model_tier,
        "aspectRatio": args.aspect_ratio,
        "videoDuration": args.video_duration,
    }
    if args.mode == "imageToVideo":
        if not args.image_url:
            fail("imageToVideo mode requires at least one --image-url (public URL).")
        payload["imageUrls"] = args.image_url
    return payload


def submit_generation(args: argparse.Namespace, api_key: str) -> dict:
    if not getattr(args, "prompt", None):
        fail("--prompt is required for submission.")
    payload = build_generate_payload(args)
    return post_json(GENERATE_URL, api_key, payload, args.timeout, args.user_agent)


def check_status(task_id: str, api_key: str, timeout: int, user_agent: str) -> dict:
    return post_json(STATUS_URL, api_key, {"taskId": task_id}, timeout, user_agent)


def run_poll_loop(task_id: str, api_key: str, args: argparse.Namespace, json_only: bool = False) -> dict:
    validate_timing(args.initial_status_delay, args.status_check_interval, args.max_wait)
    started = time.time()
    next_delay = args.initial_status_delay
    while True:
        elapsed = time.time() - started
        if elapsed > args.max_wait:
            fail(f"Timed out waiting for completion after {args.max_wait} seconds.")

        sleep_for = min(next_delay, max(args.max_wait - elapsed, 0))
        if sleep_for > 0:
            time.sleep(sleep_for)

        status_resp = check_status(task_id, api_key, args.timeout, args.user_agent)
        emit("progress", status_resp, json_only)
        current = status_resp.get("status")
        if current == "completed":
            return status_resp
        if current == "failed" or status_resp.get("success") is False:
            fail("Generation failed; see status response above.")

        next_delay = args.status_check_interval


def do_submit(args: argparse.Namespace, api_key: str) -> None:
    submit = submit_generation(args, api_key)
    emit("submitted", submit, args.json_only)

    task_id = submit.get("taskId")
    status = submit.get("status")
    if status == "completed":
        return
    if not task_id:
        fail("No taskId returned from generate endpoint.")

    if args.follow:
        run_poll_loop(task_id, api_key, args, args.json_only)


def do_status(args: argparse.Namespace, api_key: str) -> None:
    status_resp = check_status(args.task_id, api_key, args.timeout, args.user_agent)
    emit("status", status_resp, args.json_only)


def add_common_auth_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--api-key", help="NanoPhoto API key")
    parser.add_argument("--timeout", type=int, default=60, help="Per-request timeout in seconds (default: 60)")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="HTTP User-Agent override")


def add_generation_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--prompt", required=True, help="Generation prompt")
    parser.add_argument("--mode", default="textToVideo", choices=sorted(VALID_MODES), help="Generation mode")
    parser.add_argument("--model-tier", default="sora2", choices=sorted(VALID_MODEL_TIERS), help="Model tier")
    parser.add_argument("--aspect-ratio", default="portrait", choices=sorted(VALID_ASPECT_RATIOS), help="Aspect ratio")
    parser.add_argument("--video-duration", default="10", choices=sorted(VALID_DURATIONS), help="Duration in seconds")
    parser.add_argument("--image-url", action="append", default=[], help="Public image URL for imageToVideo mode; may be passed multiple times")


def add_polling_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--initial-status-delay", type=int, default=DEFAULT_INITIAL_STATUS_DELAY, help="Delay before the first status check in seconds (default: 120)")
    parser.add_argument("--status-check-interval", type=int, default=DEFAULT_STATUS_CHECK_INTERVAL, help="Interval between status checks after the first one in seconds (default: 20)")
    parser.add_argument("--max-wait", type=int, default=DEFAULT_MAX_WAIT, help="Maximum total wait time in seconds (default: 1200)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Submit and check NanoPhoto Sora 2 video generation tasks.")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    submit_parser = subparsers.add_parser("submit", help="Submit a generation task")
    add_generation_args(submit_parser)
    add_common_auth_args(submit_parser)
    add_polling_args(submit_parser)
    submit_parser.add_argument("--json-only", action="store_true", help="Print raw JSON responses without wrapper stage objects")
    submit_parser.add_argument("--follow", action="store_true", help="Keep polling in the same process after submission")

    status_parser = subparsers.add_parser("status", help="Check status of an existing task")
    status_parser.add_argument("--task-id", required=True, help="Existing Sora 2 taskId")
    add_common_auth_args(status_parser)
    status_parser.add_argument("--json-only", action="store_true", help="Print raw JSON responses without wrapper stage objects")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    api_key = resolve_api_key(getattr(args, "api_key", None))
    if not api_key:
        fail("Missing API key. Pass --api-key, set NANOPHOTO_API_KEY, or configure ~/.openclaw/openclaw.json skills.entries.sora-2-generate.env.NANOPHOTO_API_KEY.")

    if args.command == "submit":
        do_submit(args, api_key)
        return
    if args.command == "status":
        do_status(args, api_key)
        return

    fail(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
