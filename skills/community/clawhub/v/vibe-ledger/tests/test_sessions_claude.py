import sessions
from helpers.fake_logs import ClaudeSession


def parse(sess, tmp_path, **save_kw):
    f = sess.save(tmp_path / "projects", **save_kw)
    stats = sessions.Stats()
    return sessions.parse_claude_file(f, stats), stats


def test_user_assistant_edit_command_and_error(tmp_path):
    app = tmp_path / "app"
    s = ClaudeSession(app)
    s.user("只有我自己能看到我的笔记")
    s.assistant_text("好的，我会开启 RLS。")
    s.edit(app / "supabase/migrations/001.sql", "enable row level security", "disable row level security")
    s.bash("npx supabase db push", "Error: new row violates row-level security policy", is_error=True)
    s.bash("ls", "a.ts\nb.ts")
    s.tool("Read", {"file_path": str(app / "a.ts")}, "contents")
    recs, _ = parse(s, tmp_path)
    assert [(r["role"], r["kind"]) for r in recs] == [
        ("user", "text"), ("assistant", "text"), ("assistant", "edit"),
        ("assistant", "command"), ("tool", "error"), ("assistant", "command")]
    edit = recs[2]
    assert edit["old"] == "enable row level security"
    assert edit["new"] == "disable row level security"
    assert edit["files"] == [str(app / "supabase/migrations/001.sql")]
    assert recs[0]["agent"] == "claude-code" and recs[0]["session"] == "sess-1"
    assert recs[0]["ts"].startswith("2026-09-12T") and recs[0]["cwd"] == str(app)
    assert recs[0]["id"] == "sess-1-u1"


def test_bash_output_with_error_text_counts_as_error_without_flag(tmp_path):
    s = ClaudeSession(tmp_path / "app")
    s.bash("npm run dev", "ready\nError: permission denied for table notes")
    recs, _ = parse(s, tmp_path)
    assert [r["kind"] for r in recs] == ["command", "error"]


def test_error_text_is_truncated(tmp_path):
    s = ClaudeSession(tmp_path / "app")
    s.bash("x", "E" * 5000, is_error=True)
    recs, _ = parse(s, tmp_path)
    assert len(recs[1]["text"]) == sessions.TOOL_TEXT_LIMIT


def test_write_and_multiedit_are_edits(tmp_path):
    app = tmp_path / "app"
    s = ClaudeSession(app)
    s.write(app / "a.ts", "export const a = 1;")
    s.tool("MultiEdit", {"file_path": str(app / "b.ts"),
                         "edits": [{"old_string": "x", "new_string": "y"},
                                   {"old_string": "p", "new_string": "q"}]}, "ok")
    recs, _ = parse(s, tmp_path)
    assert [r["kind"] for r in recs] == ["edit", "edit"]
    assert recs[0]["new"] == "export const a = 1;" and recs[0]["old"] == ""
    assert recs[0]["text"].startswith("WRITE ")
    assert recs[1]["old"] == "x\np" and recs[1]["new"] == "y\nq"


def test_wrappers_meta_and_compact_summaries_are_not_user_words(tmp_path):
    s = ClaudeSession(tmp_path / "app")
    s.user("<task-notification>done</task-notification>")
    s.user("<command-name>/model</command-name>")
    s.user("skill text", isMeta=True)
    s.compact_summary("This session is being continued from a previous conversation...")
    s.user("real question")
    recs, stats = parse(s, tmp_path)
    assert [r["text"] for r in recs] == ["real question"]
    assert stats.compact_summaries == 1


def test_sidechain_prompts_are_agent_not_user(tmp_path):
    s = ClaudeSession(tmp_path / "app", sidechain=True)
    s.user("You are a reviewer. Check the code.")
    recs, _ = parse(s, tmp_path)
    assert recs[0]["role"] == "agent" and recs[0]["sidechain"] is True


def test_subagent_file_gets_its_own_thread(tmp_path):
    s = ClaudeSession(tmp_path / "app", session_id="sess-9")
    s.user("Review this")
    recs, _ = parse(s, tmp_path, agent_id="abc")
    assert recs[0]["session"] == "sess-9/agent-abc"
    assert recs[0]["role"] == "agent"


def test_bad_lines_and_other_types_are_counted(tmp_path):
    s = ClaudeSession(tmp_path / "app")
    s.raw({"type": "file-history-snapshot", "snapshot": {}})
    s.user("hi")
    f = s.save(tmp_path / "projects")
    with open(f, "a", encoding="utf-8") as fh:
        fh.write("{broken\n")
    stats = sessions.Stats()
    recs = sessions.parse_claude_file(f, stats)
    assert len(recs) == 1 and stats.bad_lines == 1
    assert stats.ignored_types["claude:file-history-snapshot"] == 1


def test_multi_block_message_gets_suffixed_ids(tmp_path):
    s = ClaudeSession(tmp_path / "app")
    s.raw({"type": "assistant", "uuid": "m1", "sessionId": "sess-1", "timestamp": "2026-09-12T09:00:00Z",
           "cwd": str(tmp_path / "app"),
           "message": {"role": "assistant", "content": [{"type": "text", "text": "one"},
                                                        {"type": "text", "text": "two"}]}})
    recs, _ = parse(s, tmp_path)
    assert [r["id"] for r in recs] == ["m1", "m1#1"]


def test_stats_to_dict_is_json_ready():
    st = sessions.Stats()
    st.ignored_types["claude:x"] += 2
    d = st.to_dict()
    assert d["ignored_types"] == {"claude:x": 2} and isinstance(d["by_agent"], dict)


def test_malformed_records_are_counted_not_fatal(tmp_path):
    app = tmp_path / "app"
    s = ClaudeSession(app)
    base = {"uuid": "x", "sessionId": "sess-1", "cwd": str(app)}
    s.raw({**base, "type": "user", "message": "hello", "timestamp": "2026-09-12T09:00:00Z"})
    s.raw({**base, "type": "assistant", "timestamp": "2026-09-12T09:00:01Z",
           "message": {"content": [{"type": "tool_use", "id": "t", "name": "Edit", "input": ["a"]}]}})
    s.raw({**base, "type": "assistant", "timestamp": "2026-09-12T09:00:02Z",
           "message": {"content": [{"type": "tool_use", "id": "t2", "name": "MultiEdit",
                                    "input": {"file_path": str(app / "a.ts"), "edits": ["a"]}}]}})
    s.raw({**base, "type": "assistant", "timestamp": 123, "message": {"content": [{"type": "text", "text": 5}]}})
    s.raw({**base, "type": "assistant", "timestamp": "2026-09-12T09:00:03Z",
           "message": {"content": [{"type": "tool_use", "id": "t3", "name": "Write", "input": {"file_path": 5, "content": "x"}}]}})
    s.user("still here")
    f = s.save(tmp_path / "projects")
    stats = sessions.Stats()
    recs = sessions.parse_claude_file(f, stats)
    assert recs[-1]["text"] == "still here"
    assert stats.ignored_types["claude:malformed"] >= 3
    assert all(isinstance(r["ts"], str) and all(isinstance(x, str) for x in r["files"]) for r in recs)
    out, _ = sessions.collect(app, claude_dir=tmp_path / "projects")
    assert out[-1]["text"] == "still here"
