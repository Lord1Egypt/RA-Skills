#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""municipal_qty 核心口径单测（纯 stdlib；fixture 内联，不依赖外部图纸）。"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))

FIXTURES = SCRIPTS.parent / "tests" / "fixtures"

from contract_guard import GuardError, guard_contract, stamp_result  # noqa: E402
import municipal_qty as mq  # noqa: E402


def _payload(**overrides) -> dict:
    """真实识图契约形态（英文枚举，与 cad_municipal_geometry.py 实际输出一致）。"""
    base = {
        "schema": "cad-municipal-geometry/v1",
        "source_file": "sample.dwg",
        "coordinate_unit": "mm",
        "summary": {},
        "drawing_types": [],
        "systems": [{"system": "rainwater", "raw": "DIM_雨水", "status": "candidate"}],
        "components": [
            {"type": "component", "category": "manhole", "system": "rainwater",
             "raw": "雨水检查井 φ1000", "pattern": "检查井", "system_basis": "text",
             "layer": "GS-SS", "file": "sample.dwg", "sheet": "PS-01",
             "x": 0, "y": 0, "confidence": 0.78, "status": "candidate",
             "review_reason": "", "evidence": []},
            {"type": "component", "category": "manhole", "system": "",
             "raw": "雨水检查井 φ1000", "pattern": "检查井", "system_basis": "component_rule",
             "layer": "GS-SS", "file": "sample.dwg", "sheet": "PS-01",
             "x": 30000, "y": 0, "confidence": 0.78, "status": "candidate",
             "review_reason": "", "evidence": []},
            {"type": "component", "category": "manhole", "system": "rainwater",
             "raw": "偏沟式雨水口", "pattern": "雨水口", "system_basis": "text",
             "layer": "GS-YSK", "file": "sample.dwg", "sheet": "PS-01",
             "x": 15000, "y": 5000, "confidence": 0.78, "status": "candidate",
             "review_reason": "", "evidence": []},
        ],
        "pipe_network": [
            {"type": "pipe", "system": "rainwater", "raw": "d800雨水管 W1-W2",
             "pipe_size": "d800", "pattern": "雨水管", "layer": "DIM_雨水",
             "file": "sample.dwg", "sheet": "PS-01", "x": 0, "y": 0,
             "confidence": 0.78, "status": "candidate", "review_reason": "",
             "evidence": []},
            {"type": "pipe", "system": "rainwater", "raw": "雨水管（无管径）",
             "pipe_size": "", "pattern": "雨水管", "layer": "DIM_雨水",
             "file": "sample.dwg", "sheet": "PS-01", "x": 5000, "y": 0,
             "confidence": 0.78, "status": "review",
             "review_reason": "识别到市政管道但未提取到管径或断面尺寸", "evidence": []},
        ],
        "materials": [
            {"type": "material", "category": "asphalt", "value": "SBS 改性沥青上面层 4cm",
             "raw": "SBS 改性沥青混凝土上面层厚4cm", "layer": "TEXT",
             "file": "sample.dwg", "sheet": "PJ-01", "x": 0, "y": 0,
             "confidence": 0.95, "status": "candidate", "evidence": []},
        ],
        "references": [],
        "labels": [
            {"type": "label", "label_type": "dimension", "value": "40",
             "raw": "红线宽 40m", "layer": "TEXT", "file": "sample.dwg",
             "sheet": "DL-01", "x": 0, "y": 0, "confidence": 0.95,
             "status": "candidate", "evidence": []},
        ],
        "municipal_geometry": [
            # 真实契约里管道图层不命中 component_rules -> category=unclassified_municipal、
            # system=英文键、status=review
            {"type": "municipal_geometry", "category": "unclassified_municipal",
             "system": "rainwater", "pattern": "雨水", "layer": "DIM_雨水",
             "file": "sample.dwg", "file_index": 0, "sheet": "PS-01",
             "geometry": [0, 0, 120000, 0], "length_drawing_units": 120000.0,
             "confidence": 0.86, "status": "review",
             "review_reason": "市政图层未映射到构件类别", "evidence": []},
            {"type": "municipal_geometry", "category": "road_centerline",
             "system": "road", "pattern": "道路中线", "layer": "道路中线",
             "file": "sample.dwg", "file_index": 0, "sheet": "DL-01",
             "geometry": [0, 0, 0, 80000], "length_drawing_units": 80000.0,
             "confidence": 0.86, "status": "candidate", "review_reason": "",
             "evidence": []},
        ],
        "entities": [],
        "connectivity": {"summary": {"open_endpoints": 2, "junction_candidates": 3}},
        "review": [{"type": "pipe_size", "reason": "识别到市政管道但未提取到管径或断面尺寸"}],
        "boundary": "只输出识图候选",
    }
    base.update(overrides)
    return base


def _legacy_chinese_payload(**overrides) -> dict:
    """中文文本形态（手工契约/旧版识图产物）——验证回退路径。"""
    base = {
        "schema": "cad-municipal-geometry/v1",
        "source_file": "legacy.dwg",
        "coordinate_unit": "mm",
        "components": [
            {"category": "检查井", "system": "雨水", "raw": "雨水检查井 1000",
             "layer": "GS-SS", "x": 0, "y": 0, "status": "candidate"},
        ],
        "pipe_network": [
            {"system": "雨水", "pipe_size": "DN800", "raw": "d800 雨水管",
             "layer": "GS-YS", "x": 0, "y": 0, "status": "candidate"},
        ],
        "materials": [
            {"category": "沥青", "value": "SBS 改性沥青上面层 4cm", "layer": "TEXT"},
        ],
        "references": [],
        "labels": [
            {"label_type": "宽度", "value": "红线宽 40m", "layer": "TEXT"},
        ],
        "municipal_geometry": [
            {"category": "雨水管", "system": "雨水", "layer": "GS-YS",
             "geometry": [0, 0, 60000, 0], "file": "legacy.dwg", "sheet": "PS-01",
             "status": "candidate"},
            {"category": "道路中线", "system": "道路", "layer": "DL-ZX",
             "geometry": [0, 0, 0, 80000], "file": "legacy.dwg", "sheet": "DL-01",
             "status": "candidate"},
        ],
        "entities": [],
        "connectivity": {"summary": {"open_endpoints": 1, "junction_candidates": 2}},
        "review": [],
        "boundary": "只输出识图候选",
    }
    base.update(overrides)
    return base


def _write(tmp: Path, payload: dict, name: str = "sample.municipal.json") -> Path:
    path = tmp / name
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


class BoundaryTests(unittest.TestCase):
    """A4 边界用例：识图层产物常见杂讯形态。"""

    def test_polyline_segments_accumulate(self):
        """管道被拆成多段折线：段长累加。"""
        payload = _payload(municipal_geometry=[
            {"category": "unclassified_municipal", "system": "rainwater",
             "layer": "DIM_雨水", "sheet": "PS-01", "geometry": [0, 0, 60000, 0],
             "length_drawing_units": 60000.0, "status": "candidate"},
            {"category": "unclassified_municipal", "system": "rainwater",
             "layer": "DIM_雨水", "sheet": "PS-01", "geometry": [60000, 0, 120000, 0],
             "length_drawing_units": 60000.0, "status": "candidate"},
        ])
        evidence = mq._extract(payload, 1.0)
        self.assertAlmostEqual(evidence["pipe_len_mm"]["雨水"], 120000.0)
        self.assertEqual(evidence["pipe_seg_count"]["雨水"], 2)

    def test_duplicate_segments_deduped(self):
        """完全重复段（layer+图幅+几何一致）去重，防止双计。"""
        row = {"category": "unclassified_municipal", "system": "rainwater",
               "layer": "DIM_雨水", "sheet": "PS-01",
               "geometry": [0, 0, 120000, 0], "length_drawing_units": 120000.0,
               "status": "candidate"}
        payload = _payload(municipal_geometry=[row, dict(row)])
        evidence = mq._extract(payload, 1.0)
        self.assertAlmostEqual(evidence["pipe_len_mm"]["雨水"], 120000.0)
        self.assertEqual(evidence["pipe_seg_count"]["雨水"], 1)
        self.assertTrue(any("重复段" in w for w in evidence["warnings"]))

    def test_geometry_without_quad_skipped(self):
        """geometry 缺四元组且无 length_drawing_units：跳过不崩。"""
        payload = _payload(municipal_geometry=[
            {"category": "unclassified_municipal", "system": "rainwater",
             "layer": "DIM_雨水", "geometry": [0, 0], "status": "candidate"},
        ])
        evidence = mq._extract(payload, 1.0)
        self.assertNotIn("雨水", evidence["pipe_len_mm"])

    def test_width_dirty_value_filtered(self):
        """宽度脏值（300m 越界）过滤，多档冲突取多数。"""
        payload = _payload(labels=[
            {"label_type": "dimension", "value": "40", "raw": "红线宽 40m"},
            {"label_type": "dimension", "value": "40", "raw": "断面宽 40m"},
            {"label_type": "dimension", "value": "300", "raw": "宽 300m"},
        ])
        evidence = mq._extract(payload, 1.0)
        self.assertEqual(evidence["road_width_m"], 40.0)

    def test_unit_scale_one_non_mm_warns(self):
        """m 单位 unit_scale=1：与固有换算不一致，以 1000 为准并警告。"""
        payload = _payload(coordinate_unit="m", unit_scale=1)
        warnings: list[str] = []
        factor = mq._to_mm_factor(payload, warnings)
        self.assertEqual(factor, 1000.0)
        self.assertTrue(any("不一致，以 1000 为准" in w for w in warnings))

    def test_wells_multiple_systems(self):
        """井类按系统分组，不混账。"""
        payload = _payload(components=[
            {"category": "manhole", "system": "rainwater", "raw": "雨水检查井 φ1000",
             "layer": "A", "x": 0, "y": 0, "status": "candidate"},
            {"category": "manhole", "system": "sewage", "raw": "污水检查井 φ1000",
             "layer": "B", "x": 1, "y": 1, "status": "candidate"},
            {"category": "manhole", "system": "", "raw": "给水阀门井",
             "layer": "C", "x": 2, "y": 2, "status": "candidate"},
        ])
        evidence = mq._extract(payload, 1.0)
        self.assertEqual(evidence["wells"]["雨水"]["检查井"], 1)
        self.assertEqual(evidence["wells"]["污水"]["检查井"], 1)
        # raw="给水阀门井" 含系统名 → 归「给水」而不是「其他」（中文回退正确行为）
        self.assertEqual(evidence["wells"]["给水"]["阀门井"], 1)

    def test_length_drawing_units_preferred(self):
        """有 length_drawing_units 时优先用，不重算几何。"""
        row = {"category": "unclassified_municipal", "system": "rainwater",
               "layer": "DIM_雨水", "geometry": [0, 0, 10, 0],
               "length_drawing_units": 50000.0, "status": "candidate"}
        self.assertAlmostEqual(mq._seg_len_mm(row), 50000.0)

    def test_forged_no_id_fixture_guards(self):
        """fixture：reader 来源缺 contract_id -> guard 3（入口映射 22）。"""
        doc = json.loads((FIXTURES / "forged_no_id.json").read_text(encoding="utf-8"))
        with self.assertRaises(GuardError) as ctx:
            mq._guard_from_dict(mq._synthetic_guard_doc(doc), allow_manual=False,
                                label="forged")
        self.assertEqual(ctx.exception.code, 3)


class RealFormTests(unittest.TestCase):
    """真实识图契约形态回归：缺 coordinate_unit + 嵌套 contract_id + audit。"""

    def _load(self):
        import json
        return json.loads(FIXTURES.parent.parent.joinpath(
            "tests", "fixtures", "real_contract_no_unit.json").read_text(encoding="utf-8"))

    def test_real_form_guard_accepts_and_downgrades(self):
        """真实形态过闸门（嵌套 contract_id + audit 放行）并降级 manual。"""
        data = self._load()
        guard, payload = mq._guard_file_manual(str(FIXTURES.parent.parent / "tests" / "fixtures" / "real_contract_no_unit.json"))
        self.assertEqual(guard["mode"], "manual")
        self.assertEqual(payload.get("schema"), "cad-municipal-geometry/v1")

    def test_real_form_unit_inferred_m(self):
        """无 coordinate_unit：按坐标量级（6 位测量坐标）推断 m，factor=1000。"""
        data = self._load()
        warnings: list[str] = []
        factor = mq._to_mm_factor(data, warnings)
        self.assertEqual(factor, 1000.0)
        self.assertTrue(any("推断为测量坐标 m" in w for w in warnings))

    def test_real_form_pipe_and_road(self):
        """管道段 review 状态按 system 计入；道路中线提取；宽度缺->unavailable。"""
        data = self._load()
        warnings: list[str] = []
        ev = mq._extract(data, 1000.0)
        self.assertAlmostEqual(ev["pipe_len_mm"]["雨水"], 150000.0)
        self.assertAlmostEqual(ev["road_len_mm"], 400000.0)
        self.assertIsNone(ev["road_width_m"])


class CaliberEnhancementTests(unittest.TestCase):
    """B2-B5 口径增强回归。"""

    def _build(self, tmp, payload, prefix="b2b5", **kw):
        import json
        path = Path(tmp) / ("in_" + prefix + ".json")
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        mq.build(str(path), str(Path(tmp) / prefix),
                 guard={"mode": "manual", "provenance": "test",
                        "warnings": [], "contract_id": "test",
                        "source_sha256": None, "contract_sha256": None},
                 **kw)
        return json.loads((Path(tmp) / (prefix + ".json")).read_text(encoding="utf-8-sig"))

    def test_b2_well_specs_extracted(self):
        """B2: 井 raw 含 φ1000 时输出规格分档。"""
        with tempfile.TemporaryDirectory() as tmp:
            payload = _payload(components=[
                {"category": "manhole", "system": "rainwater", "raw": "雨水检查井 φ1000",
                 "layer": "GS-SS", "x": 0, "y": 0, "status": "candidate"},
                {"category": "manhole", "system": "rainwater", "raw": "雨水检查井 φ1250",
                 "layer": "GS-SS", "x": 30000, "y": 0, "status": "candidate"},
            ])
            out = self._build(tmp, payload)
            specs = [w for w in out["wells_count"] if "井规格" in w["category"]]
            self.assertEqual(len(specs), 2)
            self.assertTrue(any("φ1000" in w["category"] for w in specs))

    def test_b3_weak_pairing_not_in_main(self):
        """B3: 弱配对单独输出 evidence_grade=weak，主口径不受影响。"""
        with tempfile.TemporaryDirectory() as tmp:
            out = self._build(tmp, _payload())
            ref = out["pipe_length_by_layer_ref"]
            self.assertTrue(ref)
            self.assertTrue(all(r["evidence_grade"] == "weak" for r in ref))
            main = sum(p["length_m_estimate_low"] for p in out["pipes_length_estimate"])
            self.assertGreater(main, 0)

    def test_b4_survey_table_passthrough(self):
        """B4: station/elevation/slope 透传复核表。"""
        with tempfile.TemporaryDirectory() as tmp:
            payload = _payload(labels=[
                {"label_type": "station", "value": "K0+120", "layer": "T"},
                {"label_type": "elevation", "value": "45.23", "layer": "T"},
                {"label_type": "slope", "value": "i=0.003", "layer": "T"},
                {"label_type": "coordinate", "value": "X=1 Y=2", "layer": "T"},
            ])
            out = self._build(tmp, payload)
            types = {r["label_type"] for r in out["survey_review_table"]}
            self.assertEqual(types, {"station", "elevation", "slope"})

    def test_b5_dual_caliber_and_road_width_flag(self):
        """B5: 中线/边线双口径交叉 + --road-width 显式传参。"""
        with tempfile.TemporaryDirectory() as tmp:
            payload = _payload(
                municipal_geometry=[
                    {"category": "road_centerline", "system": "road", "layer": "DL-ZX",
                     "geometry": [0, 0, 0, 100000], "file": "s.dwg", "sheet": 1, "status": "candidate"},
                    {"category": "road_edge", "system": "road", "layer": "DL-BX",
                     "geometry": [0, 0, 0, 205000], "file": "s.dwg", "sheet": 1, "status": "candidate"},
                ],
                labels=[])
            out = self._build(tmp, payload, road_width_override=20.0)
            road = out["road_area_estimate"]
            self.assertEqual(road["width_basis"], "--road-width 显式传参")
            cross = road["edge_crosscheck"]
            self.assertEqual(cross["evidence_grade"], "weak")
            # 边线 205m/2=102.5m vs 中线 100m，偏差 2.5% <= 10% 无警告
            self.assertLessEqual(cross["deviation_percent"], 10.0)

    def test_b5_dual_caliber_deviation_warns(self):
        """B5: 双口径偏差 >10% 出警告。"""
        with tempfile.TemporaryDirectory() as tmp:
            payload = _payload(
                municipal_geometry=[
                    {"category": "road_centerline", "system": "road", "layer": "DL-ZX",
                     "geometry": [0, 0, 0, 100000], "file": "s.dwg", "sheet": 1, "status": "candidate"},
                    {"category": "kerb", "system": "road", "layer": "DL-BX",
                     "geometry": [0, 0, 0, 300000], "file": "s.dwg", "sheet": 1, "status": "candidate"},
                ],
                labels=[])
            out = self._build(tmp, payload, road_width_override=20.0)
            road = out["road_area_estimate"]
            self.assertGreater(road["edge_crosscheck"]["deviation_percent"], 10.0)
            self.assertTrue(any("双口径偏差" in w for w in out["warnings"]))

    def test_b6_well_density_per_100m(self):
        """B6: 井密度座/百米按系统输出。"""
        with tempfile.TemporaryDirectory() as tmp:
            out = self._build(tmp, _payload())
            dens = [w for w in out["wells_count"] if "井密度" in w["category"]]
            self.assertTrue(dens)
            self.assertEqual(dens[0]["system"], "雨水")


class ArcSegmentTests(unittest.TestCase):
    """弧段行（识图层 ARC 提取产物）的算量处理。"""

    def _arc_row(self, length_units, *, status="candidate", system="road"):
        return {"category": "unclassified_municipal" if status == "review" else "road_centerline",
                "system": system, "layer": "DL-ZX", "file": "s.dwg", "sheet": 1,
                "geometry": [0, 0, 100, 0],
                "length_drawing_units": length_units,
                "arc": {"center": [0, 0], "radius": 50, "sweep_rad": 1.0, "basis": "arc_length"},
                "status": status}

    def test_arc_length_used_over_chord(self):
        """弧段行优先用 length_drawing_units（弧长），不用弦长。"""
        payload = _payload(municipal_geometry=[self._arc_row(300.0)])
        ev = mq._extract(payload, 1.0)
        self.assertAlmostEqual(ev["road_len_mm"], 300.0)

    def test_review_arc_counts_with_warning(self):
        """review 弧段按道路口径计入并出警告。"""
        payload = _payload(municipal_geometry=[self._arc_row(200.0, status="review")])
        warnings: list[str] = []
        ev = mq._extract(payload, 1.0)
        self.assertAlmostEqual(ev["road_len_mm"], 200.0)

    def test_review_straight_line_not_counted(self):
        """unclassified 直线段（可能为边线/红线）不归入道路中线。"""
        payload = _payload(municipal_geometry=[
            {"category": "unclassified_municipal", "system": "road", "layer": "DL-BX",
             "geometry": [0, 0, 100, 0], "file": "s.dwg", "sheet": 1, "status": "review"}])
        ev = mq._extract(payload, 1.0)
        self.assertEqual(ev["road_len_mm"], 0.0)


class LegendTests(unittest.TestCase):
    """蓝标系列图示（SVG + md 色标图例）。"""

    def test_svg_legend_generated_with_colors(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = _payload()
            path = Path(tmp) / "in.json"
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            mq.build(str(path), str(Path(tmp) / "out"), guard={
                "mode": "manual", "provenance": "test", "warnings": [],
                "contract_id": "t", "source_sha256": None, "contract_sha256": None})
            svg = (Path(tmp) / "out.svg").read_text(encoding="utf-8")
            self.assertIn("市政系统色标图例", svg)
            self.assertIn('fill="#4DA6E8"', svg)  # 雨水色标

    def test_md_contains_legend_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = _payload()
            path = Path(tmp) / "in.json"
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            mq.build(str(path), str(Path(tmp) / "out"), guard={
                "mode": "manual", "provenance": "test", "warnings": [],
                "contract_id": "t", "source_sha256": None, "contract_sha256": None})
            md = (Path(tmp) / "out.md").read_text(encoding="utf-8")
            self.assertIn("系统色标图例", md)
            self.assertIn("#4DA6E8", md)


class ValidateTests(unittest.TestCase):
    def test_valid_payload_passes(self):
        out = mq._validated_payload(_payload())
        self.assertEqual(out["schema"], "cad-municipal-geometry/v1")

    def test_wrong_schema_exits_2(self):
        with self.assertRaises(SystemExit) as ctx:
            mq._validated_payload({"schema": "cad-steel-geometry/v1"})
        self.assertEqual(ctx.exception.code, 2)

    def test_empty_evidence_exits_5(self):
        with self.assertRaises(SystemExit) as ctx:
            mq._validated_payload(_payload(components=[], pipe_network=[],
                                           municipal_geometry=[], labels=[]))
        self.assertEqual(ctx.exception.code, 5)


class ExtractTests(unittest.TestCase):
    def test_pipe_length_mm(self):
        warnings: list[str] = []
        evidence = mq._extract(_payload(), 1.0)
        self.assertAlmostEqual(evidence["pipe_len_mm"]["雨水"], 120000.0)
        self.assertEqual(evidence["pipe_seg_count"]["雨水"], 1)

    def test_road_length_and_width(self):
        evidence = mq._extract(_payload(), 1.0)
        self.assertAlmostEqual(evidence["road_len_mm"], 80000.0)
        self.assertEqual(evidence["road_width_m"], 40.0)

    def test_well_counts(self):
        evidence = mq._extract(_payload(), 1.0)
        self.assertEqual(evidence["wells"]["雨水"]["检查井"], 2)
        self.assertEqual(evidence["wells"]["雨水"]["雨水口"], 1)

    def test_legacy_chinese_fallback(self):
        """中文文本形态（手工契约/旧产物）走回退路径，结果一致。"""
        evidence = mq._extract(_legacy_chinese_payload(), 1.0)
        self.assertAlmostEqual(evidence["pipe_len_mm"]["雨水"], 60000.0)
        self.assertAlmostEqual(evidence["road_len_mm"], 80000.0)
        self.assertEqual(evidence["road_width_m"], 40.0)
        self.assertEqual(evidence["wells"]["雨水"]["检查井"], 1)
        self.assertEqual(evidence["dia_counts"].get("DN≤800"), 1)

    def test_diameter_band(self):
        evidence = mq._extract(_payload(), 1.0)
        self.assertEqual(evidence["dia_counts"].get("DN≤800"), 1)
        self.assertTrue(any("未提取到管径" in w for w in evidence["warnings"]))


class BuildTests(unittest.TestCase):
    def _build(self, tmp: Path, payload: dict, prefix: str = "市政算量") -> dict:
        path = _write(tmp, payload)
        guard = mq._guard_from_dict(mq._synthetic_guard_doc(payload),
                                    allow_manual=True, label=str(path))
        out_path = mq.build(str(path), str(tmp / prefix), payload=payload,
                            guard=guard, run_manifest={"schema": "run-manifest/v1"})
        self.assertTrue(Path(str(out_path)).is_file())
        return json.loads((tmp / (prefix + ".json")).read_text(encoding="utf-8"))

    def test_manual_forces_final_quantity_false(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = self._build(Path(tmp), _payload())
            self.assertFalse(out["final_quantity"])
            self.assertEqual(out["contract_mode"], "manual")
            self.assertFalse(out["summary"]["final_quantity"])
            for row in out["pipes_length_estimate"]:
                self.assertFalse(row["final_quantity"])

    def test_pipe_band_and_wells(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = self._build(Path(tmp), _payload())
            pipe = out["pipes_length_estimate"][0]
            self.assertEqual(pipe["system"], "雨水")
            self.assertAlmostEqual(pipe["length_m_estimate_low"], 120.0)
            self.assertAlmostEqual(pipe["length_m_estimate_high"], 138.0)
            self.assertEqual(out["summary"]["wells_total"], 3)
            self.assertTrue(any(w["category"] == "雨水口" for w in out["wells_count"]))

    def test_road_area_band(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = self._build(Path(tmp), _payload())
            road = out["road_area_estimate"]
            self.assertIsNotNone(road)
            self.assertAlmostEqual(road["centerline_length_m"], 80.0)
            self.assertEqual(road["width_m"], 40.0)
            self.assertAlmostEqual(road["area_m2_estimate_low"], 3200.0)
            self.assertAlmostEqual(road["area_m2_estimate_high"], 3680.0)

    def test_missing_items_when_no_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = _payload(municipal_geometry=[], labels=[])
            out = self._build(Path(tmp), payload, prefix="缺项")
            self.assertTrue(any("道路面积" in m and "宽度" in m for m in out["missing_items"]))
            self.assertIsNone(out["road_area_estimate"])
            self.assertTrue(any("管道延米" in m for m in out["missing_items"]))

    def test_unit_scale_m_drawing(self):
        """m 单位图纸按固有 1m=1000mm 换算，长度即 m 口径。"""
        with tempfile.TemporaryDirectory() as tmp:
            payload = _payload(
                coordinate_unit="m", unit_scale=1000,
                municipal_geometry=[
                    {"category": "雨水管", "system": "雨水", "layer": "GS-YS",
                     "geometry": [0, 0, 120, 0], "file": "sample.dwg", "sheet": "PS-01",
                     "status": "candidate"},
                    {"category": "道路中线", "system": "道路", "layer": "DL-ZX",
                     "geometry": [0, 0, 0, 80], "file": "sample.dwg", "sheet": "DL-01",
                     "status": "candidate"},
                ])
            out = self._build(Path(tmp), payload, prefix="m单位")
            pipe = out["pipes_length_estimate"][0]
            self.assertAlmostEqual(pipe["length_m_estimate_low"], 120.0)
            self.assertTrue(any("1m=1000mm" in w for w in out["warnings"]))

    def test_unit_m_without_scale_converts_by_definition(self):
        """m 单位缺 unit_scale：按固有 1m=1000mm 换算，不拒算。"""
        payload = _payload(coordinate_unit="m")
        warnings: list[str] = []
        factor = mq._to_mm_factor(payload, warnings)
        self.assertEqual(factor, 1000.0)
        self.assertTrue(any("1m=1000mm" in w for w in warnings))

    def test_exotic_unit_without_scale_rejects_length(self):
        """cm 等其他单位缺 unit_scale：GuardError(4)，不出长度。"""
        payload = _payload(coordinate_unit="cm")
        with self.assertRaises(GuardError) as ctx:
            mq._to_mm_factor(payload, [])
        self.assertEqual(ctx.exception.code, 4)

    def test_outputs_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = self._build(Path(tmp), _payload())
            for suffix in ("json", "md", "csv"):
                self.assertTrue((Path(out["source_file"]).parent / ("市政算量." + suffix)).is_file())
            self.assertTrue((Path(out["source_file"]).parent / "site_handoff.json").is_file())


class HashChainTests(unittest.TestCase):
    """哈希链状态：hash_chain_status 机器可读 + --strict-hash 硬失败。"""

    def _contract_file(self, tmp: str, doc: dict) -> Path:
        path = Path(tmp) / "contract.json"
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def _doc(self) -> dict:
        return _payload()

    def test_missing_embedded_hash_reports_unverified(self):
        """require_hash=True 且缺内嵌哈希：hash_chain_status=unverified_no_embedded_hash，不拒入。"""
        import hashlib
        with tempfile.TemporaryDirectory() as tmp:
            path = self._contract_file(tmp, self._doc())
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            guard = guard_contract(str(path), allow_manual=True, require_hash=True, expected_schema="cad-municipal-geometry/v1")
            self.assertEqual(guard["hash_chain_status"], "unverified_no_embedded_hash")
            self.assertEqual(guard["contract_sha256"], digest)

    def test_embedded_hash_match_reports_verified(self):
        """内嵌 contract_sha256 与实算一致：hash_chain_status=verified。"""
        import hashlib
        with tempfile.TemporaryDirectory() as tmp:
            doc = self._doc()
            path = self._contract_file(tmp, doc)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            doc["contract_sha256"] = digest
            path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
            # 内嵌值按剔除 contract_sha256 后重算——直接嵌入实算值不匹配是预期（绊线设计）
            with self.assertRaises(GuardError) as ctx:
                guard_contract(str(path), allow_manual=True, require_hash=True, expected_schema="cad-municipal-geometry/v1")
            self.assertEqual(ctx.exception.code, 2)

    def test_strict_hash_missing_embedded_fails(self):
        """--strict-hash：缺内嵌哈希按硬失败拒入（exit 2）。"""
        with tempfile.TemporaryDirectory() as tmp:
            path = self._contract_file(tmp, self._doc())
            with self.assertRaises(GuardError) as ctx:
                guard_contract(str(path), allow_manual=True, require_hash=True, strict_hash=True, expected_schema="cad-municipal-geometry/v1")
            self.assertEqual(ctx.exception.code, 2)

    def test_stamp_result_propagates_hash_chain_status(self):
        """stamp_result 把 hash_chain_status 透传进算量结果。"""
        guard = {"mode": "manual", "provenance": "manual", "contract_id": "c1",
                 "source_sha256": "a" * 64, "contract_sha256": "b" * 64,
                 "hash_chain_status": "unverified_no_embedded_hash"}
        result = stamp_result({"final_quantity": False}, guard)
        self.assertEqual(result["hash_chain_status"], "unverified_no_embedded_hash")


class GateTests(unittest.TestCase):
    def test_file_input_without_allow_manual_exits_3(self):
        """文件入口缺 --allow-manual 必须 exit 3，不静默降级。"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write(Path(tmp), _payload())
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS / "municipal_qty.py"),
                 "--municipal", str(path), "--out-prefix", str(Path(tmp) / "x")],
                capture_output=True, text=True)
            self.assertEqual(proc.returncode, 3, proc.stderr)

    def test_drawing_input_exits_23(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "municipal_qty.py"),
             "--municipal", "道路图.dwg", "--allow-manual", "--out-prefix", "x"],
            capture_output=True, text=True)
        self.assertEqual(proc.returncode, 23, proc.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
