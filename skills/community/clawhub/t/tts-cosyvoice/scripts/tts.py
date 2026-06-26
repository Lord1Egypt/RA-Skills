#!/usr/bin/env python3
# Uses comfyui-venv for edge-tts dependency
import sys
sys.path.insert(0, '/home/vincent/comfyui-venv/lib/python3.12/site-packages')
"""Edge TTS — Text-to-Speech script. No API key required. Supports SRT subtitle generation."""

import argparse
import asyncio
import os
import re
import sys

import edge_tts
from edge_tts import SubMaker


# Default voices by language
DEFAULT_VOICES = {
    "zh": "zh-CN-XiaoxiaoNeural",
    "en": "en-US-JennyNeural",
    "ja": "ja-JP-NanamiNeural",
    "ko": "ko-KR-SunHiNeural",
    "fr": "fr-FR-DeniseNeural",
    "de": "de-DE-KatjaNeural",
}


async def synthesize_with_subs(text, voice, output, srt_output=None, rate="+0%", pitch="+0Hz", volume="+0%"):
    """Generate speech with optional SRT subtitles from TTS timeline (not ASR)."""
    communicate = edge_tts.Communicate(
        text, voice, rate=rate, pitch=pitch, volume=volume
    )
    submaker = SubMaker()

    with open(output, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            else:
                submaker.feed(chunk)

    # Generate SRT if requested
    if srt_output:
        srt_content = submaker.get_srt()
        with open(srt_output, "w", encoding="utf-8") as f:
            f.write(srt_content)
        print(f"📝 SRT: {srt_output}")

    return output


async def synthesize(text, voice, output, rate="+0%", pitch="+0Hz", volume="+0%"):
    """Generate speech from text (no subtitles)."""
    communicate = edge_tts.Communicate(
        text, voice, rate=rate, pitch=pitch, volume=volume
    )
    await communicate.save(output)
    return output


async def list_voices(lang_filter=None):
    """List available voices, optionally filtered by language code."""
    voices = await edge_tts.list_voices()
    for v in sorted(voices, key=lambda x: x["Locale"]):
        locale = v["Locale"]
        if lang_filter and not locale.lower().startswith(lang_filter.lower()):
            continue
        print(f"  {v['ShortName']:<35} {v['Gender']:<8} {v['Locale']}  {v.get('FriendlyName','')}")


def main():
    parser = argparse.ArgumentParser(description="Text-to-Speech via Edge TTS (with SRT subtitles)")
    parser.add_argument("--text", help="Text to speak")
    parser.add_argument("--file", help="Read text from file")
    parser.add_argument("--voice", default=None, help="Voice ID (default: auto-detect from text)")
    parser.add_argument("--output", default="/tmp/tts_output.mp3", help="Output file path")
    parser.add_argument("--srt", default=None, help="Generate SRT subtitle file (e.g. output.srt)")
    parser.add_argument("--rate", default="+0%", help="Speed: -50%% to +100%%")
    parser.add_argument("--pitch", default="+0Hz", help="Pitch: -50Hz to +50Hz")
    parser.add_argument("--volume", default="+0%", help="Volume: -100% to +100%")
    parser.add_argument("--list-voices", dest="list_voices", metavar="LANG",
                        help="List voices for language (e.g. zh, en, ja)")
    args = parser.parse_args()

    if args.list_voices:
        asyncio.run(list_voices(args.list_voices))
        return

    # Get text
    text = args.text
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read().strip()

    if not text:
        parser.error("Provide --text or --file")

    # Auto-detect voice
    voice = args.voice
    if not voice:
        if re.search(r'[\u4e00-\u9fff]', text):
            voice = DEFAULT_VOICES["zh"]
        elif re.search(r'[\u3040-\u309f\u30a0-\u30ff]', text):
            voice = DEFAULT_VOICES["ja"]
        elif re.search(r'[\uac00-\ud7af]', text):
            voice = DEFAULT_VOICES["ko"]
        else:
            voice = DEFAULT_VOICES["en"]

    print(f"🔊 Voice: {voice}")
    print(f"📝 Text: {text[:80]}{'...' if len(text) > 80 else ''}")

    if args.srt:
        asyncio.run(synthesize_with_subs(text, voice, args.output, args.srt, args.rate, args.pitch, args.volume))
    else:
        asyncio.run(synthesize(text, voice, args.output, args.rate, args.pitch, args.volume))

    size = os.path.getsize(args.output)
    print(f"✅ Saved: {args.output} ({size/1024:.1f}KB)")


if __name__ == "__main__":
    main()
