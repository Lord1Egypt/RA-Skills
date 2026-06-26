#!/usr/bin/env python3
"""List available Supertonic voices and metadata.

Usage:
    python3 list_voices.py
"""
import sys
from pathlib import Path

# Auto-activate venv
_VENV = Path.home() / ".openclaw/workspace/.browser-use-venv"
if _VENV.is_dir():
    sp = _VENV / f"lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages"
    if not sp.is_dir():
        for v in [(3,14), (3,13), (3,12), (3,11)]:
            sp = _VENV / f"lib/python{v[0]}.{v[1]}/site-packages"
            if sp.is_dir():
                break
    if str(sp) not in sys.path and sp.is_dir():
        sys.path.insert(0, str(sp))

try:
    from supertonic import TTS
except ImportError:
    print("ERROR: supertonic not installed. Run: pip install supertonic", file=sys.stderr)
    sys.exit(1)


def main():
    print("Loading TTS (may auto-download on first run)...")
    tts = TTS(auto_download=True)

    print(f"\nSupertonic TTS")
    print(f"  Model:     {tts.model_name}")
    print(f"  Sample:    {tts.sample_rate} Hz")
    print(f"  Languages: 31 (multilingual: {tts.is_multilingual})")
    print(f"\n{'Voice':<8} {'Gender':<8} {'Description'}")
    print("-" * 50)

    descriptions = {
        "F1": "Warm, mature female",
        "F2": "Bright, clear female",
        "F3": "Soft, gentle female (great for Japanese)",
        "F4": "Energetic, youthful female",
        "F5": "Deep, authoritative female",
        "M1": "Neutral, clear male (default)",
        "M2": "Warm, conversational male",
        "M3": "Deep, serious male",
        "M4": "Bright, young male",
        "M5": "Energetic, expressive male",
    }

    for voice in tts.voice_style_names:
        gender = "Female" if voice.startswith("F") else "Male"
        desc = descriptions.get(voice, "—")
        marker = " *" if voice == "M1" else ""
        print(f"  {voice:<8} {gender:<8} {desc}{marker}")

    print("\n  * = default voice")
    print("\nUse with: python3 synthesize.py 'text' --voice F2")


if __name__ == "__main__":
    main()
