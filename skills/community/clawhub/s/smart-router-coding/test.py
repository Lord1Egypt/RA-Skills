"""Tests for smart-router-coding v1.2.0"""
import sys, json
sys.path.insert(0, "scripts")
from smart_router_coding import route, MODELS

def test_simple_query():
    r = route("how to print hello world in python")
    assert r["tier"] == "fast", f"Expected fast, got {r['tier']}"
    assert r["model"] == "DeepSeek V4 Flash"
    assert r["cost_per_query"] == MODELS["fast"]["cost"]
    print(f"✅ Simple query → {r['model']}")

def test_complex_query():
    r = route("design a distributed system architecture")
    assert r["tier"] == "deep", f"Expected deep, got {r['tier']}"
    assert r["model"] == "Kimi K2.7 Code"
    assert r["cost_per_query"] == MODELS["deep"]["cost"]
    print(f"✅ Complex query → {r['model']}")

def test_standard_query():
    r = route("review my pull request for bugs")
    assert r["tier"] == "standard", f"Expected standard, got {r['tier']}"
    assert r["model"] == "DeepSeek V4 Flash"
    assert r["cost_per_query"] == MODELS["standard"]["cost"]
    print(f"✅ Standard query → {r['model']}")

def test_empty_query():
    r = route("")
    assert r["tier"] == "standard"
    print(f"✅ Empty query → {r['model']} (default)")

def test_security_audit():
    r = route("audit this codebase for sql injection vulnerabilities")
    assert r["tier"] == "deep", f"Expected deep, got {r['tier']}"
    assert r["model"] == "Kimi K2.7 Code"
    print(f"✅ Security audit → {r['model']}")

def test_optimization():
    r = route("optimize this database query for speed")
    assert r["tier"] == "deep", f"Expected deep, got {r['tier']}"
    print(f"✅ Optimization query → {r['model']}")

if __name__ == "__main__":
    test_simple_query()
    test_complex_query()
    test_standard_query()
    test_empty_query()
    test_security_audit()
    test_optimization()
    print("\n✅ All tests passed")