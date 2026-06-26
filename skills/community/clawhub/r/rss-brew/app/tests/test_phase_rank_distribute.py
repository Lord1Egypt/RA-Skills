from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[2] / "scripts"
    mod_path = scripts_dir / "phase_rank_distribute.py"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    spec = importlib.util.spec_from_file_location("phase_rank_distribute_script", mod_path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_rank_distribute_outputs_and_guardrails(tmp_path, monkeypatch):
    mod = _load_module()

    inp = tmp_path / "model-scored-articles.json"
    ranked = tmp_path / "ranked-articles.json"
    deep = tmp_path / "deep-set.json"
    other = tmp_path / "other-set.json"
    distribution = tmp_path / "distribution.json"
    scored = tmp_path / "scored-articles.json"

    payload = {
        "generated_at": "2026-03-12T00:00:00Z",
        "model": "CHEAP",
        "article_count": 6,
        "articles": [
            {"title": "A", "url": "u1", "source": "s1", "published": "2026-03-12T10:00:00Z", "rule_score": 2, "model_score": 1.0, "confidence": 0.9, "category": "ai-frontier-tech", "score": 5},
            {"title": "B", "url": "u2", "source": "s1", "published": "2026-03-12T09:00:00Z", "rule_score": 2, "model_score": 0.9, "confidence": 0.9, "category": "ai-frontier-tech", "score": 5},
            {"title": "C", "url": "u3", "source": "s2", "published": "2026-03-12T08:00:00Z", "rule_score": 1, "model_score": 0.8, "confidence": 0.2, "category": "vc-investment", "score": 4},
            {"title": "D", "url": "u4", "source": "s3", "published": "2026-03-12T07:00:00Z", "rule_score": 1, "model_score": 0.7, "confidence": 0.9, "category": "vc-investment", "score": 4},
            {"title": "E", "url": "u5", "source": "s4", "published": "2026-03-12T06:00:00Z", "rule_score": 0, "model_score": 0.6, "confidence": 0.9, "category": "startup-strategy", "score": 3},
            {"title": "F", "url": "u6", "source": "s5", "published": "2026-03-12T05:00:00Z", "rule_score": 0, "model_score": 0.5, "confidence": 0.9, "category": "other", "score": 3},
        ],
    }
    inp.write_text(json.dumps(payload), encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        [
            "phase_rank_distribute.py",
            "--input",
            str(inp),
            "--ranked-output",
            str(ranked),
            "--distribution-output",
            str(distribution),
            "--deep-output",
            str(deep),
            "--other-output",
            str(other),
            "--compat-scored-output",
            str(scored),
            "--deep-target",
            "4",
            "--other-target",
            "3",
            "--min-other",
            "2",
        ],
    )
    mod.main()

    ranked_payload = json.loads(ranked.read_text(encoding="utf-8"))
    deep_payload = json.loads(deep.read_text(encoding="utf-8"))
    other_payload = json.loads(other.read_text(encoding="utf-8"))
    dist_payload = json.loads(distribution.read_text(encoding="utf-8"))
    compat_payload = json.loads(scored.read_text(encoding="utf-8"))

    assert ranked_payload["article_count"] == 6
    assert ranked_payload["articles"][0]["title"] == "A"
    assert "final_score" in ranked_payload["articles"][0]
    assert ranked_payload["articles"][0]["rank"] == 1

    # Low confidence article C should not appear in top-3 deep slots.
    deep_titles = [a["title"] for a in deep_payload["articles"]]
    assert len(deep_titles) == 4
    assert deep_titles[:3] == ["A", "B", "D"]

    assert other_payload["article_count"] >= 1
    assert dist_payload["deep_set_count"] == deep_payload["article_count"]
    assert dist_payload["other_set_count"] == other_payload["article_count"]

    # Compatibility scored output should remain full ranked list.
    assert compat_payload["article_count"] == 6


def test_top3_low_confidence_block_applies_across_fill_pass(tmp_path, monkeypatch):
    mod = _load_module()

    inp = tmp_path / "model-scored-articles.json"
    ranked = tmp_path / "ranked-articles.json"
    deep = tmp_path / "deep-set.json"
    other = tmp_path / "other-set.json"
    distribution = tmp_path / "distribution.json"

    payload = {
        "generated_at": "2026-03-12T00:00:00Z",
        "model": "CHEAP",
        "article_count": 4,
        "articles": [
            {"title": "A", "url": "u1", "source": "s1", "published": "2026-03-12T10:00:00Z", "rule_score": 2, "model_score": 1.0, "confidence": 0.1, "score": 5},
            {"title": "B", "url": "u2", "source": "s2", "published": "2026-03-12T09:00:00Z", "rule_score": 2, "model_score": 0.9, "confidence": 0.9, "score": 5},
            {"title": "C", "url": "u3", "source": "s3", "published": "2026-03-12T08:00:00Z", "rule_score": 1, "model_score": 0.8, "confidence": 0.2, "score": 4},
            {"title": "D", "url": "u4", "source": "s4", "published": "2026-03-12T07:00:00Z", "rule_score": 1, "model_score": 0.7, "confidence": 0.9, "score": 4},
        ],
    }
    inp.write_text(json.dumps(payload), encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        [
            "phase_rank_distribute.py",
            "--input",
            str(inp),
            "--ranked-output",
            str(ranked),
            "--distribution-output",
            str(distribution),
            "--deep-output",
            str(deep),
            "--other-output",
            str(other),
            "--deep-target",
            "3",
            "--other-target",
            "3",
            "--min-other",
            "0",
        ],
    )
    mod.main()

    deep_titles = [a["title"] for a in json.loads(deep.read_text(encoding="utf-8"))["articles"]]
    assert deep_titles == ["B", "D"]


def test_topic_cap_deferred_by_default_and_opt_in(tmp_path, monkeypatch):
    mod = _load_module()

    inp = tmp_path / "model-scored-articles.json"
    ranked = tmp_path / "ranked-articles.json"
    deep = tmp_path / "deep-set.json"
    other = tmp_path / "other-set.json"
    distribution = tmp_path / "distribution.json"

    payload = {
        "generated_at": "2026-03-12T00:00:00Z",
        "model": "CHEAP",
        "article_count": 3,
        "articles": [
            {"title": "A", "url": "u1", "source": "s1", "published": "2026-03-12T10:00:00Z", "rule_score": 2, "model_score": 1.0, "confidence": 0.9, "normalized_topic": "ai", "score": 5},
            {"title": "B", "url": "u2", "source": "s2", "published": "2026-03-12T09:00:00Z", "rule_score": 2, "model_score": 0.9, "confidence": 0.9, "normalized_topic": "ai", "score": 5},
            {"title": "C", "url": "u3", "source": "s3", "published": "2026-03-12T08:00:00Z", "rule_score": 1, "model_score": 0.8, "confidence": 0.9, "normalized_topic": "vc", "score": 4},
        ],
    }
    inp.write_text(json.dumps(payload), encoding="utf-8")

    # Default: deep topic cap is configured but not enforced yet.
    monkeypatch.setattr(
        "sys.argv",
        [
            "phase_rank_distribute.py",
            "--input",
            str(inp),
            "--ranked-output",
            str(ranked),
            "--distribution-output",
            str(distribution),
            "--deep-output",
            str(deep),
            "--other-output",
            str(other),
            "--deep-target",
            "3",
            "--other-target",
            "0",
            "--min-other",
            "0",
            "--deep-topic-cap",
            "1",
        ],
    )
    mod.main()
    deep_titles_default = [a["title"] for a in json.loads(deep.read_text(encoding="utf-8"))["articles"]]
    dist_default = json.loads(distribution.read_text(encoding="utf-8"))
    assert deep_titles_default == ["A", "B", "C"]
    assert dist_default["deep_topic_cap_enforced"] is False

    # Opt-in: enforce deep topic cap using normalized_topic.
    monkeypatch.setattr(
        "sys.argv",
        [
            "phase_rank_distribute.py",
            "--input",
            str(inp),
            "--ranked-output",
            str(ranked),
            "--distribution-output",
            str(distribution),
            "--deep-output",
            str(deep),
            "--other-output",
            str(other),
            "--deep-target",
            "3",
            "--other-target",
            "0",
            "--min-other",
            "0",
            "--deep-topic-cap",
            "1",
            "--enforce-deep-topic-cap",
        ],
    )
    mod.main()
    deep_titles_enforced = [a["title"] for a in json.loads(deep.read_text(encoding="utf-8"))["articles"]]
    assert deep_titles_enforced == ["A", "C"]
