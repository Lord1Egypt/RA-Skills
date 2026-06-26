#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps

from _utils import (
    build_output_path,
    ensure_pillow_can_save,
    iter_images,
    normalize_format,
    open_image,
    parse_exts,
    parse_suffixes,
    save_image,
    to_savable_mode,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Batch pipeline: resize + convert/compress in one command.")
    p.add_argument("--input", required=True, help="Input image file or directory")
    p.add_argument("--out-dir", default=None, help="Optional output directory")
    p.add_argument("--recursive", action="store_true", help="Scan subdirectories")
    p.add_argument("--format", default=None, help="Target format (jpg/png/webp/...) ; default keep source")
    p.add_argument("--quality", type=int, default=85, help="Quality for lossy formats")
    p.add_argument("--width", type=int, default=None, help="Optional target width")
    p.add_argument("--height", type=int, default=None, help="Optional target height")
    p.add_argument("--mode", choices=["contain", "cover", "exact"], default="contain", help="Resize mode")
    p.add_argument("--suffix", default="_batch", help="Output filename suffix")
    p.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    p.add_argument("--include-ext", default=None, help="Only process these extensions, comma-separated")
    p.add_argument("--exclude-ext", default=None, help="Skip these extensions, comma-separated")
    p.add_argument("--exclude-suffixes", default=None, help="Skip files whose stem ends with these suffixes")
    p.add_argument("--dry-run", action="store_true", help="Preview only, do not write files")
    return p.parse_args()


def infer_format(path: Path) -> str:
    ext = path.suffix.lower().lstrip('.')
    return normalize_format(ext)


def maybe_resize(img, width: int | None, height: int | None, mode: str):
    if not width and not height:
        return img
    ow, oh = img.size
    tw = width or int(ow * (height / oh))
    th = height or int(oh * (width / ow))
    if mode == "contain":
        return ImageOps.contain(img, (tw, th), method=Image.Resampling.LANCZOS)
    if mode == "cover":
        return ImageOps.fit(img, (tw, th), method=Image.Resampling.LANCZOS)
    return img.resize((tw, th), resample=Image.Resampling.LANCZOS)


def main() -> int:
    args = parse_args()
    in_path = Path(args.input).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else None

    files = iter_images(
        in_path,
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
            target_fmt = normalize_format(args.format) if args.format else infer_format(src)
            ensure_pillow_can_save(target_fmt)
            target_ext = ".jpg" if target_fmt == "JPEG" else f".{target_fmt.lower()}"

            out = build_output_path(src, out_dir, args.suffix, target_ext, args.overwrite)
            if args.dry_run:
                print(f"DRY: {src} -> {out}")
                ok += 1
                continue

            img = open_image(src)
            img = maybe_resize(img, args.width, args.height, args.mode)
            img = to_savable_mode(img, target_fmt)

            save_image(img, out, target_fmt, quality=args.quality)
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
