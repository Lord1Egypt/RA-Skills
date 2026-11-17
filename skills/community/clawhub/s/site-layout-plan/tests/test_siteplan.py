#!/usr/bin/env python3
"""site-layout-plan 0.7.0 · 分阶段平面布置模型/校核/出图回归。"""
from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
CLI = ROOT / "scripts" / "build_site_plan.py"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.bootstrap import ensure_runtime  # noqa: E402

ensure_runtime(__file__)

import ezdxf  # noqa: E402

from site_layout.siteplan import (  # noqa: E402
    SitePlanError, UnitError, build_stage_model, load_base_map,
    load_cranes, load_facilities,
)


def fixture(name: str) -> Path:
    return FIXTURES / name


class StageModelTest(unittest.TestCase):
    def setUp(self) -> None:
        self.base_map, _ = load_base_map(fixture("base_map_demo.json"))
        self.facilities, self.fac_source, _ = load_facilities(fixture("facilities_demo.json"))
        self.cranes, _ = load_cranes([str(fixture("reader_crane.json"))])

    def model(self, stage: str, **kwargs):
        return build_stage_model(self.base_map, self.facilities, self.cranes, stage, **kwargs)

    def test_structure_has_no_fail(self) -> None:
        model = self.model("structure")
        self.assertEqual(len(model["checks"]), 26)
        self.assertEqual(model["summary"]["fail"], 0, msg=[
            (c["id"], c["name"], c["message"]) for c in model["checks"] if c["status"] == "fail"
        ])
        self.assertEqual(model["counts"]["all"], 27)
        self.assertFalse(model["final_check"])
        print("  [1/6] 主体阶段 26 条校核，fail=0，设施 27 项")

    def test_stage_filtering(self) -> None:
        earthwork = self.model("earthwork")
        ids = {row["id"] for row in earthwork["facilities"]}
        self.assertIn("F-WASH-01", ids)
        self.assertNotIn("F-LIFT-01", ids)
        finish = self.model("finish")
        finish_ids = {row["id"] for row in finish["facilities"]}
        self.assertIn("F-LIFT-01", finish_ids)
        self.assertIn("F-WASH-01", finish_ids)
        structure = self.model("structure")
        self.assertIn("F-LIFT-01", {r["id"] for r in structure["facilities"]})
        print("  [2/6] 阶段过滤：洗车池全过程保留、施工电梯仅主体/装饰")

    def test_missing_unit_rejected(self) -> None:
        raw = json.loads(fixture("facilities_demo.json").read_text(encoding="utf-8"))
        raw.pop("coord_unit")
        path = Path(self.id().replace(".", "_") + ".json")
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        target = Path(tmp.name) / "no_unit.json"
        target.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(UnitError) as ctx:
            load_facilities(target)
        self.assertEqual(ctx.exception.exit_code, 4)
        print("  [3/6] 设施文件无单位：exit 4，不猜倍数")

    def test_dorm_inside_crane_radius_fails(self) -> None:
        crane = json.loads(fixture("reader_crane.json").read_text(encoding="utf-8"))
        crane["crane_layout"][0]["center_xy_m"] = [10.0, 8.0]
        crane["crane_layout"][0]["jib_length_m"] = 60.0
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "crane_near_dorm.json"
        path.write_text(json.dumps(crane, ensure_ascii=False), encoding="utf-8")
        cranes, _ = load_cranes([str(path)])
        model = build_stage_model(self.base_map, self.facilities, cranes, "structure")
        check = next(c for c in model["checks"] if c["id"] == 6)
        self.assertEqual(check["status"], "fail")
        self.assertTrue(any(item["category"] == "temporary_dormitory"
                            for item in check["evidence"]["risky"]))
        print("  [4/6] 宿舍落入塔吊回转半径：check 6 fail")

    def test_reader_default_unit_rejected(self) -> None:
        crane = json.loads(fixture("reader_crane.json").read_text(encoding="utf-8"))
        crane["units"]["basis"] = "default"
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "crane_default_unit.json"
        path.write_text(json.dumps(crane, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(UnitError):
            load_cranes([str(path)])
        print("  [5/6] reader units.basis=default：拒绝把默认 mm 当已确认单位")


class StageDrawCliTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="siteplan_test_")
        self.out = Path(self.tmp.name) / "out"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_cli(self, *extra: str, facilities: Path | None = None,
                base_map: Path | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(CLI),
             "--base-map", str(base_map or fixture("base_map_demo.json")),
             "--facilities", str(facilities or fixture("facilities_demo.json")),
             "--cranes", str(fixture("reader_crane.json")),
             "--stages", "all",
             "--out-dir", str(self.out), *extra],
            cwd=str(ROOT), capture_output=True, text=True,
        )

    def test_cli_all_stages_and_outputs(self) -> None:
        proc = self.run_cli()
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
        for stage in ("earthwork", "structure", "finish"):
            dxf = self.out / "layout-{}.dxf".format(stage)
            png = self.out / "layout-{}.png".format(stage)
            self.assertTrue(dxf.is_file())
            self.assertGreater(png.stat().st_size, 10 * 1024)
            doc = ezdxf.readfile(str(dxf))
            self.assertEqual(int(doc.header["$INSUNITS"]), 4)
            # 0.6.6：EXTMIN/EXTMAX 必须有效，否则看图软件黑屏
            ext_min = tuple(float(v) for v in doc.header["$EXTMIN"])
            ext_max = tuple(float(v) for v in doc.header["$EXTMAX"])
            self.assertTrue(all(abs(v) < 1e12 for v in ext_min + ext_max),
                            "{} 的 EXTMIN/EXTMAX 仍是哨兵值".format(stage))
            self.assertLess(ext_min[0], ext_max[0])
            names = {layer.dxf.name for layer in doc.layers}
            for required in ("BASE-底图", "BOUNDARY-红线", "CRANE-塔吊", "FAC-临时道路",
                             "DIM-尺寸", "COORD-坐标", "META-图签", "LEG-图例"):
                self.assertIn(required, names)
            blocks = {block.name for block in doc.blocks}
            self.assertIn("SLP_HYDRANT", blocks)
            self.assertTrue(any(name.startswith("SLP_") for name in blocks))
            title = json.loads((self.out / "titleblock-{}.json".format(stage)).read_text(encoding="utf-8"))
            self.assertEqual(title["version"], "0.7.2")
            self.assertIn("DRAFT", title["draft"])
            selfcheck = json.loads((self.out / "selfcheck-{}.json".format(stage)).read_text(encoding="utf-8"))
            self.assertEqual(len(selfcheck["items"]), 12)
            self.assertEqual(selfcheck["summary"]["fail"], 0)
            self.assertEqual(selfcheck["items"][7]["status"], "pass")
            self.assertEqual(selfcheck["items"][8]["status"], "pass")
            self.assertEqual(selfcheck["items"][10]["status"], "pass")
            self.assertEqual(selfcheck["items"][10]["evidence"]["unplaced_count"], 0)
            self.assertEqual(selfcheck["items"][10]["evidence"]["overlaps"], 0)
            dimensions = list(doc.modelspace().query("DIMENSION"))
            annotations = title["annotations"]
            self.assertEqual(annotations["dxf_label_overlaps"], [])
            self.assertGreater(len(dimensions), 0)
            self.assertEqual(len(dimensions), annotations["dimension_count"])
            self.assertEqual(len(dimensions), annotations["dimension_rendered"])
            coord_csv = self.out / "coordinates-{}.csv".format(stage)
            self.assertTrue(coord_csv.is_file())
            with coord_csv.open(encoding="utf-8-sig", newline="") as handle:
                csv_rows = len(list(csv.DictReader(handle)))
            self.assertEqual(csv_rows, annotations["coordinate_csv_rows"])
            self.assertEqual(csv_rows, annotations["coordinate_rows"])
            self.assertEqual(csv_rows, annotations["coordinate_model_rows"])
            if stage == "structure":
                self.assertEqual(set(annotations["dimension_kinds"]), {
                    "facility_clearance", "road_width", "fire_lane_width",
                    "crane_radius", "elevator_offset",
                })
            road = json.loads((self.out / "road-check-{}.json".format(stage)).read_text(encoding="utf-8"))
            self.assertEqual(len(road["checks"]), 4)
            self.assertEqual({c["id"] for c in road["checks"]}, {"R1", "R2", "R3", "R4"})
            panel = json.loads((self.out / "review-panel-{}.json".format(stage)).read_text(encoding="utf-8"))
            self.assertEqual(len(panel["roles"]), 6)
            self.assertFalse(panel["final_check"])
            self.assertIn("gates", panel)
            stage_json = json.loads((self.out / "stage-{}.json".format(stage)).read_text(encoding="utf-8"))
            self.assertIn("road_summary", stage_json)
            self.assertIn("review_summary", stage_json)
        manifest = json.loads((self.out / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["stages"]), 3)
        changes = json.loads((self.out / "stage-changes.json").read_text(encoding="utf-8"))
        self.assertEqual(changes["transitions"][0]["from"], "earthwork")
        self.assertIn("F-LIFT-01", changes["transitions"][0]["added"])
        self.assertNotIn("F-WASH-01", changes["transitions"][0]["removed"])
        print("  [6/6] 三阶段 DXF/PNG/自检 + 阶段变化表")

    def test_missing_structure_outline_marks_elevator_manual(self) -> None:
        base = json.loads(fixture("base_map_demo.json").read_text(encoding="utf-8"))
        base.pop("structure_outline", None)
        path = Path(self.tmp.name) / "base_no_structure.json"
        path.write_text(json.dumps(base, ensure_ascii=False), encoding="utf-8")
        proc = self.run_cli(base_map=path)
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
        title = json.loads((self.out / "titleblock-structure.json").read_text(encoding="utf-8"))
        annotations = title["annotations"]
        self.assertIn("elevator_offset", annotations["blocked"])
        self.assertNotIn("elevator_offset", annotations["dimension_kinds"])
        self.assertTrue(annotations["skipped"])
        selfcheck = json.loads((self.out / "selfcheck-structure.json").read_text(encoding="utf-8"))
        item = selfcheck["items"][7]
        self.assertEqual(item["status"], "manual")
        self.assertIn("施工电梯距结构边", item["message"])
        print("  [附] 缺结构轮廓：电梯距结构边降级 manual，未静默省略")

    def test_source_gate_contract_fallback(self) -> None:
        base = json.loads(fixture("base_map_demo.json").read_text(encoding="utf-8"))
        base.pop("drawing_sha256", None)
        base["reader_contract_id"] = "CONTRACT-SYNTH-001"
        facilities = json.loads(fixture("facilities_demo.json").read_text(encoding="utf-8"))
        facilities["contract"].pop("source_sha256", None)
        facilities["contract"]["contract_id"] = "CONTRACT-SYNTH-001"
        crane = json.loads(fixture("reader_crane.json").read_text(encoding="utf-8"))
        crane["contract"].pop("source_sha256", None)
        crane["contract"]["contract_id"] = "CONTRACT-SYNTH-001"
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        base_path = Path(tmp.name) / "base_no_sha.json"
        fac_path = Path(tmp.name) / "fac_no_sha.json"
        crane_path = Path(tmp.name) / "crane_no_sha.json"
        for path, data in ((base_path, base), (fac_path, facilities), (crane_path, crane)):
            path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(CLI), "--base-map", str(base_path),
             "--facilities", str(fac_path), "--cranes", str(crane_path),
             "--stages", "structure", "--out-dir", str(self.out)],
            cwd=str(ROOT), capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
        manifest = json.loads((self.out / "manifest.json").read_text(encoding="utf-8"))
        self.assertTrue(manifest["source"]["same_source"])
        self.assertEqual(manifest["source"]["same_source_basis"], "contract_id")
        print("  [附] 源图哈希缺失时同源闸门退回契约号，不默认放行")

    def test_source_gate_unverified(self) -> None:
        base = json.loads(fixture("base_map_demo.json").read_text(encoding="utf-8"))
        for key in ("drawing_sha256", "reader_contract_id", "contract_id"):
            base.pop(key, None)
        facilities = json.loads(fixture("facilities_demo.json").read_text(encoding="utf-8"))
        facilities["contract"].pop("source_sha256", None)
        facilities["contract"].pop("contract_id", None)
        crane = json.loads(fixture("reader_crane.json").read_text(encoding="utf-8"))
        crane["contract"].pop("source_sha256", None)
        crane["contract"].pop("contract_id", None)
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        base_path = Path(tmp.name) / "base_no_id.json"
        fac_path = Path(tmp.name) / "fac_no_id.json"
        crane_path = Path(tmp.name) / "crane_no_id.json"
        for path, data in ((base_path, base), (fac_path, facilities), (crane_path, crane)):
            path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(CLI), "--base-map", str(base_path),
             "--facilities", str(fac_path), "--cranes", str(crane_path),
             "--stages", "structure", "--out-dir", str(self.out)],
            cwd=str(ROOT), capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
        manifest = json.loads((self.out / "manifest.json").read_text(encoding="utf-8"))
        self.assertIsNone(manifest["source"]["same_source"])
        self.assertEqual(manifest["source"]["same_source_basis"], "unverified")
        stage = json.loads((self.out / "stage-structure.json").read_text(encoding="utf-8"))
        self.assertTrue(any("同源身份无法核实" in w for w in stage["warnings"]))
        print("  [附] 哈希与契约号都缺：标 unverified + 警告，不冒充 same_source")

    def test_source_mismatch_gate(self) -> None:
        base = json.loads(fixture("base_map_demo.json").read_text(encoding="utf-8"))
        base["drawing_sha256"] = "2" * 64
        bad = Path(self.tmp.name) / "base_mismatch.json"
        bad.write_text(json.dumps(base, ensure_ascii=False), encoding="utf-8")
        rejected = self.run_cli(base_map=bad)
        self.assertEqual(rejected.returncode, 5, msg=rejected.stdout + rejected.stderr)
        self.assertIn("不同源", rejected.stderr)
        allowed = self.run_cli("--allow-source-mismatch", base_map=bad)
        self.assertEqual(allowed.returncode, 0, msg=allowed.stdout + allowed.stderr)
        manifest = json.loads((self.out / "manifest.json").read_text(encoding="utf-8"))
        self.assertFalse(manifest["source"]["same_source"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
