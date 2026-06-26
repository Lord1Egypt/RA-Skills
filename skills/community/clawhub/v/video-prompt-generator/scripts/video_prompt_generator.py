#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Optional

API_URL = "https://nanophoto.ai/api/sora-2/generate-prompt"
DEFAULT_OPENCLAW_CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
SKILL_NAME = "video-prompt-generator"
ENV_KEY_NAME = "NANOPHOTO_API_KEY"
VALID_MODES = {"textToVideo", "imageToVideo"}
VALID_TECHNIQUES = {
    "montage",
    "long-take",
    "time-lapse",
    "slow-motion",
    "tracking-shot",
    "aerial-view",
    "pov",
    "split-screen",
    "match-cut",
    "fade-transition",
}
VALID_LOCALES = {"en", "zh", "zh-TW", "ja", "ko", "es", "fr", "de", "pt", "ru", "ar"}
DEFAULT_MODEL = "google/gemini-3-flash-preview"
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"


def fail(message: str, code: int = 1) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


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


def build_payload(args: argparse.Namespace) -> dict:
    if not args.topic or not args.topic.strip():
        fail("--topic is required.")
    topic = args.topic.strip()
    if len(topic) > 500:
        fail("--topic must be 500 characters or fewer.")

    payload = {
        "topic": topic,
        "mode": args.mode,
        "technique": args.technique,
        "duration": args.duration,
        "model": args.model,
        "locale": args.locale,
    }

    if args.mode == "imageToVideo":
        if not args.image_url:
            fail("imageToVideo mode requires at least one --image-url.")
        if len(args.image_url) > 3:
            fail("imageToVideo mode supports at most 3 --image-url values.")
        payload["imageUrls"] = args.image_url

    return payload


def generate_prompt(api_key: str, payload: dict, timeout: int, user_agent: str) -> str:
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": user_agent,
            "Accept": "text/plain, application/json;q=0.9, */*;q=0.8",
            "Origin": "https://nanophoto.ai",
            "Referer": "https://nanophoto.ai/",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        fail(f"HTTP {exc.code}: {body}")
    except urllib.error.URLError as exc:
        fail(f"Request failed: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate professional Sora 2 video prompts from topics.")
    parser.add_argument("--topic", required=True, help="Video topic or scene description (max 500 chars)")
    parser.add_argument("--mode", default="textToVideo", choices=sorted(VALID_MODES), help="Prompt generation mode")
    parser.add_argument("--technique", default="montage", choices=sorted(VALID_TECHNIQUES), help="Video technique")
    parser.add_argument("--duration", type=int, default=10, choices=[10, 15], help="Video duration in seconds")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Prompt generation model")
    parser.add_argument("--locale", default="en", choices=sorted(VALID_LOCALES), help="Output language locale")
    parser.add_argument("--image-url", action="append", default=[], help="Public image URL for imageToVideo mode; may be passed up to 3 times")
    parser.add_argument("--api-key", help="NanoPhoto API key")
    parser.add_argument("--timeout", type=int, default=120, help="Request timeout in seconds (default: 120)")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="HTTP User-Agent override")
    args = parser.parse_args()

    api_key = resolve_api_key(args.api_key)
    if not api_key:
        fail("Missing API key. Pass --api-key, set NANOPHOTO_API_KEY, or configure ~/.openclaw/openclaw.json skills.entries.video-prompt-generator.env.NANOPHOTO_API_KEY.")

    payload = build_payload(args)
    prompt = generate_prompt(api_key, payload, args.timeout, args.user_agent)
    print(prompt)


if __name__ == "__main__":
    main()
