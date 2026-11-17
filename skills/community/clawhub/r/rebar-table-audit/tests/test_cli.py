"""端到端 CLI 测试：子进程真实调用 rebar-audit，校验退出码与 stdout/stderr 分离。"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import make_fixtures as fx


def _run_cli(*args):
    cmd = [sys.executable, "-m", "rebar_table_audit.cli", *args]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=60)


def test_clean_table_exit_0_and_json_stdout_clean(tmp_path):
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(msp, rows=fx.clean_table_rows(), totals_lines=fx.clean_table_totals())
    dxf_path = tmp_path / "clean.dxf"
    doc.saveas(dxf_path)
    out_dir = tmp_path / "out"

    proc = _run_cli("run", str(dxf_path), "--out", str(out_dir), "--json")
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)  # 必须能直接解析；日志都在 stderr，不混入 stdout
    assert payload["tables"] == 1
    assert payload["tables_parsed"] == 1
    assert payload["complete"] is True
    assert payload["findings"]["error"] == 0
    assert payload["exit_code"] == 0
    assert (out_dir / "evidence.json").is_file()
    assert (out_dir / "钢筋数量表.xlsx").is_file()
    assert (out_dir / "report.md").is_file()


def test_no_table_exit_3(tmp_path):
    doc = fx.new_doc()
    msp = doc.modelspace()
    msp.add_text("说明：本图仅供参考", dxfattribs={"height": 3.5, "insert": (0, 0)})
    dxf_path = tmp_path / "notable.dxf"
    doc.saveas(dxf_path)
    out_dir = tmp_path / "out"

    proc = _run_cli("run", str(dxf_path), "--out", str(out_dir), "--json")
    assert proc.returncode == 3, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["tables"] == 0
    assert payload["tables_parsed"] == 0
    assert payload["exit_code"] == 3
    # 即使没找到表，也应该照常写出证据文件，方便排查
    assert (out_dir / "evidence.json").is_file()


def test_title_found_but_no_grid_still_exit_3_and_incomplete(tmp_path):
    """标题匹配上了，但下方没有合格网格（比如只是下划线，下面根本没表）——
    "找到标题" 不等于 "还原出数量表"，退出码仍是 3，且 complete=False。"""
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(msp, title_underline=True, draw_grid=False)
    dxf_path = tmp_path / "titleonly.dxf"
    doc.saveas(dxf_path)
    out_dir = tmp_path / "out"

    proc = _run_cli("run", str(dxf_path), "--out", str(out_dir), "--json")
    assert proc.returncode == 3, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["tables"] == 1  # 标题匹配上了，产出了一条表记录
    assert payload["tables_parsed"] == 0  # 但没有还原出任何数据行
    assert payload["complete"] is False
    assert payload["gaps"] >= 1
    assert payload["exit_code"] == 3


def test_error_finding_exit_2(tmp_path):
    rows = fx.clean_table_rows()
    rows[1][-1] = "27.30"  # 制造一个明显偏离的重量，触发 R001 error
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(msp, rows=rows, totals_lines=fx.clean_table_totals())
    dxf_path = tmp_path / "bad.dxf"
    doc.saveas(dxf_path)
    out_dir = tmp_path / "out"

    proc = _run_cli("run", str(dxf_path), "--out", str(out_dir), "--json")
    assert proc.returncode == 2, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["findings"]["error"] >= 1
    assert payload["exit_code"] == 2


def test_evidence_json_stable_across_repeat_runs(tmp_path):
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(msp, rows=fx.clean_table_rows(), totals_lines=fx.clean_table_totals())
    dxf_path = tmp_path / "clean.dxf"
    doc.saveas(dxf_path)

    out1, out2 = tmp_path / "out1", tmp_path / "out2"
    p1 = _run_cli("run", str(dxf_path), "--out", str(out1), "--json")
    p2 = _run_cli("run", str(dxf_path), "--out", str(out2), "--json")
    assert p1.returncode == 0 and p2.returncode == 0

    ev1 = json.loads((out1 / "evidence.json").read_text(encoding="utf-8"))
    ev2 = json.loads((out2 / "evidence.json").read_text(encoding="utf-8"))
    ev1.pop("generated_at")
    ev2.pop("generated_at")
    assert ev1 == ev2


def test_doctor_json():
    proc = _run_cli("doctor", "--json")
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert "python_version" in payload
    assert "ezdxf_version" in payload
    assert "converters" in payload
