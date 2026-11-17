#!/usr/bin/env python3
"""Saml billeder + voiceover → MP4 (ffmpeg)."""
import json, os, subprocess, sys

def main():
    if len(sys.argv) < 6:
        print("Usage: compositor.py scenes.json images/ audio/ out.mp4 [vertical]"); sys.exit(1)
    scenes, img_dir, aud_dir, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    vertical = len(sys.argv) > 5 and sys.argv[5] == "vertikal"
    scenes = json.load(open(scenes))
    parts = []
    for sc in scenes:
        img = os.path.join(img_dir, f"scene_{sc['id']:02d}.png")
        aud = os.path.join(aud_dir, f"scene_{sc['id']:02d}.mp3")
        if not (os.path.exists(img) and os.path.exists(aud)):
            print(f"⚠️ missing scene {sc['id']}"); continue
        part = f"/tmp/scene_{sc['id']:02d}.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", img, "-i", aud,
            "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac",
            "-shortest", "-pix_fmt", "yuv420p", part
        ], capture_output=True)
        parts.append(part)
    if not parts:
        print("No scenes to compose."); sys.exit(1)
    concat_file = "/tmp/concat.txt"
    # Escape enkelt-anførselstegn i filstier (ffmpeg concat-injektion fix 20/8)
    lines = ["file '" + p.replace("'", "'\\''") + "'\n" for p in parts]
    open(concat_file, "w").write("".join(lines))
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file,
                    "-c", "copy", out], capture_output=True)
    print(f"✅ Video: {out}")

if __name__ == "__main__":
    main()
