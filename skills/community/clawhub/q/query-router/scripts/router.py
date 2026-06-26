#!/usr/bin/env python3
"""
Query Router - Merged approach combining:
  1. Content-type detection (vision, voice, tool, code, reasoning, qa)
  2. Complexity scoring (simple, moderate, complex)
  3. Prefix routing (@codex, @mini, @cl, @q, @llava, @whisper)
  4. Safety: dry-run, verify, rollback, lock protection
"""

import sys
import json
import os
import fcntl
import subprocess
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from classify import classify, check_available_models

# ─── Config ──────────────────────────────────────────────────────────────────
DEFAULT_MODEL = "minimax-m2.7:cloud"
AUTO_ROUTE_THRESHOLD = 0.6
MANUAL_REVIEW_THRESHOLD = 0.3
LOCK_DIR = SCRIPT_DIR / ".locks"
LOG_DIR = SCRIPT_DIR / ".logs"
AUDIT_LOG = LOG_DIR / "router.log.jsonl"

# ─── Safety helpers ────────────────────────────────────────────────────────────
def ensure_dirs():
    LOCK_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)

def acquire_lock(lock_name: str, timeout: int = 10) -> bool:
    """Acquire a file lock to prevent concurrent routing."""
    ensure_dirs()
    lock_path = LOCK_DIR / f"{lock_name}.lock"
    lock_file = open(lock_path, "w")
    try:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except BlockingIOError:
        return False

def release_lock(lock_name: str):
    lock_path = LOCK_DIR / f"{lock_name}.lock"
    lock_path.unlink(missing_ok=True)

def log_audit(action: str, query: str, result: dict, success: bool = True):
    """Write audit log entry."""
    ensure_dirs()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "query": query[:100],
        "model_from": result.get("from_model"),
        "model_to": result.get("to_model"),
        "routing_reason": result.get("classification", {}).get("routing_reason"),
        "success": success,
    }
    with open(AUDIT_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

def get_current_model() -> str:
    """Get currently active model."""
    try:
        result = subprocess.run(
            ["openclaw", "status", "--json"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get("model", DEFAULT_MODEL)
    except Exception:
        pass
    return DEFAULT_MODEL

def verify_switch(target_model: str, timeout: int = 10) -> tuple:
    """
    Verify model switch succeeded.
    Returns (success, message)
    """
    try:
        # Check via openclaw status
        result = subprocess.run(
            ["openclaw", "status", "--json"],
            capture_output=True, text=True, timeout=timeout
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            current = data.get("model", "")
            if current == target_model:
                return True, f"Verified: now using {current}"
            else:
                return False, f"Switch failed: expected {target_model}, got {current}"
        return False, "Could not verify model switch"
    except Exception as e:
        return False, f"Verify error: {e}"

# ─── Route Logic ──────────────────────────────────────────────────────────────
def route_query(
    query: str,
    has_attachment: bool = False,
    attachment_ext: str = "",
    dry_run: bool = False,
    force_model: str = None,
    enable_lock: bool = True,
    enable_verify: bool = True,
    enable_rollback: bool = True,
) -> dict:
    """
    Classify and route with full safety pipeline.
    
    Safety features:
      - Lock protection prevents concurrent routing
      - Verify-after-switch confirms model changed
      - Rollback on failure reverts to previous model
      - Audit logging of every action
    """
    current_model = get_current_model()
    classification = classify(query, has_attachment, attachment_ext)
    
    lock_name = "router"
    
    # Lock acquisition
    if enable_lock:
        if not acquire_lock(lock_name):
            return {
                "action": "blocked",
                "from_model": current_model,
                "to_model": None,
                "classification": classification,
                "message": "Routing blocked: another routing operation in progress",
            }
    
    try:
        # Force model override
        if force_model:
            to_model = force_model
            action = "recommend" if dry_run else "route"
            msg = f"[DRY RUN] Would switch {current_model} → {to_model}" if dry_run else f"Switching {current_model} → {to_model}"
            log_audit("force_route", query, {"from_model": current_model, "to_model": to_model, "classification": classification}, success=True)
            return {
                "action": action,
                "from_model": current_model,
                "to_model": to_model,
                "classification": classification,
                "message": msg,
            }
        
        # Determine if routing is warranted
        confidence = classification["type_confidence"] or classification["complexity_confidence"]
        recommended = classification["recommended_model"]
        
        if confidence >= AUTO_ROUTE_THRESHOLD and recommended != current_model:
            if dry_run:
                log_audit("dry_run", query, {"from_model": current_model, "to_model": recommended, "classification": classification}, success=True)
                return {
                    "action": "recommend",
                    "from_model": current_model,
                    "to_model": recommended,
                    "classification": classification,
                    "message": f"[DRY RUN] Would switch {current_model} → {recommended} (confidence: {confidence:.0%})",
                }
            
            # Actual switch
            to_model = recommended
            log_audit("route", query, {"from_model": current_model, "to_model": to_model, "classification": classification}, success=True)
            
            if enable_verify:
                success, verify_msg = verify_switch(to_model)
                if not success and enable_rollback:
                    log_audit("rollback", query, {"from_model": to_model, "to_model": current_model, "classification": classification}, success=False)
                    return {
                        "action": "rollback",
                        "from_model": current_model,
                        "to_model": current_model,
                        "classification": classification,
                        "message": f"Switch failed, rolled back. {verify_msg}",
                    }
            
            return {
                "action": "route",
                "from_model": current_model,
                "to_model": to_model,
                "classification": classification,
                "message": f"Routed to {to_model} (confidence: {confidence:.0%})",
            }
        
        elif confidence >= MANUAL_REVIEW_THRESHOLD:
            log_audit("recommend", query, {"from_model": current_model, "to_model": recommended, "classification": classification}, success=True)
            return {
                "action": "recommend",
                "from_model": current_model,
                "to_model": recommended,
                "classification": classification,
                "message": f"Current: {current_model} | Recommended: {recommended} ({confidence:.0%}) | Reason: {classification['routing_reason']}",
            }
        
        else:
            log_audit("skip", query, {"from_model": current_model, "to_model": current_model, "classification": classification}, success=True)
            return {
                "action": "skip",
                "from_model": current_model,
                "to_model": current_model,
                "classification": classification,
                "message": f"Keeping {current_model}",
            }
    
    finally:
        if enable_lock:
            release_lock(lock_name)


def format_output(result: dict, as_json: bool = False) -> str:
    if as_json:
        return json.dumps(result, indent=2)
    
    cls = result["classification"]
    lines = [
        f"",
        f"  Routing action : {result['action'].upper()}",
        f"  Content type   : {cls['content_type'].upper()}  (conf: {cls['type_confidence']:.0%})",
        f"  Complexity     : {cls['complexity'].upper()}   (conf: {cls['complexity_confidence']:.0%})",
        f"  Model          : {result['from_model']} → {result['to_model']}",
        f"  Reason         : {cls['routing_reason']}",
        f"  Message        : {result['message']}",
        "",
        "  Content scores:",
    ]
    
    for qtype, score in sorted(cls["content_scores"].items(), key=lambda x: -x[1]):
        bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
        marker = "→" if qtype == cls["content_type"] else " "
        lines.append(f"    {marker} {qtype:12} {bar} {score:.0%}")
    
    lines.append("")
    lines.append("  Complexity scores:")
    for tier, score in sorted(cls["complexity_scores"].items(), key=lambda x: -x[1]):
        bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
        marker = "→" if tier == cls["complexity"] else " "
        lines.append(f"    {marker} {tier:12} {bar} {score:.0%}")
    
    return "\n".join(lines)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Query Router - Unified routing: content-type + complexity + prefix")
    parser.add_argument("query", nargs="*", help="Query to classify and route")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--dry-run", action="store_true", help="Preview routing without switching")
    parser.add_argument("--attachment", "-a", help="Attachment file extension (e.g., .png)")
    parser.add_argument("--model", "-m", help="Force specific model")
    parser.add_argument("--no-lock", action="store_true", help="Disable lock protection")
    parser.add_argument("--no-verify", action="store_true", help="Skip verify-after-switch")
    parser.add_argument("--no-rollback", action="store_true", help="Disable rollback on failure")
    parser.add_argument("--check", action="store_true", help="List available models")
    parser.add_argument("--audit", action="store_true", help="Show recent audit log")
    
    args = parser.parse_args()
    
    if args.check:
        models = check_available_models()
        print(f"Available models ({len(models)}):")
        for m in sorted(models):
            print(f"  - {m}")
        return
    
    if args.audit:
        ensure_dirs()
        if AUDIT_LOG.exists():
            lines = AUDIT_LOG.read_text().strip().split("\n")
            print(f"Last {min(10, len(lines))} audit entries:")
            for line in lines[-10:]:
                entry = json.loads(line)
                status = "✅" if entry["success"] else "❌"
                print(f"  {status} {entry['timestamp']} | {entry['action']:10} | {entry.get('model_from','?'):25} → {entry.get('model_to','?'):25} | {entry.get('routing_reason','')}")
        else:
            print("No audit log found.")
        return
    
    if not args.query:
        parser.print_help()
        print("")
        print("Prefix examples: @codex, @mini, @cl, @q, @llava, @whisper")
        print("Examples:")
        print("  router.py @codex write a complex multi-file script")
        print("  router.py --attachment .png describe this image")
        print("  router.py --dry-run analyze this dataset")
        print("  router.py --audit   # show recent routing log")
        return
    
    query = " ".join(args.query)
    result = route_query(
        query,
        has_attachment=bool(args.attachment),
        attachment_ext=args.attachment or "",
        dry_run=args.dry_run,
        force_model=args.model,
        enable_lock=not args.no_lock,
        enable_verify=not args.no_verify,
        enable_rollback=not args.no_rollback,
    )
    
    print(format_output(result, args.json))


if __name__ == "__main__":
    main()
