"""
memory_agent.py — The Hippocampus Loop
Part of the Neuromorphic Agent Architecture (v3.0)

The brain's equivalent: the hippocampus continuously consolidating short-term
episodes into long-term memory — particularly during rest (task completion),
rather than interrupting active cognition.

This agent watches 3 triggers and fires memory distillation automatically:
  1. Turn limit crossed (every N turns of conversation)
  2. Token threshold crossed (context is above X% full)
  3. Task completion signal received

When triggered, it:
  a. Runs distill_memory.py on the current history file
  b. Writes structured facts to the episodic store
  c. Optionally writes to agent-memory-mcp if MCP is enabled
  d. Signals the orchestrator that working memory can be flushed

Usage (one-shot check, called per-turn by orchestrator):
  python memory_agent.py --turn 25 --token-pct 0.72 --history chat.json
  python memory_agent.py --turn 20 --token-pct 0.55 --history chat.json --task-complete

Usage (state file — for stateless agents that can't hold turn count):
  python memory_agent.py --state session_state.json --history chat.json
"""

import sys
import json
import argparse
import os
import subprocess
from datetime import datetime, timezone

CONFIG_CANDIDATES = [
    os.path.join(os.path.dirname(__file__), "..", "orchestrator_config.json"),
    os.path.join(os.path.dirname(__file__), "orchestrator_config.json"),
    os.path.expanduser("~/.openclaw/orchestrator_config.json"),
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_config() -> dict:
    for path in CONFIG_CANDIDATES:
        resolved = os.path.abspath(path)
        if os.path.exists(resolved):
            with open(resolved, "r") as f:
                return json.load(f)
    raise FileNotFoundError("orchestrator_config.json not found.")

def resolve_script(rel_path: str) -> str:
    # Fix: try the full relative path first (primary case when scripts/ dir exists)
    candidates = [
        os.path.join(SCRIPT_DIR, rel_path),                   # e.g. /skill_root/scripts/distill_memory.py
        os.path.join(SCRIPT_DIR, os.path.basename(rel_path)), # same dir as memory_agent.py
        os.path.join(SCRIPT_DIR, "..", rel_path),             # one level up
        os.path.abspath(rel_path),                             # absolute fallback
    ]
    for c in candidates:
        resolved = os.path.abspath(c)
        if os.path.exists(resolved):
            return resolved
    raise FileNotFoundError(
        f"Script not found: {rel_path}\n"
        f"Searched from: {SCRIPT_DIR}\n"
        f"Tried: {[os.path.abspath(c) for c in candidates]}"
    )

def check_triggers(turn: int, token_pct: float, task_complete: bool, config: dict) -> dict:
    """
    Evaluate which (if any) memory triggers have fired.
    Returns human-readable trigger report.
    """
    thresholds = config.get("context_thresholds", {})
    mem_config  = config.get("memory", {})

    # Fix: canonical source of truth is context_thresholds.auto_distill_every_n_turns only.
    # agent_roles.memory_agent.check_every_n_turns was a conflicting duplicate — removed from lookup.
    turn_limit = thresholds.get("auto_distill_every_n_turns", 20)
    distill_pct   = thresholds.get("distill_pct", 0.80)
    warning_pct   = thresholds.get("warning_pct", 0.65)

    triggers_fired = []

    if task_complete:
        triggers_fired.append({
            "trigger": "task_complete",
            "severity": "high",
            "detail": "Task completion signal received. Ideal consolidation window (like sleep).",
        })

    if token_pct >= distill_pct:
        triggers_fired.append({
            "trigger": "token_threshold",
            "severity": "critical",
            "detail": f"Context at {token_pct*100:.1f}% (threshold: {distill_pct*100:.0f}%). Distill NOW.",
        })
    elif token_pct >= warning_pct:
        triggers_fired.append({
            "trigger": "token_warning",
            "severity": "warning",
            "detail": f"Context at {token_pct*100:.1f}% (warning: {warning_pct*100:.0f}%). Plan to distill soon.",
        })

    if turn > 0 and turn % turn_limit == 0:
        triggers_fired.append({
            "trigger": "turn_limit",
            "severity": "medium",
            "detail": f"Turn {turn} reached — distillation interval of {turn_limit} turns hit.",
        })

    return {
        "should_distill": any(t["trigger"] in ("task_complete", "token_threshold", "turn_limit")
                              for t in triggers_fired),
        "triggers_fired": triggers_fired,
        "turn": turn,
        "token_pct": token_pct,
    }

def run_distillation(history_path: str, config: dict) -> dict:
    """
    Execute distill_memory.py and write output to the episodic store.
    """
    mem_config = config.get("memory", {})
    distill_script_rel = mem_config.get("distill_script", "scripts/distill_memory.py")
    episodic_dir = os.path.expanduser(mem_config.get("episodic_store_path", ".openclaw/memory/episodic"))

    try:
        distill_script = resolve_script(distill_script_rel)
    except FileNotFoundError as e:
        return {"success": False, "error": str(e)}

    # Build output path in episodic store
    os.makedirs(episodic_dir, exist_ok=True)
    # Fix: datetime.utcnow() is deprecated in Python 3.12+; use timezone-aware alternative.
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = os.path.join(episodic_dir, f"session_{timestamp}.json")

    cmd = [sys.executable, distill_script, "--input", history_path, "--output", output_path]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if proc.returncode != 0:
            return {
                "success": False,
                "error": f"distill_memory.py failed: {proc.stderr.strip()}",
            }

        # Read the result to count facts and check if source_turn was resolved
        try:
            with open(output_path) as f:
                distilled = json.load(f)
            metadata = distilled.get("metadata", {})
            facts_count = metadata.get("facts_extracted_count", "?")
            turn_resolved = metadata.get("source_turn_resolved", False)
            output_chars = os.path.getsize(output_path)
        except Exception:
            facts_count = "?"
            turn_resolved = False
            output_chars = 0

        # Fix: Size gate — if distilled output is LARGER than input, it wastes context.
        # For small histories, regex extracts + JSON scaffolding inflates the file.
        input_chars = os.path.getsize(history_path)
        skipped_write = False
        if output_chars > input_chars:
            os.remove(output_path)   # discard oversized distillation
            skipped_write = True
            return {
                "success": False,
                "skipped": True,
                "reason": (
                    f"Size gate: distilled output ({output_chars} chars) > "
                    f"input ({input_chars} chars). Distilling this history inflates context. "
                    "Accumulate more turns before distilling."
                ),
                "flush_recommended": False,
            }

        return {
            "success": True,
            "output_path": output_path,
            "facts_count": facts_count,
            "input_chars": input_chars,
            "output_chars": output_chars,
            "compression_ratio": round(output_chars / input_chars, 2) if input_chars else None,
            "source_turn_resolved": turn_resolved,
            "flush_recommended": mem_config.get("flush_on_distill", True),
            "stdout": proc.stdout.strip(),
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "distill_memory.py timed out."}

def load_state(state_path: str) -> dict:
    """Load session state from a JSON file (for stateless agent integrations)."""
    if os.path.exists(state_path):
        with open(state_path) as f:
            return json.load(f)
    return {"turn": 0, "token_pct": 0.0, "task_complete": False}

def save_state(state_path: str, state: dict):
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)

def main():
    parser = argparse.ArgumentParser(
        description="Neuromorphic memory agent: watches triggers and distills memory automatically."
    )
    parser.add_argument("--turn", type=int, default=0,
                        help="Current conversation turn number.")
    parser.add_argument("--token-pct", type=float, default=0.0,
                        help="Current context fullness as a fraction (e.g. 0.72 = 72%%).")
    parser.add_argument("--task-complete", action="store_true",
                        help="Signal that the current task is complete (ideal distillation window).")
    parser.add_argument("--history", type=str,
                        help="Path to the conversation history file to distill (JSON or text).")
    parser.add_argument("--state", type=str,
                        help="Path to session state JSON file (for stateless integrations).")
    parser.add_argument("--json", action="store_true",
                        help="Output raw JSON (for orchestrator programmatic use).")
    args = parser.parse_args()

    try:
        config = load_config()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Load from state file if provided (overrides CLI args)
    turn, token_pct, task_complete = args.turn, args.token_pct, args.task_complete
    if args.state:
        state = load_state(args.state)
        turn         = state.get("turn", turn)
        token_pct    = state.get("token_pct", token_pct)
        task_complete = state.get("task_complete", task_complete)

    # --- Step 1: Check triggers ---
    trigger_report = check_triggers(turn, token_pct, task_complete, config)

    result = {
        "trigger_check": trigger_report,
        "distillation": None,
        "recommendation": None,
    }

    # --- Step 2: Distill if triggered ---
    if trigger_report["should_distill"]:
        if not args.history:
            result["distillation"] = {
                "success": False,
                "error": "Distillation triggered but --history path not provided. Cannot distill.",
            }
        else:
            result["distillation"] = run_distillation(args.history, config)

    # --- Step 3: Build recommendation for Orchestrator ---
    if not trigger_report["triggers_fired"]:
        result["recommendation"] = "NO_ACTION — context healthy, continue normally."
    elif trigger_report["should_distill"] and result["distillation"] and result["distillation"]["success"]:
        flush = result["distillation"].get("flush_recommended", True)
        result["recommendation"] = (
            "DISTILLED — "
            f"{result['distillation']['facts_count']} facts saved to episodic store. "
            + ("FLUSH working memory and start fresh context." if flush else "Keep working memory.")
        )
    elif not trigger_report["should_distill"]:
        result["recommendation"] = "WARNING — context approaching limit. Prepare to distill soon."
    else:
        result["recommendation"] = "DISTILLATION_FAILED — check logs. Do not flush context yet."

    # Output
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"\n🧠 Memory Agent Report  [turn={turn} | context={token_pct*100:.1f}%]")
        print(f"   Recommendation: {result['recommendation']}")
        if trigger_report["triggers_fired"]:
            print("\n   Triggers Fired:")
            for t in trigger_report["triggers_fired"]:
                icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "warning": "🟡"}.get(t["severity"], "⚪")
                print(f"   {icon} [{t['trigger']}] {t['detail']}")
        if result["distillation"] and result["distillation"]["success"]:
            d = result["distillation"]
            print(f"\n   ✅ Distilled: {d['facts_count']} facts → {d['output_path']}")
            if not d["source_turn_resolved"]:
                print("   ⚠️  source_turn is inferred (plain-text input). Provide JSON messages for exact tracking.")

if __name__ == "__main__":
    main()
