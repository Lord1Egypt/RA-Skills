#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASES = ROOT / "regression_cases.txt"
SCRIPT = ROOT / "search_best_image.py"

for line in CASES.read_text(encoding="utf-8").splitlines():
    q = line.strip()
    if not q or q.startswith("#"):
        continue
    proc = subprocess.run(["python3", str(SCRIPT), q], capture_output=True, text=True)
    print(f"\n=== {q} ===")
    if proc.returncode != 0:
        print("ERROR", proc.stderr.strip())
        continue
    data = json.loads(proc.stdout)
    best = data.get("best_image") or {}
    print(json.dumps({
        "intent": data.get("intent"),
        "subject_subtype": data.get("subject_subtype"),
        "confidence": data.get("confidence"),
        "best_title": best.get("title"),
        "best_page": best.get("page_url"),
        "best_score": best.get("score"),
        "best_why": best.get("why"),
    }, ensure_ascii=False, indent=2))
