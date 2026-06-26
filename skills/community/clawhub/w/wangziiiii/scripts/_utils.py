#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Set

try:
    from PIL import Image, ImageOps
except ModuleNotFoundError as e:
    raise SystemExit(
        "[image-processing-toolkit-lab] 缺少依赖 Pillow。\n"
        "请先进入技能目录并安装依赖：\n"
        "  python -m venv .venv && .venv/bin/python -m pip install -r requirements.txt\n"
        "(Windows: .venv\\Scripts\\python -m pip install -r requirements.txt)"
    ) from e

SUPPORTED_INPUT_EXTS = {
    ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif", ".gif", ".avif", ".heic", ".heif"
}

FORMAT_ALIASES = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "webp": "WEBP",
    "bmp": "BMP",
    "tif": "TIFF",
    "tiff": "TIFF",
    "gif": "GIF",
    "avif": "AVIF",
    "heic": "HEIC",
    "heif": "HEIF",
}

DEFAULT_EXCLUDE_SUFFIXES = ["_converted", "_compressed", "_resized", "_batch"]


def normalize_ext(ext: str) -> str:
    ext = ext.strip().lower()
    if not ext:
        return ""
    return ext if ext.startswith(".") else f".{ext}"


def parse_exts(raw: Optional[str]) -> Set[str]:
    if not raw:
        return set()
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    return {normalize_ext(p) for p in parts}


def parse_suffixes(raw: Optional[str]) -> List[str]:
    if not raw:
        return list(DEFAULT_EXCLUDE_SUFFIXES)
    return [p.strip() for p in raw.split(",") if p.strip()]


def normalize_format(fmt: str) -> str:
    key = fmt.strip().lower()
    if key not in FORMAT_ALIASES:
        raise ValueError(f"Unsupported output format: {fmt}")
    return FORMAT_ALIASES[key]


def ensure_pillow_can_save(target_format: str) -> None:
    fmt = target_format.upper()
    if fmt not in Image.SAVE:
        available = ", ".join(sorted(Image.SAVE.keys()))
        raise ValueError(
            f"当前环境不支持写出 {fmt}。"
            f" 可用写出格式: {available}"
        )


def is_image_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in SUPPORTED_INPUT_EXTS


def _is_excluded_by_suffix(path: Path, exclude_suffixes: Sequence[str]) -> bool:
    return any(path.stem.endswith(s) for s in exclude_suffixes)


def iter_images(
    input_path: Path,
    recursive: bool = False,
    include_exts: Optional[Set[str]] = None,
    exclude_exts: Optional[Set[str]] = None,
    exclude_suffixes: Optional[Sequence[str]] = None,
) -> List[Path]:
    include_exts = include_exts or set()
    exclude_exts = exclude_exts or set()
    exclude_suffixes = exclude_suffixes or []

    if input_path.is_file():
        if not is_image_file(input_path):
            raise ValueError(f"Not a supported image file: {input_path}")
        ext = input_path.suffix.lower()
        if include_exts and ext not in include_exts:
            return []
        if ext in exclude_exts:
            return []
        if _is_excluded_by_suffix(input_path, exclude_suffixes):
            return []
        return [input_path]

    if not input_path.is_dir():
        raise FileNotFoundError(f"Input path not found: {input_path}")

    pattern = "**/*" if recursive else "*"
    files = []
    for p in input_path.glob(pattern):
        if not is_image_file(p):
            continue
        ext = p.suffix.lower()
        if include_exts and ext not in include_exts:
            continue
        if ext in exclude_exts:
            continue
        if _is_excluded_by_suffix(p, exclude_suffixes):
            continue
        files.append(p)
    return sorted(files, key=lambda p: p.name.lower())


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    i = 1
    while True:
        candidate = path.with_name(f"{stem}_{i}{suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def build_output_path(
    src: Path,
    out_dir: Optional[Path],
    suffix: str,
    ext: str,
    overwrite: bool,
) -> Path:
    dest_dir = out_dir if out_dir else src.parent
    ext = ext if ext.startswith(".") else f".{ext}"
    base = f"{src.stem}{suffix}{ext}"
    out = dest_dir / base
    ensure_parent(out)
    return out if overwrite else unique_path(out)


def open_image(path: Path) -> Image.Image:
    img = Image.open(path)
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass
    return img


def to_savable_mode(img: Image.Image, target_format: str) -> Image.Image:
    fmt = target_format.upper()
    if fmt == "JPEG":
        if img.mode in ("RGBA", "LA"):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            alpha = img.split()[-1]
            bg.paste(img.convert("RGBA"), mask=alpha)
            return bg
        if img.mode not in ("RGB", "L"):
            return img.convert("RGB")
    return img


def save_image(
    img: Image.Image,
    out_path: Path,
    fmt: str,
    quality: int = 90,
    optimize: bool = True,
    png_compress_level: int = 6,
) -> None:
    params = {}
    fmt = fmt.upper()

    if fmt in ("JPEG", "WEBP", "AVIF", "HEIC", "HEIF"):
        params["quality"] = max(1, min(100, quality))
        params["optimize"] = optimize
    elif fmt == "PNG":
        params["optimize"] = optimize
        params["compress_level"] = max(0, min(9, png_compress_level))
    else:
        params["optimize"] = optimize

    img.save(out_path, format=fmt, **params)
