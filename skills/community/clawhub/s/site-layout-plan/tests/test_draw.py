#!/usr/bin/env python3
"""site-layout-plan 0.7.2 · 出图/图签/自检与识图闸门回归测试。

系统 python3 缺 ezdxf/Pillow 时，bootstrap 会自动切到 Codex 本地 Python 3.12。
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
DRAW_CLI = ROOT / "scripts" / "draw_layout.py"
CHECK_CLI = ROOT / "scripts" / "crane_check.py"


SITE_SAMPLE = FIXTURES / "reader_site_mm.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.bootstrap import ensure_runtime  # noqa: E402

ensure_runtime(__file__)

import ezdxf  # noqa: E402

REQUIRED_LAYERS = [
    "BASE-底图",
    "CRANE-塔吊",
    "CRANE-覆盖",
    "LIFT-合格",
    "LIFT-超载",
    "LIFT-盲区",
    "TEXT-结论",
    "META-图签",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_check(out_dir: Path) -> Path:
    proc = subprocess.run(
        [
            sys.executable,
            str(CHECK_CLI),
            "--handoff",
            str(FIXTURES / "handoff_p4.json"),
            "--fleet",
            str(FIXTURES / "fleet_p4.json"),
            "--baseline",
            str(FIXTURES / "baseline.json"),
            "--out-dir",
            str(out_dir),
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise AssertionError(f"crane_check 失败：{proc.stdout}\n{proc.stderr}")
    return out_dir / "crane_check.json"


def run_draw(
    out_dir: Path,
    *,
    check: Path,
    baseline: str = "baseline.json",
    layout: Path | None = None,
    draft: bool = True,
) -> subprocess.CompletedProcess:
    command = [
        sys.executable,
        str(DRAW_CLI),
        "--site",
        str(SITE_SAMPLE),
        "--handoff",
        str(FIXTURES / "handoff_p4.json"),
        "--check",
        str(check),
        "--baseline",
        str(FIXTURES / baseline),
        "--out-dir",
        str(out_dir),
    ]
    command.extend(["--layout", str(layout if layout is not None else FIXTURES / "site_sample.layout.json")])
    if draft:
        command.append("--draft")
    return subprocess.run(command, cwd=str(ROOT), capture_output=True, text=True)


class DrawLayoutTest(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="site_draw_test_")
        self.base = Path(self.tmp.name)
        self.check = run_check(self.base / "check")
        self.source = SITE_SAMPLE
        self.source_sha = sha256(self.source)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_01_draw_success_and_layers(self) -> None:
        out = self.base / "out"
        proc = run_draw(out, check=self.check, draft=True)
        self.assertEqual(proc.returncode, 0, msg=f"stdout={proc.stdout}\nstderr={proc.stderr}")
        self.assertTrue((out / "layout.dxf").is_file())
        self.assertTrue((out / "layout.png").is_file())
        self.assertTrue((out / "layers.csv").is_file())
        self.assertTrue((out / "titleblock.json").is_file())
        self.assertTrue((out / "selfcheck.json").is_file())

        doc = ezdxf.readfile(str(out / "layout.dxf"))
        self.assertEqual(int(doc.header["$INSUNITS"]), 4)
        # 0.6.6：EXTMIN/EXTMAX 必须是有限值，否则看图软件按空图纸打开
        ext_min = tuple(float(v) for v in doc.header["$EXTMIN"])
        ext_max = tuple(float(v) for v in doc.header["$EXTMAX"])
        self.assertTrue(all(abs(v) < 1e12 for v in ext_min + ext_max),
                        f"EXTMIN/EXTMAX 仍是哨兵值: {ext_min} {ext_max}")
        self.assertLess(ext_min[0], ext_max[0])
        self.assertLess(ext_min[1], ext_max[1])
        names = {layer.dxf.name for layer in doc.layers}
        for name in REQUIRED_LAYERS:
            self.assertIn(name, names)
        msp = doc.modelspace()
        overload = list(msp.query('*[layer=="LIFT-超载"]'))
        self.assertGreaterEqual(len(overload), 1, "LIFT-超载 必须有实体")
        print("  [1/5] 出图成功：8 图层齐全，LIFT-超载 实体数={}".format(len(overload)))

    def test_02_png_size_and_selfcheck(self) -> None:
        out = self.base / "out_png"
        proc = run_draw(out, check=self.check, draft=True)
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        png = out / "layout.png"
        self.assertGreater(png.stat().st_size, 10 * 1024, "PNG 必须 >10 KB")
        selfcheck = json.loads((out / "selfcheck.json").read_text(encoding="utf-8"))
        self.assertEqual(len(selfcheck["items"]), 8)
        self.assertEqual(selfcheck["summary"]["fail"], 0)
        self.assertEqual(selfcheck["exit_code"], 0)
        statuses = {item["id"]: item["status"] for item in selfcheck["items"]}
        self.assertEqual(statuses[1], "pass")
        self.assertEqual(statuses[5], "pass")
        self.assertEqual(statuses[7], "pass")
        self.assertEqual(statuses[8], "pass")
        print(
            "  [2/5] PNG {} B；自检 pass={} manual={} fail={}".format(
                png.stat().st_size,
                selfcheck["summary"]["pass"],
                selfcheck["summary"]["manual"],
                selfcheck["summary"]["fail"],
            )
        )

    def test_03_source_hash_unchanged(self) -> None:
        out = self.base / "out_hash"
        proc = run_draw(out, check=self.check, draft=True)
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertEqual(sha256(self.source), self.source_sha, "reader 契约字节被改动")
        title = json.loads((out / "titleblock.json").read_text(encoding="utf-8"))
        self.assertEqual(title["source_sha256_before"], self.source_sha)
        self.assertEqual(title["source_sha256_after"], self.source_sha)
        self.assertTrue(title["source_unchanged"])
        self.assertEqual(title["draft_label"], "DRAFT")
        self.assertFalse(title["final_check"])
        print("  [3/5] reader 契约 SHA 前后一致：{}".format(self.source_sha[:16] + "…"))

    def test_04_contract_missing_draft(self) -> None:
        layout = self.base / "site_sample.layout.json"
        payload = json.loads((FIXTURES / "site_sample.layout.json").read_text(encoding="utf-8"))
        payload.pop("contract_id", None)
        payload["contract_id"] = ""
        layout.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        out = self.base / "out_missing_contract"
        proc = run_draw(out, check=self.check, layout=layout, draft=True)
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        title = json.loads((out / "titleblock.json").read_text(encoding="utf-8"))
        self.assertTrue(title["contract_mismatch"])
        self.assertEqual(title["draft_label"], "DRAFT-CONTRACT-MISMATCH")

        rejected = run_draw(self.base / "out_nodraft", check=self.check, layout=layout, draft=False)
        self.assertEqual(rejected.returncode, 5, msg=rejected.stderr)
        self.assertIn("contract_id", rejected.stderr)
        print("  [4/7] 契约缺失：--draft 出 DRAFT-CONTRACT-MISMATCH；无 --draft exit 5")

    def test_06_reader_crane_json_accepted(self) -> None:
        from site_layout.draw import load_layout

        site = SITE_SAMPLE
        cranes, path, contract_id = load_layout(str(FIXTURES / "reader_crane.json"), site, {})
        self.assertEqual(len(cranes), 1)
        crane = cranes[0]
        self.assertEqual(crane.id, "TC-01")
        self.assertAlmostEqual(crane.jib_mm, 35000.0)
        self.assertAlmostEqual(crane.x_mm, 50000.0)
        self.assertAlmostEqual(crane.y_mm, 30000.0)
        self.assertEqual(contract_id, "CONTRACT-SYNTH-CRANE-001")
        print("  [6/7] reader *.crane.json 直接出图：jib_length_m/center_xy_m 解析正确")

    def test_07_unit_fallback_to_audit(self) -> None:
        from site_layout.draw import load_site

        site = load_site(str(FIXTURES / "reader_site_mm.json"))
        self.assertEqual(site.source_units, "mm")
        self.assertEqual(site.mm_per_unit, 1.0)
        self.assertEqual(len(site.redline_vertices), 4)
        self.assertTrue(site.redline_closed)
        print("  [7/7] 顶层无 coord_unit 时回退 scale_unit_audit[].units=mm")

    def test_08_draw_rejects_direct_cad(self) -> None:
        """出图也不得直读 CAD/PDF，必须走 bus -> reader。"""
        out = self.base / "out_direct_cad"
        direct_cad = self.base / "direct.dxf"
        direct_cad.write_text("0\nSECTION\n2\nHEADER\n0\nENDSEC\n0\nEOF\n", encoding="ascii")
        proc = subprocess.run(
            [
                sys.executable,
                str(DRAW_CLI),
                "--site",
                str(direct_cad),
                "--handoff",
                str(FIXTURES / "handoff_p4.json"),
                "--check",
                str(self.check),
                "--baseline",
                str(FIXTURES / "baseline.json"),
                "--out-dir",
                str(out),
                "--draft",
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 2, msg=f"stdout={proc.stdout}\nstderr={proc.stderr}")
        self.assertIn("cad-file-reader", proc.stderr)
        self.assertIn("lis-skill-bus", proc.stderr)
        self.assertFalse((out / "layout.dxf").exists(), "直读 CAD 不得生成图")
        print("  [8/8] draw_layout 直读 DXF：exit 2，提示必须走 bus -> reader")

    def test_05_baseline_unlocked_exit5(self) -> None:
        out = self.base / "out_unlocked"
        proc = run_draw(out, check=self.check, baseline="baseline_unlocked.json", draft=True)
        self.assertEqual(proc.returncode, 5, msg=proc.stderr)
        self.assertIn("locked_by", proc.stderr)
        self.assertFalse((out / "layout.dxf").exists(), "口径未锁不得生成图")
        print("  [5/5] baseline 未锁：exit 5，未生成 layout.dxf")


if __name__ == "__main__":
    unittest.main(verbosity=2)
