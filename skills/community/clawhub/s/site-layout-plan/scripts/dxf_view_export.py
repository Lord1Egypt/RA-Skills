#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 R2010 出图 DXF 转成 R12「看图版」，供 CAD快速看图等只认 R12 的阅读器打开。

原因：部分国产看图软件（实测 CAD快速看图 macOS 版）对 AC1015 及以上 DXF
直接显示黑屏，但 R12（AC1009）正常。本脚本只做“可看/可量”的降级转换：
- LWPOLYLINE/POLYLINE -> POLYLINE（保留 bulge）
- MTEXT -> TEXT（取纯文本）
- DIMENSION -> 其几何块 INSERT（视觉不变，测不到关联标注）
- 图块递归转换；不支持的实体跳过并计数
- 写 VPORT *Active / $VIEWCTR，保证打开即可见全图（该看图软件不自动缩放）
不改变主 DXF（R2010）作为编辑/出图主交付。

用法：
  python3 scripts/dxf_view_export.py layout-structure.dxf [-o layout-structure-r12.dxf]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.bootstrap import ensure_runtime  # noqa: E402

ensure_runtime(__file__)

import ezdxf  # noqa: E402

SKIP = {"HATCH", "MPOLYGON", "WIPEOUT", "IMAGE", "LEADER", "MULTILEADER", "MLINE",
        "ELLIPSE", "SPLINE", "3DFACE", "ATTDEF", "ATTRIB", "TOLERANCE", "RAY", "XLINE"}


def _attrs(e: Any, doc: Any) -> Dict[str, Any]:
    a: Dict[str, Any] = {"layer": e.dxf.get("layer", "0")}
    color = int(e.dxf.get("color", 256))
    if color != 256:
        a["color"] = color
    lt = e.dxf.get("linetype", "BYLAYER")
    if lt and lt.upper() not in ("BYLAYER", "BYBLOCK") and doc.linetypes.has_entry(lt):
        a["linetype"] = lt
    return a


def _ensure_layer(doc: Any, src_layer: Any) -> None:
    name = src_layer.dxf.name
    if doc.layers.has_entry(name):
        return
    lt = src_layer.dxf.get("linetype", "CONTINUOUS")
    if not doc.linetypes.has_entry(lt):
        lt = "CONTINUOUS"
    doc.layers.add(name, color=int(src_layer.dxf.get("color", 7)), linetype=lt)


def _ensure_style(doc: Any, src_doc: Any, name: str) -> str:
    if not name or name.upper() == "STANDARD":
        return "STANDARD"
    if doc.styles.has_entry(name):
        return name
    src = src_doc.styles.get(name) if src_doc.styles.has_entry(name) else None
    font = src.dxf.get("font", "simsun.ttc") if src is not None else "simsun.ttc"
    doc.styles.add(name, font=font)
    return name


def _copy_text(e: Any, layout: Any, doc: Any, src: Any) -> None:
    style = _ensure_style(doc, src, e.dxf.get("style", "STANDARD"))
    a = _attrs(e, doc)
    a["style"] = style
    a["height"] = float(e.dxf.get("height", 2.5)) or 2.5
    a["rotation"] = float(e.dxf.get("rotation", 0.0))
    t = layout.add_text(e.dxf.text, dxfattribs=a)
    t.set_placement(e.dxf.insert)


def _copy_mtext(e: Any, layout: Any, doc: Any, src: Any) -> None:
    style = _ensure_style(doc, src, e.dxf.get("style", "STANDARD"))
    a = _attrs(e, doc)
    a["style"] = style
    a["height"] = float(e.dxf.get("char_height", 2.5)) or 2.5
    a["rotation"] = float(e.dxf.get("rotation", 0.0))
    t = layout.add_text(e.plain_text(), dxfattribs=a)
    t.set_placement(e.dxf.insert)


def _copy_polyline(e: Any, layout: Any, doc: Any, src: Any) -> None:
    pts: List[Tuple[float, float]] = []
    bulges: List[float] = []
    if e.dxftype() == "LWPOLYLINE":
        for x, y, b in e.get_points("xyb"):
            pts.append((float(x), float(y)))
            bulges.append(float(b))
        closed = bool(e.closed)
    else:
        for v in e.vertices:
            pts.append((float(v.dxf.location.x), float(v.dxf.location.y)))
            bulges.append(float(v.dxf.get("bulge", 0.0)))
        closed = bool(e.is_closed)
    if len(pts) < 2:
        return
    pl = layout.add_polyline2d(pts, close=closed, dxfattribs=_attrs(e, doc))
    for i, b in enumerate(bulges):
        if b:
            pl.vertices[i].dxf.bulge = b


def _copy_entity(e: Any, layout: Any, doc: Any, src: Any, blocks: Dict[str, str], skipped: List[str]) -> None:
    t = e.dxftype()
    a = _attrs(e, doc)
    if t == "LINE":
        layout.add_line(e.dxf.start, e.dxf.end, dxfattribs=a)
    elif t in ("LWPOLYLINE", "POLYLINE"):
        if e.dxftype() == "POLYLINE" and (e.is_3d_polyline or e.is_2d_polyline is False):
            skipped.append(t)
            return
        _copy_polyline(e, layout, doc, src)
    elif t == "CIRCLE":
        layout.add_circle(e.dxf.center, e.dxf.radius, dxfattribs=a)
    elif t == "ARC":
        layout.add_arc(e.dxf.center, e.dxf.radius, e.dxf.start_angle, e.dxf.end_angle, dxfattribs=a)
    elif t == "POINT":
        layout.add_point(e.dxf.location, dxfattribs=a)
    elif t == "SOLID":
        layout.add_solid([e.dxf.vtx0, e.dxf.vtx1, e.dxf.vtx2, e.dxf.vtx3], dxfattribs=a)
    elif t == "TEXT":
        _copy_text(e, layout, doc, src)
    elif t == "MTEXT":
        _copy_mtext(e, layout, doc, src)
    elif t == "INSERT":
        name = _copy_block(doc, src, e.dxf.name, blocks, skipped)
        if not name:
            skipped.append("INSERT:" + e.dxf.name)
            return
        a.update({"xscale": float(e.dxf.get("xscale", 1.0)),
                  "yscale": float(e.dxf.get("yscale", 1.0)),
                  "zscale": float(e.dxf.get("zscale", 1.0)),
                  "rotation": float(e.dxf.get("rotation", 0.0))})
        layout.add_blockref(name, e.dxf.insert, dxfattribs=a)
    elif t == "DIMENSION":
        geom = e.dxf.get("geometry", "")
        if not geom or geom not in src.blocks:
            skipped.append("DIMENSION")
            return
        name = _copy_block(doc, src, geom, blocks, skipped)
        if name:
            layout.add_blockref(name, (0, 0, 0), dxfattribs=a)
        else:
            skipped.append("DIMENSION")
    elif t in SKIP:
        skipped.append(t)
    else:
        skipped.append(t)


def _copy_block(doc: Any, src: Any, name: str, blocks: Dict[str, str], skipped: List[str]) -> str:
    if name in blocks:
        return blocks[name]
    if name not in src.blocks or name.lower().startswith(("*model_space", "*paper_space")):
        return ""
    blocks[name] = name  # 占位，防递归
    try:
        blk = doc.blocks.get(name) if name in doc.blocks else doc.blocks.new(name)
    except Exception:
        blocks.pop(name, None)
        raise
    if name in doc.blocks and name in ("_ARCHTICK", "_CLOSEDFILLED", "_CLOSEDBLANK",
                                               "_DOT", "_DOTSMALL", "_DOTBLANK", "_OBLIQUE",
                                               "_OPEN", "_OPEN90", "_OPEN30", "_SMALL",
                                               "_NONE", "_BOX", "_BOXFILLED", "_BOXBLANK"):
        return name
    for e in src.blocks[name]:
        try:
            _copy_entity(e, blk, doc, src, blocks, skipped)
        except Exception:
            skipped.append(e.dxftype() + ":" + name)
    return name


def _set_active_view(doc: Any, box: Any) -> None:
    """把 *Active 视口对准图形范围。

    实测 CAD快速看图（macOS）打开时不执行 zoom-extents，直接按 DXF 的
    VPORT *Active 中心/高度定位；不设置就停在上次视图或原点附近，
    大坐标总图因此表现为全黑。这里写入覆盖全图的初始视图。
    """
    try:
        vp = doc.viewports.get("*Active")[0]
        w = float(box.extmax.x) - float(box.extmin.x)
        h = float(box.extmax.y) - float(box.extmin.y)
        aspect = 1.6
        view_h = max(h, w / aspect if aspect else h, 1.0) * 1.06
        vp.dxf.center = ((float(box.extmin.x) + float(box.extmax.x)) / 2.0,
                         (float(box.extmin.y) + float(box.extmax.y)) / 2.0)
        vp.dxf.height = view_h
        vp.dxf.aspect_ratio = aspect
        doc.header["$VIEWCTR"] = (vp.dxf.center[0], vp.dxf.center[1], 0.0)
        doc.header["$VIEWSIZE"] = view_h
    except Exception:
        pass


def convert(src_path: Path, out_path: Path) -> Dict[str, Any]:
    src = ezdxf.readfile(str(src_path))
    doc = ezdxf.new("R12", setup=True)
    doc.header["$INSBASE"] = (0, 0, 0)
    for layer in src.layers:
        try:
            _ensure_layer(doc, layer)
        except Exception:
            pass
    blocks: Dict[str, str] = {}
    skipped: List[str] = []
    msp = doc.modelspace()
    for e in src.modelspace():
        try:
            _copy_entity(e, msp, doc, src, blocks, skipped)
        except Exception:
            skipped.append(e.dxftype())

    # 平移到原点：总图常带 5e8/4e9 级工程坐标，部分看图软件用 float32 会精度失效
    from ezdxf import bbox as ezbbox
    from ezdxf.math import Matrix44
    box0 = ezbbox.extents(msp, fast=False)
    offset = (0.0, 0.0)
    if box0.has_data:
        offset = (float(box0.extmin.x), float(box0.extmin.y))
        if abs(offset[0]) > 1e5 or abs(offset[1]) > 1e5:
            mat = Matrix44.translate(-offset[0], -offset[1], 0.0)
            for e in list(msp):
                try:
                    e.transform(mat)
                except Exception:
                    skipped.append("SHIFT:" + e.dxftype())
    box = ezbbox.extents(msp, fast=False)
    if box.has_data:
        msp.dxf.extmin = box.extmin
        msp.dxf.extmax = box.extmax
        doc.header["$EXTMIN"] = box.extmin
        doc.header["$EXTMAX"] = box.extmax
        _set_active_view(doc, box)
    try:
        doc.header["$USERR1"] = offset[0]
        doc.header["$USERR2"] = offset[1]
    except Exception:
        pass
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(str(out_path))

    check = ezdxf.readfile(str(out_path))
    from collections import Counter
    counts = Counter(e.dxftype() for e in check.modelspace())
    return {
        "source": str(src_path),
        "output": str(out_path),
        "dxfversion": check.dxfversion,
        "entities": dict(sorted(counts.items())),
        "blocks": len(doc.blocks),
        "skipped": sorted(set(skipped)),
        "shift_offset": {"x": offset[0], "y": offset[1]},
    }


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="R2010 出图 DXF -> R12 看图版")
    ap.add_argument("dxf", nargs="+", help="源 DXF（可多个）")
    ap.add_argument("-o", "--out", help="输出文件；仅单个输入时可用")
    ap.add_argument("--out-dir", help="输出目录，文件名加 -r12 后缀")
    ap.add_argument("--json", action="store_true", help="输出 JSON 结果")
    args = ap.parse_args(argv)
    if args.out and len(args.dxf) > 1:
        ap.error("-o 只能配合单个输入；多文件请用 --out-dir")

    results = []
    for raw in args.dxf:
        src = Path(raw)
        if args.out:
            out = Path(args.out)
        else:
            base_dir = Path(args.out_dir) if args.out_dir else src.parent
            out = base_dir / (src.stem + "-r12.dxf")
        r = convert(src, out)
        results.append(r)
        if not args.json:
            print("{} -> {}  {}  skipped={}".format(
                src.name, out.name, r["dxfversion"], ",".join(r["skipped"]) or "none"))
    if args.json:
        import json
        print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
