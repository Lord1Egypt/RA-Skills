# /// script
# dependencies = ["requests"]
# ///
"""Generate an image from text using RunPod P-Image T2I."""

import sys
import time
import argparse
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _utils import init_keys, runsync, get_media_url, save_media

ENDPOINT = "p-image-t2i"
COST_PER_IMAGE = 0.005


def main():
    parser = argparse.ArgumentParser(description="Generate image from text (P-Image T2I)")
    parser.add_argument("--prompt", required=True, help="Text prompt describing the image")
    parser.add_argument("--aspect-ratio", default="1:1", help="Aspect ratio (default: 1:1, e.g. 16:9, 9:16, 4:3)")
    parser.add_argument("--seed", type=int, default=-1, help="Seed for reproducibility (-1 = random)")
    args = parser.parse_args()

    api_key, _ = init_keys()

    payload = {
        "prompt": args.prompt,
        "aspect_ratio": args.aspect_ratio,
    }
    if args.seed != -1:
        payload["seed"] = args.seed

    print(f"Generating image…\n  prompt: {args.prompt}\n  aspect_ratio: {args.aspect_ratio}")
    t0 = time.time()
    output = runsync(ENDPOINT, payload, api_key)
    elapsed = time.time() - t0

    url = get_media_url(output)
    if not url:
        print(f"Error: no image URL in response: {output}", file=sys.stderr)
        sys.exit(1)

    ts = int(time.time())
    dest = save_media(url, f"image_{ts}.jpg")
    print(f"Saved: {dest}")
    print(f"Time: {elapsed:.1f}s | Cost: ~${COST_PER_IMAGE:.4f}")


if __name__ == "__main__":
    main()
