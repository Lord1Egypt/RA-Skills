import copy

import pytest

import ledger


def minimal():
    return {
        "evidence": {
            "E1": {"kind": "transcript", "session": "s1", "msg_id": "m1", "quote": "只有我自己能看到账目"},
            "E2": {"kind": "code", "path": "supabase/migrations/001.sql", "line": 6,
                   "snippet": "alter table notes disable row level security;"},
            "E3": {"kind": "probe", "finding_id": "supabase_rls:supabase/migrations/001.sql:6"},
            "E4": {"kind": "transcript", "session": "s1", "msg_id": "m2", "quote": "new row violates"},
            "E5": {"kind": "transcript", "session": "s1", "msg_id": "m3", "quote": "disable row level security"},
        },
        "promises": [{"id": "P1", "type": "user_requirement", "question": "who_can_see",
                      "plain": "只有我自己能看到账目", "source": ["E1"], "status": "broken",
                      "verdict_plain": "前门锁了，后窗开着", "verdict_dev": "RLS disabled on notes",
                      "evidence": ["E2", "E3"], "fix_prompt": "Re-enable RLS on notes and add an owner policy."}],
        "compromises": [{"id": "C1", "error": "E4", "change": ["E5"], "bypassed": "rls",
                         "still_present": True, "now": ["E2"], "breaks": "P1"}],
        "map": {"nodes": [{"id": "db", "lane": "storage", "kind": "database", "label": "Supabase",
                           "holds": ["notes"], "paid": False, "evidence": ["E2"]},
                          {"id": "web", "lane": "browser", "kind": "page", "label": "Home page",
                           "holds": [], "paid": False, "evidence": ["E2"]}],
                "edges": [{"from": "web", "to": "db", "carries": "notes", "risk": "anyone can read",
                           "evidence": ["E3"]}]},
        "access": {"resources": [{"name": "notes", "required_by": "P1", "cells": {
            "anonymous": {"read": "allow", "write": "allow", "evidence": ["E3"]},
            "owner": {"read": "allow", "write": "allow", "evidence": ["E2"]}}}]},
        "paths": [{"action": "Save a note", "steps": [{"label": "supabase.insert()", "evidence": "E2", "warning": None}]}],
    }


def test_minimal_ledger_is_valid():
    ledger.validate(minimal())


def test_optional_sections_may_be_missing():
    led = minimal()
    for key in ("map", "access", "paths", "compromises"):
        del led[key]
    led["promises"][0]["status"] = "unknown"
    ledger.validate(led)
    norm = ledger.normalise(led)
    assert norm["map"] == {"nodes": [], "edges": []} and norm["paths"] == [] and norm["compromises"] == []


@pytest.mark.parametrize("mutate, needle", [
    (lambda L: L["promises"][0].update(status="maybe"), "status"),
    (lambda L: L["promises"][0].update(type="wish"), "type"),
    (lambda L: L["promises"][0].update(question="vibes"), "question"),
    (lambda L: L["promises"][0].update(status="pending"), "pending is only for type deferred"),
    (lambda L: L["promises"][0].update(source=[]), "source must list"),
    (lambda L: L["promises"][0].update(source=["E2"]), "must be transcript"),
    (lambda L: L["promises"][0].update(evidence=["E99"]), "unknown evidence id E99"),
    (lambda L: L["promises"][0].pop("verdict_plain"), "missing verdict_plain"),
    (lambda L: L["promises"].append(copy.deepcopy(L["promises"][0])), "duplicated"),
    (lambda L: L["evidence"]["E2"].update(line="6"), "line must be an integer"),
    (lambda L: L["evidence"]["E1"].pop("quote"), "missing quote"),
    (lambda L: L["evidence"].update(E9={"kind": "rumour"}), "kind must be one of"),
    (lambda L: L["compromises"][0].update(breaks="P9"), "breaks"),
    (lambda L: L["compromises"][0].update(still_present="yes"), "still_present"),
    (lambda L: L["compromises"][0].update(now=["E1"]), "must be code or probe"),
    (lambda L: L["map"]["nodes"][0].update(lane="cloud"), "lane"),
    (lambda L: L["map"]["edges"][0].update(to="nowhere"), "unknown node"),
    (lambda L: L["access"]["resources"][0]["cells"].update(admin={"read": "allow", "write": "deny", "evidence": []}), "subject"),
    (lambda L: L["access"]["resources"][0]["cells"]["owner"].update(read="yes"), "read"),
    (lambda L: L["paths"][0]["steps"][0].update(evidence=["E2"]), "one evidence id"),
    (lambda L: L["map"].update(lane_labels={"cloud": "x"}), "lane_labels"),
    (lambda L: L["map"].update(lane_labels={"browser": ""}), "lane_labels"),
])
def test_each_problem_is_reported(mutate, needle):
    led = minimal()
    mutate(led)
    with pytest.raises(ledger.LedgerError) as exc:
        ledger.validate(led)
    assert any(needle in p for p in exc.value.problems), exc.value.problems


def test_all_problems_are_listed_at_once():
    led = minimal()
    led["promises"][0]["status"] = "maybe"
    led["map"]["nodes"][0]["lane"] = "cloud"
    with pytest.raises(ledger.LedgerError) as exc:
        ledger.validate(led)
    assert len(exc.value.problems) >= 2


def test_not_an_object():
    with pytest.raises(ledger.LedgerError):
        ledger.validate([])


def part(n_quote="只有我自己能看到账目", status="broken"):
    return {"evidence": {"E1": {"kind": "transcript", "session": "s", "msg_id": "m1", "quote": n_quote},
                         "E2": {"kind": "code", "path": "a.sql", "line": 1, "snippet": "x"}},
            "promises": [{"id": "P1", "type": "user_requirement", "question": "who_can_see", "plain": "p",
                          "source": ["E1"], "status": status, "verdict_plain": "v", "verdict_dev": "d",
                          "evidence": ["E2"]}],
            "compromises": []}


def test_merge_prefixes_ids_and_keeps_distinct_promises():
    out = ledger.merge([part("quote one"), part("quote two")])
    assert [p["id"] for p in out["promises"]] == ["p1_P1", "p2_P1"]
    assert set(out["evidence"]) == {"p1_E1", "p1_E2", "p2_E1", "p2_E2"}
    assert out["promises"][1]["source"] == ["p2_E1"]
    ledger.validate(out)


def test_merge_drops_exact_duplicates_and_flags_conflicts():
    same = ledger.merge([part(), part()])
    assert len(same["promises"]) == 1
    clash = ledger.merge([part(status="broken"), part(status="kept")])
    assert len(clash["promises"]) == 2
    assert clash["promises"][0]["conflict_with"] == ["p2_P1"]
    assert clash["promises"][1]["conflict_with"] == ["p1_P1"]


def test_merge_remaps_compromise_breaks_to_the_kept_duplicate():
    a, b = part(), part()
    b["evidence"]["E3"] = {"kind": "transcript", "session": "s", "msg_id": "m2", "quote": "error text"}
    b["compromises"] = [{"id": "C1", "error": "E3", "change": ["E1"], "bypassed": "rls",
                         "still_present": True, "now": ["E2"], "breaks": "P1"}]
    out = ledger.merge([a, b])
    assert out["compromises"][0]["breaks"] == "p1_P1" and out["compromises"][0]["id"] == "p2_C1"


def test_merge_rejects_code_sections_in_parts():
    p = part()
    p["map"] = {"nodes": [{"id": "x"}], "edges": []}
    with pytest.raises(ledger.LedgerError) as exc:
        ledger.merge([p])
    assert any("map/access/paths" in s for s in exc.value.problems)


def test_a_path_without_action_is_named_by_position():
    led = minimal()
    led["paths"].append({"label": "Summarize", "steps": []})
    with pytest.raises(ledger.LedgerError) as exc:
        ledger.validate(led)
    assert any(p.startswith("path #2: missing action") for p in exc.value.problems), exc.value.problems


def test_lane_labels_are_optional_and_accepted():
    led = minimal()
    led["map"]["lane_labels"] = {"browser": "你运行的脚本", "server": "本机处理"}
    ledger.validate(led)
