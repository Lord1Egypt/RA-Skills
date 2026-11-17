#!/usr/bin/env python3
"""0.7.2 · 识图硬链路闸门：只收 lis-skill-bus → cad-file-reader 契约。"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
PREPARE = ROOT / "scripts" / "prepare_site.py"
CRANE = ROOT / "scripts" / "crane_check.py"


def run(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        text=True,
        timeout=60,
    )


class PrepareGateTest(unittest.TestCase):
    def test_direct_dxf_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dxf = Path(tmp) / "plan.dxf"
            dxf.write_text("0\nSECTION\n2\nHEADER\n0\nENDSEC\n0\nEOF\n", encoding="utf-8")
            result = run(PREPARE, "--site", str(dxf), "--out-dir", str(Path(tmp) / "out"))
            self.assertEqual(result.returncode, 2)
            self.assertIn("lis-skill-bus", result.stdout)
            self.assertIn("cad-file-reader", result.stdout)
            self.assertFalse((Path(tmp) / "out" / "base-map.json").exists())

    def test_non_reader_json_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / "manual.json"
            fake.write_text(json.dumps({"coord_unit": "mm", "site_geometry": []}), encoding="utf-8")
            result = run(PREPARE, "--site", str(fake), "--out-dir", str(Path(tmp) / "out"))
            self.assertEqual(result.returncode, 2)
            self.assertIn("cad-contract/v1", result.stdout)

    def test_wrong_contract_version_rejected(self) -> None:
        data = json.loads((FIXTURES / "reader_site_mm.json").read_text(encoding="utf-8"))
        data["contract"]["contract_version"] = "cad-contract/v0"
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / "old-contract.json"
            fake.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            result = run(PREPARE, "--site", str(fake), "--out-dir", str(Path(tmp) / "out"))
            self.assertEqual(result.returncode, 2)
            self.assertIn("cad-contract/v1", result.stdout)

    def test_reader_contract_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run(
                PREPARE,
                "--site", str(FIXTURES / "reader_site_mm.json"),
                "--out-dir", str(Path(tmp) / "out"),
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((Path(tmp) / "out" / "base-map.json").is_file())


class CraneHandoffGateTest(unittest.TestCase):
    def test_direct_dxf_as_handoff_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dxf = Path(tmp) / "crane.dxf"
            dxf.write_text("0\nSECTION\n0\nEOF\n", encoding="utf-8")
            result = run(
                CRANE,
                "--handoff", str(dxf),
                "--fleet", str(FIXTURES / "fleet_p4.json"),
                "--baseline", str(FIXTURES / "baseline.json"),
                "--out-dir", str(Path(tmp) / "out"),
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("lis-skill-bus", result.stderr)

    def test_handoff_without_contract_provenance_rejected(self) -> None:
        data = json.loads((FIXTURES / "handoff_p4.json").read_text(encoding="utf-8"))
        data.pop("contract_id", None)
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / "handoff.json"
            fake.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            result = run(
                CRANE,
                "--handoff", str(fake),
                "--fleet", str(FIXTURES / "fleet_p4.json"),
                "--baseline", str(FIXTURES / "baseline.json"),
                "--out-dir", str(Path(tmp) / "out"),
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("cad-file-reader", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
