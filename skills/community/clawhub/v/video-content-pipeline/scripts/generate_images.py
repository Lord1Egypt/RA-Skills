#!/usr/bin/env python3
"""Generate images for free via Pollinations.ai (Flux).

NOTE: each scene prompt is sent over the network to image.pollinations.ai
(a third-party service). Do not send confidential or sensitive prompts."""
import json, os, sys, urllib.request, time

def main():
    if len(sys.argv) < 3:
        print("Usage: generate_images.py scenes.json images/"); sys.exit(1)
    scenes = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for sc in scenes:
        path = os.path.join(out, f"scene_{sc['id']:02d}.png")
        if os.path.exists(path):
            print(f"  exists: {path}"); continue
        url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(sc["prompt"]) + "?width=1080&height=1920&nologo=true"
        try:
            urllib.request.urlretrieve(url, path)
            print(f"✅ scene {sc['id']}: {path}")
            time.sleep(1)
        except Exception as e:
            print(f"❌ scene {sc['id']}: {e}")
    print("Done.")

if __name__ == "__main__":
    import urllib.parse
    main()
