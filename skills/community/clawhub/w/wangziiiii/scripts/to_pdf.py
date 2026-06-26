#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

try:
    import img2pdf
except ModuleNotFoundError as e:
    raise SystemExit(
        "[image-processing-toolkit-lab] 缺少依赖 img2pdf。\n"
        "请先进入技能目录并安装依赖：\n"
        "  python -m venv .venv && .venv/bin/python -m pip install -r requirements.txt\n"
        "(Windows: .venv\\Scripts\\python -m pip install -r requirements.txt)"
    ) from e

from _utils import iter_images, parse_exts, parse_suffixes


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Convert image(s) to PDF.")
    p.add_argument("--input", required=True, help="Input image file or directory")
    p.add_argument("--output", default=None, help="Output PDF path (default: same dir/new filename)")
    p.add_argument("--recursive", action="store_true", help="Scan subdirectories when input is a directory")
    p.add_argument("--suffix", default="_images", help="Suffix for auto-generated PDF filename")
    p.add_argument("--overwrite", action="store_true", help="Overwrite existing output PDF")
    p.add_argument("--include-ext", default=None, help="Only process these extensions, comma-separated")
    p.add_argument("--exclude-ext", default=None, help="Skip these extensions, comma-separated")
    p.add_argument("--exclude-suffixes", default=None, help="Skip files whose stem ends with these suffixes")
    p.add_argument("--dry-run", action="store_true", help="Preview only, do not write files")
    return p.parse_args()


def unique_pdf(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    i = 1
    while True:
        c = path.with_name(f"{stem}_{i}.pdf")
        if not c.exists():
            return c
        i += 1


def default_output(input_path: Path, suffix: str) -> Path:
    if input_path.is_file():
        return input_path.with_name(f"{input_path.stem}{suffix}.pdf")
    return input_path.with_name(f"{input_path.name}{suffix}.pdf")


def main() -> int:
    args = parse_args()
    in_path = Path(args.input).expanduser().resolve()

    images = iter_images(
        in_path,
        recursive=args.recursive,
        include_exts=parse_exts(args.include_ext),
        exclude_exts=parse_exts(args.exclude_ext),
        exclude_suffixes=parse_suffixes(args.exclude_suffixes),
    )
    if not images:
        print("No images found.")
        return 1

    out = Path(args.output).expanduser().resolve() if args.output else default_output(in_path, args.suffix)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and not args.overwrite:
        out = unique_pdf(out)

    if args.dry_run:
        print(f"DRY: {len(images)} image(s) -> {out}")
        return 0

    paths = [str(p) for p in images]
    try:
        pdf_bytes = img2pdf.convert(paths)
    except Exception as e:
        print(f"ERR: failed to build PDF -> {e}")
        return 2

    out.write_bytes(pdf_bytes)
    print(f"OK: wrote {out} from {len(images)} image(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
