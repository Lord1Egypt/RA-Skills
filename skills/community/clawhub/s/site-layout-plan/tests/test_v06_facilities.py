#!/usr/bin/env python3
"""0.6.0 新增设施与规则 16-21 回归：分类、阶段、图块、分支判定。"""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.bootstrap import ensure_runtime  # noqa: E402

ensure_runtime(__file__)

import ezdxf  # noqa: E402

from site_layout.context import load_context  # noqa: E402
from site_layout.generator import PROFILES, generate_layout, load_requirements  # noqa: E402
from site_layout.siteplan import build_stage_model, load_base_map  # noqa: E402
from site_layout.symbols import SYMBOLS, block_name, ensure_symbol_blocks  # noqa: E402
from site_layout.taxonomy import ALIASES, FACILITIES, canonical  # noqa: E402

NEW_CATEGORIES = {
    "steel_processing": ("structure",),
    "wood_processing": ("structure", "finish"),
    "mortar_processing": ("structure", "finish"),
    "transformer": ("earthwork", "structure", "finish"),
    "fire_pump_room": ("earthwork", "structure", "finish"),
    "fire_water_tank": ("earthwork", "structure", "finish"),
    "drainage_ditch": ("earthwork", "structure", "finish"),
    "staff_dormitory": ("earthwork", "structure", "finish"),
    "worker_living_zone": ("earthwork", "structure", "finish"),
    "canteen": ("earthwork", "structure", "finish"),
    "toilet_shower": ("earthwork", "structure", "finish"),
    "drying_area": ("earthwork", "structure", "finish"),
}

NEW_BLOCKS = {
    "steel_processing": "SLP_STEEL",
    "wood_processing": "SLP_WOOD",
    "mortar_processing": "SLP_MORTAR",
    "transformer": "SLP_TRANSFORMER",
    "fire_pump_room": "SLP_FIREPUMP",
    "fire_water_tank": "SLP_FIRETANK",
    "drainage_ditch": "SLP_DITCH",
    "staff_dormitory": "SLP_STAFFDORM",
    "worker_living_zone": "SLP_LIVING",
    "canteen": "SLP_CANTEEN",
    "toilet_shower": "SLP_TOILET",
    "drying_area": "SLP_DRYING",
}


def _move_to(row, center):
    points = row["geometry"]["points_mm"]
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    dx, dy = center[0] - cx, center[1] - cy
    row["geometry"]["points_mm"] = [[x + dx, y + dy] for x, y in points]


def _center(row):
    points = row["geometry"]["points_mm"]
    return (sum(p[0] for p in points) / len(points),
            sum(p[1] for p in points) / len(points))


class TaxonomyV06Test(unittest.TestCase):
    def test_category_count_and_new_entries(self) -> None:
        self.assertEqual(len(FACILITIES), 37)
        for category, stages in NEW_CATEGORIES.items():
            self.assertIn(category, FACILITIES)
            self.assertEqual(tuple(FACILITIES[category]["stages"]), stages)
        self.assertIn("processing_zone", FACILITIES)
        print("  [1/10] 分类表 37 类，十二类新设施+地磅阶段与拆分兼容项正确")

    def test_aliases_resolve_to_new_categories(self) -> None:
        expected = {
            "rebar_yard": "steel_processing",
            "wood_yard": "wood_processing",
            "mortar": "mortar_processing",
            "fire_tank": "fire_water_tank",
            "substation": "transformer",
            "ditch": "drainage_ditch",
        }
        for alias, target in expected.items():
            self.assertIn(alias, ALIASES)
            self.assertEqual(canonical(alias), target)
        print("  [2/10] 钢筋/木工/砂浆/变压器/水池/排水沟别名归一正确")


class GeneratorV06Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_map, _ = load_base_map(FIXTURES / "base_map_demo.json")
        context = load_context(FIXTURES / "context_demo.json", base_map=cls.base_map)
        requirements = load_requirements(FIXTURES / "requirements_demo.json")
        cls.results = {key: generate_layout(cls.base_map, context, requirements, [], key)
                       for key in PROFILES}

    def test_profiles_emit_new_facilities_with_stage_scope(self) -> None:
        for key, result in self.results.items():
            categories = {row["category"] for row in result["facilities"]}
            self.assertGreaterEqual(len(categories), 26, key)
            for category, stages in NEW_CATEGORIES.items():
                self.assertIn(category, categories, (key, category))
            by_category = {}
            for row in result["facilities"]:
                by_category.setdefault(row["category"], []).append(row)
            for category, stages in NEW_CATEGORIES.items():
                rows = by_category[category]
                if category == "drainage_ditch":
                    # 环沟全阶段；A-DITCH-02 为洗车池排水接入，随洗车台全阶段保留
                    self.assertEqual(
                        [row["active_stages"] for row in rows
                         if row["id"] == "A-DITCH-01"][0], list(stages))
                    self.assertEqual(
                        [row["active_stages"] for row in rows
                         if row["id"] == "A-DITCH-02"][0], list(stages))
                    continue
                for row in rows:
                    self.assertEqual(tuple(row["active_stages"]), stages,
                                     (key, row["id"]))
            ditch_ids = {row["id"] for row in by_category["drainage_ditch"]}
            self.assertIn("A-DITCH-01", ditch_ids)
            self.assertIn("A-DITCH-02", ditch_ids)
            # 洗车台全阶段保留：结构/装饰阶段仍须有车辆冲洗设施与排水接入
            for row in by_category["wheel_wash"]:
                self.assertEqual(tuple(row["active_stages"]),
                                 ("earthwork", "structure", "finish"), (key, row["id"]))
        print("  [3/10] A/B/C 均生成 ≥26 类，十二类新设施阶段归属正确；洗车台全阶段保留")

    def test_stage_checks_have_26_rules_with_no_fail(self) -> None:
        for key, result in self.results.items():
            for stage in ("earthwork", "structure", "finish"):
                model = build_stage_model(self.base_map, result["facilities"],
                                          result["cranes"], stage)
                self.assertEqual(len(model["checks"]), 26, (key, stage))
                self.assertEqual([c["id"] for c in model["checks"]],
                                 list(range(1, 27)), (key, stage))
                self.assertEqual(model["summary"]["fail"], 0, (key, stage, [
                    (c["id"], c["message"]) for c in model["checks"]
                    if c["status"] == "fail"
                ]))
                status = {c["id"]: c["status"] for c in model["checks"]}
                for cid in (16, 17, 18, 19, 20):
                    self.assertEqual(status[cid], "pass", (key, stage, cid))
                # 洗车台全阶段保留后，排水沟各阶段均能接入沉淀池，规则 21 全阶段 pass
                self.assertEqual(status[21], "pass", (key, stage))
                # 自动生成的三套均应带洗车台/地磅，规则 22 全阶段 pass
                self.assertEqual(status[22], "pass", (key, stage))
                # 无风玫瑰时规则 23 只能 manual；规则 24-26 由自动候选保证通过
                self.assertEqual(status[23], "manual", (key, stage))
                for cid in (24, 25, 26):
                    self.assertEqual(status[cid], "pass", (key, stage, cid))
        print("  [4/10] 三套×三阶段均 26 条规则、fail=0；规则 23 manual、24-26 pass")

    def test_rule_13_accepts_split_processing_zones(self) -> None:
        result = self.results["balanced"]
        self.assertFalse([row for row in result["facilities"]
                          if row["category"] == "processing_zone"])
        model = build_stage_model(self.base_map, result["facilities"],
                                  result["cranes"], "structure")
        rule13 = [c for c in model["checks"] if c["id"] == 13][0]
        self.assertEqual(rule13["status"], "pass")
        print("  [5/10] 无 processing_zone 时，三类拆分加工区满足规则 13")


class NewRuleBranchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_map, _ = load_base_map(FIXTURES / "base_map_demo.json")
        context = load_context(FIXTURES / "context_demo.json", base_map=cls.base_map)
        requirements = load_requirements(FIXTURES / "requirements_demo.json")
        cls.result = generate_layout(cls.base_map, context, requirements, [], "balanced")

    def _model(self, facilities, stage="structure"):
        return build_stage_model(self.base_map, facilities, self.result["cranes"], stage)

    def _status(self, model, cid):
        return [c for c in model["checks"] if c["id"] == cid][0]

    def _facilities(self):
        return copy.deepcopy(self.result["facilities"])

    def test_short_distance_branches_are_manual(self) -> None:
        cases = [
            ("steel_processing", 16),
            ("wood_processing", 17),
            ("mortar_processing", 18),
        ]
        for category, cid in cases:
            facilities = self._facilities()
            office = [row for row in facilities if row["category"] == "site_office"][0]
            target = [row for row in facilities if row["category"] == category][0]
            _move_to(target, _center(office))
            check = self._status(self._model(facilities), cid)
            self.assertEqual(check["status"], "manual", (category, check))
        print("  [6/10] 钢筋/木工/砂浆加工区贴近办公区均判 manual")

    def test_fire_group_and_transformer_short_distance_manual(self) -> None:
        facilities = self._facilities()
        pump = [row for row in facilities if row["category"] == "fire_pump_room"][0]
        _move_to(pump, (3000.0, 3000.0))
        self.assertEqual(self._status(self._model(facilities), 19)["status"], "manual")

        facilities = self._facilities()
        dorm = [row for row in facilities if row["category"] == "staff_dormitory"][0]
        transformer = [row for row in facilities if row["category"] == "transformer"][0]
        _move_to(transformer, _center(dorm))
        self.assertEqual(self._status(self._model(facilities), 20)["status"], "manual")
        print("  [7/10] 泵房远离水池/车道、变压器贴近人员区均判 manual")

    def test_ditch_t_junction_on_closed_ring_passes(self) -> None:
        facilities = self._facilities()
        ring = [row for row in facilities if row["id"] == "A-DITCH-01"][0]
        points = ring["geometry"]["points_mm"]
        if points[0] == points[-1]:
            points = points[:-1]
        ring["geometry"]["points_mm"] = points
        ring["geometry"]["closed"] = True
        branch = [row for row in facilities if row["id"] == "A-DITCH-02"][0]
        branch["geometry"]["points_mm"] = [[55000.0, 14000.0], [6500.0, 21000.0]]
        # 排放口必须由洗车池/沉淀池承接；把洗车池放到支沟端点，专门验证
        # “T 形接入闭合环沟 + 有明确排放去向”同时成立，而不是依赖自动布局巧合。
        wash = [row for row in facilities if row["category"] == "wheel_wash"][0]
        _move_to(wash, (6500.0, 21000.0))
        check = self._status(self._model(facilities, "earthwork"), 21)
        self.assertEqual(check["status"], "pass", check["message"])
        print("  [8/10] 支沟端点落在闭合环沟首尾闭合段上，判为连通")

    def test_disconnected_ditch_is_manual(self) -> None:
        facilities = self._facilities()
        ditch = [row for row in facilities if row["id"] == "A-DITCH-01"][0]
        ditch["geometry"]["points_mm"] = [[6500.0, 6500.0], [93500.0, 6500.0]]
        ditch["geometry"]["closed"] = False
        second = copy.deepcopy(ditch)
        second["id"] = "A-DITCH-03"
        second["geometry"]["points_mm"] = [[6500.0, 53500.0], [93500.0, 53500.0]]
        facilities.append(second)
        check = self._status(self._model(facilities), 21)
        self.assertEqual(check["status"], "manual")
        self.assertIn("未连通", check["message"])
        print("  [9/10] 排水沟断成两段判 manual，提示未连通")


class SymbolV06Test(unittest.TestCase):
    def test_new_blocks_exist_and_are_created(self) -> None:
        for category, block in NEW_BLOCKS.items():
            self.assertIn(category, SYMBOLS)
            self.assertEqual(block_name(category), block)
        doc = ezdxf.new("R2010")
        ensure_symbol_blocks(doc)
        for block in NEW_BLOCKS.values():
            self.assertIn(block, doc.blocks)
        print("  [10/10] 十二类新设施 SLP_* 图块存在且可幂等创建")


if __name__ == "__main__":
    unittest.main()
