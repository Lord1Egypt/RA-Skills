#!/usr/bin/env python3
"""Generate cover image for EPUB using SkillBoss API Hub."""

import argparse
import os
import requests
from pathlib import Path

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
API_BASE = "https://api.heybossai.com/v1"


def pilot(body: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()


def generate_cover(prompt: str, output_path: str) -> str:
    """Generate cover image via SkillBoss API Hub and save to file."""
    result = pilot({
        "type": "image",
        "inputs": {"prompt": prompt},
        "prefer": "quality"
    })
    image_url = result["result"]["image_url"]

    img_resp = requests.get(image_url, timeout=60)
    img_resp.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(img_resp.content)

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate EPUB cover via SkillBoss API Hub")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--output", required=True, help="Output image path (.png)")
    args = parser.parse_args()

    print(f"Generating cover image...")
    path = generate_cover(args.prompt, args.output)
    print(f"Cover saved to {path}")
    return 0


if __name__ == "__main__":
    exit(main())
