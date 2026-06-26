# /// script
# dependencies = ["requests"]
# ///
"""Animate a still image into video using RunPod I2V models."""

import sys
import time
import argparse
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _utils import init_keys, run_async, poll_job, ensure_url, get_media_url, save_media

MODELS = {
    "wan25":   ("wan-2-5",           0.026),   # ~$0.026 per 5s clip
    "kling":   ("kling-v2-1-i2v-pro", 0.45),   # $0.45/5s, $0.90/10s
    "seedance": ("seedance-1-0-pro",  0.12),   # $0.12–$0.36/5s
}


def build_payload(model_key: str, image_url: str, args) -> dict:
    if model_key == "wan25":
        payload = {"image": image_url, "prompt": args.prompt}
        if args.duration:
            payload["duration"] = args.duration
        if args.negative_prompt:
            payload["negative_prompt"] = args.negative_prompt
        return payload

    if model_key == "kling":
        payload = {
            "image": image_url,
            "prompt": args.prompt,
            "duration": args.duration or 5,
            "guidance_scale": 0.5,
            "enable_safety_checker": True,
        }
        if args.negative_prompt:
            payload["negative_prompt"] = args.negative_prompt
        return payload

    if model_key == "seedance":
        payload = {
            "image": image_url,
            "prompt": args.prompt,
            "duration": args.duration or 5,
            "fps": 24,
            "size": "1920x1080",
        }
        return payload

    raise ValueError(f"Unknown model: {model_key}")


def main():
    parser = argparse.ArgumentParser(description="Animate an image to video (I2V)")
    parser.add_argument("--image", required=True, help="Input image path or URL")
    parser.add_argument("--prompt", required=True, help="Motion description prompt")
    parser.add_argument("--model", default="wan25", choices=list(MODELS),
                        help="Model: wan25 (default), kling, seedance")
    parser.add_argument("--duration", type=int, choices=[5, 10], default=None,
                        help="Clip duration in seconds (5 or 10)")
    parser.add_argument("--negative-prompt", default=None, help="Negative prompt (wan25, kling)")
    args = parser.parse_args()

    api_key, imgbb_key = init_keys()
    endpoint_id, base_cost = MODELS[args.model]

    print(f"Uploading/resolving input image…")
    image_url = ensure_url(args.image, imgbb_key)

    payload = build_payload(args.model, image_url, args)
    duration = payload.get("duration", 5)
    cost = base_cost if duration <= 5 else base_cost * 2

    print(f"Starting I2V job…\n  model: {args.model} ({endpoint_id})\n  duration: {duration}s")
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
