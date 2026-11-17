"""对齐感知定位、块参照展开的单元测试（不依赖表格结构）。"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import ezdxf
import pytest
from ezdxf.enums import TextEntityAlignment
from ezdxf.math import Matrix44, Vec3

from rebar_table_audit import extract


def test_text_position_uses_align_point_not_insert():
    """halign/valign 非默认时，真实定位点是 align_point，不是 insert——故意把 insert 改到别处来验证。"""
    doc = ezdxf.new()
    msp = doc.modelspace()
    t = msp.add_text("X", dxfattribs={"height": 3.5})
    t.set_placement((50.0, 50.0), align=TextEntityAlignment.MIDDLE_CENTER)
    t.dxf.insert = (0.0, 0.0, 0.0)  # 人为让 insert 不代表可视位置
    x, y = extract._text_position(t)
    assert abs(x - 50.0) < 1e-6
    assert abs(y - 50.0) < 1e-6


def test_nested_insert_handle_path_and_transform():
    doc = ezdxf.new()
    msp = doc.modelspace()
    inner = doc.blocks.new("INNER")
    inner_text = inner.add_text("hello", dxfattribs={"height": 1.0, "insert": (1.0, 1.0)})
    outer = doc.blocks.new("OUTER")
    outer_insert = outer.add_blockref("INNER", (5.0, 5.0))
    top_insert = msp.add_blockref("OUTER", (10.0, 10.0))

    result = extract.extract_all(doc)
    assert len(result.texts) == 1
    item = result.texts[0]
    assert abs(item.x - 16.0) < 1e-6  # 1+5+10
    assert abs(item.y - 16.0) < 1e-6
    expected_path = f"INSERT:{top_insert.dxf.handle}>INSERT:{outer_insert.dxf.handle}>TEXT:{inner_text.dxf.handle}"
    assert item.handle_path == expected_path


def test_normalize_text_unifies_encoding_variants_to_same_result():
    """ODA 直接给出解码后的字符，LibreDWG 常写成 \\U+XXXX 转义，ezdxf 兜底解码非 utf-8
    字节时可能产生孤立代理项——三种写法归一化后必须是同一个字符串。"""
    variants = [
        "Ì25",  # ODA 风格：直接是解码后的字符
        "\\U+00CC25",  # LibreDWG 风格：DXF unicode 转义
        "\udccc25",  # ezdxf surrogateescape 兜底解码产生的孤立代理项（U+DCCC -> 字节 0xCC）
    ]
    normalized = {extract.normalize_text(v) for v in variants}
    assert normalized == {"Ì25"}


# ---------------------------------------------------------------------------
# 镜像（负比例）块参照：奇数次镜像时 ezdxf 展开出的平面图元拉伸方向变成 (0,0,-1)，
# TEXT / LWPOLYLINE / 2D POLYLINE 的坐标是 OCS，必须转成 WCS 再用；
# LINE、3D POLYLINE、MTEXT.insert 本来就是 WCS，不能再转。
# 期望坐标全部用 Matrix44 手算，不经被测代码。
# ---------------------------------------------------------------------------

# INNER 块内的局部几何（块坐标）。各图元位置互不相同，防止"取错图元"碰巧对上。
_LINE = [(10.0, 0.0, 0.0), (20.0, 5.0, 0.0)]
_TEXT_POS = (5.0, 3.0, 0.0)
_TEXT_ALIGN_POS = (7.0, 4.0, 0.0)  # 居中对齐文字的真实定位点（align_point）
_MTEXT_POS = (6.0, 8.0, 0.0)
_LWP = [(0.0, 0.0, 0.0), (4.0, 0.0, 0.0), (4.0, 2.0, 0.0)]  # 建在 elevation=7 上
_LWP_BULGE = [(0.0, 10.0, 0.0), (4.0, 10.0, 0.0), (4.0, 14.0, 0.0)]  # 第二个点带 bulge=0.5
_POLY2D = [(0.0, 20.0, 3.0), (4.0, 20.0, 3.0), (4.0, 24.0, 3.0)]  # 建在 elevation=3 上
_POLY3D = [(0.0, 30.0, 1.0), (4.0, 30.0, 2.0), (4.0, 34.0, 3.0)]


def _insert_matrix(ins, sx, sy, rot_deg):
    """块 -> 父坐标系的变换（手算用）：先缩放、再绕 Z 旋转、最后平移。
    ezdxf 的 Matrix44 是行向量约定，chain 按书写顺序依次施加。"""
    return Matrix44.chain(
        Matrix44.scale(sx, sy, 1.0),
        Matrix44.z_rotate(math.radians(rot_deg)),
        Matrix44.translate(ins[0], ins[1], 0.0),
    )


def _xy(v):
    v = Vec3(v)
    return (float(v.x), float(v.y))


def _seg_xy(points, m):
    """折线点列经 m 变换后的 (x1, y1, x2, y2) 段列表。"""
    tp = [Vec3(m.transform(Vec3(p))) for p in points]
    return [(a.x, a.y, b.x, b.y) for a, b in zip(tp, tp[1:])]


def _leaf(item):
    return item.handle_path.rsplit(">", 1)[-1]


def _segments_of(result, dxftype, handle):
    return [(s.x1, s.y1, s.x2, s.y2) for s in result.segments if _leaf(s) == f"{dxftype}:{handle}"]


def _max_abs_diff(got, expected):
    assert len(got) == len(expected), (got, expected)
    return max((abs(a - b) for g, e in zip(got, expected) for a, b in zip(g, e)), default=0.0)


def _build_inner_block(doc):
    """INNER 块：LINE、默认对齐 TEXT、居中对齐 TEXT（insert 故意与 align_point 不同）、MTEXT、
    带 elevation 的 LWPOLYLINE、带 bulge 的 LWPOLYLINE、带 elevation 的 2D POLYLINE、3D POLYLINE。
    返回各图元在块定义里的 handle。"""
    inner = doc.blocks.new("INNER")
    h = {}
    h["line"] = inner.add_line(_LINE[0], _LINE[1]).dxf.handle
    h["text"] = inner.add_text("N1", dxfattribs={"height": 2.5, "insert": _TEXT_POS}).dxf.handle
    t2 = inner.add_text("N2", dxfattribs={"height": 2.5})
    t2.set_placement(_TEXT_ALIGN_POS, align=TextEntityAlignment.MIDDLE_CENTER)
    t2.dxf.insert = (1.0, 1.0, 0.0)  # 人为让 insert 不代表可视位置
    h["text_align"] = t2.dxf.handle
    h["mtext"] = inner.add_mtext("M1", dxfattribs={"insert": _MTEXT_POS, "char_height": 2.5}).dxf.handle
    h["lwp"] = inner.add_lwpolyline([(x, y) for x, y, _z in _LWP], dxfattribs={"elevation": 7.0}).dxf.handle
    h["lwp_bulge"] = inner.add_lwpolyline(
        [(_LWP_BULGE[0][0], _LWP_BULGE[0][1], 0.0), (_LWP_BULGE[1][0], _LWP_BULGE[1][1], 0.5), (_LWP_BULGE[2][0], _LWP_BULGE[2][1], 0.0)],
        format="xyb",
    ).dxf.handle
    h["poly2d"] = inner.add_polyline2d([(x, y) for x, y, _z in _POLY2D], dxfattribs={"elevation": (0.0, 0.0, 3.0)}).dxf.handle
    h["poly3d"] = inner.add_polyline3d(_POLY3D).dxf.handle
    return h


# (INNER 在 OUTER 内的 insert/xscale/yscale/rotation, OUTER 在模型空间的 insert/xscale/yscale/rotation)
# 累计镜像次数 = 两层里 xscale*yscale<0 的个数；奇数次才会让展开出的图元拉伸方向变成 (0,0,-1)。
_MIRROR_CASES = [
    pytest.param(((100, 0), 1, 1, 0), ((1000, 500), 1, 1, 0), id="no-mirror-control"),
    pytest.param(((100, 0), -1, 1, 0), ((1000, 500), 1, 1, 0), id="inner-mirror-x-odd"),
    pytest.param(((100, 0), 1, 1, 0), ((1000, 500), -1, 1, 0), id="outer-mirror-x-odd"),
    pytest.param(((100, 0), -1, 1, 0), ((1000, 500), -1, 1, 0), id="both-mirror-x-even"),
    pytest.param(((100, 50), 1, -1, 30), ((1000, 500), -2, 2, 45), id="mirror-y-rot30-then-mirror-x-scale2-rot45-even"),
    pytest.param(((0, 0), -1, -1, 0), ((1000, 500), 1, -1, 90), id="rot180-inner-then-mirror-y-rot90-outer-odd"),
]


@pytest.mark.parametrize("inner_ins, outer_ins", _MIRROR_CASES)
def test_mirrored_nested_block_text_and_polylines_use_wcs(inner_ins, outer_ins):
    doc = ezdxf.new()
    h = _build_inner_block(doc)
    outer = doc.blocks.new("OUTER")
    ii, isx, isy, irot = inner_ins
    outer.add_blockref("INNER", ii, dxfattribs={"xscale": isx, "yscale": isy, "rotation": irot})
    oi, osx, osy, orot = outer_ins
    doc.modelspace().add_blockref("OUTER", oi, dxfattribs={"xscale": osx, "yscale": osy, "rotation": orot})

    # 期望值：块内局部坐标 -> INNER 的 insert 矩阵 -> OUTER 的 insert 矩阵，纯 Matrix44 手算
    m = Matrix44.chain(_insert_matrix(ii, isx, isy, irot), _insert_matrix(oi, osx, osy, orot))

    result = extract.extract_all(doc)
    assert result.skipped == []

    texts = {t.text: t for t in result.texts}
    assert set(texts) == {"N1", "N2", "M1"}
    for name, local in (("N1", _TEXT_POS), ("N2", _TEXT_ALIGN_POS), ("M1", _MTEXT_POS)):
        ex, ey = _xy(m.transform(Vec3(local)))
        assert abs(texts[name].x - ex) < 1e-6, (name, texts[name].x, ex)
        assert abs(texts[name].y - ey) < 1e-6, (name, texts[name].y, ey)

    expected = [
        ("LINE", h["line"], _seg_xy(_LINE, m)),
        ("LWPOLYLINE", h["lwp"], _seg_xy(_LWP, m)),
        ("LWPOLYLINE", h["lwp_bulge"], _seg_xy(_LWP_BULGE, m)),
        ("POLYLINE", h["poly2d"], _seg_xy(_POLY2D, m)),
        ("POLYLINE", h["poly3d"], _seg_xy(_POLY3D, m)),
    ]
    for dxftype, handle, exp in expected:
        got = _segments_of(result, dxftype, handle)
        assert _max_abs_diff(got, exp) < 1e-6, (dxftype, handle, got, exp)


def test_mirrored_block_mtext_insert_is_already_wcs():
    """MTEXT 的 insert 按 DXF 规范是 WCS：镜像块里 ezdxf 展开后的 MTEXT 拉伸方向虽为 (0,0,-1)，
    insert 仍是世界坐标（x = 1000 - 5 = 995），不能再按 OCS 转一次。"""
    doc = ezdxf.new()
    blk = doc.blocks.new("B")
    blk.add_mtext("M1", dxfattribs={"insert": (5.0, 3.0, 0.0), "char_height": 2.5})
    doc.modelspace().add_blockref("B", (1000.0, 500.0), dxfattribs={"xscale": -1})
    result = extract.extract_all(doc)
    assert len(result.texts) == 1
    assert abs(result.texts[0].x - 995.0) < 1e-6
    assert abs(result.texts[0].y - 503.0) < 1e-6


def test_modelspace_entities_with_flipped_extrusion_are_read_as_wcs():
    """不经块参照：直接放在模型空间、拉伸方向为 (0,0,-1) 的 TEXT / LWPOLYLINE / 2D POLYLINE，
    其点是 OCS 坐标，WCS 的 x = -x_ocs（y 不变）；同样拉伸方向的 MTEXT 的 insert 与 3D POLYLINE 的顶点是 WCS，原样取。"""
    doc = ezdxf.new()
    msp = doc.modelspace()
    flip = {"extrusion": (0.0, 0.0, -1.0)}
    mirror_x = Matrix44.scale(-1.0, 1.0, 1.0)  # (0,0,-1) 的 OCS -> WCS 在平面内就是 x 取反

    msp.add_text("T1", dxfattribs={"height": 2.5, "insert": (-30.0, 12.0, 0.0), **flip})
    t2 = msp.add_text("T2", dxfattribs={"height": 2.5, **flip})
    t2.set_placement((-31.0, 13.0), align=TextEntityAlignment.MIDDLE_CENTER)
    t2.dxf.insert = (-1.0, -1.0, 0.0)
    msp.add_mtext("M1", dxfattribs={"insert": (40.0, 15.0, 0.0), "char_height": 2.5, **flip})
    lwp_pts = [(-10.0, 5.0, 0.0), (-20.0, 5.0, 0.0), (-20.0, 9.0, 0.0)]
    lwp = msp.add_lwpolyline([(x, y) for x, y, _z in lwp_pts], dxfattribs={"elevation": 4.0, **flip})
    poly_pts = [(-50.0, 1.0, 2.0), (-60.0, 1.0, 2.0), (-60.0, 6.0, 2.0)]
    poly = msp.add_polyline2d([(x, y) for x, y, _z in poly_pts], dxfattribs={"elevation": (0.0, 0.0, 2.0), **flip})
    poly3d_pts = [(70.0, 1.0, 5.0), (80.0, 1.0, 6.0), (80.0, 6.0, 7.0)]  # 3D POLYLINE 顶点恒为 WCS，哪怕带了拉伸方向
    poly3d = msp.add_polyline3d(poly3d_pts, dxfattribs=flip)

    result = extract.extract_all(doc)
    assert result.skipped == []
    texts = {t.text: t for t in result.texts}
    assert set(texts) == {"T1", "T2", "M1"}
    for name, expected in (("T1", (30.0, 12.0)), ("T2", (31.0, 13.0)), ("M1", (40.0, 15.0))):
        assert abs(texts[name].x - expected[0]) < 1e-6, (name, texts[name].x)
        assert abs(texts[name].y - expected[1]) < 1e-6, (name, texts[name].y)
    assert _max_abs_diff(_segments_of(result, "LWPOLYLINE", lwp.dxf.handle), _seg_xy(lwp_pts, mirror_x)) < 1e-6
    assert _max_abs_diff(_segments_of(result, "POLYLINE", poly.dxf.handle), _seg_xy(poly_pts, mirror_x)) < 1e-6
    assert _max_abs_diff(_segments_of(result, "POLYLINE", poly3d.dxf.handle), _seg_xy(poly3d_pts, Matrix44())) < 1e-6
    # 手算锚点，防止 mirror_x 本身写错：LWPOLYLINE 第一段 (-10,5)->(-20,5) 在 WCS 是 (10,5)->(20,5)
    assert _segments_of(result, "LWPOLYLINE", lwp.dxf.handle)[0] == pytest.approx((10.0, 5.0, 20.0, 5.0))
