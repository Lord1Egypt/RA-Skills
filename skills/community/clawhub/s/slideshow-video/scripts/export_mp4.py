#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path


def looks_like_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def main():
    parser = argparse.ArgumentParser(description="Export slideshow PNGs to MP4 with ffmpeg.")
    parser.add_argument("input_dir", help="Directory containing slide PNGs")
    parser.add_argument("output", help="Output MP4 path")
    parser.add_argument("--glob", default="slide_*.png", help="Glob for slide images inside input_dir")
    parser.add_argument("--seconds-per-slide", type=float, default=3.0, help="Duration for each slide")
    parser.add_argument("--fps", type=int, default=30, help="Output video FPS")
    parser.add_argument("--zoom", action="store_true", help="Apply a gentle Ken Burns style zoom")
    parser.add_argument("--fade", type=float, default=0.0, help="Fade in duration in seconds for each slide")
    parser.add_argument("--audio", help="Optional local audio file or remote audio URL")
    parser.add_argument("--audio-volume", type=float, default=0.22, help="Background audio volume multiplier")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output")
    args = parser.parse_args()

    input_dir = Path(args.input_dir).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    slides = sorted(input_dir.glob(args.glob))
    if not slides:
        raise SystemExit(f"No slides matched {args.glob} in {input_dir}")

    concat_path = output.with_suffix(".concat.txt")
    concat_path.parent.mkdir(parents=True, exist_ok=True)
    total_duration = len(slides) * args.seconds_per_slide

    with concat_path.open("w", encoding="utf-8") as f:
        for slide in slides:
            f.write(f"file '{slide.as_posix()}'\n")
            f.write(f"duration {args.seconds_per_slide:.3f}\n")
        f.write(f"file '{slides[-1].as_posix()}'\n")

    frames_per_slide = max(1, int(args.seconds_per_slide * args.fps))
    vf_parts = []
    if args.zoom:
        vf_parts.append(
            f"zoompan=z='min(zoom+0.0008,1.08)':d={frames_per_slide}:s=1080x1920:fps={args.fps}"
        )
    else:
        vf_parts.append(f"fps={args.fps},scale=1080:1920")

    if args.fade > 0:
        vf_parts.append(f"fade=t=in:st=0:d={args.fade}")

    vf_parts.append("format=yuv420p")
    vf = ",".join(vf_parts)

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_path),
    ]

    if args.audio:
        cmd.extend([
            "-stream_loop",
            "-1",
            "-i",
            args.audio,
            "-filter_complex",
            f"[1:a]volume={args.audio_volume},atrim=duration={total_duration}[bgm]",
            "-map",
            "0:v:0",
            "-map",
            "[bgm]",
        ])

    cmd.extend([
        "-vf",
        vf,
        "-r",
        str(args.fps),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
    ])

    if args.audio:
        cmd.extend([
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
        ])

    cmd.append(str(output))
    if args.overwrite:
        cmd.insert(1, "-y")

    subprocess.run(cmd, check=True)
    print(f"✓ {output}")


if __name__ == "__main__":
    main()
