from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def _load_phase_a_module():
    scripts_dir = Path(__file__).resolve().parents[2] / "scripts"
    mod_path = scripts_dir / "phase_a_score.py"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    spec = importlib.util.spec_from_file_location("phase_a_score_script", mod_path)
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


def test_parse_scoring_supports_wrapped_json_and_clamp():
    mod = _load_phase_a_module()
    out = mod._parse_scoring('note\\n{"score": 9, "score_reason": "great"}\\nend')
    assert out["score"] == 5
    assert out["score_reason"] == "great"


def test_retry_then_success(monkeypatch):
    mod = _load_phase_a_module()
    monkeypatch.setattr(mod.time, "sleep", lambda *_: None)

    cfg = mod.PhaseAConfig(model="deepseek-reasoner", retries=2)
    client = _FakeClient([RuntimeError("transient"), '{"score": 4, "score_reason": "ok"}'])

    content = mod._call_deepseek("p", cfg, client)
    assert "score" in content
    assert client.calls == 2


def test_main_preserves_schema_and_order(tmp_path, monkeypatch):
    mod = _load_phase_a_module()

    input_path = tmp_path / "new-articles.json"
    output_path = tmp_path / "scored-articles.json"
    payload = {
        "generated_at": "2026-03-09T00:00:00Z",
        "article_count": 2,
        "articles": [
            {"title": "A", "summary": "ai startup fund", "source": "s1", "url": "u1", "published": "p1"},
            {"title": "B", "summary": "market data vc", "source": "s2", "url": "u2", "published": "p2"},
        ],
    }
    input_path.write_text(json.dumps(payload), encoding="utf-8")

    responses = [
        '{"score": 3, "score_reason": "r1"}',
        '{"score": 5, "score_reason": "r2"}',
    ]

    monkeypatch.setattr(mod, "_load_phase_a_config", lambda: mod.PhaseAConfig(model="deepseek-reasoner", retries=0))
    monkeypatch.setattr(mod, "_build_client", lambda _cfg: _FakeClient(responses))
    monkeypatch.setattr(
        "sys.argv",
        [
            "phase_a_score.py",
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
    assert out["article_count"] == 2
    assert out["model"] == "CHEAP"
    assert [a["title"] for a in out["articles"]] == ["A", "B"]
    assert [a["score"] for a in out["articles"]] == [3, 5]
    assert [a["score_reason"] for a in out["articles"]] == ["r1", "r2"]
