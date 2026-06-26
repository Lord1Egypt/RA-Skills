#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

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
    p = argparse.ArgumentParser(description="Compress image(s) with quality/optimization controls.")
    p.add_argument("--input", required=True, help="Input image file or directory")
    p.add_argument("--format", default=None, help="Optional target format (jpg/png/webp/...) ; default keep source")
    p.add_argument("--out-dir", default=None, help="Optional output directory")
    p.add_argument("--recursive", action="store_true", help="Scan subdirectories when input is a directory")
    p.add_argument("--quality", type=int, default=80, help="Quality for lossy formats (1-100)")
    p.add_argument("--png-compress-level", type=int, default=6, help="PNG compress level (0-9)")
    p.add_argument("--optimize", action="store_true", default=True, help="Enable optimize flag")
    p.add_argument("--no-optimize", action="store_false", dest="optimize", help="Disable optimize flag")
    p.add_argument("--suffix", default="_compressed", help="Output filename suffix")
    p.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    p.add_argument("--include-ext", default=None, help="Only process these extensions, comma-separated")
    p.add_argument("--exclude-ext", default=None, help="Skip these extensions, comma-separated")
    p.add_argument("--exclude-suffixes", default=None, help="Skip files whose stem ends with these suffixes")
    p.add_argument("--dry-run", action="store_true", help="Preview only, do not write files")
    return p.parse_args()


def infer_format_from_suffix(path: Path) -> str:
    ext = path.suffix.lower().lstrip(".")
    if ext in {"jpg", "jpeg", "png", "webp", "bmp", "tif", "tiff", "gif", "avif", "heic", "heif"}:
        return normalize_format(ext)
    raise ValueError(f"Cannot infer target format from extension: {path.suffix}")


def main() -> int:
    args = parse_args()
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
            target_format = normalize_format(args.format) if args.format else infer_format_from_suffix(src)
            ensure_pillow_can_save(target_format)
            target_ext = ".jpg" if target_format == "JPEG" else f".{target_format.lower()}"

            out_path = build_output_path(src, out_dir, args.suffix, target_ext, args.overwrite)
            if args.dry_run:
                print(f"DRY: {src} -> {out_path}")
                ok += 1
                continue

            img = open_image(src)
            img = to_savable_mode(img, target_format)
            save_image(
                img,
                out_path,
                target_format,
                quality=args.quality,
                optimize=args.optimize,
                png_compress_level=args.png_compress_level,
            )
            ok += 1
            print(f"OK: {src} -> {out_path}")
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
