from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def _load_phase_model_module():
    scripts_dir = Path(__file__).resolve().parents[2] / "scripts"
    mod_path = scripts_dir / "phase_model_score.py"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    spec = importlib.util.spec_from_file_location("phase_model_score_script", mod_path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class _FakeResponse:
    def __init__(self, content: str):
        self.choices = [type("Choice", (), {"message": type("Msg", (), {"content": content})()})()]


class _FakeClient:
    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = 0
        self.chat = type("Chat", (), {})()
        self.chat.completions = type("Completions", (), {"create": self._create})()

    def _create(self, **kwargs):
        self.calls += 1
        item = self._responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return _FakeResponse(item)


def test_parse_scoring_preserves_legacy_and_structured_fields():
    mod = _load_phase_model_module()
    out = mod._parse_scoring(
        '{"score": 9, "score_reason": "great", "model_score": 3.2, "confidence": 9, '
        '"plus_tags": ["A"], "minus_tags": ["B"], "evidence": ["e1"]}'
    )
    assert out["score"] == 5
    assert out["score_reason"] == "great"
    assert out["model_score"] == 1.0
    assert out["confidence"] == 1.0
    assert out["plus_tags"] == ["a"]
    assert out["minus_tags"] == ["b"]
    assert out["evidence"] == ["e1"]


def test_parse_scoring_maps_model_score_to_legacy_score_when_missing():
    mod = _load_phase_model_module()
    out = mod._parse_scoring('{"model_score": 1.0, "score_reason": "strong"}')
    assert out["score"] == 5
    assert out["model_score"] == 1.0


def test_build_prompt_prefers_rule_tags_with_legacy_fallback():
    mod = _load_phase_model_module()

    prompt_rule = mod._build_prompt(
        {
            "title": "A",
            "summary": "S",
            "rule_plus_tags": ["domain_relevant"],
            "rule_minus_tags": ["teaser_only"],
            "plus_tags": ["legacy_plus"],
            "minus_tags": ["legacy_minus"],
        }
    )
    assert "plus=['domain_relevant']" in prompt_rule
    assert "minus=['teaser_only']" in prompt_rule

    prompt_legacy = mod._build_prompt({"title": "B", "summary": "S", "plus_tags": ["legacy_plus"], "minus_tags": ["legacy_minus"]})
    assert "plus=['legacy_plus']" in prompt_legacy
    assert "minus=['legacy_minus']" in prompt_legacy


def test_main_keeps_backward_compatibility_schema(tmp_path, monkeypatch):
    mod = _load_phase_model_module()

    input_path = tmp_path / "new-articles.json"
    output_path = tmp_path / "scored-articles.json"
    payload = {
        "generated_at": "2026-03-12T00:00:00Z",
        "article_count": 1,
        "articles": [
            {"title": "A", "summary": "ai startup fund", "source": "s1", "url": "u1", "published": "p1"},
        ],
    }
    input_path.write_text(json.dumps(payload), encoding="utf-8")

    responses = [
        '{"score": 4, "score_reason": "r1", "model_score": 0.6, "confidence": 0.8, '
        '"plus_tags": ["market-data"], "minus_tags": ["limited-scope"], "evidence": ["Revenue up 30%"]}',
    ]

    monkeypatch.setattr(mod, "_load_model_config", lambda: mod.PhaseModelConfig(model="deepseek-reasoner", retries=0, timeout=30))
    monkeypatch.setattr(mod, "_build_client", lambda _cfg: _FakeClient(responses))
    monkeypatch.setattr(
        "sys.argv",
        [
            "phase_model_score.py",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--model",
            "CHEAP",
        ],
    )

    mod.main()

    out = json.loads(output_path.read_text(encoding="utf-8"))
    assert out["generated_at"] == payload["generated_at"]
    assert out["article_count"] == 1
    assert out["model"] == "CHEAP"

    article = out["articles"][0]
    # Legacy fields must remain for backward compatibility.
    assert article["score"] == 4
    assert article["score_reason"] == "r1"

    # Structured V2 fields.
    assert article["model_score"] == 0.6
    assert article["confidence"] == 0.8
    assert article["plus_tags"] == ["market-data"]
    assert article["minus_tags"] == ["limited-scope"]
    assert article["evidence"] == ["Revenue up 30%"]
