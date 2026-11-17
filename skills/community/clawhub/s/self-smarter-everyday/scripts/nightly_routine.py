#!/usr/bin/env python3
"""
nightly_routine.py — Orchestrates the nightly self-improvement routine.

Runs 6 phases in sequence:
  1. Reflection    — journal today's performance
  2. Audit         — self-audit metrics
  3. Memory Compact — promote/demote memory tiers
  4. Prompt Evolve — mutate and evaluate prompt variants
  5. Skill Gap     — identify missing skills
  6. Improvement Plan — generate next-day plan

Usage:
  python3 nightly_routine.py [--dry-run] [--phase PHASE] [--state-dir DIR]

State is persisted as JSON files in the state directory.
"""

import argparse
import json
import logging
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DEFAULT_STATE_DIR = os.path.expanduser("~/self-smarter/state")
DEFAULT_LOG_DIR = os.path.expanduser("~/self-smarter/logs")
SCRIPTS_DIR = Path(__file__).resolve().parent

PHASES = [
    ("reflection", "Running daily reflection"),
    ("audit", "Running self-audit"),
    ("memory_compact", "Compacting memory tiers"),
    ("prompt_evolve", "Evolving prompt variants"),
    ("skill_gap", "Analyzing skill gaps"),
    ("improvement_plan", "Generating improvement plan"),
]

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
def setup_logging(log_dir: Path, dry_run: bool) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"nightly_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logger = logging.getLogger("nightly_routine")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO if not dry_run else logging.DEBUG)
    fmt = logging.Formatter("[%(asctime)s] %(levelname)-7s %(message)s", datefmt="%H:%M:%S")
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------
def load_state(state_dir: Path) -> dict:
    state_file = state_dir / "routine_state.json"
    if state_file.exists():
        with open(state_file, "r") as f:
            return json.load(f)
    return {"last_run": None, "phase_results": {}, "run_count": 0}

def save_state(state_dir: Path, state: dict):
    state_dir.mkdir(parents=True, exist_ok=True)
    state_file = state_dir / "routine_state.json"
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2, default=str)

# ---------------------------------------------------------------------------
# Phase runners
# ---------------------------------------------------------------------------
def run_phase(phase_name: str, state_dir: Path, dry_run: bool, logger: logging.Logger) -> dict:
    """Execute a single phase. Returns a result dict."""
    script_map = {
        "reflection": None,  # handled inline
        "audit": "self_audit.py",
        "memory_compact": "memory_compact.py",
        "prompt_evolve": "prompt_evolve.py",
        "skill_gap": None,  # handled inline
        "improvement_plan": None,  # handled inline
    }

    if dry_run:
        logger.info(f"[DRY-RUN] Would execute phase: {phase_name}")
        return {"status": "dry-run", "phase": phase_name}

    # Phases with dedicated scripts
    if script_map.get(phase_name):
        script_path = SCRIPTS_DIR / script_map[phase_name]
        if not script_path.exists():
            logger.warning(f"Script not found: {script_path}")
            return {"status": "skipped", "reason": "script_not_found"}
        try:
            result = subprocess.run(
                [sys.executable, str(script_path), "--state-dir", str(state_dir)],
                capture_output=True, text=True, timeout=120
            )
            logger.debug(f"Script output: {result.stdout[:500]}")
            return {"status": "completed" if result.returncode == 0 else "failed",
                    "returncode": result.returncode, "output_preview": result.stdout[:300]}
        except subprocess.TimeoutExpired:
            logger.error(f"Phase {phase_name} timed out")
            return {"status": "timeout"}
        except Exception as e:
            logger.error(f"Phase {phase_name} error: {e}")
            return {"status": "error", "message": str(e)}

    # Inline phases
    if phase_name == "reflection":
        return _run_reflection(state_dir, logger)
    elif phase_name == "skill_gap":
        return _run_skill_gap(state_dir, logger)
    elif phase_name == "improvement_plan":
        return _run_improvement_plan(state_dir, logger)

    return {"status": "unknown_phase"}

def _run_reflection(state_dir: Path, logger: logging.Logger) -> dict:
    """Generate daily reflection entry."""
    today = datetime.now().strftime("%Y-%m-%d")
    reflection_dir = state_dir / "reflections"
    reflection_dir.mkdir(parents=True, exist_ok=True)
    reflection_file = reflection_dir / f"{today}.json"
    entry = {
        "date": today,
        "timestamp": datetime.now().isoformat(),
        "tasks_completed": 0,
        "errors_encountered": 0,
        "lessons_learned": [],
        "improvement_notes": "Auto-generated placeholder — review and enrich.",
    }
    with open(reflection_file, "w") as f:
        json.dump(entry, f, indent=2)
    logger.info(f"Reflection written: {reflection_file}")
    return {"status": "completed", "file": str(reflection_file)}

def _run_skill_gap(state_dir: Path, logger: logging.Logger) -> dict:
    """Analyze skill gaps based on recent audit data."""
    audit_file = state_dir / "audit_latest.json"
    gaps = []
    if audit_file.exists():
        with open(audit_file, "r") as f:
            audit = json.load(f)
        error_rate = audit.get("error_rate", 0)
        if error_rate > 0.05:
            gaps.append({"area": "error_handling", "severity": "high", "current_rate": error_rate})
        token_eff = audit.get("token_efficiency", 1.0)
        if token_eff < 0.6:
            gaps.append({"area": "token_efficiency", "severity": "medium", "current_score": token_eff})
    gap_file = state_dir / "skill_gaps.json"
    with open(gap_file, "w") as f:
        json.dump({"generated": datetime.now().isoformat(), "gaps": gaps}, f, indent=2)
    logger.info(f"Skill gap analysis: {len(gaps)} gaps identified")
    return {"status": "completed", "gaps_found": len(gaps)}

def _run_improvement_plan(state_dir: Path, logger: logging.Logger) -> dict:
    """Generate improvement plan for tomorrow."""
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    gap_file = state_dir / "skill_gaps.json"
    gaps_data = {"gaps": []}
    if gap_file.exists():
        with open(gap_file, "r") as f:
            gaps_data = json.load(f)
    plan = {
        "date": tomorrow,
        "generated": datetime.now().isoformat(),
        "priorities": [],
        "focus_areas": [g.get("area", "unknown") for g in gaps_data.get("gaps", [])],
        "notes": "Review and adjust priorities before execution.",
    }
    plan_file = state_dir / "improvement_plan_latest.json"
    with open(plan_file, "w") as f:
        json.dump(plan, f, indent=2)
    logger.info(f"Improvement plan written for {tomorrow}")
    return {"status": "completed", "file": str(plan_file)}

# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Nightly self-improvement routine")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without writing state")
    parser.add_argument("--phase", type=str, help="Run a single phase only")
    parser.add_argument("--state-dir", type=str, default=DEFAULT_STATE_DIR, help="State directory")
    args = parser.parse_args()

    state_dir = Path(args.state_dir)
    log_dir = Path(DEFAULT_LOG_DIR)
    logger = setup_logging(log_dir, args.dry_run)

    logger.info("=" * 60)
    logger.info("Nightly Routine Started" + (" [DRY-RUN]" if args.dry_run else ""))
    logger.info("=" * 60)

    state = load_state(state_dir)
    phases_to_run = PHASES
    if args.phase:
        phases_to_run = [(name, desc) for name, desc in PHASES if name == args.phase]
        if not phases_to_run:
            logger.error(f"Unknown phase: {args.phase}")
            sys.exit(1)

    results = {}
    for phase_name, phase_desc in phases_to_run:
        logger.info(f"▶ {phase_desc}")
        result = run_phase(phase_name, state_dir, args.dry_run, logger)
        results[phase_name] = result
        status = result.get("status", "unknown")
        if status == "failed" or status == "error":
            logger.warning(f"Phase {phase_name} ended with status: {status}")
        else:
            logger.info(f"Phase {phase_name} → {status}")

    state["last_run"] = datetime.now().isoformat()
    state["phase_results"] = results
    state["run_count"] = state.get("run_count", 0) + 1
    if not args.dry_run:
        save_state(state_dir, state)

    logger.info("=" * 60)
    logger.info(f"Nightly Routine Complete — {len(results)} phases executed")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
