#!/usr/bin/env python3
"""site-layout-plan 0.7.0 · 生活区分设、整体组合搜索与规则 23-26 回归。"""
from __future__ import annotations

import copy
import inspect
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

from site_layout.context import load_context  # noqa: E402
from site_layout.generator import (  # noqa: E402
    PROFILES, _Layout, generate_layout, load_requirements,
)
from site_layout.siteplan import (  # noqa: E402
    build_stage_model, load_base_map, point_in_polygon,
)
from site_layout.taxonomy import ALIASES, FACILITIES, canonical, meta  # noqa: E402

LIVING_NEW = {
    "staff_dormitory": ("员工宿舍区", "FAC-员工宿舍", 40, "area"),
    "worker_living_zone": ("工人生活区", "FAC-工人生活区", 40, "area"),
    "canteen": ("食堂", "FAC-食堂", 40, "area"),
    "toilet_shower": ("卫生间/淋浴间", "FAC-卫生间淋浴", 40, "area"),
    "drying_area": ("晾晒区", "FAC-晾晒区", 40, "area"),
}
CHILD_CATEGORIES = ("canteen", "toilet_shower", "drying_area")
ALL_STAGES = ("earthwork", "structure", "finish")


def _rows(facilities, category):
    return [row for row in facilities if row["category"] == category]


def _center(row):
    points = row["geometry"]["points_mm"]
    return (sum(p[0] for p in points) / len(points),
            sum(p[1] for p in points) / len(points))


def _move_to(row, center):
    points = row["geometry"]["points_mm"]
    cx, cy = _center(row)
    dx, dy = center[0] - cx, center[1] - cy
    row["geometry"]["points_mm"] = [[x + dx, y + dy] for x, y in points]


def _bounds(poly):
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return min(xs), min(ys), max(xs), max(ys)


def _rect_gap_mm(a, b):
    ax0, ay0, ax1, ay1 = _bounds(a)
    bx0, by0, bx1, by1 = _bounds(b)
    dx = max(bx0 - ax1, ax0 - bx1, 0.0)
    dy = max(by0 - ay1, ay0 - by1, 0.0)
    return math.hypot(dx, dy)


def _overlap_area(a, b):
    ax0, ay0, ax1, ay1 = _bounds(a)
    bx0, by0, bx1, by1 = _bounds(b)
    return max(0.0, min(ax1, bx1) - max(ax0, bx0)) * max(
        0.0, min(ay1, by1) - max(ay0, by0))


class LivingTaxonomyTest(unittest.TestCase):
    def test_five_categories_alias_layer_color_kind_stage(self) -> None:
        self.assertEqual(len(FACILITIES), 37)
        for category, (zh, layer, color, kind) in LIVING_NEW.items():
            self.assertIn(category, FACILITIES)
            info = meta(category)
            self.assertEqual(info["zh"], zh)
            self.assertEqual(info["layer"], layer)
            self.assertEqual(info["color"], color)
            self.assertEqual(info["kind"], kind)
            self.assertEqual(tuple(info["stages"]), ALL_STAGES)
        expected = {
            "dormitory": "staff_dormitory",
            "员工宿舍": "staff_dormitory",
            "生活区": "worker_living_zone",
            "工人生活区": "worker_living_zone",
            "食堂": "canteen",
            "淋浴间": "toilet_shower",
            "厕所": "toilet_shower",
            "晾衣区": "drying_area",
        }
        for alias, target in expected.items():
            self.assertIn(alias, ALIASES)
            self.assertEqual(canonical(alias), target)
        print("  [1/11] 五类生活设施的中英文名/图层/颜色/kind/阶段与别名正确")


class LivingGeneratorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_map, _ = load_base_map(FIXTURES / "base_map_demo.json")
        cls.context = load_context(FIXTURES / "context_demo.json", base_map=cls.base_map)
        cls.requirements = load_requirements(FIXTURES / "requirements_demo.json")
        cls.results = {
            key: generate_layout(cls.base_map, cls.context, cls.requirements, [], key)
            for key in PROFILES
        }

    def test_default_gap_is_800mm_and_demo_keeps_priority_gap(self) -> None:
        default = inspect.signature(_Layout.place_living_children).parameters["gap_mm"].default
        self.assertEqual(default, 800.0)
        for key, result in self.results.items():
            children = [row for row in result["facilities"]
                        if row["category"] in CHILD_CATEGORIES]
            self.assertEqual(len(children), 3, key)
            for i in range(len(children)):
                for j in range(i + 1, len(children)):
                    gap = _rect_gap_mm(children[i]["geometry"]["points_mm"],
                                       children[j]["geometry"]["points_mm"])
                    self.assertGreaterEqual(gap, 800.0 - 1e-6, (key, children[i]["id"],
                                                                children[j]["id"], gap))
        # 尺寸降级说明必须用中文类别名，不能只写内部英文键。
        degraded = [row for result in self.results.values() for row in result["facilities"]
                    if row["category"] in CHILD_CATEGORIES
                    and row["attrs"].get("size_degraded")]
        self.assertTrue(degraded)
        for row in degraded:
            self.assertIn(meta(row["category"])["zh"], row["attrs"]["size_note"])
            self.assertIn("m", row["attrs"]["size_note"])
        print("  [2/11] 子块默认净距 0.8 m 优先；三套组合均无重叠，降级说明用中文尺寸名")

    def test_six_generated_ids_and_three_children(self) -> None:
        for key, result in self.results.items():
            ids = {row["id"] for row in result["facilities"]}
            expected = {"A-LIVING-01", "A-CANTEEN-01", "A-TOILET-01",
                        "A-DRYING-01", "A-STAFFDORM-01", "A-OFFICE-01"}
            self.assertTrue(expected <= ids, (key, expected - ids))
            for category in CHILD_CATEGORIES:
                rows = _rows(result["facilities"], category)
                self.assertEqual(len(rows), 1, (key, category))
                self.assertEqual(rows[0]["attrs"].get("parent_id"), "A-LIVING-01")
                self.assertTrue(rows[0]["attrs"].get("inside_parent"))
        print("  [3/11] A/B/C 均生成六个生活/办公 ID，三个子块均声明 parent_id=A-LIVING-01")

    def test_children_inside_parent_and_not_overlapping(self) -> None:
        for key, result in self.results.items():
            parent = _rows(result["facilities"], "worker_living_zone")[0]
            parent_poly = parent["geometry"]["points_mm"]
            children = [row for row in result["facilities"]
                        if row["category"] in CHILD_CATEGORIES]
            for child in children:
                for point in child["geometry"]["points_mm"]:
                    self.assertTrue(point_in_polygon(point, parent_poly, 1.0),
                                    (key, child["id"], point))
            for i in range(len(children)):
                for j in range(i + 1, len(children)):
                    self.assertLessEqual(_overlap_area(children[i]["geometry"]["points_mm"],
                                                       children[j]["geometry"]["points_mm"]),
                                         1e-6, (key, children[i]["id"], children[j]["id"]))
        print("  [4/11] 三个子块完全位于 A-LIVING-01 包络内且互不重叠")

    def test_staff_and_worker_living_do_not_overlap(self) -> None:
        for key, result in self.results.items():
            staff = _rows(result["facilities"], "staff_dormitory")[0]
            worker = _rows(result["facilities"], "worker_living_zone")[0]
            self.assertLessEqual(_overlap_area(staff["geometry"]["points_mm"],
                                               worker["geometry"]["points_mm"]),
                                 1e-6, key)
        print("  [5/11] 员工宿舍区与工人生活区不重叠")


class LivingRuleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_map, _ = load_base_map(FIXTURES / "base_map_demo.json")
        cls.context = load_context(FIXTURES / "context_demo.json", base_map=cls.base_map)
        cls.requirements = load_requirements(FIXTURES / "requirements_demo.json")
        cls.result = generate_layout(cls.base_map, cls.context, cls.requirements, [],
                                     "balanced")

    def _model(self, facilities=None, stage="structure", context=None):
        return build_stage_model(self.base_map,
                                 copy.deepcopy(facilities or self.result["facilities"]),
                                 self.result["cranes"], stage, context=context)

    def _check(self, model, cid):
        return [check for check in model["checks"] if check["id"] == cid][0]

    def test_rule_6_catches_living_inside_crane_radius(self) -> None:
        facilities = copy.deepcopy(self.result["facilities"])
        dorm = _rows(facilities, "staff_dormitory")[0]
        crane = self.result["cranes"][0]
        _move_to(dorm, crane["center_mm"])
        check = self._check(self._model(facilities), 6)
        self.assertEqual(check["status"], "fail", check)
        self.assertTrue(any(item["facility"] == "A-STAFFDORM-01"
                            for item in check["evidence"]["risky"]))
        print("  [6/11] 员工宿舍移入塔吊回转半径，规则 6 判 fail")

    def test_rule_24_road_crossing_fails(self) -> None:
        facilities = copy.deepcopy(self.result["facilities"])
        living = _rows(facilities, "worker_living_zone")[0]
        road = [row for row in facilities if row["id"] == "A-ROAD-RING"][0]
        p0, p1 = road["geometry"]["points_mm"][:2]
        _move_to(living, ((p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0))
        check = self._check(self._model(facilities), 24)
        self.assertEqual(check["status"], "fail", check)
        self.assertTrue(check["evidence"]["road_crossings"])
        print("  [7/11] 工人生活区被临时道路穿越，规则 24 判 fail")

    def test_rule_25_missing_canteen_and_outside_child_are_manual(self) -> None:
        facilities = [row for row in copy.deepcopy(self.result["facilities"])
                      if row["id"] != "A-CANTEEN-01"]
        check = self._check(self._model(facilities), 25)
        self.assertEqual(check["status"], "manual")
        self.assertIn("食堂", check["message"])

        facilities = copy.deepcopy(self.result["facilities"])
        canteen = _rows(facilities, "canteen")[0]
        _move_to(canteen, (90000.0, 50000.0))
        check = self._check(self._model(facilities), 25)
        self.assertEqual(check["status"], "manual")
        self.assertTrue(any("A-CANTEEN-01" in item and "未完全位于" in item
                            for item in check["evidence"]["issues"]))
        print("  [8/11] 缺食堂/子块移出父包络，规则 25 均判 manual")

    def test_rule_26_office_far_from_gate_is_manual(self) -> None:
        facilities = copy.deepcopy(self.result["facilities"])
        office = _rows(facilities, "site_office")[0]
        _move_to(office, (90000.0, 50000.0))
        check = self._check(self._model(facilities), 26)
        self.assertEqual(check["status"], "manual", check)
        self.assertTrue(check["evidence"]["far_office"])
        print("  [9/11] 办公区远离最近大门，规则 26 判 manual")

    def test_rule_14_skips_declared_parent_child(self) -> None:
        model = self._model()
        check = self._check(model, 14)
        self.assertEqual(check["status"], "pass", check)
        conflicts = check["evidence"]["conflicts"]
        child_ids = {"A-CANTEEN-01", "A-TOILET-01", "A-DRYING-01"}
        self.assertFalse([item for item in conflicts
                          if item["a"] == "A-LIVING-01" and item["b"] in child_ids])
        print("  [10/11] 规则 14 通过 parent_id 跳过父子包含，不误报几何冲突")

    def test_rule_23_without_wind_rose_is_manual(self) -> None:
        for stage in ALL_STAGES:
            model = self._model(stage=stage)
            check = self._check(model, 23)
            self.assertEqual(check["status"], "manual", (stage, check))
            self.assertFalse(check["evidence"]["wind"]["living_upwind_verified"])
        print("  [11/11] 无风玫瑰时规则 23 在三阶段均为 manual，不冒充上风向已确认")


if __name__ == "__main__":
    unittest.main()
