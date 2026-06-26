# /// script
# dependencies = ["requests"]
# ///
"""
Generic RunPod endpoint caller.
Looks up known endpoints in endpoints.json, or accepts any custom endpoint ID.

Usage:
  call_endpoint.py --endpoint nano-banana-pro --input '{"prompt": "a cat"}'
  call_endpoint.py --endpoint nano-banana-pro --prompt "a cat" --image photo.jpg
  call_endpoint.py --list
"""

import sys
import json
import time
import argparse
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _utils import init_keys, runsync, run_async, poll_job, ensure_url, get_media_url, save_media

REGISTRY_PATH = pathlib.Path(__file__).parent / "endpoints.json"


def load_registry() -> dict:
    if not REGISTRY_PATH.exists():
        return {}
    data = json.loads(REGISTRY_PATH.read_text())
    # Flatten all categories into one dict
    flat = {}
    for category in data.values():
        if isinstance(category, dict) and not category.get("_comment"):
            for eid, meta in category.items():
                if isinstance(meta, dict):
                    flat[eid] = meta
    return flat


def list_endpoints(registry: dict):
    print(f"{'ID':<30} {'Type':<8} {'Mode':<6}  Name")
    print("-" * 75)
    by_type = {}
    for eid, meta in registry.items():
        t = meta.get("type", "?")
        by_type.setdefault(t, []).append((eid, meta))
    for t in ["image", "video", "voice", "text"]:
        if t not in by_type:
            continue
        print(f"\n[{t.upper()}]")
        for eid, meta in by_type[t]:
            print(f"  {eid:<28} {meta.get('mode','?'):<6}  {meta.get('name', '')}")
            if meta.get("notes"):
                print(f"  {'':28}       ↳ {meta['notes']}")


def main():
    parser = argparse.ArgumentParser(description="Call any RunPod endpoint by ID")
    parser.add_argument("--endpoint", "-e", help="Endpoint ID (e.g. nano-banana-pro)")
    parser.add_argument("--input", "-i", help="JSON input payload (overrides individual flags)")
    parser.add_argument("--prompt", help="Shortcut: sets input.prompt")
    parser.add_argument("--image", help="Shortcut: sets input.image (local path or URL)")
    parser.add_argument("--audio", help="Shortcut: sets input.audio (local path or URL)")
    parser.add_argument("--text", help="Shortcut: sets input.text (for TTS)")
    parser.add_argument("--duration", type=int, help="Shortcut: sets input.duration")
    parser.add_argument("--aspect-ratio", dest="aspect_ratio", help="Shortcut: sets input.aspect_ratio")
    parser.add_argument("--async-mode", action="store_true", help="Force async even if registry says sync")
    parser.add_argument("--timeout", type=int, default=300, help="Max wait seconds for async jobs (default 300)")
    parser.add_argument("--output-key", help="Override the output key to extract media URL from response")
    parser.add_argument("--list", "-l", action="store_true", help="List all known endpoints and exit")
    args = parser.parse_args()

    registry = load_registry()

    if args.list:
        list_endpoints(registry)
        return

    if not args.endpoint:
        parser.error("--endpoint is required (or use --list to see available endpoints)")

    api_key, imgbb_key = init_keys()

    # Build payload
    if args.input:
        payload = json.loads(args.input)
    else:
        payload = {}
        if args.prompt:
            payload["prompt"] = args.prompt
        if args.text:
            payload["text"] = args.text
        if args.duration:
            payload["duration"] = args.duration
        if args.aspect_ratio:
            payload["aspect_ratio"] = args.aspect_ratio

    # Resolve local files → URLs for image/audio
    if args.image:
        print("Uploading/resolving image…")
        payload["image"] = ensure_url(args.image, imgbb_key)
    if args.audio:
        print("Uploading/resolving audio…")
        payload["audio"] = ensure_url(args.audio, imgbb_key)

    # Look up registry metadata
    meta = registry.get(args.endpoint, {})
    mode = "async" if args.async_mode else meta.get("mode", "async")
    output_key = args.output_key or meta.get("output_key")

    if meta.get("name"):
        print(f"Calling: {meta['name']} ({args.endpoint})")
    else:
        print(f"Calling endpoint: {args.endpoint}")
    print(f"  mode: {mode} | payload keys: {list(payload.keys())}")

    t0 = time.time()

    if mode == "sync":
        output = runsync(args.endpoint, payload, api_key, timeout=args.timeout)
    else:
        job_id = run_async(args.endpoint, payload, api_key)
        print(f"  job_id: {job_id}")
        print("Polling for result…")
        output = poll_job(args.endpoint, job_id, api_key, max_wait=args.timeout)

    elapsed = time.time() - t0

    # Try to extract and save media
    url = None
    if output_key and isinstance(output, dict):
        url = output.get(output_key)
    if not url:
        url = get_media_url(output)

    if url:
        ts = int(time.time())
        # Determine extension from URL or type
        ext = "mp4" if meta.get("type") == "video" else ("mp3" if meta.get("type") == "voice" else "jpg")
        if "." in url.split("?")[0].split("/")[-1]:
            ext = url.split("?")[0].split("/")[-1].split(".")[-1]
        dest = save_media(url, f"{args.endpoint.replace('-','_')}_{ts}.{ext}")
        print(f"Saved: {dest}")
    else:
        print(f"Raw output: {json.dumps(output, indent=2)}")

    print(f"Time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
