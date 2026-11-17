#!/usr/bin/env python3
"""site-context/v1：单位、点/线/面、高压线塔吊净距与软硬约束回归。"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.context import (  # noqa: E402
    ContextUnitError, check_context, geometry_blocked, load_context,
    point_blocked, render_context_markdown,
)


def ctx(unit="m", constraints=None, **extra):
    data = {"schema": "site-context/v1", "coord_unit": unit,
            "constraints": constraints or []}
    data.update(extra)
    return data


def write(tmp: Path, payload: dict) -> Path:
    path = tmp / "context.json"
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return path


def area(fid, category, rect):
    x0, y0, x1, y1 = rect
    return {"id": fid, "category": category,
            "geometry": {"type": "area", "points_mm": [[x0, y0], [x1, y0], [x1, y1], [x0, y1]],
                         "closed": True}}


class ContextUnitTest(unittest.TestCase):
    def test_meter_converted_to_mm(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = write(Path(tmp), ctx(constraints=[{
                "type": "river", "geometry": {"type": "line", "points": [[1, 0], [1, 2]]},
                "buffer_m": 15}]))
            result = load_context(path)
        self.assertEqual(result["coord_unit"], "mm")
        self.assertEqual(result["constraints"][0]["geometry"]["points_mm"][1], (1000.0, 2000.0))
        self.assertEqual(result["constraints"][0]["buffer_mm"], 15000.0)
        print("  [1/6] site-context 单位 m -> mm 归一")

    def test_missing_unit_exit4(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            payload = ctx(constraints=[])
            payload.pop("coord_unit")
            path = write(Path(tmp), payload)
            with self.assertRaises(ContextUnitError) as caught:
                load_context(path)
        self.assertEqual(caught.exception.exit_code, 4)
        print("  [2/6] 周边文件无 coord_unit -> exit 4，不猜倍数")

    def test_empty_context_warns(self) -> None:
        result = load_context(None)
        self.assertTrue(result["warnings"])
        self.assertEqual(result["constraints"], [])
        print("  [3/6] 无周边文件 -> 明确“未调查”警告")


class ContextCheckTest(unittest.TestCase):
    def setUp(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = write(Path(tmp), ctx(constraints=[
                {"id": "HV", "type": "high_voltage", "name": "东侧架空线",
                 "geometry": {"type": "line", "points": [[60, -20], [60, 80]]},
                 "buffer_m": 8, "severity": "hard"},
                {"id": "RES", "type": "residential", "name": "北侧住宅",
                 "geometry": {"type": "point", "points": [[50, 78]]},
                 "buffer_m": 10, "severity": "hard"},
                {"id": "SCH", "type": "sensitive_receptor", "name": "东北学校",
                 "geometry": {"type": "point", "points": [[75, 75]]},
                 "buffer_m": 20, "severity": "soft"},
            ]))
            self.context = load_context(path)

    def test_high_voltage_uses_jib_edge(self) -> None:
        cranes = [{"id": "TC-1", "center_mm": (0.0, 0.0), "jib_mm": 70000.0}]
        result = check_context([], cranes, self.context)
        hv = result["checks"][0]
        self.assertEqual(hv["status"], "fail")
        hit = hv["evidence"]["hits"][0]
        self.assertEqual(hit["category"], "tower_crane_jib")
        self.assertLess(hit["distance_m"], 8.0)
        print("  [4/6] 高压线按塔吊回转外缘净距判 fail")

    def test_soft_constraint_is_review(self) -> None:
        facilities = [area("F-OFFICE", "site_office", (68000, 58000, 78000, 68000))]
        result = check_context(facilities, [], self.context)
        school = result["checks"][2]
        self.assertEqual(school["status"], "review")
        self.assertEqual(result["summary"]["review"], 1)
        print("  [5/6] 敏感点软约束 -> review，不与硬约束混为 fail")

    def test_block_helpers_and_markdown(self) -> None:
        self.assertIsNotNone(point_blocked((55000.0, 30000.0), self.context, "temporary_dormitory"))
        self.assertIsNone(point_blocked((55000.0, 30000.0), self.context, "permanent_road"))
        blocked = geometry_blocked(
            {"type": "area", "points_mm": [[55000, 0], [65000, 0], [65000, 10000], [55000, 10000]],
             "closed": True}, self.context, "processing_zone")
        self.assertIsNotNone(blocked)
        result = check_context([], [], self.context)
        md = render_context_markdown(result)
        self.assertIn("C1", md)
        self.assertIn("汇总", md)
        self.assertIn("现场踏勘", md)
        print("  [6/6] 布点避让函数生效；Markdown 含 C1 与边界说明")


if __name__ == "__main__":
    unittest.main(verbosity=2)
