#!/usr/bin/env python3
"""
sticker.py — One-shot Telegram sticker maker.

Handles the full pipeline: background removal → animation frames → WebM encode → upload.

Usage:
    python3 sticker.py <image>                        # static PNG sticker
    python3 sticker.py <image> --animate sway         # animated WebM (sway)
    python3 sticker.py <image> --animate bounce       # animated WebM (bounce)
    python3 sticker.py <image> --animate shake        # animated WebM (shake)
    python3 sticker.py <image> --animate sway --no-upload   # skip upload

Outputs:
    Static:   <image_stem>_sticker.png
    Animated: <image_stem>_<motion>.webm  +  tmpfiles.org download URL
"""

import sys
import argparse
import shutil
from pathlib import Path


def check_deps():
    missing = []
    try:
        import rembg  # noqa
    except ImportError:
        missing.append('rembg[cpu]  →  pip install "rembg[cpu]"')
    try:
        from PIL import Image  # noqa
    except ImportError:
        missing.append('Pillow  →  pip install Pillow')
    if not shutil.which("ffmpeg"):
        missing.append('ffmpeg  →  install via your package manager (apt/brew/etc.)')
    if missing:
        print("Missing dependencies:")
        for m in missing:
            print(f"  {m}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="One-shot Telegram sticker maker.")
    parser.add_argument("image", help="Input image (any format)")
    parser.add_argument(
        "--animate",
        choices=["sway", "bounce", "shake"],
        default=None,
        help="Animation style (omit for static PNG)",
    )
    parser.add_argument("--no-upload", action="store_true", help="Skip tmpfiles.org upload")
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--duration", type=float, default=None,
                        help="Override animation duration in seconds (max 3.0)")
    args = parser.parse_args()

    check_deps()

    src = Path(args.image)
    if not src.exists():
        print(f"ERROR: File not found: {args.image}")
        sys.exit(1)

    scripts = Path(__file__).parent

    # Step 1: Make static sticker (always needed)
    sticker_path = src.parent / f"{src.stem}_sticker.png"
    print(f"\n[1/{'3' if args.animate else '1'}] Removing background + creating 512x512 PNG...")
    import subprocess
    result = subprocess.run(
        [sys.executable, str(scripts / "make_sticker.py"), str(src), str(sticker_path)],
        capture_output=False,
    )
    if result.returncode != 0:
        sys.exit(result.returncode)

    if not args.animate:
        print(f"\n✅ Static sticker ready: {sticker_path}")
        print("Send this to @Stickers bot as a Document (not a photo).")
        return

    # Step 2: Generate animation frames
    motion = args.animate
    frames_dir = src.parent / f"frames_{motion}"
    script_map = {
        "sway": ("animate_sway.py", 2.0),
        "bounce": ("animate_bounce.py", 1.5),
        "shake": ("animate_shake.py", 1.0),
    }
    script_name, default_dur = script_map[motion]
    duration = args.duration or default_dur

    print(f"\n[2/3] Generating {motion} frames ({duration}s @ {args.fps}fps)...")
    result = subprocess.run(
        [sys.executable, str(scripts / script_name), str(sticker_path),
         "--fps", str(args.fps), "--duration", str(duration),
         "--outdir", str(frames_dir)],
        capture_output=False,
    )
    if result.returncode != 0:
        sys.exit(result.returncode)

    # Step 3: Encode WebM
    webm_path = src.parent / f"{src.stem}_{motion}.webm"
    print(f"\n[3/3] Encoding WebM...")
    cmd = [sys.executable, str(scripts / "make_webm.py"),
           str(frames_dir), str(webm_path),
           "--fps", str(args.fps), "--duration", str(duration)]
    if args.no_upload:
        cmd.append("--no-upload")
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        sys.exit(result.returncode)

    print(f"\n✅ Animated sticker ready: {webm_path}")
    if not args.no_upload:
        print("⬆️  Download link printed above — send to @Stickers bot as a Document.")
        print("    Use /newvideo in @Stickers bot for video sticker packs.")


if __name__ == "__main__":
    main()
