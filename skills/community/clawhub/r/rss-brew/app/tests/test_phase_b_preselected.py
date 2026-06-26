from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[2] / "scripts"
    mod_path = scripts_dir / "phase_b_analyze.py"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    spec = importlib.util.spec_from_file_location("phase_b_analyze_script", mod_path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_phase_b_preselected_skips_internal_selection(tmp_path, monkeypatch):
    mod = _load_module()

    inp = tmp_path / "deep-set.json"
    out = tmp_path / "deep-out.json"
    data_root = tmp_path / "data"

    payload = {
        "generated_at": "2026-03-12T00:00:00Z",
        "article_count": 1,
        "articles": [
            {
                "title": "Only deep",
                "url": "u1",
                "source": "s1",
                "published": "2026-03-12T00:00:00Z",
                "score": 5,
                "summary": "AI startup VC article",
            }
        ],
    }
    inp.write_text(json.dumps(payload), encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        [
            "phase_b_analyze.py",
            "--input",
            str(inp),
            "--output",
            str(out),
            "--data-root",
            str(data_root),
            "--preselected",
            "--mock",
        ],
    )
    mod.main()

    out_payload = json.loads(out.read_text(encoding="utf-8"))
    assert out_payload["article_count"] == 1
    assert out_payload["fallback_top3"] is False
