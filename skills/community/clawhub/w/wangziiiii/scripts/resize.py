#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps

from _utils import (
    build_output_path,
    ensure_pillow_can_save,
    iter_images,
    open_image,
    parse_exts,
    parse_suffixes,
    save_image,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Resize image(s).")
    p.add_argument("--input", required=True, help="Input image file or directory")
    p.add_argument("--out-dir", default=None, help="Optional output directory")
    p.add_argument("--recursive", action="store_true", help="Scan subdirectories when input is a directory")
    p.add_argument("--width", type=int, default=None, help="Target width")
    p.add_argument("--height", type=int, default=None, help="Target height")
    p.add_argument("--mode", choices=["contain", "cover", "exact"], default="contain", help="Resize mode")
    p.add_argument("--quality", type=int, default=90, help="Output quality for lossy formats")
    p.add_argument("--suffix", default="_resized", help="Output filename suffix")
    p.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    p.add_argument("--include-ext", default=None, help="Only process these extensions, comma-separated")
    p.add_argument("--exclude-ext", default=None, help="Skip these extensions, comma-separated")
    p.add_argument("--exclude-suffixes", default=None, help="Skip files whose stem ends with these suffixes")
    p.add_argument("--dry-run", action="store_true", help="Preview only, do not write files")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if not args.width and not args.height:
        print("ERR: specify at least --width or --height")
        return 2

    input_path = Path(args.input).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else None
    files = iter_images(
        input_path,
        recursive=args.recursive,
        include_exts=parse_exts(args.include_ext),
        exclude_exts=parse_exts(args.exclude_ext),
        exclude_suffixes=parse_suffixes(args.exclude_suffixes),
    )
    if not files:
        print("No images found.")
        return 1

    ok, fail = 0, 0
    failed = []
    for src in files:
        try:
            out = build_output_path(src, out_dir, args.suffix, src.suffix, args.overwrite)
            if args.dry_run:
                print(f"DRY: {src} -> {out}")
                ok += 1
                continue

            img = open_image(src)
            ow, oh = img.size
            tw = args.width or int(ow * (args.height / oh))
            th = args.height or int(oh * (args.width / ow))

            if args.mode == "contain":
                out_img = ImageOps.contain(img, (tw, th), method=Image.Resampling.LANCZOS)
            elif args.mode == "cover":
                out_img = ImageOps.fit(img, (tw, th), method=Image.Resampling.LANCZOS)
            else:
                out_img = img.resize((tw, th), resample=Image.Resampling.LANCZOS)

            fmt = "JPEG" if src.suffix.lower() in {".jpg", ".jpeg"} else src.suffix.lower().lstrip(".").upper()
            ensure_pillow_can_save(fmt)
            save_image(out_img, out, fmt, quality=args.quality)
            ok += 1
            print(f"OK: {src} -> {out}")
        except Exception as e:
            fail += 1
            failed.append((src, str(e)))
            print(f"ERR: {src} -> {e}")

    print(f"Done. success={ok}, fail={fail}, total={len(files)}")
    if failed:
        print("Failed files:")
        for f, err in failed[:20]:
            print(f" - {f}: {err}")
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
