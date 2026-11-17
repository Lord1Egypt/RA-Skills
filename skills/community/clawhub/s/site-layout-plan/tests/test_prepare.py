#!/usr/bin/env python3
"""site-layout-plan 0.6.7 · reader 契约 -> base-map 适配回归。"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
CLI = ROOT / "scripts" / "prepare_site.py"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.prepare import assemble_loop, prepare  # noqa: E402


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def prepare_inline(data: dict, **kwargs):
    """prepare 需要真实源文件算 sha256；测试用临时 JSON，不落 workspace。"""
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False)
        path = Path(handle.name)
    try:
        return prepare(data, path, **kwargs)
    finally:
        path.unlink(missing_ok=True)


def site_rows(layer: str, points: list[tuple[int, int]]) -> list[dict]:
    rows = []
    for index, start in enumerate(points):
        end = points[(index + 1) % len(points)]
        rows.append({
            "category": "site_boundary",
            "layer": layer,
            "system": "site",
            "geometry": [start[0], start[1], end[0], end[1]],
            "status": "candidate",
        })
    return rows


class PrepareUnitTest(unittest.TestCase):
    def test_mm_passthrough_and_redline_closed(self) -> None:
        result = prepare(load("reader_site_mm.json"), FIXTURES / "reader_site_mm.json")
        self.assertEqual(result["coord_unit"], "mm")
        self.assertEqual(result["unit"]["mm_per_unit"], 1.0)
        self.assertEqual(result["unit"]["basis"], "audit")
        self.assertEqual(len(result["redline"]), 4)
        self.assertTrue(result["redline_closed"])
        self.assertAlmostEqual(result["redline_area_m2"], 6000.0, places=3)
        self.assertEqual(result["extents_mm"], [0.0, 0.0, 100000.0, 60000.0])
        self.assertEqual(result["contract_id"], "CONTRACT-SYNTH-001")

    def test_meter_converted_to_mm(self) -> None:
        result = prepare(load("reader_site_m.json"), FIXTURES / "reader_site_m.json")
        self.assertEqual(result["unit"]["mm_per_unit"], 1000.0)
        self.assertEqual(result["extents_mm"], [0.0, 0.0, 100000.0, 60000.0])
        self.assertAlmostEqual(result["redline_area_m2"], 6000.0, places=3)

    def test_centimeter_converted_to_mm(self) -> None:
        result = prepare(load("reader_site_cm.json"), FIXTURES / "reader_site_cm.json")
        self.assertEqual(result["unit"]["mm_per_unit"], 10.0)
        self.assertEqual(result["extents_mm"], [0.0, 0.0, 1000.0, 600.0])
        self.assertAlmostEqual(result["redline_area_m2"], 0.6, places=3)

    def test_manual_unit_requires_confirmation(self) -> None:
        result = prepare(
            load("reader_site_no_unit.json"),
            FIXTURES / "reader_site_no_unit.json",
            unit_override="mm",
            confirmed_by="lis",
        )
        self.assertEqual(result["unit"]["basis"], "manual_confirmed")
        self.assertEqual(result["unit"]["confirmed_by"], "lis")
        self.assertTrue(result["warnings"])

    def test_no_unit_rejected(self) -> None:
        with self.assertRaises(Exception) as ctx:
            prepare(load("reader_site_no_unit.json"), FIXTURES / "reader_site_no_unit.json")
        self.assertEqual(getattr(ctx.exception, "exit_code", None), 4)

    def test_conflicting_units_rejected(self) -> None:
        with self.assertRaises(Exception) as ctx:
            prepare(load("reader_site_conflict.json"), FIXTURES / "reader_site_conflict.json")
        self.assertEqual(getattr(ctx.exception, "exit_code", None), 4)
        self.assertIn("冲突", str(ctx.exception))

    def test_override_disagreeing_with_reader_rejected(self) -> None:
        with self.assertRaises(Exception) as ctx:
            prepare(load("reader_site_mm.json"), FIXTURES / "reader_site_mm.json", unit_override="m")
        self.assertEqual(getattr(ctx.exception, "exit_code", None), 4)


class BoundaryLoopTest(unittest.TestCase):
    def test_first_segment_in_middle_still_closes(self) -> None:
        # 第一段位于环的中间；旧实现只会串到一侧，输出 2 个点。
        segments = [
            (10000.0, 0.0, 10000.0, 10000.0),
            (0.0, 0.0, 10000.0, 0.0),
            (0.0, 10000.0, 0.0, 0.0),
            (10000.0, 10000.0, 0.0, 10000.0),
        ]
        points, closed, gap = assemble_loop(segments, 50.0)
        self.assertTrue(closed)
        self.assertEqual(len(points), 4)
        self.assertEqual(gap, 0.0)

    def test_close_gap_snap_preserves_short_edges(self) -> None:
        # 50 mm 聚类保住 1.9 m 短边；只允许首尾缺口一次性收口。
        segments = [
            (0.0, 0.0, 100000.0, 0.0),
            (100000.0, 0.0, 100000.0, 60000.0),
            (100000.0, 60000.0, 0.0, 60000.0),
            (0.0, 60000.0, 1900.0, 0.0),
        ]
        points, closed, gap = assemble_loop(segments, 50.0, close_gap_mm=2500.0)
        self.assertTrue(closed)
        self.assertEqual(len(points), 4)
        self.assertEqual(gap, 0.0)

    def test_annotation_layers_excluded_and_no_cross_layer(self) -> None:
        data = {
            "coord_unit": "mm",
            "contract": {"contract_id": "SYNTH-BOUNDARY"},
            "site_geometry": (
                site_rows("0-控制线-用地红线", [(0, 0), (100000, 0), (100000, 60000), (0, 60000)])
                + site_rows("0-控制线-建筑红线", [(10000, 10000), (20000, 10000), (20000, 20000), (10000, 20000)])
                + [{
                    "category": "annotation",
                    "layer": "1-标注-间距-建筑距红线",
                    "system": "annotation",
                    "geometry": [0, 0, 50000, 30000],
                    "status": "candidate",
                }]
            ),
        }
        result = prepare_inline(data)
        self.assertEqual(len(result["redline"]), 4)
        self.assertTrue(result["redline_closed"])
        self.assertAlmostEqual(result["redline_area_m2"], 6000.0, places=3)
        selection = result["boundary_selection"]
        self.assertEqual(selection["selected_layer"], "0-控制线-用地红线")
        self.assertEqual(selection["selected_segments"], 4)
        self.assertEqual(selection["annotation_segments_excluded"], 1)
        self.assertNotIn("建筑红线", selection["selected_layer"])

    def test_boundary_layer_cli_parameter(self) -> None:
        data = {
            "coord_unit": "mm",
            "contract": {"contract_id": "SYNTH-LAYER"},
            "site_geometry": (
                site_rows("0-控制线-用地红线", [(0, 0), (100000, 0), (100000, 60000), (0, 60000)])
                + site_rows("0-控制线-建筑红线", [(10000, 10000), (20000, 10000), (20000, 20000), (10000, 20000)])
            ),
        }
        result = prepare_inline(data, boundary_layer="0-控制线-建筑红线")
        self.assertEqual(result["boundary_selection"]["selected_layer"], "0-控制线-建筑红线")
        self.assertEqual(len(result["redline"]), 4)


class WeakUnitTest(unittest.TestCase):
    def weak_site(self) -> dict:
        return {
            "contract": {"contract_id": "SYNTH-WEAK"},
            "scale_unit_audit": [{
                "file": "synthetic.dxf",
                "units": ["mm"],
                "status": "candidate",
                "evidence": [{"text": "打印线宽 1.2mm", "layer": "0-图框"}],
            }],
            "site_geometry": site_rows("红线", [(0, 0), (100000, 0), (100000, 60000), (0, 60000)]),
        }

    def test_weak_unit_rejected_without_manual_confirmation(self) -> None:
        with self.assertRaises(Exception) as ctx:
            prepare_inline(self.weak_site())
        self.assertEqual(getattr(ctx.exception, "exit_code", None), 4)
        self.assertIn("1.2mm", str(ctx.exception))

    def test_weak_unit_manual_confirmation_allowed_with_warning(self) -> None:
        result = prepare_inline(
            self.weak_site(), unit_override="m", confirmed_by="auditor"
        )
        self.assertEqual(result["unit"]["basis"], "manual_confirmed")
        self.assertEqual(result["unit"]["mm_per_unit"], 1000.0)
        self.assertTrue(any("打印/线宽" in warning for warning in result["warnings"]))


class BaseMapSchemaTest(unittest.TestCase):
    def test_required_fields_present(self) -> None:
        schema = load("../schemas/base-map.schema.json") if False else json.loads(
            (ROOT / "schemas" / "base-map.schema.json").read_text(encoding="utf-8")
        )
        result = prepare(load("reader_site_mm.json"), FIXTURES / "reader_site_mm.json")
        for key in schema["required"]:
            self.assertIn(key, result)
        self.assertEqual(result["schema"], schema["properties"]["schema"]["const"])


class PrepareCliTest(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(CLI), *args], capture_output=True, text=True, timeout=120
        )

    def test_cli_writes_base_map_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            proc = self.run_cli(
                "--site", str(FIXTURES / "reader_site_mm.json"), "--out-dir", tmp
            )
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            base = Path(tmp) / "base-map.json"
            self.assertTrue(base.is_file())
            self.assertTrue((Path(tmp) / "base-map.md").is_file())
            data = json.loads(base.read_text(encoding="utf-8"))
            self.assertEqual(data["schema"], "site-layout-base-map/v1")
            self.assertEqual(data["coord_unit"], "mm")

    def test_cli_manual_unit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            proc = self.run_cli(
                "--site", str(FIXTURES / "reader_site_no_unit.json"),
                "--out-dir", tmp, "--unit", "mm", "--confirmed-by", "lis",
            )
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            data = json.loads((Path(tmp) / "base-map.json").read_text(encoding="utf-8"))
            self.assertEqual(data["unit"]["basis"], "manual_confirmed")

    def test_cli_missing_unit_exit4_no_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            proc = self.run_cli(
                "--site", str(FIXTURES / "reader_site_no_unit.json"), "--out-dir", tmp
            )
            self.assertEqual(proc.returncode, 4, proc.stderr + proc.stdout)
            self.assertFalse((Path(tmp) / "base-map.json").exists())

    def test_cli_conflict_exit4(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            proc = self.run_cli(
                "--site", str(FIXTURES / "reader_site_conflict.json"), "--out-dir", tmp
            )
            self.assertEqual(proc.returncode, 4, proc.stderr + proc.stdout)


class PrepareToDrawTest(unittest.TestCase):
    def test_base_map_loads_in_drawer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, str(CLI), "--site", str(FIXTURES / "reader_site_mm.json"),
                 "--out-dir", tmp],
                capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            from site_layout.bootstrap import ensure_runtime

            ensure_runtime(__file__)
            from site_layout.draw import load_site

            site = load_site(str(Path(tmp) / "base-map.json"))
            self.assertEqual(site.source_units, "mm")
            self.assertEqual(site.mm_per_unit, 1.0)
            self.assertTrue(site.redline_closed)
            self.assertEqual(len(site.redline_vertices), 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
