"""Resolve the runtime paths this skill needs.

Everything the pipeline reads or writes lives under one directory::

    <SONG_COVER_HOME>/
        libs/       python dependencies (torch, librosa, onnxruntime, ...)
        cache/      model weights (UVR, RMVPE, SoulX-Singer, Whisper)
        runs/       one work directory per song
        workspace/  scratch space

Set ``SONG_COVER_HOME`` to override.  When it is unset the skill looks for
``~/.song-cover-en``, then ``<skill>/.runtime``.  The old directory this skill
was originally developed in (``D:\\DSH\\work\\sing``) is kept as a last-resort
fallback so an existing install keeps working.

Individual locations can be overridden separately with ``SONG_COVER_LIBS``,
``SONG_COVER_CACHE``, ``SONG_COVER_RUNS``, ``SONG_COVER_WORKSPACE`` and
``SONG_COVER_REF_HUMAN``.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent


def _first_dir(*cands: Path) -> Path:
    for c in cands:
        if c.is_dir():
            return c
    return cands[0]


_env_root = os.environ.get("SONG_COVER_HOME", "").strip()
ROOT = (Path(_env_root).expanduser() if _env_root else _first_dir(
    Path.home() / ".song-cover-en",
    SKILL_DIR / ".runtime",
    Path(r"D:\DSH\work\sing"),
))

LIBS = Path(os.environ.get("SONG_COVER_LIBS") or ROOT / "libs")
CACHE = Path(os.environ.get("SONG_COVER_CACHE") or ROOT / "cache")
RUNS = Path(os.environ.get("SONG_COVER_RUNS") or ROOT / "runs")
WORKSPACE = Path(os.environ.get("SONG_COVER_WORKSPACE") or ROOT / "workspace")

# model locations, all under cache/ by default
SOULX_SRC = CACHE / "soulx_src" / "SoulX-Singer-main"
SRC = SOULX_SRC
CKPT = CACHE / "soulx" / "model.pt"
CFG = CACHE / "soulx" / "config.yaml"
RMVPE = CACHE / "rmvpe" / "rmvpe.onnx"
WHISPER = CACHE / "whisper-base"
UVR_MODEL = CACHE / "UVR-MDX-NET-Voc_FT.onnx"

# a clean human English vocal used as the spectral reference for spectral_match.py
REF_HUMAN = Path(os.environ.get("SONG_COVER_REF_HUMAN")
                 or ROOT / "smoke_out" / "_ref_human.wav")


def add_libs() -> None:
    """Put the dependency dir and the SoulX source tree on sys.path."""
    for p in (str(LIBS), str(SOULX_SRC)):
        if p not in sys.path:
            sys.path.insert(0, p)


_FONT_DIRS = [
    Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts",
    Path("/usr/share/fonts"),
    Path("/usr/local/share/fonts"),
    Path("/System/Library/Fonts"),
    Path.home() / ".fonts",
]


def _font(env_var: str, *names: str) -> str:
    """Return the first existing font file, or "" when none is installed."""
    override = os.environ.get(env_var)
    if override:
        return override
    for d in _FONT_DIRS:
        for n in names:
            p = d / n
            if p.exists():
                return str(p)
    for n in names:
        for d in _FONT_DIRS:
            if d.is_dir():
                for p in d.rglob(n):
                    return str(p)
    return ""


FONT_EN = _font("SONG_COVER_FONT_EN", "georgiab.ttf",
                "DejaVuSerif-Bold.ttf", "NotoSerif-Bold.ttf")
FONT_EN_R = _font("SONG_COVER_FONT_EN_R", "georgia.ttf",
                  "DejaVuSerif.ttf", "NotoSerif-Regular.ttf")
FONT_CN = _font("SONG_COVER_FONT_CN", "msyh.ttc",
                "NotoSansCJK-Regular.ttc", "SourceHanSansSC-Regular.otf")


def pil_font(kind: str, size: int):
    """Load one of the three fonts above, degrading to Pillow's default."""
    from PIL import ImageFont

    path = {"en": FONT_EN, "en_r": FONT_EN_R, "cn": FONT_CN}[kind]
    if path:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    try:
        return ImageFont.load_default(size=size)
    except TypeError:          # Pillow < 10.1
        return ImageFont.load_default()
