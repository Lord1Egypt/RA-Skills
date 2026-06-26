#!/usr/bin/env python3
"""Batch scan 200 random skills from /tmp/openclaw-skills/skills/ using safe-skill."""

import glob
import json
import os
import random
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

SKILLS_ROOT = "/tmp/openclaw-skills/skills"
SCAN_SCRIPT = "/home/zhangjie/safe-skill/scripts/scan.py"
OUTPUT_FILE = "/home/zhangjie/safe-skill/tests/batch_scan_200.json"
SAMPLE_SIZE = 200
SEED = 42
TIMEOUT = 30  # seconds per skill


def find_skill_dirs():
    """Find all skill directories that contain a SKILL.md."""
    pattern = os.path.join(SKILLS_ROOT, "*", "*", "SKILL.md")
    skill_md_files = glob.glob(pattern)
    return [os.path.dirname(p) for p in skill_md_files]


def scan_skill(skill_dir):
    """Run scan.py on a skill directory and return parsed JSON or None."""
    try:
        result = subprocess.run(
            [sys.executable, SCAN_SCRIPT, skill_dir, "--json"],
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
        # Try to parse JSON even on non-zero exit (scanner uses exit codes for risk levels)
        try:
            parsed = json.loads(result.stdout)
            return parsed
        except (json.JSONDecodeError, ValueError):
            if result.returncode != 0:
                return {"error": f"exit code {result.returncode}", "stderr": result.stderr[:500]}
            return {"error": "empty output"}
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    except json.JSONDecodeError as e:
        return {"error": f"json parse error: {e}"}
    except Exception as e:
        return {"error": str(e)}


def extract_rule_ids(scan_result):
    """Extract all triggered rule IDs from a scan result."""
    rule_ids = []
    for fr in scan_result.get("file_reports", []):
        for finding in fr.get("pattern_findings", []):
            rid = finding.get("rule_id") or finding.get("rule") or finding.get("id")
            if rid:
                rule_ids.append(rid)
        for finding in fr.get("ast_findings", []):
            rid = finding.get("rule_id") or finding.get("rule") or finding.get("id")
            if rid:
                rule_ids.append(rid)
        for finding in fr.get("entropy_findings", []):
            rule_ids.append("high_entropy")
    return rule_ids


def main():
    print("=" * 70)
    print("BATCH SCAN: 200 Random Skills from openclaw-skills")
    print("=" * 70)

    # Step 1: Find all skill dirs
    print("\n[1/6] Finding skill directories...")
    all_skills = find_skill_dirs()
    print(f"  Found {len(all_skills)} skills with SKILL.md")

    # Step 2: Random sample
    print(f"\n[2/6] Sampling {SAMPLE_SIZE} skills (seed={SEED})...")
    random.seed(SEED)
    sampled = random.sample(all_skills, min(SAMPLE_SIZE, len(all_skills)))
    print(f"  Sampled {len(sampled)} skills")

    # Step 3 & 4: Scan and collect results
    print(f"\n[3/6] Scanning {len(sampled)} skills (timeout={TIMEOUT}s each)...")
    results = []
    errors = 0
    timeouts = 0
    start_all = time.time()

    for i, skill_dir in enumerate(sampled):
        skill_name = os.path.basename(skill_dir)
        author = os.path.basename(os.path.dirname(skill_dir))
        label = f"{author}/{skill_name}"

        if (i + 1) % 20 == 0 or i == 0:
            elapsed = time.time() - start_all
            print(f"  [{i+1:3d}/{len(sampled)}] Scanning {label}... (elapsed: {elapsed:.0f}s)")

        scan = scan_skill(skill_dir)

        if "error" in scan:
            if scan["error"] == "timeout":
                timeouts += 1
            errors += 1
            results.append({
                "skill_path": skill_dir,
                "skill_name": label,
                "error": scan["error"],
                "risk_score": None,
                "risk_level": "ERROR",
                "total_findings": None,
                "rule_ids": [],
            })
        else:
            rule_ids = extract_rule_ids(scan)
            summary = scan.get("summary", {})
            results.append({
                "skill_path": skill_dir,
                "skill_name": label,
                "risk_score": scan.get("risk_score", 0),
                "risk_level": scan.get("risk_level", "UNKNOWN"),
                "verdict": scan.get("verdict", "UNKNOWN"),
                "total_findings": summary.get("total_findings", 0),
                "total_files": scan.get("total_files", 0),
                "files_scanned": scan.get("files_scanned", 0),
                "external_urls": summary.get("external_urls", 0),
                "hardcoded_ips": summary.get("hardcoded_ips", 0),
                "ioc_matches": summary.get("ioc_matches", 0),
                "high_entropy_strings": summary.get("high_entropy_strings", 0),
                "rule_ids": rule_ids,
            })

    elapsed_total = time.time() - start_all
    print(f"\n  Done in {elapsed_total:.1f}s ({elapsed_total/len(sampled):.2f}s/skill avg)")
    print(f"  Errors: {errors} (timeouts: {timeouts})")

    # Step 5: Compute statistics
    print("\n[4/6] Computing statistics...")

    successful = [r for r in results if r.get("risk_score") is not None]

    # Risk level distribution
    risk_dist = Counter(r["risk_level"] for r in results)

    # Most frequent rules
    all_rules = []
    for r in results:
        all_rules.extend(r.get("rule_ids", []))
    rule_freq = Counter(all_rules).most_common(20)

    # Average score
    scores = [r["risk_score"] for r in successful]
    avg_score = sum(scores) / len(scores) if scores else 0
    max_score = max(scores) if scores else 0
    median_score = sorted(scores)[len(scores) // 2] if scores else 0

    # High/Extreme count
    high_extreme = [r for r in successful if r["risk_level"] in ("HIGH", "EXTREME")]

    stats = {
        "total_sampled": len(sampled),
        "successful_scans": len(successful),
        "errors": errors,
        "timeouts": timeouts,
        "elapsed_seconds": round(elapsed_total, 1),
        "risk_level_distribution": dict(risk_dist.most_common()),
        "top_20_rules": [{"rule_id": r, "count": c} for r, c in rule_freq],
        "score_stats": {
            "average": round(avg_score, 2),
            "median": median_score,
            "max": max_score,
        },
        "high_or_extreme_count": len(high_extreme),
    }

    # Step 6: Save results
    print(f"\n[5/6] Saving results to {OUTPUT_FILE}...")
    output = {
        "meta": {
            "sample_size": len(sampled),
            "seed": SEED,
            "timeout_per_skill": TIMEOUT,
            "total_skills_available": len(all_skills),
            "scan_script": SCAN_SCRIPT,
            "elapsed_seconds": round(elapsed_total, 1),
        },
        "statistics": stats,
        "results": results,
    }
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"  Saved ({os.path.getsize(OUTPUT_FILE)} bytes)")

    # Step 7: Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print(f"\nScanned {len(successful)}/{len(sampled)} skills successfully "
          f"({errors} errors, {timeouts} timeouts)")
    print(f"Total time: {elapsed_total:.1f}s")

    print("\n--- Risk Level Distribution ---")
    for level in ["CLEAN", "LOW", "MEDIUM", "HIGH", "EXTREME", "ERROR"]:
        count = risk_dist.get(level, 0)
        pct = count / len(sampled) * 100
        bar = "#" * int(pct / 2)
        print(f"  {level:8s}: {count:4d} ({pct:5.1f}%) {bar}")

    print(f"\n--- Score Statistics ---")
    print(f"  Average risk score : {avg_score:.2f}")
    print(f"  Median risk score  : {median_score}")
    print(f"  Max risk score     : {max_score}")
    print(f"  HIGH or EXTREME    : {len(high_extreme)} skills")

    if high_extreme:
        print(f"\n--- HIGH/EXTREME Skills ---")
        for r in sorted(high_extreme, key=lambda x: x["risk_score"], reverse=True)[:15]:
            print(f"  {r['risk_score']:5d}  {r['risk_level']:8s}  {r['skill_name']}")
            if r["rule_ids"]:
                top3 = Counter(r["rule_ids"]).most_common(3)
                print(f"         rules: {', '.join(f'{rid}({c})' for rid, c in top3)}")

    if rule_freq:
        print(f"\n--- Top 20 Triggered Rules ---")
        for i, (rule, count) in enumerate(rule_freq, 1):
            bar = "#" * min(count, 50)
            print(f"  {i:2d}. {rule:45s} {count:4d} {bar}")

    print("\n" + "=" * 70)
    print(f"Full results: {OUTPUT_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    main()
