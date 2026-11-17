import pytest

import ledger
import verify

MIGRATION = "create table notes (id uuid);\n\nalter table notes disable row level security;\n"
INDEX = {
    "m1": {"id": "m1", "session": "s1", "ts": "2026-09-12T09:01:00Z", "role": "user", "kind": "text",
           "text": "只有我自己能看到我的笔记"},
    "m2": {"id": "m2", "session": "s1", "ts": "2026-09-12T09:05:00Z", "role": "tool", "kind": "error",
           "text": "new row violates row-level security policy"},
    "m3": {"id": "m3", "session": "s1", "ts": "2026-09-12T09:06:00Z", "role": "assistant", "kind": "edit",
           "text": "EDIT supabase/migrations/001.sql\n+++ after\nalter table notes disable row level security;"},
}
FINDING = {"id": "supabase_rls:supabase/migrations/001.sql:3", "probe": "supabase_rls", "level": "certain",
           "path": "supabase/migrations/001.sql", "line": 3,
           "snippet": "alter table notes disable row level security;", "message": "RLS is off for notes",
           "implies": [{"resource": "notes", "subject": "anonymous", "perm": "read", "value": "allow"},
                       {"resource": "notes", "subject": "anonymous", "perm": "write", "value": "allow"},
                       {"resource": "orders", "subject": "anonymous", "perm": "read", "value": "allow"}]}
PROBES = {"findings": [FINDING], "ran": ["supabase_rls"], "skipped": [], "stack": {}}


@pytest.fixture
def root(tmp_path):
    p = tmp_path / "supabase" / "migrations" / "001.sql"
    p.parent.mkdir(parents=True)
    p.write_text(MIGRATION, encoding="utf-8")
    return tmp_path


def base():
    return {
        "evidence": {
            "E1": {"kind": "transcript", "session": "s1", "msg_id": "m1", "quote": "只有我自己能看到我的笔记"},
            "E2": {"kind": "code", "path": "supabase/migrations/001.sql", "line": 3,
                   "snippet": "alter table notes disable row level security;"},
            "E3": {"kind": "probe", "finding_id": FINDING["id"]},
            "E4": {"kind": "transcript", "session": "s1", "msg_id": "m2", "quote": "violates row-level security"},
            "E5": {"kind": "transcript", "session": "s1", "msg_id": "m3", "quote": "disable row level security"},
            "FAKE_Q": {"kind": "transcript", "session": "s1", "msg_id": "m1", "quote": "我从来没说过这句话"},
            "FAKE_C": {"kind": "code", "path": "app/pay.ts", "line": 1, "snippet": "stripe.charge()"},
        },
        "promises": [
            {"id": "P1", "type": "user_requirement", "question": "who_can_see", "plain": "只有我能看到",
             "source": ["E1"], "status": "broken", "verdict_plain": "v", "verdict_dev": "d", "evidence": ["E2", "E3"]},
            {"id": "P2", "type": "user_requirement", "question": "what_costs", "plain": "made up",
             "source": ["FAKE_Q"], "status": "broken", "verdict_plain": "v", "verdict_dev": "d", "evidence": ["E2"]},
            {"id": "P3", "type": "deferred", "question": "what_costs", "plain": "claimed",
             "source": ["E1"], "status": "kept", "verdict_plain": "v", "verdict_dev": "d", "evidence": ["FAKE_C"]},
        ],
        "compromises": [
            {"id": "C1", "error": "E4", "change": ["E5"], "bypassed": "rls", "still_present": True,
             "now": ["E2"], "breaks": "P1"},
            {"id": "C2", "error": "E4", "change": ["E5"], "bypassed": "cors", "still_present": True,
             "now": ["FAKE_C"], "breaks": "P2"},
            {"id": "C3", "error": "FAKE_Q", "change": ["E5"], "bypassed": "x", "still_present": False,
             "now": [], "breaks": None},
        ],
        "map": {"nodes": [{"id": "db", "lane": "storage", "kind": "database", "label": "Supabase",
                           "holds": ["notes"], "paid": False, "evidence": ["E2"]},
                          {"id": "stripe", "lane": "storage", "kind": "third_party", "label": "Stripe",
                           "holds": [], "paid": True, "evidence": ["FAKE_C"]},
                          {"id": "web", "lane": "browser", "kind": "page", "label": "Home", "holds": [],
                           "paid": False, "evidence": ["E3"]}],
                "edges": [{"from": "web", "to": "db", "carries": "notes", "risk": None, "evidence": ["E2"]},
                          {"from": "web", "to": "stripe", "carries": "card", "risk": None, "evidence": ["E2"]}]},
        "access": {"resources": [{"name": "notes", "required_by": "P1", "cells": {
            "anonymous": {"read": "deny", "write": "unknown", "evidence": ["E2"]},
            "owner": {"read": "allow", "write": "allow", "evidence": ["FAKE_C"]}}}]},
        "paths": [{"action": "Save", "steps": [{"label": "insert", "evidence": "E2", "warning": None},
                                               {"label": "charge", "evidence": "FAKE_C", "warning": None}]}],
    }


def run(root, led=None):
    return verify.verify_ledger(led or base(), INDEX, root, PROBES)


def test_evidence_gets_ok_flags(root):
    out = run(root)
    ev = out["evidence"]
    assert ev["E1"]["ok"] and ev["E1"]["ts"] == "2026-09-12T09:01:00Z"
    assert ev["E3"]["ok"] and ev["E3"]["message"] == "RLS is off for notes"
    assert not ev["FAKE_Q"]["ok"] and not ev["FAKE_C"]["ok"]


def test_promises_rejected_downgraded_or_kept(root):
    out = run(root)
    ids = {p["id"]: p for p in out["promises"]}
    assert set(ids) == {"P1", "P3"}
    assert ids["P1"]["status"] == "broken"
    assert ids["P3"]["status"] == "unknown" and ids["P3"]["downgraded_from"] == "kept"
    assert [r["id"] for r in out["rejected"] if r["id"].startswith("P")] == ["P2"]


def test_compromises(root):
    out = run(root)
    comps = {c["id"]: c for c in out["compromises"]}
    assert comps["C1"]["still_present"] is True and comps["C1"]["breaks"] == "P1"
    assert comps["C2"]["still_present"] is None and comps["C2"]["breaks"] is None
    assert "C3" not in comps and any(r["id"] == "C3" for r in out["rejected"])


def test_map_draws_only_verified(root):
    m = run(root)["map"]
    assert [n["id"] for n in m["nodes"]] == ["db", "web"]
    assert [n["id"] for n in m["unverified_nodes"]] == ["stripe"]
    assert [(e["from"], e["to"]) for e in m["edges"]] == [("web", "db")]
    assert [(e["from"], e["to"]) for e in m["unverified_edges"]] == [("web", "stripe")]


def test_access_unknown_cells_probe_fill_and_conflicts(root):
    res = {r["name"]: r for r in run(root)["access"]["resources"]}
    notes = res["notes"]["cells"]
    assert notes["owner"]["read"] == "unknown" and notes["owner"]["claimed"] == {"read": "allow", "write": "allow"}
    assert notes["anonymous"]["read"] == "deny"
    assert notes["anonymous"]["conflicts"][0]["probe_says"] == "allow"
    assert notes["anonymous"]["write"] == "allow" and notes["anonymous"]["from_probe"] == [FINDING["id"]]
    assert res["orders"]["added_by_probe"] is True and res["orders"]["cells"]["anonymous"]["read"] == "allow"


def test_star_resource_added_only_when_ledger_has_none(root):
    probes = {"findings": [{**FINDING, "id": "fb", "path": "supabase/migrations/001.sql",
                            "implies": [{"resource": "*", "subject": "anonymous", "perm": "read", "value": "allow"}]}]}
    led = base()
    led["access"] = {"resources": []}
    out = verify.verify_ledger(led, INDEX, root, probes)
    assert [r["name"] for r in out["access"]["resources"]] == ["*"]
    out2 = verify.verify_ledger(base(), INDEX, root, probes)
    assert [r["name"] for r in out2["access"]["resources"]] == ["notes"]
    assert out2["access"]["resources"][0]["cells"]["anonymous"]["conflicts"]


def test_paths_mark_unverified_steps(root):
    steps = run(root)["paths"][0]["steps"]
    assert [s["unverified"] for s in steps] == [False, True]


def test_summary_counts_and_lines(root):
    out = run(root)
    v = out["verification"]
    assert v["evidence_total"] == 7 and v["evidence_ok"] == 5
    assert v["downgraded"] == 1 and v["rejected"] == 2 and v["nodes_unverified"] == 1 and v["conflicts"] == 1
    text = "\n".join(verify.summary_lines(out))
    assert "FAKE_C" in text and "file not found" in text


def test_format_error_raises(root):
    led = base()
    led["promises"][0]["status"] = "maybe"
    with pytest.raises(ledger.LedgerError):
        run(root, led)


def test_input_is_not_mutated(root):
    led = base()
    run(root, led)
    assert "ok" not in led["evidence"]["E1"]


def test_sources_must_come_from_the_right_speaker(root):
    led = base()
    led["promises"].append({"id": "P8", "type": "user_requirement", "question": "who_can_see", "plain": "x",
                            "source": ["E4"], "status": "unknown", "verdict_plain": "v", "verdict_dev": "d",
                            "evidence": []})
    led["promises"].append({"id": "P9", "type": "ai_claim", "question": "who_can_see", "plain": "y",
                            "source": ["E1"], "status": "unknown", "verdict_plain": "v", "verdict_dev": "d",
                            "evidence": []})
    out = run(root, led)
    reasons = {r["id"]: r["reason"] for r in out["rejected"]}
    assert "user" in reasons["P8"] and "AI" in reasons["P9"]


def test_stale_probe_findings_do_not_fill_cells(root):
    stale = {**FINDING, "id": "stale", "snippet": "alter table ghost disable row level security;",
             "implies": [{"resource": "ghost", "subject": "anonymous", "perm": "read", "value": "allow"}]}
    out = verify.verify_ledger(base(), INDEX, root, {"findings": [FINDING, stale]})
    assert "ghost" not in {r["name"] for r in out["access"]["resources"]}


def test_map_keeps_its_lane_labels(root):
    led = base()
    led["map"]["lane_labels"] = {"server": "本机处理"}
    assert run(root, led)["map"]["lane_labels"] == {"server": "本机处理"}
    assert run(root)["map"]["lane_labels"] == {}
