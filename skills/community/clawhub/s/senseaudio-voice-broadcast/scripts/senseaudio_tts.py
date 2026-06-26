#!/usr/bin/env python3
import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


DEFAULT_URL = "https://api.senseaudio.cn/v1/t2a_v2"
DEFAULT_MODEL = "SenseAudio-TTS-1.0"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call SenseAudio TTS and save the result to a local file."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Text to synthesize.")
    group.add_argument("--text-file", help="Path to a UTF-8 text file to synthesize.")
    parser.add_argument("--voice-id", required=True, help="SenseAudio voice_id.")
    parser.add_argument("--output", required=True, help="Output audio file path.")
    parser.add_argument("--api-key", help="SenseAudio API key. Defaults to SENSEAUDIO_API_KEY.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model name.")
    parser.add_argument("--url", default=DEFAULT_URL, help="SenseAudio API URL.")
    return parser.parse_args()


def load_text(args: argparse.Namespace) -> str:
    if args.text is not None:
        return args.text
    with open(args.text_file, "r", encoding="utf-8") as f:
        return f.read().strip()


def build_request(args: argparse.Namespace, text: str) -> urllib.request.Request:
    api_key = args.api_key or os.environ.get("SENSEAUDIO_API_KEY")
    if not api_key:
        raise SystemExit("Missing API key. Set SENSEAUDIO_API_KEY or pass --api-key.")

    payload = {
        "model": args.model,
        "text": text,
        "voice_setting": {"voice_id": args.voice_id},
    }
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    return urllib.request.Request(args.url, data=data, headers=headers, method="POST")


def ensure_parent(path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)


def save_bytes(path: str, data: bytes) -> None:
    ensure_parent(path)
    with open(path, "wb") as f:
        f.write(data)


def maybe_download_url(url: str) -> bytes:
    with urllib.request.urlopen(url) as resp:
        return resp.read()


def extract_audio_bytes(body: bytes, content_type: str) -> bytes:
    if content_type.startswith("audio/") or content_type == "application/octet-stream":
        return body

    payload = json.loads(body.decode("utf-8"))

    encoded_candidates = [
        ("hex", payload.get("audio")),
        ("base64", payload.get("audio_base64")),
        ("hex", payload.get("data", {}).get("audio")),
        ("base64", payload.get("data", {}).get("audio_base64")),
        ("hex", payload.get("result", {}).get("audio")),
        ("base64", payload.get("result", {}).get("audio_base64")),
    ]
    for encoding, item in encoded_candidates:
        if isinstance(item, str) and item:
            if encoding == "hex":
                return bytes.fromhex(item)
            return base64.b64decode(item, validate=True)

    url_candidates = [
        payload.get("audio_url"),
        payload.get("url"),
        payload.get("data", {}).get("audio_url"),
        payload.get("data", {}).get("url"),
        payload.get("result", {}).get("audio_url"),
        payload.get("result", {}).get("url"),
    ]
    for item in url_candidates:
        if isinstance(item, str) and item:
            return maybe_download_url(item)

    raise ValueError(
        "Unable to find audio content in response. "
        "Response body was JSON but no known audio field was present."
    )


def main() -> int:
    args = parse_args()
    text = load_text(args)
    if not text:
        raise SystemExit("Input text is empty.")

    request = build_request(args, text)
    try:
        with urllib.request.urlopen(request) as resp:
            body = resp.read()
            content_type = resp.headers.get_content_type()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        print(f"HTTP {exc.code}: {detail}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        return 1

    try:
        audio_bytes = extract_audio_bytes(body, content_type)
    except Exception as exc:
        print(f"Failed to parse response: {exc}", file=sys.stderr)
        return 1

    save_bytes(args.output, audio_bytes)
    print(os.path.abspath(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
