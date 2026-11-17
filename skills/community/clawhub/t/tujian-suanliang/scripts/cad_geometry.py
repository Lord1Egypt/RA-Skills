#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cad_geometry.py - 兼容薄壳（s5 起禁止直读 DWG/DXF）。

正式链路固定：cad-file-reader → lis-skill-bus → 算量技能。
历史 `cad_geometry.sh 图纸.dwg` 展开入口已停用；纯数学函数迁到 cad_geometry_math.py，
老调用方仍可从本模块 import（向后兼容一个版本周期）。
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Optional

from cad_geometry_math import (  # noqa: F401  (re-export)
    _apply,
    _compose,
    _dxf_layer_name,
    _insert_matrix,
    _label_fallback_bbox,
    _label_like,
    _sibling_title_re,
    _svg_color,
    _svg_escape,
    color_for_layer,
    distance_to_polygon,
    find_sheet_bbox,
    point_in_bbox,
    point_in_polygon,
    write_svg,
)

MIGRATION_HINT = (
    "[cad_geometry] 已停用 DWG/DXF 直读展开；几何提取已迁移到 cad-file-reader packs/structural-geometry，请用 cad_structural_geometry.sh。\n"
    "正式链路：cad-file-reader 产出 cad-contract/v1 → 算量技能消费契约。\n"
    "纯数学/图框函数请改从 cad_geometry_math import；本技能不提供任何 DXF/DWG 直读开关，图纸一律先由 cad-file-reader 产出 cad-contract/v1。"
)


def expand_drawing_geometry(path: str, max_depth: int = 8) -> list[dict[str, Any]]:
    from dev_dxf import expand_drawing_geometry as _impl
    return _impl(path, max_depth=max_depth)


def layer_map(path: str, handles: list[int]) -> dict[int, str]:
    from dev_dxf import layer_map as _impl
    return _impl(path, handles)


def write_dxf(out_path: Path, bbox: list[float], margin: float,
              segments: list[dict[str, Any]], layers: dict[int, str]) -> None:
    from dev_dxf import write_dxf as _impl
    return _impl(out_path, bbox, margin, segments, layers)


def main() -> int:
    print(MIGRATION_HINT, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
