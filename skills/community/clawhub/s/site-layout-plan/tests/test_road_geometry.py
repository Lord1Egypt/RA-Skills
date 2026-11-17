#!/usr/bin/env python3
"""道路几何校核回归：宽度、会车、转弯半径、回车场。"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.road_geometry import check_roads, render_road_markdown  # noqa: E402

PARAMS = {
    "road_min_width_m": 3.5,
    "road_dual_min_width_m": 6.0,
    "fire_lane_min_width_m": 4.0,
    "passing_bay_interval_m": 100.0,
    "turning_radius_min_m": 9.0,
    "fire_turning_radius_min_m": 12.0,
    "dead_end_turnaround_min_m": 12.0,
}


def road(fid: str, points, width_m=None, category="temporary_road", attrs=None):
    return {
        "id": fid,
        "category": category,
        "width_mm": None if width_m is None else width_m * 1000.0,
        "geometry": {"type": "line", "points_mm": [tuple(p) for p in points], "closed": False},
        "attrs": attrs or {},
    }


def by_id(result, cid):
    return next(c for c in result["checks"] if c["id"] == cid)


class RoadWidthTest(unittest.TestCase):
    def test_dual_lane_pass_and_single_narrow_fail(self) -> None:
        rows = [road("R1", [(0, 0), (100000, 0)], 6.5, attrs={"lanes": 2}),
                road("R2", [(0, 5000), (100000, 5000)], 3.0, attrs={"lanes": 1})]
        result = check_roads(rows, PARAMS)
        width = by_id(result, "R1")
        self.assertEqual(width["status"], "fail")
        self.assertEqual(len(width["evidence"]["narrow"]), 1)
        self.assertEqual(width["evidence"]["narrow"][0]["road"], "R2")
        print("  [1/5] 双车道 6.5m 通过、单车道 3.0m 判不足")

    def test_fire_lane_min_four_meters(self) -> None:
        rows = [road("F1", [(0, 0), (50000, 0)], 3.8, category="fire_access")]
        result = check_roads(rows, PARAMS)
        self.assertEqual(by_id(result, "R1")["status"], "fail")
        print("  [2/5] 消防车道 3.8m 判不足（<4.0m）")


class PassingBayTest(unittest.TestCase):
    def test_long_single_lane_without_bays_is_manual(self) -> None:
        rows = [road("R1", [(0, 0), (200000, 0)], 4.0, attrs={"lanes": 1})]
        result = check_roads(rows, PARAMS)
        self.assertEqual(by_id(result, "R2")["status"], "manual")
        self.assertEqual(len(by_id(result, "R2")["evidence"]["missing"]), 1)
        print("  [3/5] 200m 单车道未标会车点 → manual")

    def test_passing_bays_within_interval_pass(self) -> None:
        rows = [road("R1", [(0, 0), (200000, 0)], 4.0,
                     attrs={"lanes": 1, "passing_bays": [60, 140]})]
        result = check_roads(rows, PARAMS)
        self.assertEqual(by_id(result, "R2")["status"], "pass")
        self.assertEqual(by_id(result, "R2")["evidence"]["over"], [])
        print("  [4/5] 会车点 60/140m，最大间隔 80m ≤ 100m → pass")

    def test_passing_bay_gap_fail(self) -> None:
        rows = [road("R1", [(0, 0), (300000, 0)], 4.0,
                     attrs={"lanes": 1, "passing_bays": [60]})]
        result = check_roads(rows, PARAMS)
        self.assertEqual(by_id(result, "R2")["status"], "fail")
        print("  [5/5] 会车点间隔 180m 超限 → fail")


class TurningRadiusTest(unittest.TestCase):
    def test_sharp_corner_fail_and_gentle_corner_pass(self) -> None:
        sharp = [road("R1", [(0, 0), (10000, 0), (10000, 10000)], 4.0)]
        result = check_roads(sharp, PARAMS)
        turn = by_id(result, "R3")
        self.assertEqual(turn["status"], "fail")
        self.assertAlmostEqual(turn["evidence"]["over"][0]["radius_m"], 7.07, places=2)

        gentle = [road("R2", [(0, 0), (50000, 0), (50000, 50000)], 4.0)]
        result = check_roads(gentle, PARAMS)
        self.assertEqual(by_id(result, "R3")["status"], "pass")
        print("  [1/3] 10m 折角 R≈7.07m fail；50m 折角 R≈35.36m pass")

    def test_fire_lane_requires_twelve_meters(self) -> None:
        rows = [road("F1", [(0, 0), (15000, 0), (15000, 15000)], 4.0, category="fire_access")]
        result = check_roads(rows, PARAMS)
        self.assertEqual(by_id(result, "R3")["status"], "fail")
        self.assertEqual(by_id(result, "R3")["evidence"]["over"][0]["limit_m"], 12.0)
        print("  [2/3] 消防车道 R≈10.61m <12m 判 fail")


class DeadEndTest(unittest.TestCase):
    def test_fire_lane_dead_end_without_turnaround_fails(self) -> None:
        rows = [road("F1", [(0, 0), (100000, 0)], 4.0, category="fire_access")]
        result = check_roads(rows, PARAMS)
        dead = by_id(result, "R4")
        self.assertEqual(dead["status"], "fail")
        self.assertEqual(len(dead["evidence"]["dead_ends"]), 2)
        print("  [3/3] 尽头式消防车道无回车场 → fail（两端均报）")

    def test_permanent_road_endpoint_is_connection_not_dead_end(self) -> None:
        rows = [road("P1", [(0, 0), (100000, 0)], category="permanent_road"),
                road("T1", [(0, 0), (0, 50000)], 4.0,
                     attrs={"turnaround": True, "turnaround_area_m": 225.0})]
        result = check_roads(rows, PARAMS)
        dead = by_id(result, "R4")
        self.assertEqual(dead["status"], "pass")
        self.assertEqual(dead["evidence"]["dead_ends"], [])
        only_perm = check_roads(
            [road("P1", [(0, 0), (100000, 0)], category="permanent_road")], PARAMS)
        perm = by_id(only_perm, "R4")
        self.assertEqual(perm["evidence"]["dead_ends"], [])
        self.assertNotIn("尽头", perm["message"])
        print("  [3/3] 永久道路端点可作为接顺点，不被误判为尽头路")

    def test_turnaround_attr_clears_dead_end(self) -> None:
        rows = [road("F1", [(0, 0), (100000, 0)], 4.0, category="fire_access",
                     attrs={"turnaround": True})]
        result = check_roads(rows, PARAMS)
        self.assertEqual(by_id(result, "R4")["status"], "pass")
        print("  [3/3] attrs.turnaround=true → pass")


class MarkdownTest(unittest.TestCase):
    def test_markdown_contains_all_checks(self) -> None:
        rows = [road("R1", [(0, 0), (200000, 0)], 3.0, attrs={"lanes": 1})]
        md = render_road_markdown(check_roads(rows, PARAMS))
        for key in ("R1", "R2", "R3", "R4", "汇总"):
            self.assertIn(key, md)
        print("  [附] Markdown 含 R1~R4 与汇总")


if __name__ == "__main__":
    unittest.main(verbosity=2)
