#!/usr/bin/env python3
"""Script → scener (JSON) med billede-prompts."""
import json, sys, re

def main():
    if len(sys.argv) < 3:
        print("Usage: scene_plan.py script.txt scenes.json"); sys.exit(1)
    text = open(sys.argv[1]).read().strip()
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    scenes = []
    for i, s in enumerate(sentences[:12]):
        scenes.append({
            "id": i + 1,
            "narration": s,
            "prompt": f"Pixar-style cinematic illustration, warm lighting, {s[:80]}",
            "duration": max(3, min(5, len(s.split()) / 2.5)),
        })
    json.dump(scenes, open(sys.argv[2], "w"), indent=2, ensure_ascii=False)
    print(f"✅ {len(scenes)} scener → {sys.argv[2]}")

if __name__ == "__main__":
    main()
