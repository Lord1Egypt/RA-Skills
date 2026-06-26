from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd
from psd_tools import PSDImage


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "psd_batch.py"
sys.path.insert(0, str(ROOT / "scripts"))

from render_psd_batch import get_text_style, psd_color_values_to_rgb


def run_cli(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    result = subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        env=env,
        timeout=120,
    )
    if check and result.returncode != 0:
        raise AssertionError(
            f"command failed: {args}\nreturncode={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}"
        )
    return result


def write_sample_xlsx(path: Path, rows: int = 2) -> None:
    df = pd.DataFrame(
        {
            "图层14": ["好", "新"][:rows],
            "图层19": ["早", "行"][:rows],
            "图层11": ["早", "晨"][:rows],
            "图层12": ["安", "好"][:rows],
        }
    )
    df.to_excel(path, index=False)


def test_psd_color_values_skip_space_marker() -> None:
    assert psd_color_values_to_rgb([1.0, 0.0, 0.0, 0.0]) == (0, 0, 0)
    assert psd_color_values_to_rgb([1.0, 0.46275, 0.25882, 0.20392]) == (118, 66, 52)
    assert psd_color_values_to_rgb([1.0, 1.0, 1.0, 1.0]) == (255, 255, 255)
    assert psd_color_values_to_rgb([12, 34, 56]) == (12, 34, 56)
    assert psd_color_values_to_rgb([255, 0, 0, 128]) == (255, 0, 0)


def test_template_text_color_reads_original_layer_rgb() -> None:
    psd = PSDImage.open(str(ROOT / "templates" / "morning_greeting" / "早安手绘风日签__2026-05-31+17_54_52.psd"))
    layer = next(layer for layer in psd.descendants() if layer.kind == "type" and layer.name == "图层14")
    assert get_text_style(layer)["fill_color"] == (0, 0, 0)


def test_cli_help_smoke() -> None:
    commands = [
        ("diagnose", "--help"),
        ("analyze", "--help"),
        ("preview", "--help"),
        ("export", "--help"),
        ("verify", "--help"),
        ("templates", "--help"),
        ("templates", "list", "--help"),
        ("templates", "info", "--help"),
    ]
    for args in commands:
        result = run_cli(*args)
        assert "usage:" in result.stdout


def test_diagnose_json() -> None:
    result = run_cli("diagnose", "--json")
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["dependencies"]["required"]["psd_tools"] is True
    assert payload["templates"]
    assert "fonts" in payload


def test_templates_info_json() -> None:
    result = run_cli("templates", "info", "morning", "--json")
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["templates"]["name"] == "早安手绘风日签"
    assert Path(payload["templates"]["resolved_psd"]).exists()


def test_analyze_json_with_sample_data(tmp_path: Path) -> None:
    data = tmp_path / "data.xlsx"
    write_sample_xlsx(data)
    report_path = tmp_path / "report.json"

    result = run_cli("analyze", "morning", "--data", str(data), "--json", "--json-out", str(report_path))
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["layers"]
    assert payload["mapping"]
    assert report_path.exists()


def test_preview_generates_png(tmp_path: Path) -> None:
    data = tmp_path / "data.xlsx"
    out = tmp_path / "out"
    write_sample_xlsx(data, rows=1)

    result = run_cli("preview", "morning", "--data", str(data), "--out", str(out), "--rows", "1", "--json")
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    previews = payload["outputs"]["preview_png"]
    assert payload["outputs"]["text_color"] == "psd-layer"
    assert len(previews) == 1
    assert Path(previews[0]).exists()
    assert Path(previews[0]).stat().st_size > 0


def test_export_generates_report(tmp_path: Path) -> None:
    data = tmp_path / "data.xlsx"
    out = tmp_path / "out"
    write_sample_xlsx(data, rows=1)

    result = run_cli(
        "export",
        "morning",
        "--data",
        str(data),
        "--out",
        str(out),
        "--verify-samples",
        "0",
        "--json",
    )
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["outputs"]["generated_psd"] == 1
    assert payload["outputs"]["generated_png"] == 1
    assert payload["outputs"]["text_color"] == "psd-layer"
    assert Path(payload["outputs"]["verify_report"]).exists()
