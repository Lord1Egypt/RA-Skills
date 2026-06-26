#!/usr/bin/env python3
"""test.py for smart-router-intents v1.0.1"""
import json, sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent

def test_skill_md_exists():
    assert (SKILL_DIR / "SKILL.md").exists()
    print("✅ SKILL.md exists")

def test_meta_json():
    with open(SKILL_DIR / "_meta.json") as f:
        m = json.load(f)
    assert m["slug"] == "smart-router-intents"
    print(f"✅ _meta.json: {m['slug']}")

def test_skill_json():
    with open(SKILL_DIR / "skill.json") as f:
        j = json.load(f)
    assert "name" in j
    print(f"✅ skill.json: {j['name']}")

def test_intent_detection():
    sys.path.insert(0, str(SKILL_DIR / "scripts"))
    from smart_router_intents import route
    r = route("write a function in python")
    assert r["intent"] == "code", f"Expected code, got {r['intent']}"
    r = route("explain how blockchain works")
    assert r["intent"] == "analysis", f"Expected analysis, got {r['intent']}"
    r = route("write a story about a robot")
    assert r["intent"] == "creative", f"Expected creative, got {r['intent']}"
    r = route("what is the price of bitcoin today")
    assert r["intent"] == "realtime", f"Expected realtime, got {r['intent']}"
    r = route("hi how are you")
    assert r["intent"] == "general", f"Expected general, got {r['intent']}"
    assert all(k in r for k in ["intent","tier","model","cost_per_query","latency","reasoning"])
    print("✅ Intent detection classifies correctly (5/5)")

if __name__ == "__main__":
    tests = [test_skill_md_exists, test_meta_json, test_skill_json, test_intent_detection]
    for t in tests:
        t()
    print("\n✅ All tests passed")