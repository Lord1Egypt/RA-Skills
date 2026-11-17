"""文字标注排版：包围盒、碰撞检测、确定性四级降级与自检。

设计要点：
- 只用 stdlib，不依赖 ezdxf/Pillow，便于单测和复用；
- 字宽按“中文/全角=1.0 em、数字与大写=0.62 em、小写=0.55 em”估算，
  比真实字宽略保守，宁可留白也不压图；
- 候选位置固定顺序，同一输入必得同一输出（可回归、可截图比对）；
- 降级顺序：贴边直放 → 引线外移 → 换位 → 缩到基准字高 60% → 编号入图例；
  全部失败记 `unplaced`，由 selfcheck 判 fail，不再静默选“最不差”位置。
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

Point = Tuple[float, float]

# 降级层级（越大越差）
LEVEL_ORDER = ("direct", "leader", "shifted", "shrunk", "index", "unplaced")
ACCEPT_LEVELS = ("direct", "leader", "shifted", "shrunk")
MIN_SHRINK = 0.6


@dataclass(frozen=True)
class Box:
    x0: float
    y0: float
    x1: float
    y1: float

    @property
    def width(self) -> float:
        return max(0.0, self.x1 - self.x0)

    @property
    def height(self) -> float:
        return max(0.0, self.y1 - self.y0)

    def pad(self, dx: float, dy: Optional[float] = None) -> "Box":
        dy = dx if dy is None else dy
        return Box(self.x0 - dx, self.y0 - dy, self.x1 + dx, self.y1 + dy)

    def overlap_area(self, other: "Box") -> float:
        w = min(self.x1, other.x1) - max(self.x0, other.x0)
        h = min(self.y1, other.y1) - max(self.y0, other.y0)
        return w * h if w > 0 and h > 0 else 0.0

    def contains(self, other: "Box") -> bool:
        return (self.x0 <= other.x0 and self.y0 <= other.y0
                and other.x1 <= self.x1 and other.y1 <= self.y1)

    def as_list(self) -> List[float]:
        return [round(self.x0, 3), round(self.y0, 3), round(self.x1, 3), round(self.y1, 3)]


def char_em(char: str) -> float:
    """单字符宽度（em）。中文/全角按 1.0，数字与大写按 0.62，其余按 0.55。"""
    code = ord(char)
    if code >= 0x2E80 or 0xFF00 <= code <= 0xFF60:
        return 1.0
    if char == " ":
        return 0.36
    if char in ".,:;'`!|":
        return 0.34
    if char in "ilI":
        return 0.32
    if char in "mwMW":
        return 0.86
    if char.isupper() or char.isdigit():
        return 0.62
    return 0.55


def text_width(text: str, height: float) -> float:
    return sum(char_em(ch) for ch in str(text)) * float(height)


def text_box(text: str, x: float, y: float, height: float) -> Box:
    """以 (x, y) 为左下角基线的 TEXT 包围盒；纵向按 1.2 倍字高留上下余量。"""
    return Box(float(x), float(y), float(x) + text_width(text, height),
               float(y) + float(height) * 1.2)


def box_hits_segment(box: Box, p1: Point, p2: Point) -> bool:
    """线段与矩形是否相交（Liang-Barsky 裁剪）。"""
    x0, y0, x1, y1 = box.x0, box.y0, box.x1, box.y1
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, p1[0] - x0), (dx, x1 - p1[0]),
                 (-dy, p1[1] - y0), (dy, y1 - p1[1])):
        if abs(p) < 1e-12:
            if q < 0:
                return False
            continue
        t = q / p
        if p < 0:
            if t > t1:
                return False
            t0 = max(t0, t)
        else:
            if t < t0:
                return False
            t1 = min(t1, t)
    return t0 <= t1


@dataclass
class Placement:
    ref: str
    text: str
    box: Box
    height: float
    level: str
    layer: str = "TEXT-标注"
    color: int = 7
    leader: Optional[Tuple[Point, Point]] = None
    short_for: str = ""

    def as_dict(self) -> Dict[str, Any]:
        return {
            "ref": self.ref,
            "text": self.text,
            "x": round(self.box.x0, 3),
            "y": round(self.box.y0, 3),
            "height": round(self.height, 2),
            "level": self.level,
            "layer": self.layer,
            "color": int(self.color),
            "leader": ([[round(p[0], 3), round(p[1], 3)] for p in self.leader]
                       if self.leader else None),
            "short_for": self.short_for,
            "box": self.box.as_list(),
        }


class TextPlacer:
    """确定性文字排版器：先到先得，先近后远，先大后小。"""

    def __init__(self, bounds: Box, gap_ratio: float = 0.55):
        self.bounds = bounds
        self.gap_ratio = gap_ratio
        self.placed: List[Placement] = []
        self.boxes: List[Box] = []
        self.footprints: List[Tuple[Box, str]] = []   # (box, ref) 允许自身压自身轮廓
        self.symbols: List[Tuple[Box, str]] = []      # (box, ref) 任何文字都不压图块
        self.segments: List[Tuple[Point, Point, str]] = []
        self._seg_grid: Optional[Dict[Tuple[int, int], List[int]]] = None
        self._seg_cell: float = 0.0

    # ---------- 障碍登记 ----------
    def add_footprint(self, box: Box, ref: str) -> None:
        if box.width > 0 and box.height > 0:
            self.footprints.append((box, str(ref)))

    def add_symbol(self, box: Box, ref: str) -> None:
        if box.width > 0 and box.height > 0:
            self.symbols.append((box, str(ref)))

    def add_segment(self, p1: Point, p2: Point, ref: str) -> None:
        self.segments.append(((float(p1[0]), float(p1[1])),
                              (float(p2[0]), float(p2[1])), str(ref)))
        self._seg_grid = None  # 惰性重建空间索引

    def _segment_index(self) -> Tuple[float, Dict[Tuple[int, int], List[int]]]:
        """底图线段的均匀网格索引：大图几千条线段时避免每个文字候选全量扫描。"""
        if self._seg_grid is not None:
            return self._seg_cell, self._seg_grid
        cell = max(5_000.0, min(20_000.0, max(self.bounds.width, self.bounds.height) / 48.0))
        grid: Dict[Tuple[int, int], List[int]] = {}
        for index, (p1, p2, _ref) in enumerate(self.segments):
            ix0 = int(math.floor(min(p1[0], p2[0]) / cell))
            ix1 = int(math.floor(max(p1[0], p2[0]) / cell))
            iy0 = int(math.floor(min(p1[1], p2[1]) / cell))
            iy1 = int(math.floor(max(p1[1], p2[1]) / cell))
            for ix in range(ix0, ix1 + 1):
                for iy in range(iy0, iy1 + 1):
                    grid.setdefault((ix, iy), []).append(index)
        self._seg_grid = grid
        self._seg_cell = cell
        return cell, grid

    # ---------- 冲突检测 ----------
    def conflicts(self, box: Box, ref: str, pad: float, check_segments: bool = True) -> List[str]:
        hits: List[str] = []
        probe = box.pad(pad)
        if not self.bounds.contains(probe):
            hits.append("越界")
        for other in self.boxes:
            if other.overlap_area(probe) > 0:
                hits.append("文字重叠")
        for fp, fp_ref in self.footprints:
            if fp_ref == ref:
                continue
            if fp.overlap_area(probe) > 0:
                hits.append("压设施:{}".format(fp_ref))
        for sym, sym_ref in self.symbols:
            if sym.overlap_area(probe) > 0:
                hits.append("压图块:{}".format(sym_ref))
        if check_segments and self.segments:
            cell, grid = self._segment_index()
            ix0 = int(math.floor(probe.x0 / cell))
            ix1 = int(math.floor(probe.x1 / cell))
            iy0 = int(math.floor(probe.y0 / cell))
            iy1 = int(math.floor(probe.y1 / cell))
            checked: set[int] = set()
            for ix in range(ix0, ix1 + 1):
                for iy in range(iy0, iy1 + 1):
                    for index in grid.get((ix, iy), ()):
                        if index in checked:
                            continue
                        checked.add(index)
                        p1, p2, seg_ref = self.segments[index]
                        if seg_ref == ref:
                            continue
                        if box_hits_segment(probe, p1, p2):
                            hits.append("压线:{}".format(seg_ref))
        return hits

    # ---------- 候选 ----------
    @staticmethod
    def _candidates(anchor: Point, width: float, height: float, gap: float,
                    distance: float) -> Iterable[Tuple[str, Point]]:
        ax, ay = anchor
        d = gap + distance
        yield "e", (ax + d, ay - height / 2.0)
        yield "w", (ax - d - width, ay - height / 2.0)
        yield "n", (ax - width / 2.0, ay + d)
        yield "s", (ax - width / 2.0, ay - d - height)
        yield "ne", (ax + d, ay + d)
        yield "nw", (ax - d - width, ay + d)
        yield "se", (ax + d, ay - d - height)
        yield "sw", (ax - d - width, ay - d - height)

    def _try(self, text: str, anchor: Point, height: float, ref: str, layer: str,
             color: int, pad: float, distance: float, level: str,
             short_for: str = "") -> Optional[Placement]:
        width = text_width(text, height)
        gap = height * self.gap_ratio
        for _side, (x, y) in self._candidates(anchor, width, height, gap, distance):
            box = text_box(text, x, y, height)
            if self.conflicts(box, ref, pad):
                continue
            leader = None
            if distance > 0 or level in ("shifted", "leader"):
                cx = min(max(anchor[0], box.x0), box.x1)
                cy = min(max(anchor[1], box.y0), box.y1)
                if math.hypot(cx - anchor[0], cy - anchor[1]) > gap * 0.8:
                    leader = ((anchor[0], anchor[1]), (cx, cy))
            return Placement(ref=ref, text=text, box=box, height=height, level=level,
                             layer=layer, color=color, leader=leader, short_for=short_for)
        return None

    def place(self, text: str, anchor: Point, height: float, ref: str = "",
              layer: str = "TEXT-标注", color: int = 7,
              short: str = "", scale_hint: float = 1.0) -> Placement:
        """按四级降级放置；全部失败返回 level=unplaced，绝不硬塞。"""
        pad = height * 0.18
        font = height * float(scale_hint)
        attempt = self._try(text, anchor, font, ref, layer, color, pad, 0.0, "direct")
        if attempt:
            return self._commit(attempt)
        for distance, level in ((font * 1.4, "leader"), (font * 3.0, "leader"),
                                (font * 5.0, "shifted"), (font * 8.0, "shifted"),
                                (font * 12.0, "shifted")):
            attempt = self._try(text, anchor, font, ref, layer, color, pad, distance, level)
            if attempt:
                return self._commit(attempt)
        small = font * MIN_SHRINK
        attempt = self._try(text, anchor, small, ref, layer, color, small * 0.18, 0.0, "shrunk")
        if attempt is None:
            for distance in (small * 2.0, small * 4.0, small * 7.0):
                attempt = self._try(text, anchor, small, ref, layer, color,
                                    small * 0.18, distance, "shrunk")
                if attempt:
                    break
        if attempt:
            return self._commit(attempt)
        if short and short != text:
            tag = self._try(short, anchor, small, ref, layer, color, small * 0.18,
                            0.0, "index", short_for=text)
            if tag is None:
                for distance in (small * 3.0, small * 6.0, small * 10.0):
                    tag = self._try(short, anchor, small, ref, layer, color,
                                    small * 0.18, distance, "index", short_for=text)
                    if tag:
                        break
            if tag:
                return self._commit(tag)
        return Placement(ref=ref, text=text, box=text_box(text, anchor[0], anchor[1], font),
                         height=font, level="unplaced", layer=layer, color=color)

    def _commit(self, placement: Placement) -> Placement:
        self.placed.append(placement)
        if placement.level != "unplaced":
            self.boxes.append(placement.box)
        return placement


def verify(placements: Sequence[Placement]) -> List[Dict[str, Any]]:
    """排版后独立复检：任意两条文字不得相交。"""
    problems: List[Dict[str, Any]] = []
    live = [p for p in placements if p.level != "unplaced"]
    for index, first in enumerate(live):
        for second in live[index + 1:]:
            area = first.box.overlap_area(second.box)
            if area > 0:
                problems.append({"a": first.ref or first.text, "b": second.ref or second.text,
                                 "area": round(area, 1)})
    return problems


def summarize(placements: Sequence[Placement]) -> Dict[str, Any]:
    stats = {level: 0 for level in LEVEL_ORDER}
    for placement in placements:
        stats[placement.level] = stats.get(placement.level, 0) + 1
    problems = verify(placements)
    stats["total"] = len(placements)
    stats["overlaps"] = len(problems)
    stats["problems"] = problems[:20]
    stats["index_entries"] = [{"tag": p.text, "ref": p.ref,
                               "text": p.short_for or p.text}
                              for p in placements if p.level == "index"]
    stats["unplaced"] = [{"ref": p.ref, "text": p.text}
                         for p in placements if p.level == "unplaced"]
    stats["unplaced_count"] = len(stats["unplaced"])
    return stats
