#!/usr/bin/env python3
import argparse
import os
import subprocess
import tempfile
from pathlib import Path

import requests


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(str(c) for c in cmd)}\n{result.stderr}")
    return result


def ensure_runtime_python() -> str:
    """Return python path with required video deps for make_talking_circle_video.py."""
    venv_dir = Path("/tmp/talking-circle-venv")
    py = venv_dir / "bin" / "python"
    if py.exists():
        return str(py)

    subprocess.run(["python3", "-m", "venv", str(venv_dir)], check=True)
    pip = venv_dir / "bin" / "pip"
    req = Path(__file__).resolve().parents[1] / "requirements.txt"
    subprocess.run([str(pip), "install", "--quiet", "-r", str(req)], check=True)
    return str(py)


def build_static_circle_video(neutral_path: Path, audio_path: Path, out: Path, size: int = 720, diameter: int = 640):
    # Optional fallback only (disabled by default)
    from PIL import Image, ImageDraw

    bg = (242, 242, 242)
    r = diameter // 2
    center = (size // 2, size // 2)

    im = Image.open(neutral_path).convert("RGB").resize((diameter, diameter), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (size, size), bg)
    canvas.paste(im, (center[0] - r, center[1] - r))

    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((center[0] - r, center[1] - r, center[0] + r, center[1] + r), fill=255)

    out_img = out.with_suffix(".png")
    final = Image.new("RGB", (size, size), bg)
    final.paste(canvas, mask=mask)
    d2 = ImageDraw.Draw(final)
    d2.ellipse((center[0] - r, center[1] - r, center[0] + r, center[1] + r), outline=(210, 210, 210), width=2)
    final.save(out_img)

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            str(out_img),
            "-i",
            str(audio_path),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-tune",
            "stillimage",
            "-shortest",
            str(out),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main():
    p = argparse.ArgumentParser(description="One-shot: ElevenLabs TTS + animated circle avatar video")
    p.add_argument("--text", required=True)
    p.add_argument("--out", required=True)

    p.add_argument("--neutral", required=True)
    p.add_argument("--slight", required=True)
    p.add_argument("--wide", required=True)
    p.add_argument("--blink", required=True)

    p.add_argument("--api-key", default=os.getenv("ELEVENLABS_API_KEY"))
    p.add_argument("--voice-id", required=True)
    p.add_argument("--model-id", default="eleven_multilingual_v2")

    p.add_argument("--stability", type=float, default=0.50)
    p.add_argument("--similarity-boost", type=float, default=0.75)
    p.add_argument("--style", type=float, default=0.00)
    p.add_argument("--use-speaker-boost", action="store_true")
    p.add_argument("--speed", type=float, default=1.00)

    p.add_argument("--size", type=int, default=720)
    p.add_argument("--diameter", type=int, default=640)
    p.add_argument("--fps", type=int, default=30)

    p.add_argument("--blink-start", type=float, default=1.1)
    p.add_argument("--blink-every", type=float, default=3.8)
    p.add_argument("--blink-duration-frames", type=int, default=4)

    p.add_argument("--amp-low", type=int, default=1200)
    p.add_argument("--amp-high", type=int, default=2600)

    p.add_argument("--allow-static-fallback", action="store_true", help="Use static video fallback if animation build fails")
    args = p.parse_args()

    if not args.api_key:
        raise SystemExit("Missing ElevenLabs API key. Set ELEVENLABS_API_KEY or pass --api-key.")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    neutral = Path(args.neutral)
    slight = Path(args.slight)
    wide = Path(args.wide)
    blink = Path(args.blink)
    for f in [neutral, slight, wide, blink]:
        if not f.exists():
            raise SystemExit(f"Missing frame file: {f}")

    log_path = out.with_suffix(".build.log")

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        audio = td / "speech.mp3"

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{args.voice_id}?output_format=mp3_44100_128"
        payload = {
            "text": args.text,
            "model_id": args.model_id,
            "voice_settings": {
                "stability": args.stability,
                "similarity_boost": args.similarity_boost,
                "style": args.style,
                "use_speaker_boost": bool(args.use_speaker_boost),
                "speed": args.speed,
            },
        }
        r = requests.post(
            url,
            headers={"xi-api-key": args.api_key, "Content-Type": "application/json"},
            json=payload,
            timeout=90,
        )
        r.raise_for_status()
        audio.write_bytes(r.content)

        script = Path(__file__).with_name("make_talking_circle_video.py")
        runtime_python = ensure_runtime_python()
        cmd = [
            runtime_python,
            str(script),
            "--neutral",
            str(neutral),
            "--slight",
            str(slight),
            "--wide",
            str(wide),
            "--blink",
            str(blink),
            "--audio",
            str(audio),
            "--out",
            str(out),
            "--blink-start",
            str(args.blink_start),
            "--blink-every",
            str(args.blink_every),
            "--blink-duration-frames",
            str(args.blink_duration_frames),
            "--size",
            str(args.size),
            "--diameter",
            str(args.diameter),
            "--fps",
            str(args.fps),
            "--amp-low",
            str(args.amp_low),
            "--amp-high",
            str(args.amp_high),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        log_path.write_text(
            f"RC={result.returncode}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}\n"
        )

        if result.returncode != 0:
            if args.allow_static_fallback:
                build_static_circle_video(neutral, audio, out)
            else:
                raise SystemExit(
                    f"Animated video build failed.\n{result.stderr}\nSee build log: {log_path}"
                )

    if not out.exists() or out.stat().st_size == 0:
        raise RuntimeError("Output video is missing or empty")

    print(str(out))


if __name__ == "__main__":
    main()
