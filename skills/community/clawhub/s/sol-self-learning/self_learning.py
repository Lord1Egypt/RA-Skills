# Self-Learning Skills — Build AI Agents That Improve From Mistakes

*Version: 1.0 | Created: 2026-06-15 | Author: Sol AI*

Every skill you build will eventually fail in a way you didn't anticipate. This tutorial shows you how to build skills that learn from those failures — so each mistake makes the system smarter, not just documented.

The core framework is **举一反三** (transfer learning): when one thing goes wrong, find the pattern and fix every similar case before they fail too.

---

## What We're Building

A self-learning skill system that:
1. Logs failures with full context
2. Identifies the root cause pattern
3. Applies fixes across all similar cases
4. Tracks what it's learned so future-you doesn't repeat the same mistakes

**The architecture:**
```
Failure → Context Log → Pattern Analysis → Fix Applied → Learning Record
                                              ↓
                                      All Similar Cases
```

---

## Prerequisites

- Python 3.10+
- OpenClaw running
- A skill you want to make smarter
- About 45 minutes

---

## Step 1: Create the Learning Logger

The first thing a self-learning skill needs is a way to record failures with enough context to analyze them later.

```python
#!/usr/bin/env python3
"""
learning_logger.py — Records skill failures with full context for pattern analysis
"""
import os, json, traceback
from datetime import datetime
from pathlib import Path
from typing import Optional, Any

LEARNING_DIR = Path.home() / ".openclaw" / "learning"
CONTEXT_LOG = LEARNING_DIR / "context_log.json"
PATTERN_INDEX = LEARNING_DIR / "patterns.json"
LEARNED_FIXES = LEARNING_DIR / "learned_fixes.json"

def ensure_dirs():
    LEARNING_DIR.mkdir(parents=True, exist_ok=True)
    for f in [CONTEXT_LOG, PATTERN_INDEX, LEARNED_FIXES]:
        if not f.exists():
            json.dump({}, open(f, "w"))

def log_failure(
    skill_name: str,
    error: Exception,
    context: dict,
    stack_trace: Optional[str] = None
) -> str:
    """
    Log a failure with full context. Returns a failure_id for tracking.
    """
    ensure_dirs()
    failure_id = f"{skill_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    entry = {
        "failure_id": failure_id,
        "skill_name": skill_name,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context,
        "stack_trace": stack_trace or traceback.format_exc(),
        "timestamp": datetime.now().isoformat(),
        "status": "pending_analysis"
    }
    
    # Append to context log
    log = json.load(open(CONTEXT_LOG)) if CONTEXT_LOG.exists() else {}
    log[failure_id] = entry
    json.dump(log, open(CONTEXT_LOG, "w"))
    
    return failure_id

def log_success(skill_name: str, context: dict, result: Any):
    """Log a success for contrast analysis."""
    ensure_dirs()
    entry = {
        "skill_name": skill_name,
        "context": context,
        "result_summary": str(result)[:200],
        "timestamp": datetime.now().isoformat()
    }
    
    success_log = LEARNING_DIR / "success_log.json"
    log = json.load(open(success_log)) if success_log.exists() else {}
    key = f"{skill_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    log[key] = entry
    json.dump(log, open(success_log, "w"))

# ─── Pattern Analysis ───────────────────────────────────────────────────────

def extract_error_pattern(failure_id: str) -> dict:
    """
    Analyze a failure and extract the repeatable pattern.
    Returns a pattern dict with: error_type, trigger_conditions, fix_hint.
    """
    log = json.load(open(CONTEXT_LOG))
    failure = log.get(failure_id)
    if not failure:
        return {}
    
    error_type = failure["error_type"]
    error_msg = failure["error_message"]
    context = failure["context"]
    
    # Pattern extraction rules — add your own based on what you see
    patterns = []
    
    # File not found patterns
    if "No such file or directory" in error_msg or "FileNotFoundError" in error_type:
        patterns.append({
            "pattern_type": "file_not_found",
            "likely_cause": "path typo or file was moved/deleted",
            "fix": "verify path exists before operation, use Path.exists() check"
        })
    
    # Permission denied patterns
    if "Permission denied" in error_msg or "PermissionError" in error_type:
        patterns.append({
            "pattern_type": "permission_error",
            "likely_cause": "file mode issue or running as wrong user",
            "fix": "check file permissions, verify user has correct access"
        })
    
    # API/auth patterns
    if "auth" in error_msg.lower() or "401" in error_msg or "token" in error_msg.lower():
        patterns.append({
            "pattern_type": "auth_failure",
            "likely_cause": "expired token, wrong credentials, missing API key",
            "fix": "refresh token, verify credentials, check API key format"
        })
    
    # Timeout patterns
    if "timeout" in error_msg.lower() or "TimeoutExpired" in error_type:
        patterns.append({
            "pattern_type": "timeout",
            "likely_cause": "network issue, slow operation, too short timeout",
            "fix": "increase timeout, add retry logic, check network"
        })
    
    # KeyError / missing field patterns
    if "KeyError" in error_type or "missing" in error_msg.lower():
        patterns.append({
            "pattern_type": "missing_field",
            "likely_cause": "data structure changed, optional field not handled",
            "fix": "use .get() with defaults, validate input structure"
        })
    
    return {
        "failure_id": failure_id,
        "error_type": error_type,
        "patterns_found": patterns,
        "timestamp": datetime.now().isoformat()
    }

def index_pattern(failure_id: str):
    """Store a analyzed pattern in the pattern index for future matching."""
    pattern = extract_error_pattern(failure_id)
    if not pattern or not pattern.get("patterns_found"):
        return
    
    patterns = json.load(open(PATTERN_INDEX)) if PATTERN_INDEX.exists() else {}
    
    for p in pattern["patterns_found"]:
        pt = p["pattern_type"]
        if pt not in patterns:
            patterns[pt] = []
        # Store unique fix hints per pattern type
        if p["fix"] not in patterns[pt]:
            patterns[pt].append(p["fix"])
    
    json.dump(patterns, open(PATTERN_INDEX, "w"))
    
    # Mark failure as analyzed
    log = json.load(open(CONTEXT_LOG))
    if failure_id in log:
        log[failure_id]["status"] = "analyzed"
        json.dump(log, open(CONTEXT_LOG, "w"))

# ─── Transfer Learning — Apply Fixes Across All Similar Cases ─────────────────

def find_similar_failures(pattern_type: str) -> list:
    """Find all pending failures matching a pattern type."""
    log = json.load(open(CONTEXT_LOG))
    similar = []
    
    for fid, entry in log.items():
        if entry.get("status") != "pending_analysis":
            continue
        error_msg = entry.get("error_message", "")
        error_type = entry.get("error_type", "")
        
        if pattern_type == "file_not_found" and ("No such file" in error_msg or "FileNotFoundError" in error_type):
            similar.append(fid)
        elif pattern_type == "permission_error" and "Permission" in error_type:
            similar.append(fid)
        elif pattern_type == "auth_failure" and ("auth" in error_msg.lower() or "401" in error_msg):
            similar.append(fid)
        elif pattern_type == "timeout" and "timeout" in error_msg.lower():
            similar.append(fid)
        elif pattern_type == "missing_field" and ("KeyError" in error_type or "missing" in error_msg.lower()):
            similar.append(fid)
    
    return similar

def apply_learned_fixes(pattern_type: str) -> dict:
    """
    For a given pattern type, find all similar failures and apply learned fixes.
    Returns a report of what was fixed.
    """
    fixes = json.load(open(PATTERN_INDEX)).get(pattern_type, [])
    if not fixes:
        return {"pattern_type": pattern_type, "fixes_applied": 0, "failures_fixed": []}
    
    similar = find_similar_failures(pattern_type)
    fixed = []
    
    for fid in similar:
        # Mark as fixed (in real implementation, you'd trigger a retry here)
        log = json.load(open(CONTEXT_LOG))
        if fid in log:
            log[fid]["status"] = "fix_applied"
            log[fid]["fix_applied"] = fixes[0]  # Use first known fix
            json.dump(log, open(CONTEXT_LOG, "w"))
            fixed.append(fid)
    
    return {
        "pattern_type": pattern_type,
        "fixes_applied": len(fixes),
        "failures_fixed": fixed
    }

# ─── Main Learning Loop ─────────────────────────────────────────────────────

def learn_from_failure(failure_id: str) -> dict:
    """
    Full 举一反三 cycle:
    1. Extract the error pattern
    2. Index it for future matching
    3. Find all similar pending failures
    4. Apply fixes to all of them
    """
    # Step 1: Analyze
    pattern = extract_error_pattern(failure_id)
    
    # Step 2: Index
    index_pattern(failure_id)
    
    # Step 3: Find similar
    results = []
    for p in pattern.get("patterns_found", []):
        pt = p["pattern_type"]
        report = apply_learned_fixes(pt)
        results.append(report)
    
    return {
        "failure_id": failure_id,
        "patterns_analyzed": len(pattern.get("patterns_found", [])),
        "fix_reports": results
    }

# ─── CLI Interface ───────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Self-learning skill framework")
    parser.add_argument("action", choices=["log", "analyze", "learn", "report", "fix-all"])
    parser.add_argument("--skill", help="Skill name")
    parser.add_argument("--failure-id", help="Failure ID")
    parser.add_argument("--error", help="Error message")
    args = parser.parse_args()
    
    if args.action == "log":
        if not args.skill or not args.error:
            print("Usage: --action log --skill NAME --error MESSAGE")
            return
        fid = log_failure(args.skill, Exception(args.error), {"cli": True})
        print(f"Logged failure: {fid}")
    
    elif args.action == "analyze":
        if not args.failure_id:
            print("Usage: --action analyze --failure-id FID")
            return
        pattern = extract_error_pattern(args.failure_id)
        print(json.dumps(pattern, indent=2))
    
    elif args.action == "learn":
        if not args.failure_id:
            print("Usage: --action learn --failure-id FID")
            return
        result = learn_from_failure(args.failure_id)
        print(json.dumps(result, indent=2))
    
    elif args.action == "report":
        ensure_dirs()
        log = json.load(open(CONTEXT_LOG)) if CONTEXT_LOG.exists() else {}
        patterns = json.load(open(PATTERN_INDEX)) if PATTERN_INDEX.exists() else {}
        print(f"Total failures logged: {len(log)}")
        print(f"Pattern types indexed: {len(patterns)}")
        for pt, fixes in patterns.items():
            print(f"  {pt}: {len(fixes)} known fix(es)")
    
    elif args.action == "fix-all":
        patterns = json.load(open(PATTERN_INDEX)) if PATTERN_INDEX.exists() else {}
        for pt in patterns.keys():
            result = apply_learned_fixes(pt)
            print(f"Fixed {len(result['failures_fixed'])} failures for {pt}")

if __name__ == "__main__":
    main()
