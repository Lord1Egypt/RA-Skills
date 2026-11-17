#!/usr/bin/env python3
"""site-layout-plan 0.1.0 · crane_check 回归测试（纯 stdlib）。"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
CLI = ROOT / "scripts" / "crane_check.py"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.crane_check import check_member, interpolate_capacity, render_markdown  # noqa: E402
from site_layout.model import CapacityPoint, Crane, Member  # noqa: E402


def run_cli(handoff: str, fleet: str, baseline: str, out_dir: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            str(CLI),
            "--handoff",
            str(FIXTURES / handoff),
            "--fleet",
            str(FIXTURES / fleet),
            "--baseline",
            str(FIXTURES / baseline),
            "--out-dir",
            str(out_dir),
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )


class CraneCheckTest(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="crane_check_test_")
        self.out = Path(self.tmp.name) / "out"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _result(self, handoff: str, fleet: str, baseline: str = "baseline.json") -> dict:
        proc = run_cli(handoff, fleet, baseline, self.out)
        self.assertEqual(proc.returncode, 0, msg=f"stdout={proc.stdout}\nstderr={proc.stderr}")
        data = json.loads((self.out / "crane_check.json").read_text(encoding="utf-8"))
        self.assertFalse(data["final_check"])
        return data

    def test_01_p4_insufficient(self) -> None:
        data = self._result("handoff_p4.json", "fleet_p4.json")
        row = data["members"][0]
        self.assertEqual(row["conclusion"], "insufficient")
        self.assertAlmostEqual(row["radius_m"], 27.7, places=2)
        self.assertAlmostEqual(row["capacity_t"], 8.92, delta=0.05)
        self.assertAlmostEqual(row["demand_t"], 28.46, delta=0.01)
        self.assertAlmostEqual(row["utilization"], 3.19, delta=0.02)
        print(
            "  [1/7] P4 25.6t@27.7m -> capacity={:.2f}t demand={:.2f}t "
            "util={:.3f} conclusion={}".format(
                row["capacity_t"], row["demand_t"], row["utilization"], row["conclusion"]
            )
        )

    def test_02_p3_insufficient(self) -> None:
        data = self._result("handoff_p3.json", "fleet_p3.json")
        row = data["members"][0]
        self.assertEqual(row["conclusion"], "insufficient")
        self.assertAlmostEqual(row["capacity_t"], 7.78, delta=0.05)
        self.assertAlmostEqual(row["utilization"], 3.66, delta=0.03)
        print(
            "  [2/7] P3 25.6t@67.4m -> capacity={:.2f}t demand={:.2f}t "
            "util={:.3f} conclusion={}".format(
                row["capacity_t"], row["demand_t"], row["utilization"], row["conclusion"]
            )
        )

    def test_03_p6_review_not_ok(self) -> None:
        data = self._result("handoff_p6.json", "fleet_p6.json")
        row = data["members"][0]
        self.assertEqual(row["conclusion"], "review")
        self.assertNotEqual(row["conclusion"], "ok")
        self.assertAlmostEqual(row["capacity_t"], 12.0, delta=0.1)
        self.assertAlmostEqual(row["utilization"], 0.91, delta=0.01)
        self.assertGreater(row["utilization"], 0.85)
        print(
            "  [3/7] P6 9.69t@14.9m -> capacity={:.2f}t demand={:.3f}t "
            "util={:.3f} conclusion={}".format(
                row["capacity_t"], row["demand_t"], row["utilization"], row["conclusion"]
            )
        )

    def test_04_missing_table_never_pass(self) -> None:
        data = self._result("handoff_d.json", "fleet_d.json")
        row = data["members"][0]
        self.assertEqual(row["conclusion"], "unknown_no_table")
        self.assertEqual(data["summary"]["unknown_no_table"], 1)
        self.assertEqual(data["summary"]["ok"], 0)
        report = (self.out / "crane_check.md").read_text(encoding="utf-8")
        self.assertNotIn("通过", report)
        self.assertNotIn("pass", report.lower())
        print(
            "  [4/7] D 系列 capacity_source=missing -> {}；报告不含“通过/pass”".format(
                row["conclusion"]
            )
        )

    def test_05_zone_blind_no_cross_zone(self) -> None:
        data = self._result("handoff_zone.json", "fleet_zone.json")
        row = data["members"][0]
        self.assertEqual(row["conclusion"], "blind")
        self.assertIsNone(row["crane_id"])
        self.assertEqual(data["summary"]["blind"], 1)
        print("  [5/7] A 区柱 + 仅 B 区塔吊 -> blind，未跨区分配")

    def test_06_baseline_lock_required(self) -> None:
        proc = run_cli("handoff_p4.json", "fleet_p4.json", "missing_baseline.json", self.out)
        self.assertEqual(proc.returncode, 5)
        self.assertIn("先锁口径再校核", proc.stderr)
        self.assertFalse(self.out.exists())

        proc = run_cli("handoff_p4.json", "fleet_p4.json", "baseline_unlocked.json", self.out)
        self.assertEqual(proc.returncode, 5)
        self.assertIn("先锁口径再校核", proc.stderr)

        proc = run_cli("handoff_p4.json", "fleet_p4.json", "baseline_version_mismatch.json", self.out)
        self.assertEqual(proc.returncode, 5)
        self.assertIn("先锁口径再校核", proc.stderr)
        print("  [6/7] baseline 缺失/未锁/版本不一致 -> exit 5，未出结论")

    def test_07_cm_unit_rejected(self) -> None:
        proc = run_cli("handoff_cm.json", "fleet_p4.json", "baseline.json", self.out)
        self.assertEqual(proc.returncode, 4)
        self.assertIn("单位", proc.stderr)
        self.assertIn("cm", proc.stderr)
        self.assertFalse(self.out.exists())
        print("  [7/7] 坐标声明 cm -> exit 4：{}".format(proc.stderr.strip()))

    # ---- 额外规则边界（不属于 7 条必测，但防止回归） ----

    def test_08_interpolation_edges(self) -> None:
        table = [CapacityPoint(20, 40), CapacityPoint(30, 8)]
        self.assertAlmostEqual(interpolate_capacity(table, 25), 24.0, places=6)
        self.assertAlmostEqual(interpolate_capacity(table, 20), 40.0, places=6)
        self.assertIsNone(interpolate_capacity(table, 19.9))
        self.assertIsNone(interpolate_capacity(table, 30.1))
        self.assertIsNone(interpolate_capacity([], 10))
        self.assertEqual(interpolate_capacity([CapacityPoint(10, 5)], 10), 5)
        self.assertIsNone(interpolate_capacity([CapacityPoint(10, 5)], 11))
        print("  [extra] 线性插值/单点/超范围 7 项断言 OK")

    def test_09_threshold_boundaries(self) -> None:
        crane = Crane(
            id="T1",
            model="TEST",
            jib_m=100,
            capacity_source="manufacturer",
            capacity_table=[CapacityPoint(10, 10), CapacityPoint(20, 1)],
            hook_weight_t=0.0,
            zones=["Z"],
            x_m=0.0,
            y_m=0.0,
        )
        member = Member("M", 8.5, 10.0, 0.0, "Z", "total", "confirmed")
        row = check_member(member, [crane], dynamic_factor=1.0, default_hook_t=0.0)
        self.assertEqual(row["conclusion"], "ok")
        self.assertAlmostEqual(row["utilization"], 0.85, places=6)

        member.weight_t = 10.0
        row = check_member(member, [crane], dynamic_factor=1.0, default_hook_t=0.0)
        self.assertEqual(row["conclusion"], "review")
        self.assertAlmostEqual(row["utilization"], 1.0, places=6)

        member.weight_t = 10.1
        row = check_member(member, [crane], dynamic_factor=1.0, default_hook_t=0.0)
        self.assertEqual(row["conclusion"], "insufficient")
        print("  [extra] 利用率 0.85 ok / 1.00 review / 1.01 insufficient OK")

    def test_10_missing_weight(self) -> None:
        data = self._result("handoff_missing_weight.json", "fleet_p4.json")
        row = data["members"][0]
        self.assertEqual(row["conclusion"], "unknown_no_weight")
        print("  [extra] 缺重量 -> unknown_no_weight，不补 0")

    def test_11_report_sections(self) -> None:
        data = self._result("handoff_d.json", "fleet_d.json")
        report = render_markdown(data)
        for heading in ("不合格", "盲区", "无性能表", "估算项", "逐柱明细"):
            self.assertIn(heading, report)
        self.assertIn("final_check=false", report)
        self.assertIn("estimated", report)
        print("  [extra] 报告含不合格/盲区/无性能表/估算项/明细分区")


if __name__ == "__main__":
    unittest.main(verbosity=2)
