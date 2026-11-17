#!/usr/bin/env python3
"""Tests for vet_translator.py — run: python3 scripts/test_vet_translator.py"""
import importlib.util
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("vt", os.path.join(HERE, "vet_translator.py"))
vt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vt)

PASS, FAIL = 0, 0


def check(name, cond, extra=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ok  {name}")
    else:
        FAIL += 1
        print(f" FAIL {name} {extra}")


# ── Marker evaluation ────────────────────────────────────────────────────────
print("marker evaluation:")
e = vt.evaluate_marker("CREA", 2.8, "cat")
check("cat CREA 2.8 is HIGH", e["verdict"] == "HIGH", e["verdict"])
e = vt.evaluate_marker("CREA", 1.2, "dog")
check("dog CREA 1.2 is NORMAL", e["verdict"] == "NORMAL", e["verdict"])
e = vt.evaluate_marker("CREA", 2.8, "dog")
check("dog CREA 2.8 is HIGH (stricter than cat)", e["verdict"] == "HIGH", e["verdict"])
e = vt.evaluate_marker("SDMA", 28, "cat")
check("SDMA 28 cat is HIGH", e["verdict"] == "HIGH", e["verdict"])
e = vt.evaluate_marker("SDMA", 10, "cat")
check("SDMA 10 cat is NORMAL", e["verdict"] == "NORMAL", e["verdict"])
e = vt.evaluate_marker("ALT", 92, "cat")
check("ALT 92 flagged borderline", e["verdict"].startswith("BORDERLINE"), e["verdict"])
e = vt.evaluate_marker("PLT", 118, "dog", breed="greyhound")
check("greyhound PLT 118 breed-adjusted NORMAL", e["verdict"] == "NORMAL (breed-adjusted)", e["verdict"])
e = vt.evaluate_marker("CREA", 1.7, "dog", breed="greyhound")
check("greyhound CREA 1.7 NORMAL (adjusted range)", e["verdict"] == "NORMAL (breed-adjusted)", e["verdict"])
e = vt.evaluate_marker("PLT", 118, "dog", breed="beagle")
check("beagle PLT 118 stays LOW", e["verdict"] == "LOW", e["verdict"])
e = vt.evaluate_marker("T4", 8.2, "cat")
check("cat T4 8.2 HIGH (hyperthyroid pattern)", e["verdict"] == "HIGH", e["verdict"])

# importance sorting: SDMA/CREA/T4 above BUN
w = vt.WEIGHTS
check("SDMA outranks BUN", w["SDMA"] > w["BUN"])
check("T4 outranks default-weight markers", w["T4"] > vt.WEIGHTS.get("ALT", 1))

# ── Parsing ──────────────────────────────────────────────────────────────────
print("parsing:")
r = vt.parse_results("BUN 38, CREA 2.8, SDMA 28")
check("3 markers parsed", len(r) == 3, str(r))
r = vt.parse_results("crea: 1.5 glu 90 = alk 200")
check("lowercase + separators parsed", len(r) >= 2, str(r))
s = vt.parse_series("2024-01:10,2024-07:14")
check("series parsed", s == [("2024-01", 10.0), ("2024-07", 14.0)], str(s))

# ── Trend ────────────────────────────────────────────────────────────────────
print("trend:")
t = vt.trend_analysis("SDMA", [("a", 10), ("b", 14), ("c", 19)], "cat")
check("rising detected", t["direction"] == "rising")
check("deltas computed", t["deltas"] == [4.0, 5.0])
t = vt.trend_analysis("CREA", [("a", 2.0), ("b", 1.8), ("c", 1.6)], "dog")
check("falling detected", t["direction"] == "falling")
t = vt.trend_analysis("CREA", [("a", 1.0), ("b", 1.2), ("c", 1.5)], "cat")
check("drift alert on in-range rise (50%)", t["drift_alert"] is True and t["last_in_range"] is True)
t = vt.trend_analysis("CREA", [("a", 1.0), ("b", 1.05), ("c", 1.1)], "cat")
check("no drift alert on small wiggle", t["drift_alert"] is False)

# ── IRIS staging ─────────────────────────────────────────────────────────────
print("IRIS staging:")
s = vt.iris_stage("cat", 1.2)
check("cat CREA 1.2 = STAGE1", s["stage"] == "STAGE1", s["stage"])
s = vt.iris_stage("cat", 2.0)
check("cat CREA 2.0 = STAGE2", s["stage"] == "STAGE2", s["stage"])
s = vt.iris_stage("cat", 2.8)
check("cat CREA 2.8 = STAGE3", s["stage"] == "STAGE3", s["stage"])
s = vt.iris_stage("dog", 1.8)
check("dog CREA 1.8 = STAGE2 (dog thresholds stricter)", s["stage"] == "STAGE2", s["stage"])
s = vt.iris_stage("dog", 2.8)
check("dog CREA 2.8 = STAGE3", s["stage"] == "STAGE3", s["stage"])
s = vt.iris_stage("cat", 6.0)
check("cat CREA 6.0 = STAGE4", s["stage"] == "STAGE4", s["stage"])
s = vt.iris_stage("cat", 2.0, upc=0.6)
check("UPC 0.6 cat = proteinuric", s["substages"][0][1] == "proteinuric")
s = vt.iris_stage("cat", 2.0, bp=170)
check("BP 170 = hypertensive", s["substages"][0][1] == "hypertensive")

# ── Abbreviation decode ──────────────────────────────────────────────────────
print("abbreviations:")
d = vt.explain_text("MC cat Hx weight loss, r/o CKD, recheck in 4 wks")
words = [x[1] for x in d]
check("MC decoded", "male castrated" in words)
check("Hx decoded", "history" in words)
check("r/o decoded", "rule out" in words)
check("CKD decoded", "chronic kidney disease" in words)

# ── CLI ──────────────────────────────────────────────────────────────────────
print("cli:")
r = subprocess.run([sys.executable, os.path.join(HERE, "vet_translator.py"),
                    "labs", "--species", "cat", "--results", "CREA 2.4, SDMA 22"],
                   capture_output=True, text=True)
check("labs cmd exits 0", r.returncode == 0, r.stderr)
check("labs flags CREA 2.4 HIGH", "CREA" in r.stdout and "HIGH" in r.stdout)
check("labs includes disclaimer", "veterinarian" in r.stdout)

r = subprocess.run([sys.executable, os.path.join(HERE, "vet_translator.py"),
                    "ckd", "--species", "cat", "--crea", "2.4", "--sdma", "22"],
                   capture_output=True, text=True)
check("ckd cmd exits 0", r.returncode == 0, r.stderr)
check("ckd shows stage", "STAGE2" in r.stdout)
check("ckd generates questions", "Questions for your vet" in r.stdout)

r = subprocess.run([sys.executable, os.path.join(HERE, "vet_translator.py"), "demo"],
                   capture_output=True, text=True)
check("demo runs clean", r.returncode == 0 and "DEMO 4" in r.stdout)

print(f"\n{PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
