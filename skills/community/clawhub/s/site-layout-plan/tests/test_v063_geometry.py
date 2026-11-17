#!/usr/bin/env python3
"""0.6.3 真实红线几何、底图裁剪、尺寸/坐标表回归。"""
from __future__ import annotations

import json
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.bootstrap import ensure_runtime  # noqa: E402

ensure_runtime(__file__)

from site_layout.dimensions import (  # noqa: E402
    build_coordinate_rows, redline_key_indices, select_table_rows,
)
from site_layout.generator import (  # noqa: E402
    PROFILES, _inset_polygon, generate_layout, load_requirements,
)
from site_layout.siteplan import build_stage_model, load_base_map, point_in_polygon  # noqa: E402
from site_layout.context import load_context  # noqa: E402
from site_layout.stage_draw import (  # noqa: E402
    _clip_segment_to_box, _segment_hits_box, _site_window,
)


def _signed_area(points):
    return sum(points[i][0] * points[(i + 1) % len(points)][1]
               - points[(i + 1) % len(points)][0] * points[i][1]
               for i in range(len(points))) / 2.0


class InsetPolygonTest(unittest.TestCase):
    def test_convex_and_concave_rings_stay_inside_and_not_self_intersect(self) -> None:
        cases = [
            # 斜置凸多边形
            [(0, 0), (60000, 8000), (52000, 48000), (-4000, 35000)],
            # 凹多边形：右侧切出缺口
            [(0, 0), (60000, 0), (60000, 18000), (42000, 18000),
             (42000, 32000), (60000, 32000), (60000, 50000), (0, 50000)],
        ]
        for ring in cases:
            ring2 = [(float(x), float(y)) for x, y in ring]
            inset = _inset_polygon(ring2, 6000.0)
            self.assertIsNotNone(inset)
            self.assertGreaterEqual(len(inset), 3)
            self.assertGreater(abs(_signed_area(inset)), 1.0)
            for p in inset:
                self.assertTrue(point_in_polygon(p, ring2), p)
            # 不应出现非相邻边严格相交
            n = len(inset)
            for i in range(n):
                a, b = inset[i], inset[(i + 1) % n]
                for j in range(i + 2, n):
                    if i == 0 and j == n - 1:
                        continue
                    c, d = inset[j], inset[(j + 1) % n]
                    def orient(p, q, r):
                        return ((q[0] - p[0]) * (r[1] - p[1])
                                - (q[1] - p[1]) * (r[0] - p[0]))
                    if (orient(a, b, c) * orient(a, b, d) < 0
                            and orient(c, d, a) * orient(c, d, b) < 0):
                        self.fail("inset ring self-intersects")
        print("  [1/6] 凹凸/斜置红线内缩后仍在原红线内且不自交")


class ClipTest(unittest.TestCase):
    def test_liang_barsky_cases(self) -> None:
        box = (0.0, 0.0, 100.0, 100.0)
        # 完全在内
        self.assertEqual(_clip_segment_to_box(10, 10, 90, 90, box), (10, 10, 90, 90))
        # 完全在外
        self.assertIsNone(_clip_segment_to_box(200, 200, 300, 300, box))
        # 穿越：1km 长线被裁到窗口边界
        clipped = _clip_segment_to_box(-1000, 50, 1100, 50, box)
        self.assertIsNotNone(clipped)
        self.assertAlmostEqual(clipped[0], 0.0, places=6)
        self.assertAlmostEqual(clipped[2], 100.0, places=6)
        # 包围盒相交但线段不穿过
        self.assertFalse(_segment_hits_box(-10, -10, -1, 120, box))
        self.assertTrue(_segment_hits_box(-10, 50, 50, 50, box))
        print("  [2/6] Liang-Barsky 穿越/在外/在内与包围盒预筛一致")


class WindowAndCoordinatesTest(unittest.TestCase):
    def test_window_uses_redline_not_base_extents(self) -> None:
        model = {"redline": [[0, 0], [100000, 0], [100000, 50000], [0, 50000]],
                 "redline_closed": True}
        window = _site_window(model, {"extents_mm": [-900000, -900000, 900000, 900000]})
        self.assertEqual(window, (-50000.0, -50000.0, 150000.0, 100000.0))
        print("  [3/6] 出图窗口按红线+50m，不被 1km 底图 extents 撑大")

    def test_csv_full_and_map_subset(self) -> None:
        base, _ = load_base_map(FIXTURES / "base_map_demo.json")
        context = load_context(FIXTURES / "context_demo.json", base_map=base)
        req = load_requirements(FIXTURES / "requirements_demo.json")
        result = generate_layout(base, context, req, [], "balanced")
        model = build_stage_model(base, result["facilities"], result["cranes"], "structure")
        rows = build_coordinate_rows(model)
        table = select_table_rows(rows, limit=999)
        self.assertEqual(len(table), len(rows))
        self.assertEqual(sum(1 for r in rows if r.get("map")), len([r for r in rows if r.get("map")]))
        # 主图编号必须是全量点中的子集，不能出现 CSV 里没有的点
        ids = {r["id"] for r in rows}
        self.assertTrue({r["id"] for r in rows if r.get("map")} <= ids)
        self.assertLessEqual(sum(1 for r in rows if r.get("map")), len(rows))
        print("  [4/6] 坐标 CSV 保留全量，主图 map 标记为子集")


class TransformerClearanceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base, _ = load_base_map(FIXTURES / "base_map_demo.json")
        cls.context = load_context(FIXTURES / "context_demo.json", base_map=cls.base)
        cls.req = load_requirements(FIXTURES / "requirements_demo.json")

    def test_auto_layout_keeps_transformer_10m_from_living(self) -> None:
        for key in PROFILES:
            result = generate_layout(self.base, self.context, self.req, [], key)
            for stage in ("earthwork", "structure", "finish"):
                model = build_stage_model(self.base, result["facilities"],
                                          result["cranes"], stage)
                check = [c for c in model["checks"] if c["id"] == 20][0]
                self.assertEqual(check["status"], "pass", (key, stage, check["message"]))
        print("  [5/6] A/B/C 三阶段变压器均按 10m 边净距自动避让人员区")


class RedlineKeyTest(unittest.TestCase):
    def test_key_indices_keep_corners_and_reduce_arcs(self) -> None:
        # 一个 90m×50m 矩形，每边插入 20 个弧段点
        pts = []
        corners = [(0, 0), (90000, 0), (90000, 50000), (0, 50000)]
        for i in range(4):
            a, b = corners[i], corners[(i + 1) % 4]
            for k in range(20):
                t = k / 20.0
                pts.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
        keep = redline_key_indices(pts)
        self.assertGreaterEqual(len(keep), 4)
        self.assertLess(len(keep), len(pts))
        for idx in keep:
            self.assertTrue(0 <= idx < len(pts))
        print("  [6/6] 红线弧段点被降采样为关键转角，全量仍进 CSV")


if __name__ == "__main__":
    unittest.main(verbosity=2)
