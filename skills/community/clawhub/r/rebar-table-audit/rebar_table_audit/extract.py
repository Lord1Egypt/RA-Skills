"""从已打开的 ezdxf Drawing 里抽取文字与线段图元，展开块参照（含嵌套），带 handle 路径证据。

handle 路径格式：``INSERT:<handle>>INSERT:<handle>>...>TEXT:<handle>``。
每一段的 handle 都是"定义处"的真实 handle——顶层直接实体用它在所在布局里的 handle；
块参照内部的虚拟实体用 ezdxf 的 ``source_of_copy`` 找回它在块定义里的真实 handle。
这样同一份输入重复运行，handle 路径完全确定、可复现。

文字在进一步解析前会先做一次编码归一化（见 ``normalize_text``）：ODA 和 LibreDWG 两条
转换链对同一个符号可能写出不同形式（比如 LibreDWG 常把控制字符写成 ``\\U+00CC`` 这种
DXF unicode 转义，ODA 直接给出解码后的字符 ``Ì``；ezdxf 遇到非 utf-8 字节兜底解码时也
可能产生孤立代理项）。``TextItem.text`` 是归一化后的文字（后续所有匹配都用这个），
``TextItem.raw`` 保留归一化前的原始文字，两者都会进 evidence，方便审核对比。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from ezdxf.lldxf.encoding import (
    decode_dxf_unicode,
    decode_mif_to_unicode,
    has_dxf_unicode,
    has_mif_encoding,
)
from ezdxf.math import Vec3

TEXT_LIKE = {"TEXT", "MTEXT", "ATTRIB"}
LINE_LIKE = {"LINE", "LWPOLYLINE", "POLYLINE"}

# ezdxf 用 surrogateescape 语义兜底解码非 utf-8 字节时，每个解不出来的字节 b 会变成
# chr(0xDC00 + b)；这里按同样的语义映射回去（0xDC80~0xDCFF -> 0x80~0xFF，Latin-1 下
# 这个范围的码位和字节值是恒等映射，U+DCCC -> 字节 0xCC -> 'Ì'）。
_SURROGATE_LOW, _SURROGATE_HIGH = 0xDC80, 0xDCFF


def normalize_text(raw: str) -> str:
    """把几种常见的 DWG/DXF 转换链编码差异归一化成同一种表示。"""
    if not raw:
        return raw
    s = raw
    if has_dxf_unicode(s):
        s = decode_dxf_unicode(s)
    if has_mif_encoding(s):
        s = decode_mif_to_unicode(s)
    if any(_SURROGATE_LOW <= ord(c) <= _SURROGATE_HIGH for c in s):
        s = "".join(chr(ord(c) - 0xDC00) if _SURROGATE_LOW <= ord(c) <= _SURROGATE_HIGH else c for c in s)
    return s


@dataclass
class TextItem:
    text: str  # 归一化后的文字，后续匹配/解析都用这个
    raw: str  # 归一化前的原始文字，进 evidence 供审核对比
    x: float
    y: float
    height: float
    handle_path: str
    layout: str


@dataclass
class SegmentItem:
    x1: float
    y1: float
    x2: float
    y2: float
    handle_path: str
    layout: str


def _own_or_source_handle(entity) -> Optional[str]:
    if getattr(entity, "is_virtual", False):
        src = entity.source_of_copy
        if src is not None and src.dxf.hasattr("handle"):
            return src.dxf.handle
        return None
    if entity.dxf.hasattr("handle"):
        return entity.dxf.handle
    return None


def _text_position(entity) -> tuple[float, float]:
    """文字的 WCS 定位点 (x, y)。

    TEXT / ATTRIB 的 insert / align_point 是 OCS 坐标：块参照被奇数次镜像（xscale*yscale<0）后，
    ``INSERT.virtual_entities()`` 展开出的 TEXT 拉伸方向为 (0, 0, -1)，OCS 的 x 轴与 WCS 相反，
    必须经 ``ocs().to_wcs`` 转换（拉伸方向为 (0, 0, 1) 时是恒等变换）。
    MTEXT 的 insert 按 DXF 规范就是 WCS，展开后 ezdxf 也已按 WCS 变换好，不能再转。
    """
    dxftype = entity.dxftype()
    if dxftype == "MTEXT":
        p = entity.dxf.insert
        return float(p.x), float(p.y)
    # TEXT / ATTRIB：对齐感知，halign/valign 非默认时真实定位点是 align_point
    try:
        _align, p1, _p2 = entity.get_placement()
    except Exception:
        p1 = entity.dxf.insert
    w = entity.ocs().to_wcs(Vec3(p1))
    return float(w.x), float(w.y)


def _text_string(entity) -> str:
    dxftype = entity.dxftype()
    if dxftype == "MTEXT":
        return entity.plain_text()
    if dxftype in ("TEXT", "ATTRIB"):
        return entity.dxf.text
    return ""


def _text_height(entity) -> float:
    try:
        if entity.dxftype() == "MTEXT":
            return float(entity.dxf.char_height)
        return float(entity.dxf.height)
    except Exception:
        return 0.0


def _polyline_points(entity) -> list[tuple[float, float]]:
    """多段线顶点的 WCS (x, y) 列表。

    LWPOLYLINE 与 2D POLYLINE 的顶点是 OCS 坐标（z 取 elevation），奇数次镜像的块展开后拉伸方向为
    (0, 0, -1)，必须经 ``ocs().to_wcs`` 转换（拉伸方向为 (0, 0, 1) 时是恒等变换）；
    3D POLYLINE 的顶点本来就是 WCS，不转。
    """
    dxftype = entity.dxftype()
    pts: list[tuple[float, float]] = []
    if dxftype == "LWPOLYLINE":
        ocs = entity.ocs()
        elevation = float(entity.dxf.get("elevation", 0.0))
        for p in entity.get_points("xy"):
            w = ocs.to_wcs(Vec3(p[0], p[1], elevation))
            pts.append((float(w.x), float(w.y)))
        if entity.closed and pts:
            pts.append(pts[0])
    elif dxftype == "POLYLINE":
        is_2d = bool(getattr(entity, "is_2d_polyline", False))
        ocs = entity.ocs() if is_2d else None
        # 与 ezdxf 的 Polyline.transform 一致：2D 多段线的 z 以 elevation 为准，没有 elevation 才用顶点自带的 z
        elevation = entity.dxf.elevation.z if is_2d and entity.dxf.hasattr("elevation") else None
        for v in entity.vertices:
            loc = v.dxf.location
            if ocs is not None:
                if elevation is not None:
                    loc = Vec3(loc).replace(z=elevation)
                loc = ocs.to_wcs(Vec3(loc))
            pts.append((float(loc.x), float(loc.y)))
        if entity.is_closed and pts:
            pts.append(pts[0])
    return pts


class ExtractionResult:
    def __init__(self) -> None:
        self.texts: list[TextItem] = []
        self.segments: list[SegmentItem] = []
        self.skipped: list[tuple[str, str]] = []  # (dxftype, reason)


def _walk(entity, path_prefix: list[str], layout_name: str, result: ExtractionResult, insert_chain: frozenset, depth: int) -> None:
    if depth > 20:
        result.skipped.append((entity.dxftype(), "块嵌套超过 20 层，判定为循环引用，已停止展开"))
        return
    dxftype = entity.dxftype()
    if dxftype == "INSERT":
        own_handle = _own_or_source_handle(entity)
        chain_key = insert_chain | {(tuple(path_prefix), own_handle)}
        if (tuple(path_prefix), own_handle) in insert_chain:
            result.skipped.append(("INSERT", f"检测到块自引用循环，handle={own_handle}，已跳过"))
            return
        new_prefix = path_prefix + [f"INSERT:{own_handle}"]

        def _on_skip(skipped_entity, reason):
            result.skipped.append((skipped_entity.dxftype(), reason))

        for child in entity.virtual_entities(skipped_entity_callback=_on_skip):
            _walk(child, new_prefix, layout_name, result, chain_key, depth + 1)
        return

    handle = _own_or_source_handle(entity)
    leaf = f"{dxftype}:{handle}"
    handle_path = ">".join(path_prefix + [leaf]) if path_prefix else leaf

    if dxftype in TEXT_LIKE:
        raw_text = _text_string(entity)
        if raw_text is None or raw_text.strip() == "":
            return
        x, y = _text_position(entity)
        normalized = normalize_text(raw_text)
        result.texts.append(TextItem(text=normalized, raw=raw_text, x=x, y=y, height=_text_height(entity), handle_path=handle_path, layout=layout_name))
    elif dxftype == "LINE":
        p1, p2 = entity.dxf.start, entity.dxf.end
        result.segments.append(SegmentItem(float(p1.x), float(p1.y), float(p2.x), float(p2.y), handle_path, layout_name))
    elif dxftype in ("LWPOLYLINE", "POLYLINE"):
        pts = _polyline_points(entity)
        for a, b in zip(pts, pts[1:]):
            result.segments.append(SegmentItem(a[0], a[1], b[0], b[1], handle_path, layout_name))


def extract_from_layout(layout, layout_name: str, result: ExtractionResult) -> None:
    for entity in layout:
        try:
            _walk(entity, [], layout_name, result, frozenset(), 0)
        except Exception as exc:  # 单个图元展开失败不应中断整份图纸
            result.skipped.append((entity.dxftype(), f"展开失败：{exc}"))


def extract_all(doc) -> ExtractionResult:
    """遍历模型空间 + 所有布局，展开块参照，收集文字与线段。"""
    result = ExtractionResult()
    extract_from_layout(doc.modelspace(), "Model", result)
    for layout in doc.layouts:
        if layout.name == "Model":
            continue
        extract_from_layout(layout, layout.name, result)
    return result
