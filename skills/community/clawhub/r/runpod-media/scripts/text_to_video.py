# /// script
# dependencies = ["requests"]
# ///
"""Generate video from text using RunPod T2V models."""

import sys
import time
import argparse
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _utils import init_keys, run_async, poll_job, get_media_url, save_media

MODELS = {
    "wan26":    ("wan-2-6-t2v",     0.04),    # ~$0.04/5s clip
    "seedance": ("seedance-1-0-pro", 0.122),  # ~$0.122/5s clip (~$1.22/50s max)
}


def build_payload(model_key: str, args) -> dict:
    if model_key == "wan26":
        payload = {"prompt": args.prompt}
        if args.duration:
            payload["duration"] = args.duration
        if args.size:
            payload["size"] = args.size
        if args.negative_prompt:
            payload["negative_prompt"] = args.negative_prompt
        return payload

    if model_key == "seedance":
        payload = {
            "prompt": args.prompt,
            "duration": args.duration or 5,
            "fps": 24,
            "size": args.size or "1920x1080",
        }
        return payload

    raise ValueError(f"Unknown model: {model_key}")


def main():
    parser = argparse.ArgumentParser(description="Generate video from text (T2V)")
    parser.add_argument("--prompt", required=True, help="Text description of the video")
    parser.add_argument("--model", default="wan26", choices=list(MODELS),
                        help="Model: wan26 (default), seedance")
    parser.add_argument("--duration", type=int, choices=[5, 10, 15], default=None,
                        help="Duration in seconds (5, 10, or 15)")
    parser.add_argument("--size", default=None,
                        help="Resolution, e.g. 1920x1080, 1280x720 (default: model default)")
    parser.add_argument("--negative-prompt", default=None, help="Negative prompt (wan26)")
    args = parser.parse_args()

    api_key, _ = init_keys()
    endpoint_id, base_cost = MODELS[args.model]

    payload = build_payload(args.model, args)
    duration = payload.get("duration", 5)
    cost = base_cost * max(1, duration // 5)

    print(f"Starting T2V job…\n  model: {args.model} ({endpoint_id})\n  prompt: {args.prompt}\n  duration: {duration}s")
    job_id = run_async(endpoint_id, payload, api_key)
    print(f"  job_id: {job_id}")

    t0 = time.time()
    print("Polling for result (this may take 30–120 s)…")
    output = poll_job(endpoint_id, job_id, api_key, max_wait=300)
    elapsed = time.time() - t0

    url = get_media_url(output)
    if not url:
        print(f"Error: no video URL in response: {output}", file=sys.stderr)
        sys.exit(1)

    ts = int(time.time())
    dest = save_media(url, f"video_{args.model}_{ts}.mp4")
    print(f"Saved: {dest}")
    print(f"Time: {elapsed:.1f}s | Cost: ~${cost:.3f}")


if __name__ == "__main__":
    main()
