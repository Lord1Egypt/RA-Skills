import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

import pytest

import vl
from common import load_json
from helpers.fake_logs import ClaudeSession


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("VIBE_LEDGER_HOME", str(tmp_path / "home"))
    monkeypatch.setenv("VIBE_LEDGER_OUT_DIR", str(tmp_path / "out"))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude"))
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))  # never read the real ~/.codex in tests
    return tmp_path


def make_project(tmp_path, name="app"):
    app = tmp_path / name
    (app / "supabase" / "migrations").mkdir(parents=True)
    (app / "supabase" / "migrations" / "001.sql").write_text(
        "create table notes (id uuid);\n\nalter table notes disable row level security;\n", encoding="utf-8")
    (app / "package.json").write_text(json.dumps({"dependencies": {"@supabase/supabase-js": "2"}}), encoding="utf-8")
    s = ClaudeSession(app, "s1")
    uid = s.user("只有我自己能看到我的笔记")
    s.bash("npx supabase db push", "Error: new row violates row-level security policy", is_error=True)
    s.edit(app / "supabase/migrations/001.sql", "enable row level security", "disable row level security")
    s.save(tmp_path / "claude" / "projects")
    return app, uid


def next_commands(out):
    return [shlex.split(line.strip()) for line in out.splitlines() if line.strip().startswith("python3 ")]


def minimal_ledger(uid):
    return {"evidence": {
                "E1": {"kind": "transcript", "session": "s1", "msg_id": uid, "quote": "只有我自己能看到我的笔记"},
                "E2": {"kind": "code", "path": "supabase/migrations/001.sql", "line": 3,
                       "snippet": "alter table notes disable row level security;"}},
            "promises": [{"id": "P1", "type": "user_requirement", "question": "who_can_see",
                          "plain": "只有我自己能看到我的笔记", "source": ["E1"], "status": "broken",
                          "verdict_plain": "陌生人也能读", "verdict_dev": "RLS off", "evidence": ["E2"],
                          "fix_prompt": "Enable RLS on notes."}]}


EMPTY_EXPLAIN = {"evidence": {}, "files": {}}


def test_start_writes_the_run_folder(env, capsys):
    app, _ = make_project(env)
    assert vl.main(["start", "--project", str(app)]) == 0
    out = capsys.readouterr().out
    run = vl.latest_run(app)
    for name in ("digest.jsonl", "candidates.json", "reading_pack_01.md", "probes.json", "run.json"):
        assert (run / name).exists(), name
    manifest = load_json(run / "run.json")
    assert manifest["lang"] == "zh" and manifest["sessions"]["threads"] == 1
    assert manifest["retention"]["days"] == 30 and manifest["packs"] == ["reading_pack_01.md"]
    assert "supabase_rls" in manifest["probes"]["ran"]
    assert "NEXT" in out and "retention --set" in out
    assert not any(p.name.startswith(".vibe") for p in app.iterdir())  # nothing written into the project


def test_start_prints_runnable_next_commands_for_unusual_path(env, capsys):
    app, uid = make_project(env, name="我的 应用")
    assert vl.main(["start", "--project", str(app)]) == 0
    cmds = next_commands(capsys.readouterr().out)
    check = next(c for c in cmds if "check" in c)
    (vl.latest_run(app) / "ledger.json").write_text(json.dumps(minimal_ledger(uid), ensure_ascii=False), encoding="utf-8")
    (vl.latest_run(app) / "explain.json").write_text(json.dumps(EMPTY_EXPLAIN), encoding="utf-8")
    (vl.latest_run(app) / "requirements.json").write_text(json.dumps({"evidence": {}, "requirements": []}), encoding="utf-8")
    res = subprocess.run([sys.executable] + check[1:], capture_output=True, text=True)
    assert res.returncode == 0, res.stdout + res.stderr
    assert (vl.latest_run(app) / "ledger.verified.json").exists()
    render_cmd = next(c for c in next_commands(res.stdout) if "render" in c)
    res2 = subprocess.run([sys.executable] + render_cmd[1:], capture_output=True, text=True)
    assert res2.returncode == 0, res2.stdout + res2.stderr
    report = re.search(r"Report: (.+)", res2.stdout).group(1).strip()
    assert report.endswith(".html") and Path(report).parent == env / "out"


def test_check_reports_format_problems_and_missing_ledger(env, capsys):
    app, uid = make_project(env)
    vl.main(["start", "--project", str(app)])
    capsys.readouterr()
    assert vl.main(["check", "--project", str(app)]) == 2
    assert "does not exist yet" in capsys.readouterr().out
    bad = minimal_ledger(uid)
    bad["promises"][0]["status"] = "maybe"
    (vl.latest_run(app) / "ledger.json").write_text(json.dumps(bad), encoding="utf-8")
    assert vl.main(["check", "--project", str(app)]) == 2
    assert "status must be one of" in capsys.readouterr().out
    (vl.latest_run(app) / "ledger.json").write_text("{not json", encoding="utf-8")
    assert vl.main(["check", "--project", str(app)]) == 2


def test_merge_reads_parts_dir(env, capsys):
    app, uid = make_project(env)
    vl.main(["start", "--project", str(app)])
    parts = vl.latest_run(app) / "parts"
    parts.mkdir()
    (parts / "part_01.json").write_text(json.dumps(minimal_ledger(uid), ensure_ascii=False), encoding="utf-8")
    assert vl.main(["merge", "--project", str(app)]) == 0
    merged = load_json(vl.latest_run(app) / "ledger.json")
    assert [p["id"] for p in merged["promises"]] == ["p1_P1"]
    assert "check" in capsys.readouterr().out


def test_render_requires_check_first(env, capsys):
    app, _ = make_project(env)
    vl.main(["start", "--project", str(app)])
    assert vl.main(["render", "--project", str(app)]) == 2


def test_commands_before_start_explain_what_to_do(env, capsys):
    app, _ = make_project(env)
    with pytest.raises(SystemExit) as exc:
        vl.main(["check", "--project", str(app)])
    assert "start" in str(exc.value)


def test_missing_project_folder(env):
    with pytest.raises(SystemExit) as exc:
        vl.main(["start", "--project", str(env / "nope")])
    assert "not found" in str(exc.value)


def test_start_without_git_and_without_logs(env, capsys):
    app = env / "bare"
    app.mkdir()
    (app / "index.html").write_text("<h1>hi</h1>", encoding="utf-8")
    assert vl.main(["start", "--project", str(app)]) == 0
    out = capsys.readouterr().out
    assert "No conversations were found" in out
    assert load_json(vl.latest_run(app) / "run.json")["unattributed"] == ["index.html"]


def test_retention_read_and_set(env, capsys):
    settings = env / "settings.json"
    assert vl.main(["retention", "--settings", str(settings)]) == 0
    assert "30 days" in capsys.readouterr().out
    settings.write_text(json.dumps({"theme": "dark"}), encoding="utf-8")
    assert vl.main(["retention", "--settings", str(settings), "--set", "365"]) == 0
    data = load_json(settings)
    assert data == {"theme": "dark", "cleanupPeriodDays": 365}
    assert (env / "settings.json.vibe-ledger.bak").exists()
    settings.write_text("{oops", encoding="utf-8")
    assert vl.main(["retention", "--settings", str(settings), "--set", "365"]) == 2
    assert settings.read_text() == "{oops"
    assert vl.main(["retention", "--settings", str(settings), "--set", "0"]) == 2


def test_two_starts_in_the_same_second_get_distinct_runs(env):
    app, _ = make_project(env)
    vl.main(["start", "--project", str(app)])
    first = vl.latest_run(app)
    vl.main(["start", "--project", str(app)])
    assert vl.latest_run(app) != first


def test_shot_without_chrome_says_so(env, capsys, monkeypatch):
    app, uid = make_project(env)
    vl.main(["start", "--project", str(app)])
    (vl.latest_run(app) / "ledger.json").write_text(json.dumps(minimal_ledger(uid), ensure_ascii=False), encoding="utf-8")
    (vl.latest_run(app) / "explain.json").write_text(json.dumps(EMPTY_EXPLAIN), encoding="utf-8")
    (vl.latest_run(app) / "requirements.json").write_text(json.dumps({"evidence": {}, "requirements": []}), encoding="utf-8")
    vl.main(["check", "--project", str(app)])
    vl.main(["render", "--project", str(app)])
    import shot
    monkeypatch.setattr(shot, "find_chrome", lambda: None)
    capsys.readouterr()
    assert vl.main(["shot", "--project", str(app)]) == 1
    assert "not found" in capsys.readouterr().out


def test_version(capsys):
    with pytest.raises(SystemExit):
        vl.main(["--version"])
    assert vl.__version__ in capsys.readouterr().out


def test_a_failed_start_does_not_leave_a_half_built_latest_run(env, monkeypatch):
    app, _ = make_project(env)
    import sessions

    def boom(*a, **k):
        raise RuntimeError("disk full")
    monkeypatch.setattr(sessions, "collect", boom)
    with pytest.raises(RuntimeError):
        vl.main(["start", "--project", str(app)])
    with pytest.raises(SystemExit):
        vl.latest_run(app)
