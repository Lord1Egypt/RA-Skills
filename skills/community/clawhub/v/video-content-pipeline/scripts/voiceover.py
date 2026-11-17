#!/usr/bin/env python3
"""Voiceover via Edge TTS (free) — da-DK-JeppeNeural by default.

🔒 PRIVACY NOTICE: Edge TTS is Microsoft's external cloud service. Each scene's
narration text is sent to Microsoft's servers for synthesis. Do NOT use this
script with confidential narration content unless you accept this.
"""
import sys
print("🔒 NOTE: narration text is sent to Microsoft Edge TTS (external service).", file=sys.stderr)
import json, os, sys, asyncio

def main():
    if len(sys.argv) < 3:
        print("Usage: voiceover.py scenes.json audio/"); sys.exit(1)
    scenes = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    voice = os.environ.get("VOICE", "da-DK-JeppeNeural")
    try:
        import edge_tts
    except ImportError:
        print("pip install edge-tts"); sys.exit(1)
    async def gen():
        for sc in scenes:
            path = os.path.join(out, f"scene_{sc['id']:02d}.mp3")
            if os.path.exists(path):
                print(f"  exists: {path}"); continue
            tts = edge_tts.Communicate(sc["narration"], voice, rate="-5%")
            await tts.save(path)
            print(f"✅ scene {sc['id']}: {path}")
    asyncio.run(gen())
    print("Done.")

if __name__ == "__main__":
    main()
