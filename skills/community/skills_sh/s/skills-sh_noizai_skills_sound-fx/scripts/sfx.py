#!/usr/bin/env python3
"""Generate sound effects from text prompts using the Noiz API.

Usage:
    python3 sfx.py "a cat knocking things off a table"
    python3 sfx.py "heavy rain" --duration 10 -o rain.wav
    python3 sfx.py config --set-api-key YOUR_KEY
"""
import argparse
import os
import sys
from pathlib import Path

NOIZ_KEY_FILE = Path.home() / ".config" / "noiz" / "api_key"
API_BASE = "https://noiz.ai/v1"


def load_api_key(override: str = None) -> str:
    if override:
        return override.strip()
    env = os.environ.get("NOIZ_API_KEY", "").strip()
    if env:
        return env
    if NOIZ_KEY_FILE.exists():
        key = NOIZ_KEY_FILE.read_text(encoding="utf-8").strip()
        if key:
            return key
    return ""


def save_api_key(key: str) -> None:
    NOIZ_KEY_FILE.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    NOIZ_KEY_FILE.write_text(key.strip(), encoding="utf-8")
    os.chmod(str(NOIZ_KEY_FILE), 0o600)
    print(f"[config] API key saved to {NOIZ_KEY_FILE}")


def generate(prompt: str, duration: float = None, output_format: str = "wav",
             api_key: str = None, out_path: Path = None) -> Path:
    try:
        import requests
    except ImportError:
        print("error: 'requests' package is required. Run: pip install requests", file=sys.stderr)
        sys.exit(1)

    key = load_api_key(api_key)
    if not key:
        print(
            "error: No API key found.\n"
            "  Set one with: python3 sfx.py config --set-api-key YOUR_KEY\n"
            "  Or: export NOIZ_API_KEY=YOUR_KEY\n"
            "  Get a key at: https://developers.noiz.ai/api-keys",
            file=sys.stderr,
        )
        sys.exit(1)

    data = {"prompt": prompt, "output_format": output_format}
    if duration is not None:
        if not (1 <= duration <= 30):
            print("error: duration must be between 1 and 30 seconds", file=sys.stderr)
            sys.exit(1)
        data["duration"] = str(int(duration))

    resp = requests.post(
        f"{API_BASE}/text-to-sound",
        headers={"Authorization": key},
        data=data,
        timeout=120,
    )

    if resp.status_code != 200:
        print(f"error: API returned HTTP {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)

    body = resp.json()
    code = body.get("code", -1)
    if code == 429:
        print("error: Rate limit exceeded. Please wait and retry.", file=sys.stderr)
        sys.exit(1)
    if code == 401:
        print("error: Invalid or missing API key.", file=sys.stderr)
        sys.exit(1)
    if code != 0:
        print(f"error: API error code={code} message={body.get('message', '')}", file=sys.stderr)
        sys.exit(1)

    results = body.get("data", {}).get("results", [])
    if not results:
        print("error: No results returned from API", file=sys.stderr)
        sys.exit(1)

    result = results[0]
    file_url = result.get("file_url")
    err = result.get("error")
    if err or not file_url:
        print(f"error: Generation failed: {err or 'no file_url'}", file=sys.stderr)
        sys.exit(1)

    # Download the audio
    audio_resp = requests.get(file_url, timeout=60)
    if audio_resp.status_code != 200:
        print(f"error: Failed to download audio: HTTP {audio_resp.status_code}", file=sys.stderr)
        sys.exit(1)

    if out_path is None:
        out_path = Path(f"output.{output_format}")

    out_path.write_bytes(audio_resp.content)

    size_kb = len(audio_resp.content) / 1024
    print(f"✓ Saved to {out_path} ({size_kb:.0f} KB)")
    print(f"  URL: {file_url}")
    return out_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate sound effects from text using Noiz API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 sfx.py "a cat knocking things off a table"
  python3 sfx.py "heavy rain on a tin roof" --duration 10 -o rain.wav
  python3 sfx.py "cartoon character getting spanked, exaggerated squeaky yelp" -d 3
  python3 sfx.py config --set-api-key YOUR_KEY
        """,
    )

    subparsers = parser.add_subparsers(dest="subcommand")

    # config subcommand
    cfg = subparsers.add_parser("config", help="Configure API key")
    cfg.add_argument("--set-api-key", metavar="KEY", help="Save API key to ~/.config/noiz/api_key")

    # generate (default, no subcommand)
    parser.add_argument("prompt", nargs="?", help="Text description of the sound to generate")
    parser.add_argument("--duration", "-d", type=float, default=None,
                        help="Duration in seconds (1-30). Omit to let the model decide.")
    parser.add_argument("--format", "-f", dest="fmt", default="wav",
                        choices=["wav", "mp3", "flac"],
                        help="Output audio format (default: wav)")
    parser.add_argument("--output", "-o", default=None,
                        help="Output file path (default: output.<format>)")
    parser.add_argument("--api-key", default=None, help="Noiz API key (overrides stored key)")

    args = parser.parse_args()

    if args.subcommand == "config":
        if args.set_api_key:
            save_api_key(args.set_api_key)
        else:
            cfg.print_help()
        return

    if not args.prompt:
        parser.print_help()
        sys.exit(1)

    out_path = Path(args.output) if args.output else Path(f"output.{args.fmt}")
    generate(
        prompt=args.prompt,
        duration=args.duration,
        output_format=args.fmt,
        api_key=args.api_key,
        out_path=out_path,
    )


if __name__ == "__main__":
    main()
