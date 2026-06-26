"""
yumnb TTS — dual-voice talk-show MP3 generation via Microsoft edge-tts.

No API key required; voices are streamed from Microsoft's free online
voice service. Voice ↔ speaker mapping comes from yumnb's config so this
module stays content-agnostic.

The intro/outro chime is generated procedurally in pure Python (no
external assets bundled).
"""
from __future__ import annotations

import argparse
import asyncio
import math
import os
import re
import struct
import subprocess
import sys
import tempfile
import wave
from typing import Dict, Tuple

SAMPLE_RATE = 44100


def _ffmpeg():
    """Return path to bundled ffmpeg binary (imageio-ffmpeg) or system one."""
    try:
        import imageio_ffmpeg  # type: ignore

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return "ffmpeg"


# ── edge-tts single segment ────────────────────────────────────────────────

async def _render_segment(text: str, voice: str, rate: str, output_path: str):
    import edge_tts  # type: ignore

    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_path)


def render_single(text: str, output_path: str,
                  voice: str = "en-US-AriaNeural", rate: str = "+0%") -> str:
    asyncio.run(_render_segment(text, voice, rate, output_path))
    size = os.path.getsize(output_path)
    print(f"Generated: {output_path} ({size:,} bytes)")
    return output_path


# ── Procedurally-generated jingle (sine + triangle harmonic, pentatonic) ──

def _make_note_samples(freq, duration_s, volume=0.35, fade_in_s=0.015, fade_out_s=0.025):
    n = int(SAMPLE_RATE * duration_s)
    fi = int(SAMPLE_RATE * fade_in_s)
    fo = int(SAMPLE_RATE * fade_out_s)
    out = []
    for i in range(n):
        t = i / SAMPLE_RATE
        sine_val = math.sin(2 * math.pi * freq * t)
        tri_phase = (2 * freq * t) % 1.0
        tri_val = (2 * abs(2 * tri_phase - 1) - 1) * 0.22
        amp = volume * (sine_val + tri_val)
        if i < fi:
            amp *= i / fi
        elif i > n - fo:
            amp *= (n - i) / fo
        out.append(int(max(-32767, min(32767, amp * 32767))))
    return out


def _generate_jingle_wav(style: str, output_path: str):
    notes = {
        "C4": 261.63, "E4": 329.63, "G4": 392.00,
        "A4": 440.00, "C5": 523.25, "E5": 659.25,
    }
    if style == "intro":
        sequence = [("C4", 0.22), ("E4", 0.22), ("G4", 0.22), ("C5", 0.25),
                    ("E5", 0.35), ("C5", 0.22), ("G4", 0.18), ("C5", 0.22),
                    ("E5", 1.20)]
    else:
        sequence = [("E5", 0.35), ("C5", 0.28), ("G4", 0.28), ("E4", 0.28),
                    ("C4", 0.22), ("E4", 0.22), ("G4", 0.28),
                    ("C4", 1.60)]
    samples = [0] * int(SAMPLE_RATE * 0.4)
    for name, dur in sequence:
        samples += _make_note_samples(notes[name], dur)
    if style == "outro":
        fade_len = int(SAMPLE_RATE * 0.60)
        for i in range(fade_len):
            idx = len(samples) - fade_len + i
            if idx >= 0:
                samples[idx] = int(samples[idx] * (1 - i / fade_len))
    samples += [0] * int(SAMPLE_RATE * 0.4)
    with wave.open(output_path, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SAMPLE_RATE)
        wf.writeframes(struct.pack(f"<{len(samples)}h", *samples))
    return output_path


def _wav_to_mp3(wav_path, mp3_path):
    subprocess.run([_ffmpeg(), "-y", "-i", wav_path, "-q:a", "2", mp3_path],
                   check=True, capture_output=True)


def _concat_mp3s(input_files, output_mp3):
    """Concat MP3s with re-encoding (avoids DTS discontinuities)."""
    list_path = output_mp3 + "_concat.txt"
    with open(list_path, "w", encoding="utf-8") as f:
        for p in input_files:
            f.write(f"file '{os.path.abspath(p).replace(chr(39), '_')}'\n")
    subprocess.run([
        _ffmpeg(), "-y", "-f", "concat", "-safe", "0", "-i", list_path,
        "-codec:a", "libmp3lame", "-b:a", "128k", "-ar", "44100", "-ac", "2",
        output_mp3,
    ], check=True, capture_output=True)
    os.remove(list_path)


# ── Dual-voice script renderer ─────────────────────────────────────────────

def build_dual_audio(script_text: str,
                     output_mp3: str,
                     voices: Dict[str, Tuple[str, str]],
                     use_jingle: bool = True,
                     custom_jingle_mp3: str = "") -> str:
    """Render a [Speaker]-tagged script into one MP3.

    voices: {speaker_tag: (edge_tts_voice, rate)}.
    """
    if not voices:
        raise ValueError("No voices configured. Set tts.voices in config.yaml.")

    # Build regex from configured speaker tags so users can pick any names
    # (云飞/小晓, HostA/HostB, Alice/Bob, …).
    tag_alt = "|".join(re.escape(t) for t in voices.keys())
    parts = re.split(rf"\[({tag_alt})\]", script_text)
    if len(parts) < 3:
        raise ValueError(
            "No speaker tags found in script. Expected lines like "
            f"`[{next(iter(voices))}] …`")

    tmpdir = tempfile.mkdtemp(prefix="yumnb_tts_")
    temp_files = []
    seg_mp3s = []
    i = 1
    idx = 0
    while i < len(parts):
        speaker = parts[i].strip()
        text = parts[i + 1].strip() if i + 1 < len(parts) else ""
        if text and speaker in voices:
            tmp = os.path.join(tmpdir, f"seg_{idx}.mp3")
            voice, rate = voices[speaker]
            asyncio.run(_render_segment(text, voice, rate, tmp))
            size = os.path.getsize(tmp)
            print(f"  [{speaker}] seg {idx}: {size:,} bytes")
            seg_mp3s.append(tmp)
            temp_files.append(tmp)
            idx += 1
        i += 2

    if not seg_mp3s:
        raise RuntimeError("No audio segments produced.")

    all_mp3s = []
    if use_jingle:
        if custom_jingle_mp3 and os.path.isfile(custom_jingle_mp3):
            print(f"  Using custom jingle: {custom_jingle_mp3}")
            all_mp3s = [custom_jingle_mp3] + seg_mp3s + [custom_jingle_mp3]
        else:
            intro_wav = os.path.join(tmpdir, "intro.wav")
            outro_wav = os.path.join(tmpdir, "outro.wav")
            intro_mp3 = os.path.join(tmpdir, "intro.mp3")
            outro_mp3 = os.path.join(tmpdir, "outro.mp3")
            _generate_jingle_wav("intro", intro_wav)
            _generate_jingle_wav("outro", outro_wav)
            _wav_to_mp3(intro_wav, intro_mp3)
            _wav_to_mp3(outro_wav, outro_mp3)
            temp_files += [intro_wav, outro_wav, intro_mp3, outro_mp3]
            all_mp3s = [intro_mp3] + seg_mp3s + [outro_mp3]
    else:
        all_mp3s = seg_mp3s

    _concat_mp3s(all_mp3s, output_mp3)

    for f in temp_files:
        try:
            os.remove(f)
        except OSError:
            pass
    try:
        os.rmdir(tmpdir)
    except OSError:
        pass

    size = os.path.getsize(output_mp3)
    print(f"Done: {output_mp3} ({size:,} bytes)")
    return output_mp3


# ── CLI ────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="yumnb TTS")
    ap.add_argument("--text", help="Text to speak")
    ap.add_argument("--file", help="Read text from file")
    ap.add_argument("--output", required=True, help="Output MP3 path")
    ap.add_argument("--voice", default="en-US-AriaNeural",
                    help="edge-tts voice (single mode)")
    ap.add_argument("--rate", default="+0%", help="Speech rate, e.g. +10%%")
    ap.add_argument("--dual", action="store_true",
                    help="Dual-voice mode (split by [Speaker] tags)")
    ap.add_argument("--no-jingle", action="store_true",
                    help="Skip intro/outro chime (dual mode only)")
    ap.add_argument("--voices-json", help="JSON: {speaker: [voice, rate]} for --dual")
    ap.add_argument("--custom-jingle", default="",
                    help="Path to custom MP3 to use as intro/outro instead of generated chime")
    args = ap.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("ERROR: No text provided", file=sys.stderr)
        sys.exit(1)

    if args.dual:
        import json as _json

        if args.voices_json:
            raw = _json.loads(args.voices_json)
            voices = {k: tuple(v) for k, v in raw.items()}
        else:
            voices = {"HostA": ("en-US-AndrewNeural", "+5%"),
                      "HostB": ("en-US-AriaNeural", "+5%")}
        build_dual_audio(text, args.output, voices,
                         use_jingle=not args.no_jingle,
                         custom_jingle_mp3=args.custom_jingle)
    else:
        render_single(text, args.output, args.voice, args.rate)


if __name__ == "__main__":
    main()
