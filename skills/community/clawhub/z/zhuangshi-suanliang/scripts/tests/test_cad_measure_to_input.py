#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "cad_measure_to_input.py"


class CadMeasureToInputTest(unittest.TestCase):
    def test_converts_area_and_length_but_marks_review(self):
        payload = {
            "schema": "cad-measurement-candidates/v1",
            "measurements": [
                {"kind": "area", "value": 12.5, "unit": "m2", "formula": "50000000 mm² = 50 m2", "basis": "polygon", "method": "shoelace", "status": "candidate", "review_reason": "", "source_schema": "cad-descriptive-geometry/v7", "source_id": "room-1", "rooms": ["办公室"]},
                {"kind": "length", "value": None, "unit": "m", "value_drawing_units": 3000, "drawing_unit": "mm", "review_reason": "缺比例或单位", "basis": "wall_segment", "method": "segment_sum", "status": "review", "source_schema": "cad-descriptive-geometry/v7", "source_id": "wall-1"},
                {"kind": "volume", "value": 3.0, "unit": "m3", "basis": "area_x_thickness", "method": "area_times_explicit_parameter", "status": "review", "source_schema": "cad-descriptive-geometry/v7", "source_id": "v-1"},
            ],
        }
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            src = root / "measure.json"
            out = root / "decor.csv"
            src.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            proc = subprocess.run([sys.executable, str(SCRIPT), "--measurements", str(src), "--out", str(out), "--floor", "二层", "--no-validate"], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            with out.open(encoding="utf-8-sig") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 2)
            self.assertTrue(all(row["需核对"] == "是" for row in rows))
            self.assertTrue(all(row["做法编号"] == "" for row in rows))
            self.assertEqual(rows[0]["直接面积_m2"], "12.5")
            self.assertEqual(rows[1]["直接长度_m"], "")
            self.assertIn("图面值 3000 mm", rows[1]["说明"])

    def test_imports_descriptive_candidates_all_review(self):
        payload = {"schema": "cad-measurement-candidates/v1", "measurements": []}
        descriptive = {
            "schema": "cad-descriptive-geometry/v7",
            "room_boundaries": [{"source_id": "room-1", "rooms": ["办公室"], "bbox": [0, 0, 12000, 8000]}],
            "wall_segments": [{"source_id": "wall-1", "rooms": ["办公室"], "segment": [0, 0, 12000, 0],
                               "segment_kind": "clear", "height_m": 3.0}],
            "ceiling_zones": [{"source_id": "ceil-1", "rooms": ["办公室"], "zone_kind": "ceiling", "elevation_m": 2.8}],
            "openings": [{"source_id": "op-1", "code": "M1021", "geometry": {"room_candidates": ["办公室"]}}],
            "node_detail_index": [{"source_id": "node-1", "practice_codes": ["地101"], "node_codes": ["A"]}],
        }
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            src = root / "measure.json"
            desc = root / "desc.json"
            out = root / "decor.csv"
            src.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            desc.write_text(json.dumps(descriptive, ensure_ascii=False), encoding="utf-8")
            proc = subprocess.run([sys.executable, str(SCRIPT), "--measurements", str(src),
                                   "--descriptive", str(desc), "--out", str(out), "--floor", "二层", "--no-validate"],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            with out.open(encoding="utf-8-sig") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 5)
            self.assertTrue(all(row["需核对"] == "是" for row in rows))
            self.assertEqual(rows[0]["部位类型"], "待确认-房间")
            self.assertEqual(rows[1]["部位类型"], "待确认-墙面")
            self.assertEqual(rows[2]["部位类型"], "待确认-顶棚")
            self.assertEqual(rows[3]["部位类型"], "待确认-门窗洞口")
            self.assertEqual(rows[4]["做法编号"], "地101")
            self.assertEqual(rows[4]["节点编号"], "A")

    def test_imports_interior_finish_and_insulation_candidates_all_review(self):
        payload = {
            "schema": "cad-interior-finish-geometry/v1",
            "components": [
                {"source_id": "floor-1", "system": "floor", "category": "floor_layer", "raw": "地面做法 瓷砖", "evidence": [{"text": "地面做法 瓷砖", "layer": "INT-FLOOR", "coord": [1, 2]}]},
                {"source_id": "ins-1", "system": "insulation", "category": "insulation", "raw": "外墙外保温 岩棉", "evidence": [{"text": "外墙外保温 岩棉", "layer": "INT-WALL-保温"}]},
            ],
            "references": [
                {"source_id": "ref-1", "reference_type": "finish_code", "value": "DM-01", "raw": "DM-01", "evidence": [{"text": "DM-01", "layer": "TITLE"}]},
            ],
        }
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            src = root / "finish.json"
            out = root / "decor.csv"
            src.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            proc = subprocess.run([sys.executable, str(SCRIPT), "--interior-finish", str(src), "--out", str(out), "--floor", "三层", "--no-validate"], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            with out.open(encoding="utf-8-sig") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 3)
            self.assertTrue(all(row["需核对"] == "是" for row in rows))
            self.assertEqual(rows[0]["部位类型"], "待确认-地面")
            self.assertEqual(rows[1]["部位类型"], "待确认-保温")
            self.assertEqual(rows[2]["做法编号"], "DM-01")

    def test_imports_local_notes_text_as_review_evidence(self):
        payload = {"schema": "cad-measurement-candidates/v1", "measurements": []}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            src = root / "measure.json"
            notes = root / "finish-ocr.txt"
            out = root / "decor.csv"
            src.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            notes.write_text(
                "外墙外保温 120厚岩棉 传热系数需复核\n"
                "地下室顶板 2厚聚氨酯防水涂料\n"
                "无关说明文字\n",
                encoding="utf-8",
            )
            proc = subprocess.run([
                sys.executable, str(SCRIPT), "--measurements", str(src),
                "--notes-text", str(notes), "--out", str(out), "--floor", "四层",
                "--no-validate",
            ], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            with out.open(encoding="utf-8-sig") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 2)
            self.assertTrue(all(row["需核对"] == "是" for row in rows))
            self.assertEqual(rows[0]["部位类型"], "待确认-保温")
            self.assertEqual(rows[1]["部位类型"], "待确认-防水")
            self.assertIn("OCR 文本证据", rows[0]["说明"])
            self.assertEqual(rows[0]["做法编号"], "")

    def test_validate_fails_when_base_missing_by_default(self):
        """默认 --validate 缺底座必须 exit 1，不能静默跳过。"""
        payload = {"schema": "cad-measurement-candidates/v1", "measurements": []}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            src = root / "measure.json"
            out = root / "decor.csv"
            src.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            env = {"PATH": "/usr/bin:/bin", "CAD_SKILL_DIR": str(root / "not-exists")}
            proc = subprocess.run([sys.executable, str(SCRIPT), "--measurements", str(src),
                                   "--out", str(out), "--floor", "二层"],
                                  capture_output=True, text=True, env=env)
            self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
            self.assertFalse(out.exists())
            self.assertIn("cad-file-reader", proc.stderr)

    def test_explicit_no_validate_marks_skipped(self):
        payload = {"schema": "cad-measurement-candidates/v1", "measurements": []}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            src = root / "measure.json"
            out = root / "decor.csv"
            src.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            env = {"PATH": "/usr/bin:/bin", "CAD_SKILL_DIR": str(root / "not-exists")}
            proc = subprocess.run([sys.executable, str(SCRIPT), "--measurements", str(src),
                                   "--out", str(out), "--floor", "二层", "--no-validate"],
                                  capture_output=True, text=True, env=env)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            summary = json.loads(proc.stdout)
            self.assertEqual(summary["validation"], "skipped")


if __name__ == "__main__":
    unittest.main()
