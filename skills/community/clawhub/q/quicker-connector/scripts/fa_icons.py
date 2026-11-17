#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FontAwesome 5 图标 SVG 数据访问层

数据来源（二选一，自动回退）：
1. data/fontawesome5_svg_index.json.gz —— 预提取的全量索引（5996 个图标，
   覆盖 Solid / Regular / Light / Brands 四种样式），推荐，无额外依赖
2. Quicker 自带的 FontAwesomeIconsWpf.dll（需 pythonnet）—— 用于索引缺失时按需补充

索引结构：{"Light_SortDown": ["M287.968 ...", 320, 512], ...}
        键 = Quicker 图标写法（fa: 后面的部分），值 = [SVG path, viewBox宽, viewBox高]
"""
from __future__ import annotations

import gzip
import json
import os
from pathlib import Path
from typing import Dict, Optional, Tuple

_INDEX_FILE = Path(__file__).resolve().parent.parent / "data" / "fontawesome5_svg_index.json.gz"

_index: Optional[Dict[str, Tuple[str, int, int]]] = None


def _load_index() -> Dict[str, Tuple[str, int, int]]:
    global _index
    if _index is None:
        if not _INDEX_FILE.exists():
            _index = {}
        else:
            with gzip.open(_INDEX_FILE, "rt", encoding="utf-8") as f:
                _index = {k: (v[0], int(v[1]), int(v[2])) for k, v in json.load(f).items()}
    return _index


def _extract_from_dll(keys) -> Dict[str, Tuple[str, int, int]]:
    """从 Quicker 安装目录的 FontAwesomeIconsWpf.dll 按需提取（需 pythonnet）。"""
    result: Dict[str, Tuple[str, int, int]] = {}
    try:
        import clr  # type: ignore
    except ImportError:
        return result

    dll = None
    for cand in (
        Path(os.environ.get("PROGRAMFILES", r"C:\Program Files")) / "Quicker" / "FontAwesomeIconsWpf.dll",
        Path(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")) / "Quicker" / "FontAwesomeIconsWpf.dll",
    ):
        if cand.exists():
            dll = cand
            break
    if dll is None:
        return result

    try:
        clr.AddReference(str(dll))
        import System  # type: ignore

        asm = System.Reflection.Assembly.LoadFrom(str(dll))
        etype = asm.GetType("FontAwesome5.EFontAwesomeIcon")
        atype = asm.GetType("FontAwesome5.FontAwesomeSvgInformationAttribute")
        names = set(System.Enum.GetNames(etype))
        for key in keys:
            if key not in names:
                continue
            ats = etype.GetField(key).GetCustomAttributes(atype, False)
            if not ats:
                continue
            at = ats[0]
            result[key] = (str(at.Path), int(at.Width), int(at.Height))
    except Exception:
        pass
    return result


def get(key: str) -> Optional[Tuple[str, int, int]]:
    """取图标数据，key 形如 'Light_SortDown'。找不到返回 None。"""
    idx = _load_index()
    if key in idx:
        return idx[key]
    # 索引缺失时尝试从 DLL 补充并回写缓存
    got = _extract_from_dll([key])
    if got:
        idx.update(got)
        _save_index(idx)
        return got[key]
    return None


def contains(key: str) -> bool:
    return key in _load_index()


def _save_index(idx) -> None:
    try:
        _INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
        payload = {k: [v[0], v[1], v[2]] for k, v in idx.items()}
        with gzip.open(_INDEX_FILE, "wt", encoding="utf-8", compresslevel=9) as f:
            json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
    except Exception:
        pass


def total() -> int:
    return len(_load_index())
