#!/usr/bin/env python3
"""自动布置候选 A/B/C：设施可信标记、塔吊单位、避让与评分回归。"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.context import load_context  # noqa: E402
from site_layout.generator import (  # noqa: E402
    GeneratorError, PROFILES, compare_schemes, evaluate_scheme, generate_layout,
    load_requirements,
)
from site_layout.road_geometry import check_roads  # noqa: E402
from site_layout.siteplan import (  # noqa: E402
    build_stage_model, load_base_map, load_cranes, load_facilities,
)


def _inside(point, polygon) -> bool:
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


def _seg_dist(p, a, b) -> float:
    import math
    dx, dy = b[0] - a[0], b[1] - a[1]
    if abs(dx) < 1e-12 and abs(dy) < 1e-12:
        return math.hypot(p[0] - a[0], p[1] - a[1])
    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - (a[0] + t * dx), p[1] - (a[1] + t * dy))


class GeneratorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_map, cls.base_sha = load_base_map(FIXTURES / "base_map_demo.json")
        cls.context = load_context(FIXTURES / "context_demo.json", base_map=cls.base_map)
        cls.requirements = load_requirements(FIXTURES / "requirements_demo.json")
        cls.results = {key: generate_layout(cls.base_map, cls.context, cls.requirements, [], key)
                       for key in PROFILES}

    def test_all_profiles_generate(self) -> None:
        self.assertEqual(set(self.results), set(PROFILES))
        for key, result in self.results.items():
            self.assertGreaterEqual(len(result["facilities"]), 20, key)
            self.assertFalse(result["final_check"])
            self.assertIn("自动布置候选", result["boundary"])
        print("  [1/6] A/B/C 三套均生成，final_check=false")

    def test_every_auto_facility_is_candidate(self) -> None:
        for key, result in self.results.items():
            for row in result["facilities"]:
                self.assertEqual(row["source"], "auto-layout", (key, row["id"]))
                self.assertEqual(row["confidence"], "candidate", (key, row["id"]))
                self.assertTrue(row["active_stages"], (key, row["id"]))
        print("  [2/6] 自动设施全部 source=auto-layout、confidence=candidate")

    def test_crane_only_active_in_structure(self) -> None:
        result = self.results["balanced"]
        self.assertEqual(result["cranes"][0]["active_stages"], ["structure"])
        for stage, expected in (("earthwork", 0), ("structure", 1), ("finish", 0)):
            model = build_stage_model(self.base_map, result["facilities"],
                                      result["cranes"], stage)
            self.assertEqual(len(model["cranes"]), expected, stage)
            if expected == 0:
                checks = {str(item["id"]): item for item in model["checks"]}
                self.assertEqual(checks["6"]["status"], "pass")
                self.assertIn("已退出", checks["6"]["message"])
        print("  [附] 塔吊仅主体阶段生效：土石方/装饰自动退场，规则 6 判不适用")

    def test_crane_jib_unit_is_mm(self) -> None:
        for key, result in self.results.items():
            self.assertTrue(result["cranes"], key)
            jib = float(result["cranes"][0]["jib_mm"])
            self.assertGreater(jib, 5000.0)
            self.assertLess(jib, 100000.0)
            center = result["cranes"][0]["center_mm"]
            self.assertGreater(center[0], 0.0)
            self.assertGreater(center[1], 0.0)
        print("  [3/6] 塔吊臂长/回转半径为 mm，未再出现 km 级数值")

    def test_notice_board_and_box_avoidance(self) -> None:
        for key, result in self.results.items():
            boundary = [(float(p[0]), float(p[1])) for p in self.base_map["redline"]]
            by_id = {row["id"]: row for row in result["facilities"]}
            board = by_id["A-NOTICE-01"]
            point = board["geometry"]["points_mm"][0]
            self.assertTrue(_inside(point, boundary), key)
            for row in result["facilities"]:
                if row["category"] in ("temporary_road", "fire_access"):
                    pts = row["geometry"]["points_mm"]
                    half = float(row.get("width_mm") or 4000.0) / 2.0
                    nearest = min(_seg_dist(point, pts[i], pts[i + 1])
                                  for i in range(len(pts) - 1))
                    self.assertGreater(nearest, half, (key, row["id"]))
            box = by_id["A-BOX-01"]
            box_pt = box["geometry"]["points_mm"][0]
            for row in result["facilities"]:
                if row["geometry"]["type"] == "area":
                    self.assertFalse(_inside(box_pt, row["geometry"]["points_mm"]),
                                     (key, row["id"]))
        print("  [4/6] 九牌一图不压道路/出红线；一级箱不压区域设施")

    def test_unknown_scheme_rejected(self) -> None:
        with self.assertRaises(GeneratorError):
            generate_layout(self.base_map, self.context, self.requirements, [], "Z")
        print("  [5/6] 未知方案 -> GeneratorError，不静默回退")

    def test_requirements_missing_unit_adds_assumption(self) -> None:
        raw = json.loads((FIXTURES / "requirements_demo.json").read_text(encoding="utf-8"))
        raw.pop("coord_unit")
        raw["building"] = {"footprint": [[29000, 20000], [71000, 20000],
                                         [71000, 40000], [29000, 40000]]}
        result = generate_layout(self.base_map, self.context, raw, [], "balanced")
        self.assertTrue(any("coord_unit" in item for item in result["assumptions"]))
        print("  [6/6] 需求文件缺单位 -> assumptions 明确提示，不静默")

    def test_collinear_fire_lane_length_counted_once(self) -> None:
        metrics = self.results["balanced"]["metrics"]
        stats = metrics["road_length_by_category_m"]
        self.assertNotIn("fire_access", stats)
        self.assertAlmostEqual(sum(stats.values()), metrics["road_length_m"], places=1)
        self.assertGreater(stats.get("temporary_road", 0), 0)
        self.assertGreater(stats.get("permanent_road", 0), 0)
        print("  [附] 共线消防车道不重复计长：临时+永久=总长")

    def test_not_applicable_rules_pass_in_early_stage(self) -> None:
        result = self.results["balanced"]
        model = build_stage_model(self.base_map, result["facilities"],
                                  result["cranes"], "earthwork")
        checks = {str(item["id"]): item for item in model["checks"]}
        self.assertEqual(checks["8"]["status"], "pass")
        self.assertIn("不适用", checks["8"]["message"])
        self.assertEqual(checks["10"]["status"], "pass")
        self.assertIn("间距满足", checks["10"]["message"])
        print("  [附] 土石方阶段未设加工区：规则 8 判不适用；垃圾池全阶段保留，规则 10 正常校核")

    def test_all_stage_evaluation_and_compare(self) -> None:
        result = self.results["balanced"]
        models, roads, contexts = {}, {}, {}
        for stage in ("earthwork", "structure", "finish"):
            model = build_stage_model(self.base_map, result["facilities"],
                                      result["cranes"], stage)
            models[stage] = model
            roads[stage] = check_roads(model["facilities"], model["rule_params"])
            contexts[stage] = {"checks": [], "summary": {"pass": 0, "review": 0, "fail": 0}}
        evaluation = evaluate_scheme(result, models, roads, contexts,
                                     stages=["earthwork", "structure", "finish"])
        self.assertEqual(sorted(evaluation["evaluated_stages"]),
                         ["earthwork", "finish", "structure"])
        self.assertEqual(len(evaluation["stage_summary"]), 3)
        self.assertFalse(evaluation["final_check"])
        comparison = compare_schemes([evaluation])
        self.assertEqual(comparison["rows"][0]["scheme"], "balanced")
        print("  [附] 三阶段汇总评分：stage_summary 3 项、比选可运行")

    def test_single_stage_fail_becomes_hard_find(self) -> None:
        result = self.results["balanced"]
        models, roads, contexts = {}, {}, {}
        for stage in ("earthwork", "structure", "finish"):
            models[stage] = build_stage_model(self.base_map, result["facilities"],
                                              result["cranes"], stage)
            roads[stage] = check_roads(models[stage]["facilities"],
                                       models[stage]["rule_params"])
            contexts[stage] = {"checks": [], "summary": {"pass": 0, "review": 0, "fail": 0}}
        roads["finish"]["checks"] = [
            {"id": "R1", "name": "道路宽度", "status": "fail", "message": "测试注入"}
        ]
        roads["finish"]["summary"] = {"pass": 0, "fail": 1, "manual": 0}
        evaluation = evaluate_scheme(result, models, roads, contexts,
                                     stages=["earthwork", "structure", "finish"])
        self.assertEqual(evaluation["verdict"], "不推荐（存在硬伤）")
        self.assertTrue(any("装饰" in item and "道路校核 fail" in item
                            for item in evaluation["hard_finds"]))
        self.assertEqual(evaluation["stage_summary"]["finish"]["road_fail"], 1)
        print("  [附] 任一阶段 fail 即硬伤，分数取最不利阶段")


class GeneratedCraneHandoffTest(unittest.TestCase):
    """A/B/C 输出必须能原样进入 build_site_plan 的塔吊入口。"""

    def test_generated_crane_file_is_consumable_and_rule_13_sees_it(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        out = Path(tmp.name) / "generated"
        generated = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "generate_site_layout.py"),
             "--base-map", str(FIXTURES / "base_map_demo.json"),
             "--context", str(FIXTURES / "context_demo.json"),
             "--requirements", str(FIXTURES / "requirements_demo.json"),
             "--scheme", "B", "--stages", "structure", "--out-dir", str(out)],
            text=True, capture_output=True, timeout=180,
        )
        self.assertEqual(generated.returncode, 0, generated.stderr)
        scheme_dir = out / "scheme-B"
        crane_path = scheme_dir / "generated-cranes.json"
        crane_data = json.loads(crane_path.read_text(encoding="utf-8"))
        self.assertEqual(crane_data["units"]["basis"], "explicit")
        self.assertEqual(crane_data["crane_layout"][0]["center_status"], "insert_point")
        self.assertGreater(crane_data["crane_layout"][0]["jib_length_m"], 0)

        base_map, _ = load_base_map(FIXTURES / "base_map_demo.json")
        facilities, _, _ = load_facilities(scheme_dir / "generated-facilities.json")
        cranes, sources = load_cranes([str(crane_path)], base_map["extents_mm"])
        self.assertEqual(len(cranes), 1)
        self.assertEqual(sources[0]["coordinate_gate"]["status"], "same_source")
        model = build_stage_model(base_map, facilities, cranes, "structure")
        rule13 = next(c for c in model["checks"] if c["id"] == 13)
        self.assertEqual(rule13["status"], "pass", rule13["message"])
        print("  [E2E] 生成设施+生成塔吊可进入正式构建，规则 13 不再误报缺塔吊")


if __name__ == "__main__":
    unittest.main(verbosity=2)
