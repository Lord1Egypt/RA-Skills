import unicodedata

import verify

INDEX = {"m1": {"id": "m1", "session": "s1", "ts": "2026-09-12T09:01:00Z", "role": "user", "kind": "text",
                "text": "帮我做一个笔记应用。只有我自己能看到我的笔记。\nThanks!"}}


def write(root, rel, text, newline="\n"):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text.replace("\n", newline).encode("utf-8"))
    return p


def test_transcript_quote_found_and_timestamp_taken_from_digest():
    out = verify.check_transcript({"msg_id": "m1", "session": "wrong", "quote": "只有我自己能看到我的笔记",
                                   "ts": "1999-01-01"}, INDEX)
    assert out == {"ok": True, "ts": "2026-09-12T09:01:00Z", "session": "s1", "role": "user", "msg_kind": "text"}


def test_transcript_quote_whitespace_insensitive():
    assert verify.check_transcript({"msg_id": "m1", "quote": "我的笔记。 Thanks!"}, INDEX)["ok"]


def test_quote_matches_across_unicode_normalisation():
    index = {"m": {**INDEX["m1"], "text": unicodedata.normalize("NFC", "café is open")}}
    quote = unicodedata.normalize("NFD", "café is open")
    assert verify.check_transcript({"msg_id": "m", "quote": quote}, index)["ok"]


def test_transcript_failures():
    assert verify.check_transcript({"msg_id": "nope", "quote": "abcdef"}, INDEX)["reason"].startswith("message id not found")
    assert "shorter" in verify.check_transcript({"msg_id": "m1", "quote": "我的"}, INDEX)["reason"]
    assert "word for word" in verify.check_transcript({"msg_id": "m1", "quote": "我从来没说过这句话"}, INDEX)["reason"]


CODE = "line one\n\nconst a = 1;\nconst b = 2;\n\n\nconst c = 3;\nconst a = 1;\n"


def test_code_snippet_near_given_line(tmp_path):
    write(tmp_path, "src/x.ts", CODE)
    out = verify.check_code({"path": "src/x.ts", "line": 5, "snippet": "const b = 2;"}, tmp_path)
    assert out["ok"] and out["line"] == 4 and out["line_corrected"] is False and out["path"] == "src/x.ts"


def test_code_snippet_far_but_unique_is_corrected(tmp_path):
    write(tmp_path, "src/x.ts", CODE)
    out = verify.check_code({"path": "src/x.ts", "line": 40, "snippet": "const c = 3;"}, tmp_path)
    assert out["ok"] and out["line"] == 7 and out["line_corrected"] is True and "corrected" in out["reason"]


def test_code_snippet_repeated_far_away_fails(tmp_path):
    write(tmp_path, "src/x.ts", CODE)
    out = verify.check_code({"path": "src/x.ts", "line": 40, "snippet": "const a = 1;"}, tmp_path)
    assert not out["ok"] and "occurs 2 times" in out["reason"]


def test_multi_line_snippet_across_a_blank_line(tmp_path):
    write(tmp_path, "src/x.ts", CODE)
    out = verify.check_code({"path": "src/x.ts", "line": 4, "snippet": "const b = 2;\nconst c = 3;"}, tmp_path)
    assert out["ok"] and out["line"] == 4


def test_code_evidence_with_crlf_file(tmp_path):
    write(tmp_path, "a.sql", "create table t (id int);\nalter table t disable row level security;\n", newline="\r\n")
    assert verify.check_code({"path": "a.sql", "line": 2, "snippet": "alter table t disable row level security;"}, tmp_path)["ok"]


def test_code_failures(tmp_path):
    write(tmp_path, "a.ts", "x\n")
    outside = tmp_path.parent / "outside.ts"
    outside.write_text("x\n")
    assert verify.check_code({"path": "../outside.ts", "line": 1, "snippet": "x"}, tmp_path)["reason"] == "path is outside the project"
    assert verify.check_code({"path": str(outside), "line": 1, "snippet": "x"}, tmp_path)["reason"] == "path is outside the project"
    assert verify.check_code({"path": "missing.ts", "line": 1, "snippet": "x"}, tmp_path)["reason"] == "file not found"
    assert verify.check_code({"path": "a.ts", "line": 1, "snippet": "   "}, tmp_path)["reason"] == "snippet is empty"
    assert verify.check_code({"path": "a.ts", "line": 1, "snippet": "const missing = 1;"}, tmp_path)["reason"] == "snippet not found in the file"


def test_symlink_pointing_outside_is_rejected(tmp_path):
    secret = tmp_path.parent / "elsewhere.txt"
    secret.write_text("token\n")
    root = tmp_path / "app"
    root.mkdir()
    (root / "link.txt").symlink_to(secret)
    assert not verify.check_code({"path": "link.txt", "line": 1, "snippet": "token"}, root)["ok"]


def test_probe_evidence(tmp_path):
    write(tmp_path, "a.sql", "alter table t disable row level security;\n")
    finding = {"id": "supabase_rls:a.sql:1", "probe": "supabase_rls", "level": "certain", "path": "a.sql",
               "line": 1, "snippet": "alter table t disable row level security;", "message": "RLS off", "implies": []}
    good = verify.check_probe({"finding_id": finding["id"]}, {finding["id"]: finding}, tmp_path)
    assert good["ok"] and good["probe"] == "supabase_rls" and good["message"] == "RLS off"
    assert verify.check_probe({"finding_id": "nope"}, {}, tmp_path)["reason"] == "probe finding not found in probes.json"
    write(tmp_path, "a.sql", "alter table t enable row level security;\n")
    stale = verify.check_probe({"finding_id": finding["id"]}, {finding["id"]: finding}, tmp_path)
    assert not stale["ok"] and stale["reason"].startswith("the code changed since the probe ran")


def test_find_snippet_lines():
    lines = ["a b", "", "c", "a b"]
    assert verify.find_snippet_lines(lines, "a  b") == [1, 4]
    assert verify.find_snippet_lines(lines, "b\nc") == [1]
    assert verify.find_snippet_lines(lines, "") == []


KEY = "sk-proj-" + "Ab3dE5fG7hJ9kL1mN3pQ5rS7tU9vW1xY"


def test_masked_or_raw_snippet_matches_a_line_holding_a_secret(tmp_path):
    import redact
    write(tmp_path, ".env.local", f"A=1\nNEXT_PUBLIC_OPENAI_API_KEY={KEY}\n")
    raw = f"NEXT_PUBLIC_OPENAI_API_KEY={KEY}"
    assert verify.check_code({"path": ".env.local", "line": 2, "snippet": raw}, tmp_path)["ok"]
    assert verify.check_code({"path": ".env.local", "line": 2, "snippet": redact.redact(raw)}, tmp_path)["ok"]


def test_trivially_short_snippets_do_not_count_as_evidence(tmp_path):
    write(tmp_path, "a.ts", "a\nconsole.log(1);\n")
    out = verify.check_code({"path": "a.ts", "line": 200, "snippet": "a"}, tmp_path)
    assert not out["ok"] and "too short" in out["reason"]
