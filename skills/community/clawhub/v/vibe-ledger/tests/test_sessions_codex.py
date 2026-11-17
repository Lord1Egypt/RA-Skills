import sessions
from helpers.fake_logs import CodexSession


def parse(sess, tmp_path):
    f = sess.save(tmp_path / "sessions")
    stats = sessions.Stats()
    return sessions.parse_codex_file(f, stats), stats, f


def test_text_patch_and_failed_exec(tmp_path):
    app = tmp_path / "app"
    s = CodexSession(app)
    ln_user = s.user("Each user should only see their own habits.")
    s.agent("For now I'm starting Firestore in test mode.")
    s.update(app / "firestore.rules", "@@ -1,2 +1,2 @@\n-allow read: if false;\n+allow read: if true;\n")
    s.add(app / "src/App.tsx", "export default function App() {}")
    s.exec_end("npm test", "1 failing", exit_code=1)
    recs, _, f = parse(s, tmp_path)
    assert [(r["role"], r["kind"]) for r in recs] == [
        ("user", "text"), ("assistant", "text"), ("assistant", "edit"), ("assistant", "edit"),
        ("assistant", "command"), ("tool", "error")]
    assert recs[0]["id"] == f"{f.name}:{ln_user}"
    assert recs[0]["session"] == "codex-1" and recs[0]["agent"] == "codex"
    assert recs[2]["old"] == "allow read: if false;" and recs[2]["new"] == "allow read: if true;"
    assert recs[3]["new"] == "export default function App() {}" and recs[3]["text"].startswith("WRITE ")
    assert recs[4]["text"] == "npm test"


def test_item_command_strips_file_url_and_reads_string_exit_code(tmp_path):
    app = tmp_path / "app"
    s = CodexSession(app, version="0.154.0")
    s.user("run it")
    s.item_command("npm run dev", "boom", exit_code="1", cwd=app / "web")
    recs, _, _ = parse(s, tmp_path)
    assert [r["kind"] for r in recs] == ["text", "command", "error"]
    assert recs[1]["cwd"] == str(app / "web")


def test_filechange_and_patch_end_for_the_same_change_count_once(tmp_path):
    app = tmp_path / "app"
    s = CodexSession(app)
    change = {str(app / "a.ts"): {"type": "add", "content": "x"}}
    s.user("go")
    s.add(app / "a.ts", "x")
    s.item_filechange(change)
    recs, _, _ = parse(s, tmp_path)
    assert [r["kind"] for r in recs] == ["text", "edit"]


def test_function_call_fallback_and_exit_code_in_output(tmp_path):
    s = CodexSession(tmp_path / "app", version="0.141.0")
    s.user("go")
    s.function_exec("supabase db push", "Chunk ID: 1\nProcess exited with code 1\nOutput:\npermission denied")
    recs, _, _ = parse(s, tmp_path)
    assert [r["kind"] for r in recs] == ["text", "command", "error"]
    assert recs[1]["text"] == "supabase db push"


def test_custom_exec_javascript_command(tmp_path):
    s = CodexSession(tmp_path / "app", version="0.154.0")
    s.user("go")
    s.custom_exec("sed -n '1,20p' a.ts", "Process exited with code 0\nOutput:\nfine")
    recs, _, _ = parse(s, tmp_path)
    assert [r["kind"] for r in recs] == ["text", "command"]
    assert recs[1]["text"] == "sed -n '1,20p' a.ts"


def test_apply_patch_call_used_when_no_patch_events_and_relative_paths_kept(tmp_path):
    s = CodexSession(tmp_path / "app")
    s.user("go")
    s.apply_patch_call("*** Begin Patch\n*** Add File: src/a.ts\n+export const a = 1;\n*** End Patch")
    recs, _, _ = parse(s, tmp_path)
    assert recs[1]["kind"] == "edit" and recs[1]["files"] == ["src/a.ts"]
    assert recs[1]["new"] == "export const a = 1;"


def test_guardian_sessions_are_skipped(tmp_path):
    s = CodexSession(tmp_path / "app", source={"subagent": {"other": "guardian"}})
    s.user("The following is the Codex agent history whose request action you are assessing ...")
    recs, stats, _ = parse(s, tmp_path)
    assert recs == [] and stats.skipped_sessions == 1


def test_spawned_subagent_prompt_is_agent(tmp_path):
    s = CodexSession(tmp_path / "app", source={"subagent": {"thread_spawn": {"parent_thread_id": "p", "depth": 1}}})
    s.user("You are a critic.")
    recs, _, _ = parse(s, tmp_path)
    assert recs[0]["role"] == "agent" and recs[0]["sidechain"] is True


def test_compaction_is_counted(tmp_path):
    s = CodexSession(tmp_path / "app")
    s.user("go")
    s.compacted()
    _, stats, _ = parse(s, tmp_path)
    assert stats.compact_summaries == 1


def test_malformed_codex_events_are_counted_not_fatal(tmp_path):
    s = CodexSession(tmp_path / "app")
    s.user("go")
    s._ev("event_msg", {"type": "patch_apply_end", "changes": ["not", "a", "dict"]})
    s.agent("done")
    recs, stats, _ = parse(s, tmp_path)
    assert [r["text"] for r in recs] == ["go", "done"]
    assert stats.ignored_types["codex:malformed"] == 1
