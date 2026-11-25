#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Red-team a skill reviewer: score two fake packages, fail if the reviewer is fooled.

How the verdict is decided (this took two experiments to get right):

  · shape   (runner prints PASS with zero assertions; demo prints one line)
      → must land BELOW the pass line, and must LOSE reproducible points.
  · vacuity (formally complete, content empty: 若-table, ten NEVER...因为 rules, stub refs)
      → its TOTAL may legitimately pass, because a structure score only sees shape.
        What must happen is that it LOSES reproducible points too.

Why not judge by total score alone: a well-shaped fake reaches 88–92/100 on our own
ruler even after two patches. Total is a shape score. The reproducible dimension is where
"this package verifies nothing" actually shows up, so that is what the suite asserts.

Measured (lgd-skill-review v1.1.16 vs a copy with its three anti-gaming checks disabled):

    reviewer        shape                 vacuity
    v1.1.16       78 WARN  repro 11/20    88 PASS  repro 16/20   → both blocked
    weakened      87 PASS  repro 20/20    92 PASS  repro 20/20   → both get through

Run: python run_suite.py --reviewer /path/to/review.py [--threshold 80]
Exit 0 = no probe got through; 1 = at least one did.
"""
import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
PROBES = os.path.join(HERE, "probes")
PROBES_ZIP = os.path.join(HERE, "probes.zip")
PROBES_JSON = os.path.join(HERE, "probes.json")
PROBES_JSON = os.path.join(HERE, "probes.json")
PROBES_JSON = os.path.join(HERE, "probes.json")
PROBES_JSON = os.path.join(HERE, "probes.json")
PROBES_JSON = os.path.join(HERE, "probes.json")


def probe_root():
    """优先用目录（开发态）；没有目录就用 probes.zip（分发态）。

    为什么要 zip：假包不能作为可安装目录跟着技能一起发出去，那等于往公共索引里
    塞故意坏掉的包。压缩成夹具，只有 runner 解到临时目录里用。
    """
    if os.path.isdir(PROBES):
        return PROBES, None
    if os.path.exists(PROBES_ZIP):
        d = tempfile.mkdtemp(prefix="redteam-fixtures-")
        with zipfile.ZipFile(PROBES_ZIP) as z:
            z.extractall(d)
        return d, d
    if os.path.exists(PROBES_JSON):
        d = tempfile.mkdtemp(prefix="redteam-fixtures-")
        with io.open(PROBES_JSON, encoding="utf-8") as f:
            doc = json.load(f)
        for it in doc.get("files", []):
            full = os.path.join(d, it["path"].replace("/", os.sep))
            os.makedirs(os.path.dirname(full), exist_ok=True)
            io.open(full, "w", encoding="utf-8", newline="\n").write(it.get("text") or "")
        return d, d
    return None, None

PROBE_RULES = {
    # name: (must be below the pass line, must lose reproducible points)
    "shape": (True, True),
    "vacuity": (False, True),
}


def score(reviewer, pkg):
    p = subprocess.run([sys.executable, reviewer, pkg, "--run"],
                       capture_output=True, text=True, encoding="utf-8", timeout=300)
    out = (p.stdout or "") + (p.stderr or "")
    total = re.search(r"(?:总分|total)[：:]\s*(\d+)/100", out)
    repro = re.search(r"reproducible\s+(\d+)/20", out)
    return {
        "total": int(total.group(1)) if total else None,
        "repro": int(repro.group(1)) if repro else None,
    }


def judge(name, r, threshold):
    """Return (blocked, reasons)."""
    must_total, must_repro = PROBE_RULES[name]
    reasons, ok = [], True
    if r["total"] is None:
        return True, ["reviewer printed no score (cannot be fooled by what it cannot read)"]
    if must_total and r["total"] >= threshold:
        ok = False
        reasons.append("total %d >= pass line %d" % (r["total"], threshold))
    if must_repro:
        if r["repro"] is None:
            reasons.append("warn: no reproducible breakdown printed, key rule unverified")
        elif r["repro"] >= 20:
            ok = False
            reasons.append("reproducible %d/20 — a package that verifies nothing earned full marks"
                           % r["repro"])
    return ok, reasons


def main():
    ap = argparse.ArgumentParser(description="Red-team a skill reviewer with two fake packages.")
    ap.add_argument("--reviewer", required=True, help="path to a reviewer CLI")
    ap.add_argument("--threshold", type=int, default=80, help="pass line for the shape probe")
    ap.add_argument("--keep", action="store_true", help="keep a copy of the probes used")
    a = ap.parse_args()

    if not os.path.exists(a.reviewer):
        sys.stderr.write("reviewer not found: %s\n" % a.reviewer)
        return 2
    src, cleanup = probe_root()
    if src is None:
        sys.stderr.write("probes/ or probes.zip missing next to run_suite.py\n")
        return 2

    tmp = tempfile.mkdtemp(prefix="redteam-")
    fails = 0
    try:
        print("reviewer: %s   pass line: %d   probes: %d"
              % (a.reviewer, a.threshold, len(PROBE_RULES)))
        for name in sorted(PROBE_RULES):
            dst = os.path.join(tmp, name)
            shutil.copytree(os.path.join(src, name), dst)
            r = score(a.reviewer, dst)
            blocked, reasons = judge(name, r, a.threshold)
            print("  %-8s total %s   repro %s   %s"
                  % (name, r["total"],
                     ("%d/20" % r["repro"]) if r["repro"] is not None else "-",
                     "BLOCKED" if blocked else "GOT THROUGH <- hole"))
            for why in reasons:
                print("           - %s" % why)
            if not blocked:
                fails += 1
        print("\n%s" % ("ALL PROBES BLOCKED" if fails == 0 else
                        "%d probe(s) got through - this reviewer can be fooled" % fails))
    finally:
        if cleanup:
            shutil.rmtree(cleanup, ignore_errors=True)
        if a.keep:
            print("probes kept at:", tmp)
        else:
            shutil.rmtree(tmp, ignore_errors=True)
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
