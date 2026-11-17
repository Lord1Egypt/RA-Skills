import json

import sessions
from helpers.fake_logs import ClaudeSession, CodexSession

OPENAI = "sk-proj-" + "Ab3dE5fG7hJ9kL1mN3pQ5rS7tU9vW1xY"


def run(app, tmp_path, archive=False):
    return sessions.collect(app, claude_dir=tmp_path / "projects", codex_dir=tmp_path / "sessions",
                            archive_dir=(tmp_path / "archive") if archive else None)


def test_collect_claims_sessions_by_cwd_and_edit_paths(tmp_path):
    app, other = tmp_path / "app", tmp_path / "other"
    app.mkdir()
    other.mkdir()
    a = ClaudeSession(app, "s-app")
    a.user("build the app")
    a.save(tmp_path / "projects")
    b = ClaudeSession(other, "s-other")
    b.user("unrelated app question")
    b.save(tmp_path / "projects")
    c = ClaudeSession(tmp_path, "s-home")
    c.user("fix the app from home")
    c.edit(app / "x.ts", "a", "b")
    c.save(tmp_path / "projects")
    recs, stats = run(app, tmp_path)
    assert {r["session"] for r in recs} == {"s-app", "s-home"}
    assert any(r["text"] == "fix the app from home" for r in recs)
    assert all(r["in_project"] for r in recs)
    assert stats.threads == 2 and stats.by_agent["claude-code"] == 2


def test_cwd_change_mid_session_keeps_only_project_records(tmp_path):
    app, other = tmp_path / "app", tmp_path / "other"
    app.mkdir()
    other.mkdir()
    s = ClaudeSession(app, "s1")
    s.user("app question")
    s.set_cwd(other)
    s.user("other question")
    s.save(tmp_path / "projects")
    recs, _ = run(app, tmp_path)
    assert [r["text"] for r in recs] == ["app question"]


def test_symlinked_project_path(tmp_path):
    real = tmp_path / "real" / "app"
    real.mkdir(parents=True)
    (tmp_path / "link").symlink_to(tmp_path / "real")
    s = ClaudeSession(tmp_path / "link" / "app", "s1")
    s.user("hello app")
    s.save(tmp_path / "projects")
    recs, _ = run(real, tmp_path)
    assert [r["text"] for r in recs] == ["hello app"]


def test_turns_and_seq(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    s = ClaudeSession(app, "s1")
    s.user("one")
    s.assistant_text("reply")
    s.user("two")
    s.save(tmp_path / "projects")
    recs, _ = run(app, tmp_path)
    assert [(r["seq"], r["turn"]) for r in recs] == [(0, 1), (1, 1), (2, 2)]


def test_codex_and_claude_threads_are_ordered_by_time(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    c = CodexSession(app, "x1")
    c.user("codex first")
    c.save(tmp_path / "sessions")
    s = ClaudeSession(app, "s1", start=100)
    s.user("claude later")
    s.save(tmp_path / "projects")
    recs, stats = run(app, tmp_path)
    assert [r["text"] for r in recs] == ["codex first", "claude later"]
    assert stats.by_agent == {"codex": 1, "claude-code": 1}
    assert stats.earliest < stats.latest


def test_relative_codex_patch_paths_resolve_against_cwd(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    s = CodexSession(app)
    s.user("go")
    s.apply_patch_call("*** Begin Patch\n*** Add File: src/a.ts\n+x\n*** End Patch")
    s.save(tmp_path / "sessions")
    recs, _ = run(app, tmp_path)
    assert recs[1]["files"] == [str(app / "src/a.ts")]


def test_digest_is_masked(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    s = ClaudeSession(app, "s1")
    s.user(f"my key is {OPENAI}")
    s.save(tmp_path / "projects")
    recs, _ = run(app, tmp_path)
    assert OPENAI not in recs[0]["text"] and "sk-proj-…" in recs[0]["text"]


def test_archive_keeps_threads_whose_logs_were_deleted(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    s = ClaudeSession(app, "s1")
    s.user(f"remember this {OPENAI}")
    f = s.save(tmp_path / "projects")
    run(app, tmp_path, archive=True)
    archived = list((tmp_path / "archive").glob("*.jsonl"))
    assert archived and OPENAI not in archived[0].read_text(encoding="utf-8")
    f.unlink()
    recs, stats = run(app, tmp_path, archive=True)
    assert [r["text"][:13] for r in recs] == ["remember this"]
    assert stats.archived_threads == 1


def test_prefilter_skips_unrelated_files(tmp_path):
    app = tmp_path / "myapp"
    app.mkdir()
    for i in range(3):
        u = ClaudeSession(tmp_path / f"elsewhere{i}", f"u{i}")
        u.user("nothing to see")
        u.save(tmp_path / "projects")
    s = ClaudeSession(app, "s1")
    s.user("hello")
    s.save(tmp_path / "projects")
    _, stats = run(app, tmp_path)
    assert stats.files_scanned == 4 and stats.files_parsed == 1 and stats.files_matched == 1


def test_prefilter_accepts_json_escaped_folder_names(tmp_path):
    app = tmp_path / "笔记"
    app.mkdir()
    f = tmp_path / "projects" / "x" / "s1.jsonl"
    f.parent.mkdir(parents=True)
    rec = {"type": "user", "uuid": "u1", "sessionId": "s1", "timestamp": "2026-09-12T09:00:00Z",
           "cwd": str(app), "message": {"role": "user", "content": "hello"}}
    f.write_text(json.dumps(rec) + "\n", encoding="utf-8")  # ensure_ascii=True escapes the folder name
    recs, _ = run(app, tmp_path)
    assert [r["text"] for r in recs] == ["hello"]


def test_unreadable_format_warns(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    f = tmp_path / "projects" / "x" / "weird.jsonl"
    f.parent.mkdir(parents=True)
    f.write_text(json.dumps({"type": "brand-new-format", "cwd": str(app), "body": "hi"}) + "\n", encoding="utf-8")
    recs, stats = run(app, tmp_path)
    assert recs == [] and any("format may have changed" in w for w in stats.warnings)


def test_missing_log_dirs_are_fine(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    recs, stats = sessions.collect(app, claude_dir=tmp_path / "nope", codex_dir=None)
    assert recs == [] and stats.files_scanned == 0


def test_prefilter_ignores_mentions_that_are_not_paths(tmp_path):
    app = tmp_path / "myapp"
    app.mkdir()
    noise = ClaudeSession(tmp_path / "elsewhere", "n1")
    noise.user("- [My App](myapp.md) — memory index line injected into every session")
    noise.save(tmp_path / "projects")
    _, stats = run(app, tmp_path)
    assert stats.files_scanned == 1 and stats.files_parsed == 0


def test_records_of_other_projects_are_not_counted_as_skipped(tmp_path):
    app = tmp_path / "myapp"
    app.mkdir()
    other = ClaudeSession(tmp_path / "x" / "myapp-docs", "o1")  # passes the prefilter, belongs elsewhere
    other.raw({"type": "file-history-snapshot", "snapshot": {}})
    other.user("cd /somewhere/myapp/ and look")
    other.save(tmp_path / "projects")
    _, stats = run(app, tmp_path)
    assert stats.files_parsed == 1 and stats.files_matched == 0
    assert sum(stats.ignored_types.values()) == 0


def test_vibe_ledger_analysis_is_not_part_of_the_build_history(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    s = ClaudeSession(app, "s1")
    s.user("build the page")
    s.edit(app / "x.ts", "a", "b")
    s.bash("python3 /skills/vibe-ledger/scripts/vl.py start --project " + str(app), "run folder: …")
    s.user("explain my app")
    s.bash("grep -n fetch src/api.ts", "12: fetch(url)")
    s.save(tmp_path / "projects")
    only = ClaudeSession(app, "s2", start=50)
    only.bash("python3 vl.py check --project .", "Evidence: 3 checked")
    only.user("what did it find?")
    only.save(tmp_path / "projects")
    recs, stats = run(app, tmp_path)
    assert [r["text"] for r in recs if r["role"] == "user"] == ["build the page"]
    assert {r["session"] for r in recs} == {"s1"}


def test_archive_restores_only_threads_whose_logs_are_gone(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    s = ClaudeSession(app, "s1")
    s.user("hello app")
    f = s.save(tmp_path / "projects")
    run(app, tmp_path, archive=True)  # archived while it still counted
    s.bash("python3 /x/vl.py start --project " + str(app), "ok")
    result, command = s.lines.pop(), s.lines.pop()
    s.lines[0:0] = [command, result]  # the analysis run now comes first, so nothing in s1 counts
    f.write_text("".join(json.dumps(x) + "\n" for x in s.lines), encoding="utf-8")
    recs, stats = run(app, tmp_path, archive=True)
    assert recs == [] and stats.archived_threads == 0
    assert not list((tmp_path / "archive").glob("s1*.jsonl"))


def test_helpers_working_on_vibe_ledger_files_are_analysis_too(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    build = ClaudeSession(app, "s1")
    build.user("build the page")
    build.edit(app / "x.ts", "a", "b")
    build.save(tmp_path / "projects")
    helper = ClaudeSession(app, "s2", start=50)  # a subagent handed one group of explain_pack.md; it never runs vl.py
    helper.user("Write <run>/parts/explain_01.json for the files under Group 1 in explain_pack.md.")
    helper.bash("cat src/x.ts", "export const x = 1;")
    helper.save(tmp_path / "projects")
    reader = ClaudeSession(app, "s3", start=80)
    reader.user("Read <run>/reading_pack_01.md and probes.json, then write ledger.json")
    reader.save(tmp_path / "projects")
    recs, _ = run(app, tmp_path)
    assert {r["session"] for r in recs} == {"s1"}


def test_typed_requests_survive_a_wandering_working_folder(tmp_path):
    """The assistant cd'd into its memory folder; what the user typed next is still this project's."""
    from pathlib import Path as P
    app, other = tmp_path / "app", tmp_path / "other"
    (app / "lib").mkdir(parents=True)
    other.mkdir()
    s = ClaudeSession(app, "s-wander")
    s.user("做一个笔记应用")
    s.edit(app / "lib/a.ts", "x", "y")
    s.set_cwd(P.home() / ".claude" / "projects" / "-x" / "memory")
    kept = s.user("只用 kiwi 就可以了")  # typed from a neutral folder; the thread was last working on app
    s.assistant_text("好的")
    s.set_cwd(other)
    gone = s.user("给 other 项目加个按钮")  # another project's folder, and the turn never touches app
    s.write(other / "b.ts", "button")
    linked = s.user("顺便把 app 的标题改了")  # another folder, but the turn edits app
    s.edit(app / "lib/a.ts", "y", "z")
    s.save(tmp_path / "claude" / "projects")
    recs, _ = sessions.collect(app, tmp_path / "claude", tmp_path / "codex")
    ids = {r["id"] for r in recs if r["role"] == "user"}
    assert kept in ids and linked in ids and gone not in ids
    assert not any(r["text"] == "button" or "b.ts" in r["text"] for r in recs)
