"""
SVG path -> PNG 栅格化（纯 Python + Pillow，无外部依赖）

仅覆盖 FontAwesome 图标所需的 SVG path 子集：
M m L l H h V v C c S s Q q T t A a Z z

填充规则：对每个子路径独立填充后做异或叠加（等价 even-odd），
这是 FontAwesome 图标（外轮廓 + 独立孔洞子路径）的正确表现。
"""
from __future__ import annotations

import math
import re
from typing import List, Sequence, Tuple

from PIL import Image, ImageChops, ImageDraw

Point = Tuple[float, float]
Polygon = List[Point]

_TOKEN_RE = re.compile(
    r"[MmLlHhVvCcSsQqTtAaZz]|-?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?"
)

CURVE_STEPS = 24
ARC_STEP_RAD = math.pi / 36  # 5°


def _tokenize(d: str) -> List[str]:
    return _TOKEN_RE.findall(d or "")


def _arc_to_points(
    x0: float, y0: float, rx: float, ry: float, phi_deg: float,
    large_arc: int, sweep: int, x1: float, y1: float,
) -> List[Point]:
    """SVG 端点式圆弧 → 折线点集（不含起点）。"""
    if rx == 0 or ry == 0:
        return [(x1, y1)]
    phi = math.radians(phi_deg % 360)
    cos_p, sin_p = math.cos(phi), math.sin(phi)
    dx2, dy2 = (x0 - x1) / 2.0, (y0 - y1) / 2.0
    x1p = cos_p * dx2 + sin_p * dy2
    y1p = -sin_p * dx2 + cos_p * dy2

    rx, ry = abs(rx), abs(ry)
    lam = (x1p * x1p) / (rx * rx) + (y1p * y1p) / (ry * ry)
    if lam > 1:
        s = math.sqrt(lam)
        rx *= s
        ry *= s

    num = rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p
    den = rx * rx * y1p * y1p + ry * ry * x1p * x1p
    if den == 0:
        return [(x1, y1)]
    coef = math.sqrt(max(num / den, 0.0))
    if large_arc == sweep:
        coef = -coef
    cxp = coef * rx * y1p / ry
    cyp = -coef * ry * x1p / rx

    cx = cos_p * cxp - sin_p * cyp + (x0 + x1) / 2.0
    cy = sin_p * cxp + cos_p * cyp + (y0 + y1) / 2.0

    def angle(ux, uy, vx, vy):
        dot = ux * vx + uy * vy
        n = math.hypot(ux, uy) * math.hypot(vx, vy)
        if n == 0:
            return 0.0
        a = math.acos(max(-1.0, min(1.0, dot / n)))
        return -a if (ux * vy - uy * vx) < 0 else a

    theta1 = angle(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dtheta = angle(
        (x1p - cxp) / rx, (y1p - cyp) / ry,
        (-x1p - cxp) / rx, (-y1p - cyp) / ry,
    )
    if not sweep and dtheta > 0:
        dtheta -= 2 * math.pi
    elif sweep and dtheta < 0:
        dtheta += 2 * math.pi

    n = max(2, int(abs(dtheta) / ARC_STEP_RAD) + 1)
    pts = []
    for i in range(1, n + 1):
        t = theta1 + dtheta * i / n
        xt = rx * math.cos(t)
        yt = ry * math.sin(t)
        pts.append((cos_p * xt - sin_p * yt + cx, sin_p * xt + cos_p * yt + cy))
    pts[-1] = (x1, y1)
    return pts


def path_to_polygons(d: str) -> List[Polygon]:
    """解析 SVG path 字符串为若干闭合子路径（折线）。"""
    tokens = _tokenize(d)
    polygons: List[Polygon] = []
    cur: Polygon = []

    x = y = 0.0
    start: Point = (0.0, 0.0)
    prev_c2: Point | None = None
    prev_q: Point | None = None
    cmd = ""
    i = 0

    def flush():
        if len(cur) >= 3:
            polygons.append(list(cur))
        cur.clear()

    def num() -> float:
        nonlocal i
        v = float(tokens[i])
        i += 1
        return v

    def line_to(px: float, py: float):
        cur.append((px, py))

    while i < len(tokens):
        t = tokens[i]
        if t.isalpha():
            cmd = t
            i += 1
        elif not cmd:
            i += 1
            continue

        rel = cmd.islower()
        C = cmd.upper()

        if C == "M":
            px, py = num(), num()
            if rel:
                px, py = x + px, y + py
            flush()
            x, y = px, py
            start = (x, y)
            cur.append((x, y))
            cmd = "l" if rel else "L"
            prev_c2 = prev_q = None
        elif C == "L":
            px, py = num(), num()
            if rel:
                px, py = x + px, y + py
            x, y = px, py
            line_to(x, y)
            prev_c2 = prev_q = None
        elif C == "H":
            px = num()
            x = x + px if rel else px
            line_to(x, y)
            prev_c2 = prev_q = None
        elif C == "V":
            py = num()
            y = y + py if rel else py
            line_to(x, y)
            prev_c2 = prev_q = None
        elif C in ("C", "S"):
            if C == "C":
                x1, y1, x2, y2, px, py = (num() for _ in range(6))
                if rel:
                    x1, y1, x2, y2, px, py = (
                        x + x1, y + y1, x + x2, y + y2, x + px, y + py,
                    )
            else:
                x2, y2, px, py = (num() for _ in range(4))
                if rel:
                    x2, y2, px, py = x + x2, y + y2, x + px, y + py
                if prev_c2 is None:
                    x1, y1 = x, y
                else:
                    x1, y1 = 2 * x - prev_c2[0], 2 * y - prev_c2[1]
            for s in range(1, CURVE_STEPS + 1):
                u = s / CURVE_STEPS
                mu = 1 - u
                bx = (mu ** 3) * x + 3 * (mu ** 2) * u * x1 + 3 * mu * (u ** 2) * x2 + (u ** 3) * px
                by = (mu ** 3) * y + 3 * (mu ** 2) * u * y1 + 3 * mu * (u ** 2) * y2 + (u ** 3) * py
                line_to(bx, by)
            prev_c2 = (x2, y2)
            prev_q = None
            x, y = px, py
        elif C in ("Q", "T"):
            if C == "Q":
                qx, qy, px, py = (num() for _ in range(4))
                if rel:
                    qx, qy, px, py = x + qx, y + qy, x + px, y + py
            else:
                px, py = num(), num()
                if rel:
                    px, py = x + px, y + py
                if prev_q is None:
                    qx, qy = x, y
                else:
                    qx, qy = 2 * x - prev_q[0], 2 * y - prev_q[1]
            for s in range(1, CURVE_STEPS + 1):
                u = s / CURVE_STEPS
                mu = 1 - u
                bx = (mu ** 2) * x + 2 * mu * u * qx + (u ** 2) * px
                by = (mu ** 2) * y + 2 * mu * u * qy + (u ** 2) * py
                line_to(bx, by)
            prev_q = (qx, qy)
            prev_c2 = None
            x, y = px, py
        elif C == "A":
            rx, ry = num(), num()
            rot = num()
            large = int(num())
            sweep = int(num())
            px, py = num(), num()
            if rel:
                px, py = x + px, y + py
            for p in _arc_to_points(x, y, rx, ry, rot, large, sweep, px, py):
                line_to(*p)
            x, y = px, py
            prev_c2 = prev_q = None
        elif C == "Z":
            flush()
            x, y = start
            cur.append((x, y))
            prev_c2 = prev_q = None
        else:
            i += 1

    flush()
    return polygons


def render_icon(
    path_d: str,
    vb_width: float,
    vb_height: float,
    size: int = 48,
    color: Tuple[int, int, int, int] = (255, 255, 255, 255),
    supersample: int = 4,
    padding: int = 2,
) -> Image.Image:
    """把 SVG path 渲染为指定尺寸的 RGBA 图标。"""
    polys = path_to_polygons(path_d)
    return _paint([(polys, color)], vb_width, vb_height, size, supersample, padding)


# --------------------------------------------------------------------------
# 轻量 SVG 文件渲染（覆盖常见 iconfont / 图标站导出的静态 SVG）
# --------------------------------------------------------------------------
import io  # noqa: E402
import xml.etree.ElementTree as ET  # noqa: E402

_SVG_NS = "{http://www.w3.org/2000/svg}"


def _parse_color(value, fallback):
    """解析 CSS 颜色为 RGBA；'none' 返回 None。"""
    if not value:
        return fallback
    v = value.strip().lower()
    if v in ("none", "transparent"):
        return None
    if v.startswith("#"):
        hx = v[1:]
        try:
            if len(hx) == 3:
                hx = "".join(c * 2 for c in hx)
            if len(hx) == 6:
                hx += "ff"
            if len(hx) == 8:
                return (int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16), int(hx[6:8], 16))
        except ValueError:
            return fallback
    # 常见命名色（仅图标常用的几种）
    named = {"white": (255, 255, 255, 255), "black": (0, 0, 0, 255),
             "red": (255, 0, 0, 255), "blue": (0, 0, 255, 255),
             "green": (0, 128, 0, 255), "gray": (128, 128, 128, 255),
             "grey": (128, 128, 128, 255), "orange": (255, 165, 0, 255),
             "yellow": (255, 255, 0, 255), "currentcolor": fallback}
    return named.get(v, fallback)


def _mat_mul(a, b):
    """3x2 仿射矩阵相乘（a ∘ b，先应用 b 再 a）。"""
    a0, a1, a2, a3, a4, a5 = a
    b0, b1, b2, b3, b4, b5 = b
    return (
        a0 * b0 + a2 * b1,
        a1 * b0 + a3 * b1,
        a0 * b2 + a2 * b3,
        a1 * b2 + a3 * b3,
        a0 * b4 + a2 * b5 + a4,
        a1 * b4 + a3 * b5 + a5,
    )


_IDENTITY = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


def _parse_transform(text):
    m = _IDENTITY
    if not text:
        return m
    for name, args in re.findall(r"(\w+)\s*\(([^)]*)\)", text):
        nums = [float(x) for x in re.findall(r"-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?", args)]
        if name == "translate" and len(nums) >= 1:
            t = (1.0, 0.0, 0.0, 1.0, nums[0], nums[1] if len(nums) > 1 else 0.0)
        elif name == "scale" and nums:
            s = nums[0]
            sy = nums[1] if len(nums) > 1 else s
            t = (s, 0.0, 0.0, sy, 0.0, 0.0)
        elif name == "matrix" and len(nums) >= 6:
            t = tuple(nums[:6])
        elif name == "rotate" and nums:
            a = math.radians(nums[0])
            ca, sa = math.cos(a), math.sin(a)
            t = (ca, sa, -sa, ca, 0.0, 0.0)
            if len(nums) >= 3:
                cx, cy = nums[1], nums[2]
                t = _mat_mul(_mat_mul((1, 0, 0, 1, cx, cy), t), (1, 0, 0, 1, -cx, -cy))
        else:
            continue
        m = _mat_mul(m, t)
    return m


def _apply(m, pt):
    return (m[0] * pt[0] + m[2] * pt[1] + m[4], m[1] * pt[0] + m[3] * pt[1] + m[5])


def _svg_fill_color(el, inherited):
    fill = el.get("fill")
    if not fill:
        style = el.get("style") or ""
        mm = re.search(r"fill\s*:\s*([^;]+)", style)
        if mm:
            fill = mm.group(1)
    return _parse_color(fill, inherited)


def _shape_polygons(el, m, inherited):
    """把基础形状转成 (折线子路径列表, 填充色)。"""
    tag = el.tag.replace(_SVG_NS, "")
    color = _svg_fill_color(el, inherited)
    if color is None:
        return []
    out = []
    if tag == "path":
        polys = path_to_polygons(el.get("d") or "")
        for p in polys:
            out.append([_apply(m, pt) for pt in p])
    elif tag in ("polygon", "polyline"):
        nums = [float(x) for x in re.findall(r"-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?", el.get("points") or "")]
        pts = [(_apply(m, (nums[i], nums[i + 1]))) for i in range(0, len(nums) - 1, 2)]
        if len(pts) >= 3:
            out.append(pts)
    elif tag == "rect":
        x = float(el.get("x", 0)); y = float(el.get("y", 0))
        w = float(el.get("width", 0)); h = float(el.get("height", 0))
        raw = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        out.append([_apply(m, p) for p in raw])
    elif tag in ("circle", "ellipse"):
        cx = float(el.get("cx", 0)); cy = float(el.get("cy", 0))
        rx = float(el.get("r", 0) or el.get("rx", 0))
        ry = float(el.get("r", 0) or el.get("ry", 0))
        pts = [(_apply(m, (cx + rx * math.cos(2 * math.pi * i / 48),
                           cy + ry * math.sin(2 * math.pi * i / 48)))) for i in range(48)]
        out.append(pts)
    return out


def parse_svg(svg_text: str):
    """解析 SVG 文本 -> (分组列表[(多边形列表, 颜色)], viewBox宽, viewBox高)"""
    root = ET.fromstring(svg_text)
    vb = root.get("viewBox")
    if vb:
        parts = re.findall(r"-?(?:\d+\.?\d*|\.\d+)", vb)
        vx, vy, vw, vh = (float(p) for p in parts[:4])
    else:
        vx, vy = 0.0, 0.0
        vw = float(root.get("width", 512) or 512)
        vh = float(root.get("height", 512) or 512)

    groups = []

    def walk(el, m, color):
        m = _mat_mul(m, _parse_transform(el.get("transform")))
        color = _svg_fill_color(el, color)
        tag = el.tag.replace(_SVG_NS, "")
        if tag in ("path", "rect", "circle", "ellipse", "polygon", "polyline"):
            polys = _shape_polygons(el, m, color)
            if polys:
                groups.append((polys, color))
        for child in el:
            walk(child, m, color)

    walk(root, _IDENTITY, (0, 0, 0, 255))
    return groups, vw, vh


def _paint(groups, vb_w, vb_h, size, supersample, padding):
    inner = max(size - padding * 2, 1)
    s = inner * supersample
    canvas = Image.new("1", (s, s), 0)

    vb_w = vb_w or 512
    vb_h = vb_h or 512
    scale = s / max(vb_w, vb_h)
    off_x = (s - vb_w * scale) / 2.0
    off_y = (s - vb_h * scale) / 2.0

    for polys, color in groups:
        layer = Image.new("1", (s, s), 0)
        for poly in polys:
            pts = [(px * scale + off_x, py * scale + off_y) for px, py in poly]
            if len(pts) >= 3:
                ImageDraw.Draw(layer).polygon(pts, fill=1, outline=1)
        if color is None:
            continue
        canvas = ImageChops.logical_xor(canvas, layer)

    mask = canvas.convert("L").resize((inner, inner), Image.LANCZOS)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    # 逐组着色：整体用主色近似，多色 SVG 取每组颜色合成
    if len(groups) == 1:
        out.paste(Image.new("RGBA", (inner, inner), groups[0][1]), (padding, padding), mask)
    else:
        alpha = mask.point(lambda v: 255 if v > 8 else 0)
        main = groups[0][1]
        out.paste(Image.new("RGBA", (inner, inner), main), (padding, padding), alpha)
    return out


def render_svg(svg_text: str, size: int = 48,
               default_color: Tuple[int, int, int, int] = (0, 0, 0, 255),
               supersample: int = 4, padding: int = 2) -> Image.Image:
    """把 SVG 文本渲染为 RGBA 图标。"""
    groups, vw, vh = parse_svg(svg_text)
    if not groups:
        raise ValueError("SVG 中没有可渲染的形状")
    # 未显式指定颜色的形状用 default_color
    norm = []
    for polys, color in groups:
        c = color if color is not None else default_color
        norm.append((polys, c))
    return _paint(norm, vw, vh, size, supersample, padding)
