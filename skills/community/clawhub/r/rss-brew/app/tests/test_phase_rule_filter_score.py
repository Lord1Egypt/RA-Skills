from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[2] / "scripts"
    mod_path = scripts_dir / "phase_rule_filter_score.py"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    spec = importlib.util.spec_from_file_location("phase_rule_filter_score_script", mod_path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_rule_filter_adds_fields_and_rejects_teaser(tmp_path, monkeypatch):
    mod = _load_module()

    inp = tmp_path / "new-articles.json"
    out = tmp_path / "rule-filtered-articles.json"

    payload = {
        "generated_at": "2026-03-12T00:00:00Z",
        "article_count": 2,
        "articles": [
            {
                "title": "Deep VC analysis",
                "summary": "A balanced startup market analysis with use cases and data.",
                "text": "This is a long analysis. " * 220,
                "url": "https://example.com/a",
                "source": "src",
                "published": "2026-03-12T00:00:00Z",
            },
            {
                "title": "Sign up now",
                "summary": "Join now",
                "text": "Buy now",
                "url": "https://example.com/b",
                "source": "src",
                "published": "2026-03-12T00:00:00Z",
            },
        ],
    }
    inp.write_text(json.dumps(payload), encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        [
            "phase_rule_filter_score.py",
            "--input",
            str(inp),
            "--output",
            str(out),
            "--floor-count",
            "1",
        ],
    )
    mod.main()

    out_payload = json.loads(out.read_text(encoding="utf-8"))
    assert out_payload["input_article_count"] == 2
    assert out_payload["article_count"] == 1
    assert out_payload["rejected_count"] == 1
    assert out_payload["articles"][0]["rule_reject"] is False
    assert "rule_score" in out_payload["articles"][0]
    assert isinstance(out_payload["articles"][0]["rule_plus_tags"], list)


def test_floor_fallback_does_not_relax_promo_cta_unless_explicit():
    mod = _load_module()

    scored = [
        {"title": "promo", "rule_reject": True, "rule_reject_reason": "promo_cta", "rule_score": 3, "rule_floor_relaxed": False},
        {"title": "teaser", "rule_reject": True, "rule_reject_reason": "teaser_only", "rule_score": 2, "rule_floor_relaxed": False},
    ]

    mod._apply_floor_fallback(scored, floor_count=1)
    promo = next(x for x in scored if x["title"] == "promo")
    teaser = next(x for x in scored if x["title"] == "teaser")
    assert teaser["rule_reject"] is False
    assert promo["rule_reject"] is True

    scored2 = [
        {"title": "promo", "rule_reject": True, "rule_reject_reason": "promo_cta", "rule_score": 3, "rule_floor_relaxed": False},
    ]
    mod._apply_floor_fallback(scored2, floor_count=1, allow_promo_cta=True)
    assert scored2[0]["rule_reject"] is False
