import json

import pytest

import shot
import vl
from common import load_json
from e2e.medium import make_medium


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("VIBE_LEDGER_HOME", str(tmp_path / "home"))
    monkeypatch.setenv("VIBE_LEDGER_OUT_DIR", str(tmp_path / "out"))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude"))
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))
    return tmp_path


def test_medium_project_collapses_into_folders(env, capsys):
    app = make_medium(env / "medium")
    assert vl.main(["start", "--project", str(app)]) == 0
    g = load_json(vl.latest_run(app) / "graph.json")
    assert len(g["nodes"]) == 101 and g["collapsed"] is True
    assert [f["id"] for f in g["folders"]] == ["src/api", "src/components", "src/lib", "src/pages", "src/utils"]
    assert {x["id"] for x in g["externals"]} == {"ext:openai", "ext:supabase"}
    assert [e["path"] for e in g["entries"]] == ["src/main.tsx"]
    assert sum(n["explain"] for n in g["nodes"]) == 30
    assert "large project, so folders start collapsed" in capsys.readouterr().out


def test_medium_project_renders_without_overlaps_in_a_real_browser(env, capsys):
    chrome = shot.find_chrome()
    if not chrome:
        pytest.skip("Chrome/Chromium not available")
    app = make_medium(env / "medium")
    assert vl.main(["start", "--project", str(app)]) == 0
    run = vl.latest_run(app)
    (run / "ledger.json").write_text(json.dumps({"evidence": {}, "promises": []}), encoding="utf-8")
    (run / "explain.json").write_text(json.dumps({"evidence": {}, "files": {"src/api/a0.ts": {
        "purpose_plain": "把用户的问题发给 OpenAI。", "functions": [{"name": "ask0", "line": 4, "plain": "发问题"}]}}},
        ensure_ascii=False), encoding="utf-8")
    (run / "requirements.json").write_text(json.dumps({"evidence": {}, "requirements": []}), encoding="utf-8")
    assert vl.main(["check", "--project", str(app)]) == 0
    assert vl.main(["render", "--project", str(app)]) == 0
    page = (run / "report.html").as_uri()
    closed = shot.layout_report(shot.dump_dom(chrome, page))
    assert closed["done"] and closed["overlaps"] == []
    assert {n["id"] for n in closed["nodes"]} == {"folder:src/api", "folder:src/components", "folder:src/lib",
                                                   "folder:src/pages", "folder:src/utils", "src/main.tsx",
                                                   "ext:openai", "ext:supabase"}
    opened = shot.layout_report(shot.dump_dom(chrome, page + "?select=src/api/a0.ts"))
    assert opened["done"] and opened["overlaps"] == [] and opened["selected"] == ["src/api/a0.ts"]
    assert "folder:src/api" not in {n["id"] for n in opened["nodes"]}
