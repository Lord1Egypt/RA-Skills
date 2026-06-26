#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Union


def ensure_file(path: Union[str, Path]) -> Path:
    """Validate that path exists and is a file; return resolved Path."""
    p = Path(path).resolve()
    if not p.exists():
        raise FileNotFoundError(f"音频文件不存在：{p}")
    if not p.is_file():
        raise ValueError(f"路径不是文件：{p}")
    return p


def ensure_ffmpeg_exists() -> None:
    """Ensure ffmpeg is available in PATH."""
    if shutil.which("ffmpeg") is None:
        raise FileNotFoundError("ffmpeg 未安装或不在 PATH 中")


def resolve_edge_tts(bin_override: str | None = None) -> str:
    """Resolve edge-tts executable path or raise if missing."""
    candidates = []
    if bin_override:
        candidates.append(bin_override)
    env = os.environ.get("EDGE_TTS_BIN")
    if env:
        candidates.append(env)
    which = shutil.which("edge-tts")
    if which:
        candidates.append(which)
    
    for c in candidates:
        if c and os.path.exists(c):
            return c
    
    # Fallback: try using Python module
    try:
        import edge_tts
        return "python -m edge_tts"
    except ImportError:
        pass
    
    raise FileNotFoundError(f"edge-tts 未找到：{bin_override or os.environ.get('EDGE_TTS_BIN') or 'edge-tts'}")
