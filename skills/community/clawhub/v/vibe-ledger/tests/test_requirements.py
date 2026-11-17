import json
import re
import subprocess
from pathlib import Path

import pytest

import requirements as R
import vl
from common import load_json
from helpers.fake_logs import ClaudeSession
from ledger_report.requirements_html import render_requirements


def rec(i, role, text, seq, session="s1", kind="text", turn=None, ts=None):
    return {"id": i, "role": role, "kind": kind, "text": text, "session": session, "agent": "claude-code",
            "ts": ts or f"2026-10-01T10:{seq:02d}:00Z", "seq": seq, "turn": turn if turn is not None else seq,
            "files": [], "cwd": "", "sidechain": False, "in_project": True}


RECS = [
    rec("u1", "user", "字幕要按语音时长计时，另外 README 只留名字", 0),
    rec("a1", "assistant", "好的。我可以做三件事：1. 字幕计时 2. 网络断了用 say 配音 3. 清空 README", 1),
    rec("u2", "user", "先把 2 做了", 2),
    rec("n1", "user", "[Request interrupted by user for tool use]", 3),
    rec("u3", "user", "继续", 4),
    rec("u4", "user", "仿照 slides_maker 写一个完整的 README", 5),
    rec("u5", "user", "push", 6),
]


def app(tmp_path):
    root = tmp_path / "app"
    (root / "scripts").mkdir(parents=True)
    (root / "scripts" / "captions.py").write_text("import json\n\n\ndef cue_times(durations):\n    return durations\n",
                                                  encoding="utf-8")
    (root / "README.md").write_text("# app\n\nTurn text into a narrated video.\n", encoding="utf-8")
    return root


def ev_tx(mid, quote):
    return {"kind": "transcript", "session": "s1", "msg_id": mid, "quote": quote}


def base_doc():
    return {
        "evidence": {
            "E1": ev_tx("u1", "字幕要按语音时长计时"),
            "E2": {"kind": "code", "path": "scripts/captions.py", "line": 4, "snippet": "def cue_times(durations):"},
            "E3": ev_tx("u1", "README 只留名字"),
            "E4": ev_tx("u4", "仿照 slides_maker 写一个完整的 README"),
            "E5": ev_tx("u2", "先把 2 做了"),
            "E6": ev_tx("a1", "网络断了用 say 配音"),
        },
        "requirements": [
            {"id": "R1", "area": "字幕", "plain": "字幕按语音时长计时", "source": ["E1"], "status": "done",
             "verdict_plain": "做到了", "verdict_dev": "cue_times", "evidence": ["E2"]},
            {"id": "R2", "area": "README", "plain": "README 只留名字", "source": ["E3"], "status": "superseded",
             "superseded_by": "E4", "verdict_plain": "你后来改了", "verdict_dev": "u4", "evidence": []},
            {"id": "R3", "area": "配音", "plain": "网络断了用 say 配音", "source": ["E5", "E6"], "status": "missing",
             "searched": ["say -v"], "verdict_plain": "没有", "verdict_dev": "no say call", "evidence": [],
             "fix_prompt": "add a say fallback"},
        ],
        "skipped": {"ack": ["u3"], "process": ["u5"]},
    }


# ---- request packs ----

def test_packs_hold_every_typed_message_with_its_context_and_drop_harness_notes(tmp_path):
    packs, info = R.build_packs(tmp_path, RECS)
    assert len(packs) == 1 and info["messages"] == 5 and info["noise"] == 1 and info["sessions"] == 1
    text = packs[0]
    assert all(f"[{i}] USER" in text for i in ("u1", "u2", "u3", "u4", "u5")) and "[n1]" not in text
    block = text.split("[u2] USER")[1].split("####")[0]
    assert "AI before this:" in block and "网络断了用 say 配音" in block  # the proposal "2" refers to
    assert "AI before this" not in text.split("[u1] USER")[1].split("####")[0]  # nothing came before u1


def test_packs_split_at_the_limit_and_cut_long_context(tmp_path):
    recs = [rec(f"a{k}", "assistant", "x" * 1000 + f"END{k}", 2 * k) for k in range(30)]
    recs += [rec(f"u{k}", "user", f"请求 {k}", 2 * k + 1) for k in range(30)]
    packs, info = R.build_packs(tmp_path, recs, limit=3000)
    assert len(packs) > 1 and info["messages"] == 30
    joined = "".join(packs)
    assert all(f"[u{k}] USER" in joined for k in range(30))
    assert "x" * (R.CONTEXT_CHARS + 1) not in joined and "END3" in joined


def test_packs_say_when_there_are_no_messages(tmp_path):
    packs, info = R.build_packs(tmp_path, [])
    assert info["messages"] == 0 and "No messages from the user" in packs[0]


# ---- format ----

@pytest.mark.parametrize("change, problem", [
    (lambda d: d["requirements"][0].update(status="changed"), "needs changed_to"),
    (lambda d: d["requirements"][1].pop("superseded_by"), "needs superseded_by"),
    (lambda d: d["requirements"][1].update(superseded_by="E2"), "needs superseded_by"),
    (lambda d: d["requirements"][0].update(status="kept"), "status must be one of"),
    (lambda d: d["requirements"][0].update(source=[]), "source must list"),
    (lambda d: d["requirements"][0].update(source=["E2"]), "must be transcript"),
    (lambda d: d["requirements"][0].pop("verdict_dev"), "missing verdict_dev"),
    (lambda d: d["skipped"].update(chitchat=["u3"]), "reason chitchat"),
    (lambda d: d["requirements"][2].update(searched="say"), "searched must be a list"),
])
def test_validate_names_each_problem(change, problem):
    d = base_doc()
    change(d)
    with pytest.raises(R.RequirementsError) as exc:
        R.validate(d)
    assert any(problem in p for p in exc.value.problems), exc.value.problems


# ---- verification ----

def test_verify_keeps_what_the_evidence_shows(tmp_path):
    out = R.verify(base_doc(), RECS, app(tmp_path), {"findings": []})
    by = {x["id"]: x for x in out["requirements"]}
    assert by["R1"]["status"] == "done" and by["R1"]["files"] == ["scripts/captions.py"]
    assert by["R2"]["status"] == "superseded"
    assert by["R3"]["status"] == "missing" and by["R3"]["absent_verified"] is True
    assert by["R3"]["source"] == ["E5", "E6"]  # the user's reply first, the AI proposal it approved after
    cov = out["coverage"]
    assert cov["messages"] == 5 and cov["noise"] == 1 and cov["unaccounted"] == []
    assert cov["cited"] == 3 and cov["skipped"] == {"ack": 1, "process": 1}


def test_verify_downgrades_unsupported_verdicts(tmp_path):
    d = base_doc()
    d["evidence"]["E2"]["snippet"] = "def cue_times(seconds):"  # not in the file
    d["requirements"][2]["searched"] = ["narrated"]  # it is in README.md
    d["requirements"][1]["superseded_by"] = "E1"  # the same moment, not later
    d["requirements"].append({"id": "R4", "plain": "短词", "source": ["E1"], "status": "missing", "searched": ["say"],
                              "verdict_plain": "v", "verdict_dev": "d", "evidence": []})
    out = R.verify(d, RECS, app(tmp_path), {"findings": []})
    by = {x["id"]: x for x in out["requirements"]}
    assert all(by[i]["status"] == "unknown" for i in ("R1", "R2", "R3", "R4"))
    assert by["R1"]["downgraded_from"] == "done" and "no code" in by["R1"]["downgrade_reason"]
    assert "README.md:3" in by["R3"]["downgrade_reason"]
    assert "not later" in by["R2"]["downgrade_reason"]
    assert "at least 4 characters" in by["R4"]["downgrade_reason"]
    assert out["verification"]["downgraded"] == 4 and by["R1"]["files"] == []


def test_verify_rejects_requirements_the_user_never_said(tmp_path):
    d = base_doc()
    d["requirements"][2]["source"] = ["E6"]  # only the AI's message
    d["evidence"]["E1"]["quote"] = "字幕必须完美同步"  # not in u1
    out = R.verify(d, RECS, app(tmp_path), {"findings": []})
    reasons = {x["id"]: x["reason"] for x in out["rejected"]}
    assert "user said" in reasons["R3"] and "could be found" in reasons["R1"]
    assert [x["id"] for x in out["requirements"]] == ["R2"]


def test_coverage_lists_messages_nobody_accounted_for(tmp_path):
    d = base_doc()
    d["skipped"] = {"ack": ["u3", "not-a-message"]}
    out = R.verify(d, RECS, app(tmp_path), {"findings": []})
    cov = out["coverage"]
    assert [u["id"] for u in cov["unaccounted"]] == ["u5"] and cov["stray_skipped"] == ["not-a-message"]
    lines = "\n".join(R.summary_lines(out))
    assert "1 unaccounted" in lines and "u5: push" in lines


def test_each_message_counts_once_and_a_citation_beats_a_skip(tmp_path):
    d = base_doc()
    d["skipped"] = {"ack": ["u3", "u3", "u1"], "process": ["u5", "u3"]}  # u1 is cited by R1
    cov = R.verify(d, RECS, app(tmp_path), {"findings": []})["coverage"]
    assert cov["skipped"] == {"ack": 1, "process": 1} and cov["cited"] == 3 and cov["unaccounted"] == []
    assert cov["cited"] + sum(cov["skipped"].values()) == cov["messages"]


def test_search_ignores_git_ignored_and_binary_files(tmp_path):
    root = app(tmp_path)
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    (root / ".gitignore").write_text("out/\n", encoding="utf-8")
    (root / "out").mkdir()
    (root / "out" / "log.txt").write_text("say -v Ting-Ting\n", encoding="utf-8")
    (root / "blob.bin").write_bytes(b"\0say -v")
    subprocess.run(["git", "-C", str(root), "add", ".gitignore", "README.md", "scripts", "blob.bin"], check=True)
    assert R.search_terms(["say -v"], R._project_texts(root)) == {}
    assert R.search_terms(["NARRATED"], R._project_texts(root)) == {"NARRATED": "README.md:3"}


def test_merge_prefixes_ids_and_keeps_links():
    a, b = base_doc(), base_doc()
    b["skipped"] = {"process": ["u5", "u6"]}
    out = R.merge([a, b])
    ids = [x["id"] for x in out["requirements"]]
    assert ids[:3] == ["r1_R1", "r1_R2", "r1_R3"] and ids[3] == "r2_R1"
    assert out["requirements"][1]["superseded_by"] == "r1_E4" and out["requirements"][4]["superseded_by"] == "r2_E4"
    assert out["skipped"] == {"ack": ["u3"], "process": ["u5", "u6"]}


# ---- the page ----

def test_tab_groups_by_area_and_puts_problems_first(tmp_path):
    out = R.verify(base_doc(), RECS, app(tmp_path), {"findings": []})
    html = render_requirements(out, "zh")
    areas = re.findall(r'<section class="req-area"><h3>([^<]+) <span', html)
    assert areas[0] == "配音"  # the area with a problem comes first
    assert set(areas) == {"配音", "字幕", "README"}
    assert 'data-rstatus="missing"' in html and 'data-rfilter="problems"' in html
    assert "在项目里找过 “say -v”，都没有。" in html and 'data-file="scripts/captions.py"' in html
    assert "你后来改了说法" in html and "仿照 slides_maker" in html
    assert "复制" in html  # the fix prompt of the missing requirement
    assert "Your asks" not in html


def test_tab_says_so_when_there_are_no_conversations():
    html = render_requirements({"requirements": [], "none": True}, "en")
    assert "No conversations that built this project were found" in html


def test_tab_tells_conversations_without_typed_messages_apart():
    html = render_requirements({"requirements": [], "none": True, "threads": 80}, "en")
    assert "80 conversations were found, but none holds a message you typed" in html


# ---- command line ----

@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("VIBE_LEDGER_HOME", str(tmp_path / "home"))
    monkeypatch.setenv("VIBE_LEDGER_OUT_DIR", str(tmp_path / "out"))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude"))
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))
    return tmp_path


def make_session_app(tmp_path):
    root = app(tmp_path)
    s = ClaudeSession(root, "s1")
    ids = [s.user("字幕要按语音时长计时"), s.user("继续")]
    s.edit(root / "scripts/captions.py", "return []", "return durations")
    s.save(tmp_path / "claude" / "projects")
    return root, ids


def put(run, name, doc):
    (run / name).write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")


def test_cli_start_check_render_with_requirements(env, capsys):
    root, (u1, u2) = make_session_app(env)
    assert vl.main(["start", "--project", str(root)]) == 0
    out = capsys.readouterr().out
    run = vl.latest_run(root)
    assert (run / "requests_01.md").exists() and "Requests: 2 messages" in out and "requirements-guide.md" in out
    assert load_json(run / "run.json")["requests"]["messages"] == 2
    put(run, "ledger.json", {"evidence": {}, "promises": []})
    put(run, "explain.json", {"evidence": {}, "files": {}})
    assert vl.main(["check", "--project", str(root)]) == 2
    assert "requirements.json does not exist yet" in capsys.readouterr().out
    put(run, "requirements.json", {
        "evidence": {"E1": {"kind": "transcript", "session": "s1", "msg_id": u1, "quote": "字幕要按语音时长计时"},
                     "E2": {"kind": "code", "path": "scripts/captions.py", "line": 4, "snippet": "def cue_times(durations):"}},
        "requirements": [{"id": "R1", "area": "字幕", "plain": "字幕按语音时长计时", "source": ["E1"], "status": "done",
                          "verdict_plain": "做到了", "verdict_dev": "cue_times", "evidence": ["E2"]}]})
    assert vl.main(["check", "--project", str(root)]) == 0
    out = capsys.readouterr().out
    assert "Requirements: 1 (" in out and "1 unaccounted" in out and "继续" in out
    assert vl.main(["render", "--project", str(root)]) == 0
    html = (run / "report.html").read_text(encoding="utf-8")
    assert 'data-tab="requirements"' in html and 'id="tab-requirements"' in html
    data = json.loads(re.search(r'<script type="application/json" id="vl-data">(.+?)</script>', html, re.S).group(1))
    assert data["requirements"]["unaccounted"] == 1
    card = next(n for n in data["nodes"] if n["id"] == "scripts/captions.py")["card"]
    assert card["requirements"] == [{"id": "R1", "glyph": "✅", "plain": "字幕按语音时长计时"}]


def test_cli_run_without_user_messages_skips_requirements(env, capsys):
    root = app(env)
    assert vl.main(["start", "--project", str(root)]) == 0
    assert "skip requirements.json" in capsys.readouterr().out
    run = vl.latest_run(root)
    put(run, "ledger.json", {"evidence": {}, "promises": []})
    put(run, "explain.json", {"evidence": {}, "files": {}})
    assert vl.main(["check", "--project", str(root)]) == 0
    assert vl.main(["render", "--project", str(root)]) == 0
    html = (run / "report.html").read_text(encoding="utf-8")
    assert "没有找到搭建这个项目的对话记录" in html or "No conversations that built this project" in html


def test_cli_old_run_renders_without_the_tab(env, capsys):
    root, _ = make_session_app(env)
    vl.main(["start", "--project", str(root)])
    run = vl.latest_run(root)
    manifest = load_json(run / "run.json")
    manifest.pop("requests")  # a run started before requirement coverage existed
    put(run, "run.json", manifest)
    put(run, "ledger.json", {"evidence": {}, "promises": []})
    put(run, "explain.json", {"evidence": {}, "files": {}})
    assert vl.main(["check", "--project", str(root)]) == 0
    assert vl.main(["render", "--project", str(root)]) == 0
    html = (run / "report.html").read_text(encoding="utf-8")
    assert "tab-requirements" not in html and 'data-tab="requirements"' not in html
    assert '"requirements": null' in html


def test_cli_merges_requirement_parts(env, capsys):
    root, (u1, u2) = make_session_app(env)
    vl.main(["start", "--project", str(root)])
    run = vl.latest_run(root)
    (run / "parts").mkdir()
    put(run / "parts", "req_01.json", {
        "evidence": {"E1": {"kind": "transcript", "session": "s1", "msg_id": u1, "quote": "字幕要按语音时长计时"}},
        "requirements": [{"id": "R1", "plain": "字幕计时", "source": ["E1"], "status": "unknown",
                          "verdict_plain": "v", "verdict_dev": "d", "evidence": []}],
        "skipped": {"ack": [u2]}})
    assert vl.main(["merge", "--project", str(root)]) == 0
    merged = load_json(run / "requirements.json")
    assert merged["requirements"][0]["id"] == "r1_R1" and merged["skipped"] == {"ack": [u2]}


def test_a_helper_given_a_request_pack_is_analysis_not_building():
    import sessions
    assert sessions._ANALYSIS_FILES.search("read /x/runs/1/requests_01.md and write parts/req_01.json")
    assert sessions._ANALYSIS_FILES.search("requirements.verified.json")
    assert not sessions._ANALYSIS_FILES.search("pip install -r requirements.txt")


def test_guide_example_is_valid_and_covers_the_vocabulary():
    guide = (Path(__file__).resolve().parents[1] / "references" / "requirements-guide.md").read_text(encoding="utf-8")
    block = re.search(r"`{3}json\n(.+?)\n`{3}", guide, re.S).group(1)
    R.validate(json.loads(block))
    missing = [w for w in R.STATUSES + R.SKIP_REASONS if f"`{w}`" not in guide]
    assert not missing, missing
    assert f"≥ {R.MIN_TERM} characters" in guide
