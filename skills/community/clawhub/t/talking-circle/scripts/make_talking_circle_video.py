#!/usr/bin/env python3
import argparse
import subprocess
import numpy as np
import tempfile
import wave
from pathlib import Path

from PIL import Image, ImageDraw


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(str(c) for c in cmd)}\n{result.stderr}")


def prep_circle_frame(path: Path, size: int, diameter: int, bg=(242, 242, 242)) -> Image.Image:
    r = diameter // 2
    center = (size // 2, size // 2)

    im = Image.open(path).convert("RGB").resize((diameter, diameter), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (size, size), bg)
    canvas.paste(im, (center[0] - r, center[1] - r))

    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((center[0] - r, center[1] - r, center[0] + r, center[1] + r), fill=255)

    out = Image.new("RGB", (size, size), bg)
    out.paste(canvas, mask=mask)
    d2 = ImageDraw.Draw(out)
    d2.ellipse((center[0] - r, center[1] - r, center[0] + r, center[1] + r), outline=(210, 210, 210), width=2)
    return out


def build_blink_frames(total: int, fps: int, dur: float, start: float, every: float, duration_frames: int):
    """Always schedule visible blink frames (at least one for short clips)."""
    frames = set()
    if duration_frames <= 0 or total <= 0:
        return frames

    half = duration_frames // 2
    centers = []

    # Regular schedule for normal-duration clips
    if every > 0:
        t = start
        while t < dur - 0.2:
            centers.append(int(t * fps))
            t += every

    # Mandatory fallback: at least one blink even for short videos
    if not centers:
        if dur >= 0.8:
            centers.append(int((dur * 0.5) * fps))
        else:
            centers.append(total // 2)

    for c in centers:
        for j in range(duration_frames):
            idx = c - half + j
            if 0 <= idx < total:
                frames.add(idx)

    return frames


def audio_rms_for_frame(raw: bytes, sr: int, frame_idx: int, fps: int, sample_width: int):
    total_samples = len(raw) // sample_width
    center_sample = int((frame_idx / fps) * sr)
    win_samples = int(0.035 * sr)
    s = max(0, center_sample - win_samples // 2)
    e = min(total_samples, center_sample + win_samples // 2)
    if e <= s:
        return 0

    seg = raw[s * sample_width : e * sample_width]
    if sample_width != 2:
        return 0

    arr = np.frombuffer(seg, dtype=np.int16).astype(np.float32)
    if arr.size == 0:
        return 0
    return int(np.sqrt(np.mean(np.square(arr))))


def render_sequence_frames(frames_dir: Path, prepared: dict, total: int, blink_frames: set, key_selector):
    used = set()
    for i in range(total):
        if i in blink_frames:
            key = "blink"
        else:
            key = key_selector(i)
        used.add(key)
        prepared[key].save(frames_dir / f"frame_{i:06d}.png")
    return used


def build_silent_video_from_frames(frames_dir: Path, fps: int, out_silent: Path):
    run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(fps),
            "-i",
            str(frames_dir / "frame_%06d.png"),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(out_silent),
        ]
    )


def main():
    p = argparse.ArgumentParser(description="Create talking circle avatar video from mouth/eye frames + audio")
    p.add_argument("--neutral", required=True)
    p.add_argument("--slight", required=True)
    p.add_argument("--wide", required=True)
    p.add_argument("--blink", required=True)
    p.add_argument("--audio", required=True)
    p.add_argument("--out", required=True)

    p.add_argument("--size", type=int, default=720)
    p.add_argument("--diameter", type=int, default=640)
    p.add_argument("--fps", type=int, default=30)

    # mandatory blink: visible but still natural
    p.add_argument("--blink-start", type=float, default=1.1)
    p.add_argument("--blink-every", type=float, default=3.8)
    p.add_argument("--blink-duration-frames", type=int, default=4)

    # thresholds in 16-bit PCM RMS units
    p.add_argument("--amp-low", type=int, default=1200)
    p.add_argument("--amp-high", type=int, default=2600)

    args = p.parse_args()

    neutral = Path(args.neutral)
    slight = Path(args.slight)
    wide = Path(args.wide)
    blink = Path(args.blink)
    audio = Path(args.audio)
    out = Path(args.out)

    for f in [neutral, slight, wide, blink, audio]:
        if not f.exists():
            raise FileNotFoundError(f"Missing required input: {f}")

    out.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        wav = td / "speech.wav"
        frames_dir = td / "frames"
        frames_dir.mkdir(parents=True, exist_ok=True)
        out_silent = td / "silent.mp4"

        run(["ffmpeg", "-y", "-i", str(audio), "-ac", "1", "-ar", "16000", str(wav)])

        with wave.open(str(wav), "rb") as w:
            sr = w.getframerate()
            n = w.getnframes()
            sample_width = w.getsampwidth()
            channels = w.getnchannels()
            if channels != 1:
                raise RuntimeError("Expected mono wav after ffmpeg conversion")
            raw = w.readframes(n)

        dur = n / sr
        total = max(1, int(dur * args.fps))

        prepared = {
            "neutral": prep_circle_frame(neutral, args.size, args.diameter),
            "slight": prep_circle_frame(slight, args.size, args.diameter),
            "wide": prep_circle_frame(wide, args.size, args.diameter),
            "blink": prep_circle_frame(blink, args.size, args.diameter),
        }

        blink_frames = build_blink_frames(
            total=total,
            fps=args.fps,
            dur=dur,
            start=args.blink_start,
            every=args.blink_every,
            duration_frames=args.blink_duration_frames,
        )

        # Audio-driven selection
        def select_key(i):
            rms = audio_rms_for_frame(raw, sr, i, args.fps, sample_width)
            if rms < args.amp_low:
                return "neutral"
            if rms < args.amp_high:
                return "slight"
            return "wide"

        used = render_sequence_frames(frames_dir, prepared, total, blink_frames, select_key)

        # If visually static by key usage (ignoring blink), fallback cycle
        non_blink_used = {k for k in used if k != "blink"}
        if len(non_blink_used) <= 1:
            for f in frames_dir.glob("frame_*.png"):
                f.unlink(missing_ok=True)
            cycle = ["neutral", "slight", "wide", "slight", "neutral", "slight", "wide", "slight"]

            def cycle_key(i):
                return cycle[i % len(cycle)]

            render_sequence_frames(frames_dir, prepared, total, blink_frames, cycle_key)

        build_silent_video_from_frames(frames_dir, args.fps, out_silent)

        run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(out_silent),
                "-i",
                str(audio),
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-shortest",
                str(out),
            ]
        )

    if not out.exists() or out.stat().st_size == 0:
        raise RuntimeError("Output video is missing or empty")

    print(str(out))


if __name__ == "__main__":
    main()
