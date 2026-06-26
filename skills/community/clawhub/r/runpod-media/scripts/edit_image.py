# /// script
# dependencies = ["requests"]
# ///
"""Edit images with text instructions using RunPod P-Image Edit."""

import sys
import time
import argparse
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _utils import init_keys, runsync, ensure_url, get_media_url, save_media

ENDPOINT = "p-image-edit"
COST_PER_IMAGE = 0.005


def main():
    parser = argparse.ArgumentParser(description="Edit images with text (P-Image Edit, 1–5 input images)")
    parser.add_argument("--images", required=True, nargs="+", metavar="PATH_OR_URL",
                        help="1–5 input image paths or URLs")
    parser.add_argument("--prompt", required=True, help="Edit instruction / description")
    parser.add_argument("--aspect-ratio", default="1:1", help="Output aspect ratio (default: 1:1)")
    parser.add_argument("--seed", type=int, default=-1, help="Seed (-1 = random)")
    args = parser.parse_args()

    if len(args.images) > 5:
        parser.error("Maximum 5 input images supported")

    api_key, imgbb_key = init_keys()

    print(f"Uploading/resolving {len(args.images)} image(s)…")
    image_urls = [ensure_url(img, imgbb_key) for img in args.images]

    payload = {
        "prompt": args.prompt,
        "images": image_urls,
        "aspect_ratio": args.aspect_ratio,
    }
    if args.seed != -1:
        payload["seed"] = args.seed

    print(f"Editing image…\n  prompt: {args.prompt}\n  inputs: {len(image_urls)}")
    t0 = time.time()
    output = runsync(ENDPOINT, payload, api_key)
    elapsed = time.time() - t0

    url = get_media_url(output)
    if not url:
        print(f"Error: no image URL in response: {output}", file=sys.stderr)
        sys.exit(1)

    ts = int(time.time())
    dest = save_media(url, f"edit_{ts}.jpg")
    print(f"Saved: {dest}")
    print(f"Time: {elapsed:.1f}s | Cost: ~${COST_PER_IMAGE:.4f}")


if __name__ == "__main__":
    main()
