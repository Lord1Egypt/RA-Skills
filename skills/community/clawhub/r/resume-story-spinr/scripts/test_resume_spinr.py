#!/usr/bin/env python3
"""Offline smoke tests for resume_spinr.py — stdlib only."""
import importlib.util
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
SCRIPT = HERE / "resume_spinr.py"

spec = importlib.util.spec_from_file_location("rs", SCRIPT)
rs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rs)

passed = failed = 0


def ok(name, cond):
    global passed, failed
    if cond:
        passed += 1
        print(f"  ok  {name}")
    else:
        failed += 1
        print(f"FAIL  {name}")


def run(args):
    return subprocess.run([sys.executable, str(SCRIPT)] + args,
                          capture_output=True, text=True)


# ── weak opener replacement ──────────────────────────────────────────────
t, ch = rs.strengthen_opener("Responsible for the payments API")
ok("'Responsible for' → 'Owned'", ch and t.startswith("Owned the"))

t, ch = rs.strengthen_opener("Helped with migration of services")
ok("'Helped with' → 'Drove'", ch and t.startswith("Drove migration"))

t, ch = rs.strengthen_opener("Worked on improving test coverage")
ok("gerund fix: 'improving' → 'Improved'", ch and t == "Improved test coverage")

t, ch = rs.strengthen_opener("Owned the API from day one")
ok("already-strong bullet untouched", not ch and t.startswith("Owned"))

# no space bugs
t, ch = rs.strengthen_opener("Responsible for API")
ok("space preserved after verb", ch and t == "Owned API")

# ── quantification detector ──────────────────────────────────────────────
for s in ["cut p99 latency 38%", "deploy 40min to 6min", "2.1M requests/day",
          "saved $12,000", "mentors 3 engineers", "reduced errors by 50 percent"]:
    ok(f"metric detected: {s!r}", rs.has_metrics(s))
for s in ["Owned the payments API", "Improved reliability", "Led the team"]:
    ok(f"no false metric: {s!r}", not rs.has_metrics(s))

# ── STAR decomposition ───────────────────────────────────────────────────
star = rs.bullet_to_star(
    "Led migration of 14 services; cut deploy time from 40min to 6min")
ok("action extracted", star["a"].startswith("Led migration"))
ok("result extracted", "cut deploy time" in (star["r"] or ""))
ok("quantified bullet flagged", star["quantified"])

star2 = rs.bullet_to_star("Responsible for the payments API")
ok("unquantified flagged", not star2["quantified"])
ok("metric hints offered", len(star2.get("metric_hints", [])) >= 1)

# ── follow-up questions ──────────────────────────────────────────────────
qs = rs.followup_questions(star)
ok("quantified bullets get 'how measured'", any("measure" in q for q in qs))
ok("contribution question always present",
   any("YOUR specific" in q for q in qs))

# ── render ───────────────────────────────────────────────────────────────
out = rs.render_star(star, "resume")
ok("resume render has action and result", "Led migration" in out and "40min" in out)
story = rs.render_star(star2, "story")
ok("story render has S/T/A/R lines", all(f"{k}:" in story for k in "STAR"))

# ── ATS scoring ──────────────────────────────────────────────────────────
resume = """Senior Backend Engineer
- Owned payments API serving 2.1M requests/day
- Led migration of 14 services to Kubernetes
- Cut p99 latency 38% via request batching
- Mentor 3 junior engineers, run on-call"""
job_match = """Backend engineer with Kubernetes, payments API experience,
on-call rotation, mentoring junior engineers."""
job_miss = """Looking for: React, Figma, marketing, SEO, copywriting."""
rep = rs.ats_score(resume, job_match)
ok("well-matched JD scores high", rep["match_score"] >= 60)
rep2 = rs.ats_score(resume, job_miss)
ok("mismatched JD scores low", rep2["match_score"] < 40)
ok("missing terms listed", "react" in rep2["missing"])
ok("weak openers counted", rs.ats_score(
    "Responsible for things\nWorked on stuff", job_match)["bullets_analyzed"] == 2)

# ── CLI ──────────────────────────────────────────────────────────────────
r = run(["transform", "--bullets", "Responsible for the payments API\nHelped with tests"])
ok("transform cmd exits 0", r.returncode == 0)
ok("transform shows BEFORE/AFTER", "BEFORE" in r.stdout and "AFTER" in r.stdout)

r = run(["interview", "--bullet",
         "Led migration of 14 services; cut deploy time 40min to 6min"])
ok("interview cmd exits 0", r.returncode == 0)
ok("interview prints STAR", "S:" in r.stdout and "R:" in r.stdout)
ok("interview prints follow-ups", "?" in r.stdout)

import tempfile, os
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
    f.write(resume); rf = f.name
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
    f.write(job_match); jf = f.name
r = run(["ats", "--resume", rf, "--job", jf])
ok("ats cmd exits 0", r.returncode == 0)
ok("ats prints coverage", "Keyword coverage" in r.stdout)
os.unlink(rf); os.unlink(jf)

r = run(["demo"])
ok("demo runs clean", r.returncode == 0 and len(r.stdout) > 300)

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
