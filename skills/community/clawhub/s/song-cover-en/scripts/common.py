"""Shared helpers for the pipeline stages: JSON, wav IO and ffmpeg lookup.

Kept dependency-light on purpose: importing this module must not pull in torch or
librosa, otherwise even `--help` becomes slow.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# stage 02 writes everything at this rate; stage 03 resamples up to 44.1 kHz itself
SR = 22050


def ffmpeg_exe() -> str:
    """Prefer the ffmpeg binary bundled with imageio-ffmpeg, else PATH."""
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def load_mono(path: str | Path, sr: int = SR):
    """Read any soundfile-supported file as mono float32 at `sr`."""
    import numpy as np
    import soundfile as sf
    import soxr

    y, got = sf.read(str(path), dtype="float32", always_2d=True)
    y = y.mean(axis=1)
    if got != sr:
        y = soxr.resample(y.astype(np.float32), got, sr)
    return np.ascontiguousarray(y, dtype=np.float32)


def save_wav(path: str | Path, y, sr: int = SR) -> None:
    import soundfile as sf

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(p), y, sr, subtype="PCM_16")


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path: str | Path, obj: Any, indent: int = 2) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=indent), encoding="utf-8")
