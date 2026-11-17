#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dev_dxf.py - 已停用：本技能不再内置 DXF/DWG 直读层。

正式链路固定：cad-file-reader → lis-skill-bus → 算量技能。
历史开发直读实现只保留在 $HOME/.codex/backups/suanliang-s9/ 的改动前备份里，
不随技能发布，也不提供 CAD_DEV_DXF 等环境变量重启生产直读。
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


class DevDirectDisabled(RuntimeError):
    pass


_MESSAGE = (
    "[dev_dxf] 本技能已删除 DXF/DWG 直读层，生产脚本不再加载 CAD 直读库。\n"
    "正式链路：cad-file-reader 产出 cad-contract/v1 → lis-skill-bus → 算量技能消费契约。"
)


def _disabled(*_args, **_kwargs):
    raise DevDirectDisabled(_MESSAGE)


def readfile(path):
    _disabled(path)


def new(version="R2010"):
    _disabled(version)


def plain_mtext(text):
    _disabled(text)


def make_path(entity):
    _disabled(entity)


def expand_drawing_geometry(path: str, max_depth: int = 8) -> list[dict[str, Any]]:
    _disabled(path, max_depth)


def layer_map(path: str, handles: list[int]) -> dict[int, str]:
    _disabled(path, handles)


def write_dxf(out_path: Path, bbox: list[float], margin: float,
              segments: list[dict[str, Any]], layers: dict[int, str]) -> None:
    _disabled(out_path, bbox, margin, segments, layers)


class _RawProxy:
    def __getattr__(self, name):
        _disabled(name)


raw = _RawProxy()

__all__ = [
    "DevDirectDisabled", "readfile", "new", "plain_mtext", "make_path",
    "expand_drawing_geometry", "layer_map", "write_dxf", "raw",
]

if __name__ == "__main__":
    import sys
    sys.stderr.write(_MESSAGE + "\n")
    raise SystemExit(23)
