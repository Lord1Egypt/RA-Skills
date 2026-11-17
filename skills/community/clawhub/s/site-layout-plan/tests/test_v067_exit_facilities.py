#!/usr/bin/env python3
"""0.6.7 出入口服务带回归：九牌直排、洗车台跨路、地磅贴主路、规则 22 分支。"""
from __future__ import annotations

import copy
import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
GEN = ROOT / "scripts" / "generate_site_layout.py"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.bootstrap import ensure_runtime  # noqa: E402

ensure_runtime(__file__)

import ezdxf  # noqa: E402

from site_layout.siteplan import (  # noqa: E402
    _centroid, _dist, _polylines_intersect, _point_segment_distance,
    build_stage_model, load_base_map, load_cranes, load_facilities,
)


def _center(row):
    return _centroid(row)


def _points(row):
    return [(float(p[0]), float(p[1])) for p in row["geometry"]["points_mm"]]


def _closed(row):
    pts = _points(row)
    return pts + [pts[0]]


def _inside(point, polygon):
    x, y = point
    inside = False
    j = len(polygon) - 1
    for i in range(len(polygon)):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi:
            inside = not inside
        j = i
    return inside


def _road_distance(center, road):
    pts = _points(road)
    closed = bool(road["geometry"].get("closed"))
    best = None
    last = len(pts) if closed else len(pts) - 1
    for index in range(last):
        value = _point_segment_distance(center, pts[index], pts[(index + 1) % len(pts)])
        best = value if best is None else min(best, value)
    return best


def _translate(row, dx, dy):
    row["geometry"]["points_mm"] = [[float(x) + dx, float(y) + dy]
                                    for x, y in row["geometry"]["points_mm"]]


class ExitFacilitiesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory(prefix="slp_v067_")
        out = Path(cls.tmp.name) / "gen"
        proc = subprocess.run(
            [sys.executable, str(GEN),
             "--base-map", str(FIXTURES / "base_map_demo.json"),
             "--context", str(FIXTURES / "context_demo.json"),
             "--requirements", str(FIXTURES / "requirements_demo.json"),
             "--scheme", "balanced", "--stages", "all",
             "--out-dir", str(out)],
            cwd=str(ROOT), capture_output=True, text=True,
        )
        if proc.returncode != 0:
            raise AssertionError("generate_site_layout 失败:\n" + proc.stdout + proc.stderr)
        cls.scheme = out / "scheme-B"
        cls.base_map, _ = load_base_map(FIXTURES / "base_map_demo.json")
        cls.facilities, _, _ = load_facilities(cls.scheme / "generated-facilities.json")
        cls.cranes, _ = load_cranes([str(cls.scheme / "generated-cranes.json")],
                                    cls.base_map.get("extents_mm"))
        cls.dxf = ezdxf.readfile(str(cls.scheme / "layout-earthwork.dxf"))
        cls.model = build_stage_model(cls.base_map, cls.facilities, cls.cranes, "earthwork")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def _check22(self, model):
        return [c for c in model["checks"] if c["id"] == 22][0]

    def _check14(self, model):
        return [c for c in model["checks"] if c["id"] == 14][0]

    def test_notice_board_is_nine_panel_linear_area(self) -> None:
        row = [r for r in self.facilities if r["category"] == "notice_board"][0]
        attrs = row["attrs"]
        self.assertEqual(row["geometry"]["type"], "area")
        self.assertEqual(attrs["layout"], "linear")
        self.assertEqual(int(attrs["board_count"]), 9)
        self.assertAlmostEqual(float(attrs["total_length_m"]), 11.0, places=1)
        redline = self.base_map["redline"]
        for point in _points(row):
            self.assertTrue(_inside(point, redline), point)
        for road in [r for r in self.facilities if r["geometry"]["type"] == "line"]:
            if road["category"] in ("temporary_road", "fire_access"):
                self.assertFalse(_polylines_intersect(_closed(row), _points(road)),
                                 "九牌一图压到道路: {}".format(road["id"]))
        layer_lines = [e for e in self.dxf.modelspace().query("LINE")
                       if e.dxf.layer == "FAC-九牌一图"]
        self.assertEqual(len(layer_lines), 8)
        print("  [1/4] 九牌一图 9 块×1.2m 直排（11.0m），8 条分隔线，不压路不出红线")

    def test_wheel_wash_crosses_access_road(self) -> None:
        wash = [r for r in self.facilities if r["category"] == "wheel_wash"][0]
        gate = [r for r in self.facilities if r["category"] == "site_access"][0]
        access = [r for r in self.facilities if r["id"] == "A-ROAD-GATE-1"][0]
        self.assertEqual(wash["attrs"]["layout"], "drive-through")
        self.assertTrue(wash["attrs"]["on_access_road"])
        self.assertTrue(_polylines_intersect(_closed(wash), _points(access)))
        self.assertLessEqual(_dist(_center(wash), _center(gate)) / 1000.0, 30.0)
        wash_road_dist = _road_distance(_center(wash), access)
        self.assertIsNotNone(wash_road_dist)
        self.assertLessEqual(wash_road_dist, 8000.0)
        # 多门示例：默认第 1 个大门，并把假设写进属性
        self.assertEqual(int(wash["attrs"]["gate_index"]), 1)
        self.assertGreaterEqual(int(wash["attrs"]["gate_count"]), 2)
        self.assertTrue(wash["attrs"]["main_gate_assumption"])
        rule14 = self._check14(self.model)
        bad = [c for c in rule14["evidence"].get("conflicts", [])
               if "wheel_wash" in (c.get("a_category"), c.get("b_category"))]
        self.assertEqual(bad, [])
        self.assertEqual(self._check22(self.model)["status"], "pass")
        print("  [2/4] 洗车台实际跨接入道路，距门≤30m；规则 14 不误报、规则 22 pass")

    def test_weighbridge_on_main_ring_near_gate(self) -> None:
        scale = [r for r in self.facilities if r["category"] == "weighbridge"][0]
        gate = [r for r in self.facilities if r["category"] == "site_access"][0]
        ring = [r for r in self.facilities if r["id"] == "A-ROAD-RING"][0]
        self.assertEqual(scale["attrs"]["layout"], "on_main_road")
        self.assertLessEqual(_dist(_center(scale), _center(gate)) / 1000.0, 60.0)
        scale_road_dist = _road_distance(_center(scale), ring)
        self.assertIsNotNone(scale_road_dist)
        self.assertLessEqual(scale_road_dist, 10000.0)
        layers = {layer.dxf.name for layer in self.dxf.layers}
        self.assertIn("FAC-地磅", layers)
        inserts = [e for e in self.dxf.modelspace().query("INSERT")
                   if e.dxf.name == "SLP_WEIGHBRIDGE"]
        self.assertTrue(inserts)
        self.assertTrue(any(e.dxf.layer == "FAC-地磅" for e in inserts))
        print("  [3/4] 地磅存在、贴主环道且距门≤60m，DXF 有 FAC-地磅 与 SLP_WEIGHBRIDGE")

    def test_centroid_large_project_coordinates(self) -> None:
        rect = [(519329282.3, 4065912915.7), (519334267.953, 4065912537.335),
                (519334703.953, 4065918281.9), (519329718.3, 4065918660.4)]
        row = {"geometry": {"type": "area", "points_mm": rect}}
        center = _centroid(row)
        self.assertIsNotNone(center)
        # 大坐标下重心必须落在矩形包围盒内，不能因叉积相消漂移数千米
        xs = [p[0] for p in rect]
        ys = [p[1] for p in rect]
        self.assertTrue(min(xs) < center[0] < max(xs), center)
        self.assertTrue(min(ys) < center[1] < max(ys), center)
        self.assertAlmostEqual(center[0], (min(xs) + max(xs)) / 2.0, delta=1.0)
        self.assertAlmostEqual(center[1], (min(ys) + max(ys)) / 2.0, delta=1.0)

    def test_wheel_wash_falls_back_to_second_gate(self) -> None:
        import json as _json
        from site_layout.generator import PROFILES, _Layout
        raw = _json.loads((FIXTURES / "base_map_demo.json").read_text(encoding="utf-8"))
        ctx = {"warnings": []}
        req = _json.loads((FIXTURES / "requirements_demo.json").read_text(encoding="utf-8"))
        layout = _Layout(raw, ctx, req, [], PROFILES["balanced"])
        self._fallback_case(layout)

    def _fallback_case(self, layout) -> None:
        layout.ring = [(8000.0, 8000.0), (92000.0, 8000.0),
                       (92000.0, 52000.0), (8000.0, 52000.0)]
        layout.building_rect = (30000.0, 25000.0, 70000.0, 45000.0)
        layout.building_poly = [(30000.0, 25000.0), (70000.0, 25000.0),
                                (70000.0, 45000.0), (30000.0, 45000.0)]
        # 第 1 个门接入段仅 2 m，第 2 个门 8 m：应自动退到第 2 个门
        layout.gate_access = [[(58000.0, 0.0), (58000.0, 2000.0)],
                              [(0.0, 22000.0), (8000.0, 22000.0)]]
        gates = [(58000.0, 0.0), (0.0, 22000.0)]
        layout.place_wheel_wash(gates)
        wash = [r for r in layout.facilities if r["category"] == "wheel_wash"][0]
        self.assertEqual(int(wash["attrs"]["gate_index"]), 2)
        self.assertFalse(bool(wash["attrs"]["short_pad"]))
        layout.place_weighbridge(gates)
        scale = [r for r in layout.facilities if r["category"] == "weighbridge"][0]
        self.assertEqual(int(scale["attrs"]["gate_index"]), 2)
        print("  [5/6] 首门接入段不足时自动选用第 2 个门，地磅同门")

    def test_rule22_manual_branches(self) -> None:
        facilities = copy.deepcopy(self.facilities)
        no_scale = [r for r in facilities if r["category"] != "weighbridge"]
        self.assertEqual(self._check22(build_stage_model(
            self.base_map, no_scale, self.cranes, "earthwork"))["status"], "manual")

        facilities = copy.deepcopy(self.facilities)
        wash = [r for r in facilities if r["category"] == "wheel_wash"][0]
        _translate(wash, 200000.0, 0.0)
        self.assertEqual(self._check22(build_stage_model(
            self.base_map, facilities, self.cranes, "earthwork"))["status"], "manual")

        facilities = copy.deepcopy(self.facilities)
        wash = [r for r in facilities if r["category"] == "wheel_wash"][0]
        wash["attrs"].pop("on_access_road", None)
        self.assertEqual(self._check22(build_stage_model(
            self.base_map, facilities, self.cranes, "earthwork"))["status"], "manual")
        print("  [4/4] 规则 22 分支：缺地磅/洗车台挪远/缺跨路属性均判 manual")


    def test_short_ring_edges_trim_keeps_geometry_and_r3(self) -> None:
        """碎边环清理：去掉红线内缩环的小台阶后仍在红线内、不自交、R3 通过。"""
        from site_layout.generator import _trim_short_ring_edges
        from site_layout.road_geometry import check_roads

        boundary = [(0.0, 0.0), (100000.0, 0.0), (100000.0, 80000.0), (0.0, 80000.0)]
        jittered = [(8000.0, 8000.0), (30000.0, 8000.0),
                    (30000.0, 72000.0), (31000.0, 72000.0), (31000.0, 71000.0),
                    (32000.0, 71000.0), (32000.0, 72000.0), (92000.0, 72000.0),
                    (92000.0, 8000.0)]
        cleaned = _trim_short_ring_edges(jittered, boundary)
        self.assertLess(len(cleaned), len(jittered))
        # 全部顶点仍在红线内、闭合环不自交
        for point in cleaned:
            self.assertTrue(_inside(point, boundary), point)
        from site_layout.generator import _polyline_self_intersects
        self.assertFalse(_polyline_self_intersects(cleaned))
        # 最短边不小于清理阈值（避免又留下会被 R3 误判的碎边）
        edges = [_dist(cleaned[i], cleaned[(i + 1) % len(cleaned)]) for i in range(len(cleaned))]
        self.assertGreaterEqual(min(edges), 3000.0)
        # 原始碎边环 R3 必然失败；清理后同一几何 R3 应通过
        def road(points):
            return {"id": "RING", "category": "temporary_road", "width_mm": 6000.0,
                    "geometry": {"type": "line", "closed": True,
                                 "points_mm": [[float(x), float(y)] for x, y in points]},
                    "attrs": {"lanes": 2}}
        before = [c for c in check_roads([road(jittered)], {})["checks"] if c["id"] == "R3"][0]
        after = [c for c in check_roads([road(cleaned)], {})["checks"] if c["id"] == "R3"][0]
        self.assertEqual(before["status"], "fail")
        self.assertEqual(after["status"], "pass")
        print("  [6/6] 碎边环清理：{} 点→{} 点，仍在红线内/不自交，R3 fail→pass".format(
            len(jittered), len(cleaned)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
