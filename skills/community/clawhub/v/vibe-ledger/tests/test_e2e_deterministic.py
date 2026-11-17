import json
from pathlib import Path

import pytest

import render
import vl
from common import load_json, read_jsonl
from e2e.prepare import FAKE_OPENAI, prepare
from e2e.scenarios import SCENARIOS
from e2e.score import score, score_explain, score_graph
from helpers.verified import sample

ANSWERS = Path(__file__).resolve().parent / "fixtures" / "answers"


@pytest.fixture(scope="module")
def prepared(tmp_path_factory):
    return prepare(tmp_path_factory.mktemp("e2e"))


def start(prepared, name, tmp_path, monkeypatch):
    monkeypatch.setenv("VIBE_LEDGER_HOME", str(tmp_path / "home"))
    monkeypatch.setenv("VIBE_LEDGER_OUT_DIR", str(tmp_path / "out"))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude-config"))
    f = prepared[name]
    assert vl.main(["start", "--project", str(f["project"]), "--claude-dir", str(f["claude_dir"]),
                    "--codex-dir", str(f["codex_dir"])]) == 0
    return f, vl.latest_run(f["project"])


@pytest.mark.parametrize("name", list(SCENARIOS))
def test_deterministic_half_matches_the_answer_key(prepared, name, tmp_path, monkeypatch, capsys):
    f, run = start(prepared, name, tmp_path, monkeypatch)
    want = load_json(ANSWERS / f"{name}.json")["deterministic"]
    found = load_json(run / "probes.json")
    cands = load_json(run / "candidates.json")
    manifest = load_json(run / "run.json")
    for exp in want["findings"]:
        assert any(x["probe"] == exp["probe"] and x["path"] == exp["path"] and x["level"] == exp["level"]
                   for x in found["findings"]), (exp, found["findings"])
    if want["no_certain_findings"]:
        assert not [x for x in found["findings"] if x["level"] == "certain"], found["findings"]
    hints = {h for c in cands["compromises"] for h in c["hints"]}
    if want["compromise_hints"]:
        assert set(want["compromise_hints"]) <= hints, hints
    else:
        assert hints == set(), hints
    assert len(cands["deferrals"]) >= want["min_deferrals"]
    assert len(cands["claims"]) >= want["min_claims"]
    assert found["stack"]["unsupported"] == want["unsupported"]
    assert manifest["lang"] == want["lang"]
    assert manifest["sessions"]["threads"] == 1
    assert manifest["sessions"]["by_agent"] == {f["agent"]: 1}
    assert FAKE_OPENAI not in (run / "digest.jsonl").read_text(encoding="utf-8")


def test_fabricated_ledger_draws_nothing_and_counts_nothing(prepared, tmp_path, monkeypatch, capsys):
    f, run = start(prepared, "notes-supabase", tmp_path, monkeypatch)
    user_msg = next(obj for _, obj in read_jsonl(run / "digest.jsonl") if obj and obj["role"] == "user")
    fake = {
        "evidence": {
            "R1": {"kind": "transcript", "session": user_msg["session"], "msg_id": user_msg["id"],
                   "quote": "只有我自己能看到我的笔记"},
            "F1": {"kind": "transcript", "session": user_msg["session"], "msg_id": user_msg["id"],
                   "quote": "我从来没说过这句话"},
            "F2": {"kind": "transcript", "session": "x", "msg_id": "not-a-real-id", "quote": "something said"},
            "FC": {"kind": "code", "path": "app/pay.ts", "line": 1, "snippet": "stripe.charges.create()"},
            "FS": {"kind": "code", "path": "app/api/summarize/route.ts", "line": 2, "snippet": "await requireAuth(req);"},
            "FP": {"kind": "probe", "finding_id": "made-up:finding:1"},
        },
        "promises": [
            {"id": "P1", "type": "user_requirement", "question": "who_can_see", "plain": "invented requirement",
             "source": ["F1"], "status": "broken", "verdict_plain": "v", "verdict_dev": "d", "evidence": ["FC"]},
            {"id": "P2", "type": "user_requirement", "question": "what_costs", "plain": "login is enforced",
             "source": ["R1"], "status": "kept", "verdict_plain": "v", "verdict_dev": "d", "evidence": ["FS"]},
            {"id": "P3", "type": "deferred", "question": "open_debts", "plain": "invented debt",
             "source": ["F2"], "status": "pending", "verdict_plain": "v", "verdict_dev": "d", "evidence": []},
            {"id": "P4", "type": "user_requirement", "question": "what_costs", "plain": "no charges",
             "source": ["R1"], "status": "broken", "verdict_plain": "v", "verdict_dev": "d", "evidence": ["FP", "FC"]},
        ],
        "compromises": [{"id": "C1", "error": "F2", "change": ["F1"], "bypassed": "made up", "still_present": True,
                         "now": ["FC"], "breaks": "P1"}],
        "map": {"nodes": [{"id": "stripe", "lane": "storage", "kind": "third_party", "label": "Stripe",
                           "holds": ["cards"], "paid": True, "evidence": ["FC"]}], "edges": []},
        "access": {"resources": [{"name": "payments", "required_by": "P4", "cells": {
            "anonymous": {"read": "deny", "write": "deny", "evidence": ["FC"]}}}]},
        "paths": [{"action": "Pay", "steps": [{"label": "charge", "evidence": "FC", "warning": None}]}],
    }
    (run / "ledger.json").write_text(json.dumps(fake, ensure_ascii=False), encoding="utf-8")
    (run / "explain.json").write_text(json.dumps({"evidence": {}, "files": {}}), encoding="utf-8")
    (run / "requirements.json").write_text(json.dumps({"evidence": {}, "requirements": []}), encoding="utf-8")
    assert vl.main(["check", "--project", str(f["project"])]) == 0
    out = load_json(run / "ledger.verified.json")
    assert {p["status"] for p in out["promises"]} == {"unknown"}
    assert {r["id"] for r in out["rejected"]} == {"P1", "P3", "C1"}
    assert out["map"]["nodes"] == [] and out["verification"]["evidence_ok"] == 1
    payments = next(r for r in out["access"]["resources"] if r["name"] == "payments")
    assert payments["cells"]["anonymous"]["read"] == "unknown"
    assert out["paths"][0]["steps"][0]["unverified"] is True
    assert vl.main(["render", "--project", str(f["project"])]) == 0
    html = (run / "report.html").read_text(encoding="utf-8")
    svgs = "".join(part.split("</svg>")[0] for part in html.split("<svg")[1:])
    assert "Stripe" not in svgs and "invented requirement" not in html.split("这份报告没看到什么")[0]
    assert FAKE_OPENAI not in html and render.find_secrets(html) == []


def test_score_passes_and_fails_as_expected():
    good = sample()
    answers = {"must_find": [{"label": "rls", "status": ["broken"], "paths_any": ["supabase/migrations"],
                              "text_any": ["rls"]}],
               "must_find_compromises": [{"label": "rls", "still_present": True, "text_any": ["rls"]}],
               "clean": False}
    assert all(ok for ok, _ in score(good, answers))
    assert not all(ok for ok, _ in score(good, {**answers, "clean": True}))
    missing = {**answers, "must_find": [{"label": "x", "status": ["broken"], "paths_any": ["nowhere"], "text_any": ["rls"]}]}
    assert not all(ok for ok, _ in score(good, missing))


@pytest.mark.parametrize("name", list(SCENARIOS))
def test_graph_matches_the_answer_key(prepared, name, tmp_path, monkeypatch, capsys):
    f, run = start(prepared, name, tmp_path, monkeypatch)
    results = score_graph(load_json(run / "graph.json"), load_json(ANSWERS / f"{name}.json")["graph"])
    assert all(ok for ok, _ in results), [label for ok, label in results if not ok]


def test_graph_and_explain_scores_fail_as_expected():
    g = {"nodes": [{"id": "a.ts", "explain": True}, {"id": "b.ts", "explain": False}], "externals": [{"id": "ext:openai"}],
         "entries": [{"path": "a.ts"}], "edges": [{"from": "a.ts", "to": "ext:openai"}]}
    want = {"nodes": ["a.ts", "b.ts"], "entries": ["a.ts"], "externals": ["ext:openai"], "edges": [["a.ts", "ext:openai"]]}
    assert all(ok for ok, _ in score_graph(g, want))
    assert not all(ok for ok, _ in score_graph(g, {**want, "edges": [["b.ts", "a.ts"]]}))
    assert not all(ok for ok, _ in score_graph(g, {**want, "entries": ["b.ts"]}))
    explained = {"files": {"a.ts": {"purpose_plain": "把文字发给 OpenAI 总结", "purpose_dev": ""}}, "rejected": [],
                 "verification": {"functions_dropped": 0, "unverified_purposes": 0}}
    keys = [{"path": "a.ts", "label": "calls OpenAI", "text_any": ["openai"]}]
    assert all(ok for ok, _ in score_explain(explained, g, keys))
    assert not all(ok for ok, _ in score_explain({**explained, "files": {}}, g, keys))
    dropped = {**explained, "verification": {"functions_dropped": 1, "unverified_purposes": 0}}
    assert not all(ok for ok, _ in score_explain(dropped, g, keys))
    rejected = {**explained, "rejected": [{"path": "zzz.ts", "reason": "not a file in the graph"}]}
    assert not all(ok for ok, _ in score_explain(rejected, g, keys))
