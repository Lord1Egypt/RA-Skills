import candidates


def rec(i, role, kind, text, turn, session="s1", **extra):
    r = {"id": f"r{i}", "session": session, "agent": "claude-code", "ts": f"2026-09-12T09:{i:02d}:00Z",
         "role": role, "kind": kind, "text": text, "files": [], "cwd": "/app", "sidechain": False,
         "seq": i, "turn": turn, "in_project": True}
    r.update(extra)
    return r


def edit(i, turn, old, new, path="/app/supabase/migrations/001.sql"):
    return rec(i, "assistant", "edit", f"EDIT {path}\n--- before\n{old}\n+++ after\n{new}", turn,
               files=[path], old=old, new=new)


def test_error_then_bypass_edit_is_a_candidate():
    recs = [rec(0, "user", "text", "save my notes", 1),
            rec(1, "tool", "error", "new row violates row-level security policy", 1),
            edit(2, 1, "alter table notes enable row level security;\ncreate policy p on notes using (auth.uid() = user_id);",
                 "alter table notes disable row level security;")]
    [c] = candidates.find_compromises(recs)
    assert c["id"] == "K1" and c["error_id"] == "r1" and c["change_ids"] == ["r2"]
    assert "rls_disabled" in c["hints"] and "removed_guard" in c["hints"]
    assert c["priority"] == len(c["hints"])


def test_user_reported_error_counts():
    recs = [rec(0, "user", "text", "保存的时候报错了", 1),
            edit(1, 1, "", "app.use(cors());", path="/app/server.js")]
    [c] = candidates.find_compromises(recs)
    assert c["error_id"] == "r0" and "cors_wildcard" in c["hints"]


def test_error_without_a_following_change_is_not_a_candidate():
    recs = [rec(0, "tool", "error", "Error: boom", 1), rec(1, "assistant", "text", "Let me look.", 1)]
    assert candidates.find_compromises(recs) == []


def test_window_stops_after_the_next_turn():
    recs = [rec(0, "tool", "error", "Error: boom", 1),
            rec(1, "user", "text", "ok", 2),
            rec(2, "user", "text", "now something else", 3),
            edit(3, 3, "a", "b")]
    assert candidates.find_compromises(recs) == []


def test_window_stops_after_twenty_records():
    recs = [rec(0, "tool", "error", "Error: boom", 1)]
    recs += [rec(i, "assistant", "text", "thinking", 1) for i in range(1, 22)]
    recs.append(edit(22, 1, "a", "b"))
    assert candidates.find_compromises(recs) == []


def test_overlapping_errors_merge_into_one_candidate():
    recs = [rec(0, "tool", "error", "Error: one", 1), rec(1, "tool", "error", "Error: two", 1),
            edit(2, 1, "a", "b")]
    assert len(candidates.find_compromises(recs)) == 1


def test_command_writes_count_as_changes_but_not_dev_null():
    assert candidates.is_change(rec(0, "assistant", "command", "cat > a.sql <<'EOF'\nselect 1;\nEOF", 1))
    assert candidates.is_change(rec(0, "assistant", "command", "sed -i '' 's/a/b/' x.ts", 1))
    assert not candidates.is_change(rec(0, "assistant", "command", "ls > /dev/null 2>&1", 1))
    assert not candidates.is_change(rec(0, "assistant", "command", "npm test", 1))


def test_bypass_hint_catalogue():
    def hints(new, old=""):
        return candidates.bypass_hints({"kind": "edit", "text": "", "old": old, "new": new})
    assert "policy_allows_all" in hints("create policy p on t for select using (true);")
    assert "type_check_silenced" in hints("// @ts-ignore\nconst x = y as any;")
    assert "verify_skipped" in hints("https.Agent({ rejectUnauthorized: false })")
    assert "service_role_used" in hints("createClient(url, process.env.SUPABASE_SERVICE_ROLE_KEY)")
    assert "empty_catch" in hints("try { go() } catch (e) {}")
    assert "mock_data" in hints("const notes = mockNotes;")
    assert "removed_guard" in hints("handler()", old="requireAuth(handler)")
    assert hints("const total = a + b;") == []


def test_deferrals_from_text_records():
    recs = [rec(0, "assistant", "text", "为了先跑起来，我暂时关闭 RLS，之后再补策略。", 1),
            rec(1, "assistant", "text", "For now I'm using test mode; lock it down before launch.", 1),
            rec(2, "assistant", "text", "All done.", 1),
            rec(3, "tool", "error", "temporary failure", 1)]
    found = candidates.find_deferrals(recs)
    assert [d["msg_id"] for d in found] == ["r0", "r1"]
    assert "暂时" in found[0]["phrases"] and "for now" in found[1]["phrases"]


def test_claims_are_the_last_ai_text_of_each_turn():
    recs = [rec(0, "user", "text", "add login", 1),
            rec(1, "assistant", "text", "I've added the login check.", 1),
            rec(2, "assistant", "text", "接口已经加了登录保护。", 1),
            rec(3, "user", "text", "thanks", 2),
            rec(4, "assistant", "text", "You're welcome.", 2)]
    found = candidates.find_claims(recs)
    assert [a["msg_id"] for a in found] == ["r2"]


def test_code_todos_only_in_comments(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.ts").write_text(
        'const PASSWORD = "admin123"; // hardcoded for now\n'
        '<input placeholder="Email" />\n'
        "# TODO: lock down\n"
        "/* 这里暂时写死 */\n", encoding="utf-8")
    found = candidates.scan_code_todos(tmp_path)
    assert [(t["path"], t["line"]) for t in found] == [("src/a.ts", 1), ("src/a.ts", 3), ("src/a.ts", 4)]


def test_single_small_pack_contains_every_user_message_and_ids(tmp_path):
    recs = [rec(0, "user", "text", "只有我自己能看到我的笔记", 1),
            rec(1, "tool", "error", "Error: violates row-level security", 1),
            edit(2, 1, "enable row level security", "disable row level security")]
    out = candidates.run(tmp_path, recs)
    assert len(out["packs_text"]) == 1
    pack = out["packs_text"][0]
    assert "[r0]" in pack and "只有我自己能看到我的笔记" in pack
    assert "Candidate K1" in pack and "[r2]" in pack
    assert out["stats"]["packs"] == 1 and out["stats"]["compromises"] == 1


def test_large_digest_splits_into_packs_under_the_limit(tmp_path):
    recs = []
    for turn in range(1, 41):
        recs.append(rec(turn, "user", "text", f"turn {turn} " + "x" * 900, turn))
    packs = candidates.build_packs(tmp_path, recs, [], [], [], [], limit=5000)
    assert len(packs) > 1
    joined = "".join(packs)
    assert all(f"[r{i}]" in joined for i in range(1, 41))
    assert all(len(p) <= 5000 + 1000 for p in packs)  # limit plus the fixed header


def test_long_record_is_truncated_with_a_marker():
    text = candidates.render_record(rec(0, "user", "text", "y" * (candidates.RECORD_LIMIT + 50), 1))
    assert "50 more characters not shown" in text


def test_empty_digest_still_makes_one_pack(tmp_path):
    out = candidates.run(tmp_path, [])
    assert len(out["packs_text"]) == 1 and "No conversation records" in out["packs_text"][0]


def test_code_todos_are_masked(tmp_path):
    key = "sk-proj-" + "Zq8vK2mXp9Lr4Tn6Wb3Yc5Ud7"
    (tmp_path / "a.ts").write_text(f'const k = "{key}"; // TODO: temporary hardcoded key {key}\n', encoding="utf-8")
    out = candidates.run(tmp_path, [])
    assert key not in out["todos"][0]["text"] and key not in out["packs_text"][0]
