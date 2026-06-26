#!/usr/bin/env python3
"""tetra_scar.py — Scar memory and reflex arc for AI agents.

Standalone module. Zero external dependencies (stdlib only).
Extract from Tetra Genesis (B Button Corp).

Two-layer memory:
  - Scar layer (immutable): failure records that block future mistakes
  - Narrative layer (mutable): success records for session handoff

Reflex arc: pattern-matching against scars, no LLM calls needed.
4-axis check: emotion / action / life / ethics validation.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# ============================================================================
# Configuration
# ============================================================================

DEFAULT_MEMORY_DIR = Path.cwd() / "memory"
SCAR_FILENAME = "scars.jsonl"
NARRATIVE_FILENAME = "narrative.jsonl"


def _memory_dir(memory_dir: Optional[str] = None) -> Path:
    """Resolve memory directory. Creates if not exists."""
    d = Path(memory_dir) if memory_dir else DEFAULT_MEMORY_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def _read_jsonl(filepath: Path) -> list[dict]:
    """Read a JSONL file, skipping malformed lines."""
    if not filepath.exists():
        return []
    entries = []
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


# ============================================================================
# Scar Layer — Immutable. Never delete.
# ============================================================================

def read_scars(
    n: int = 20,
    memory_dir: Optional[str] = None,
) -> list[dict]:
    """Read the most recent n scars.

    Returns list of dicts with keys: id, what_broke, never_again, created_at
    """
    d = _memory_dir(memory_dir)
    entries = _read_jsonl(d / SCAR_FILENAME)
    return entries[-n:]


def write_scar(
    what_broke: str,
    never_again: str,
    memory_dir: Optional[str] = None,
) -> dict:
    """Record an immutable scar. Cannot be deleted or overwritten.

    Args:
        what_broke: What went wrong.
        never_again: The constraint to prevent recurrence.
    Returns:
        The scar entry dict.
    """
    d = _memory_dir(memory_dir)
    entry = {
        "id": f"scar_{int(time.time() * 1000)}",
        "what_broke": what_broke,
        "never_again": never_again,
        "created_at": datetime.now().isoformat(),
    }
    with open(d / SCAR_FILENAME, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


# ============================================================================
# Narrative Layer — Mutable. Overwritable. Session handoff.
# ============================================================================

def read_narrative(
    n: int = 10,
    memory_dir: Optional[str] = None,
) -> list[dict]:
    """Read the most recent n narrative entries."""
    d = _memory_dir(memory_dir)
    entries = _read_jsonl(d / NARRATIVE_FILENAME)
    return entries[-n:]


def write_narrative(
    what: str,
    who_benefited: str = "",
    memory_dir: Optional[str] = None,
) -> dict:
    """Record what was done and who benefited."""
    d = _memory_dir(memory_dir)
    entry = {
        "id": f"narr_{int(time.time() * 1000)}",
        "what": what,
        "who_benefited": who_benefited,
        "created_at": datetime.now().isoformat(),
    }
    with open(d / NARRATIVE_FILENAME, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


# ============================================================================
# Reflex Arc — Spinal reflex. No LLM. Pure pattern matching.
# ============================================================================

def _extract_keywords(text: str) -> list[str]:
    """Extract keywords from text (English 3+ chars, Japanese kanji/katakana 2+ chars)."""
    en_words = re.findall(r'[a-zA-Z_]{3,}', text)
    ja_words = re.findall(r'[\u4e00-\u9fff\u30a0-\u30ff]{2,}', text)
    return en_words + ja_words


def reflex_check(
    task_or_prompt: str,
    scars: list[dict],
    threshold_ratio: float = 0.4,
    min_matches: int = 2,
) -> Optional[str]:
    """Check if a task collides with any scar. Spinal reflex — no LLM needed.

    Returns: block reason (str) if collision detected, None if safe.
    """
    if not task_or_prompt:
        return None

    task_lower = task_or_prompt.lower()

    for scar in scars:
        never = scar.get("never_again", "")
        if not never:
            continue

        keywords = _extract_keywords(never)
        if len(keywords) < 2:
            continue

        matches = [kw for kw in keywords if kw.lower() in task_lower]
        threshold = max(min_matches, len(keywords) * threshold_ratio)
        if len(matches) >= threshold:
            return (
                f"scar collision: '{never[:60]}' "
                f"(matched: {', '.join(matches[:5])})"
            )

    return None


# ============================================================================
# 4-Axis Check — Emotion / Action / Life / Ethics
# ============================================================================

# Action verbs for the action axis (Japanese + English)
_ACTION_WORDS = frozenset([
    "作成", "修正", "追加", "削除", "確認", "改善", "実行",
    "生成", "更新", "分析", "報告", "変更", "読み", "書き",
    "create", "fix", "add", "remove", "read", "write", "check",
    "update", "improve", "report", "analyze", "generate", "delete",
    "refactor", "test", "deploy", "build", "run", "install",
    "push", "pull", "merge", "send", "move", "copy", "migrate",
])

# Dangerous operations for the ethics axis
_DANGEROUS_OPS = frozenset([
    "rm -rf", "drop table", "force push", "reset --hard",
    "全削除", "全ファイル", "truncate table", "format disk",
    "sudo rm", "del /f /s",
])


def tetra_check(
    task_description: str,
    scars: list[dict],
) -> tuple[bool, str]:
    """4-axis self-refutation. No LLM calls.

    Axes:
      1. Emotion: motivation exists (non-empty description)
      2. Action: concrete action verb present
      3. Life: no scar collision (reflex arc)
      4. Ethics: no dangerous operations

    Returns: (approved: bool, reason: str)
    """
    # Emotion axis
    if not task_description or len(task_description.strip()) < 5:
        return False, "emotion axis: no motivation (empty task)"

    # Action axis
    task_lower = task_description.lower()
    has_action = any(w in task_lower for w in _ACTION_WORDS)
    if not has_action:
        return False, "action axis: no concrete action verb found"

    # Life axis (reflex arc)
    block = reflex_check(task_description, scars)
    if block:
        return False, f"life axis: {block}"

    # Ethics axis
    for d in _DANGEROUS_OPS:
        if d in task_lower:
            return False, f"ethics axis: dangerous operation — {d}"

    return True, "all 4 axes passed"


# ============================================================================
# Delayed Verification — Check past decisions after N days
# ============================================================================

def schedule_verification(
    what: str,
    check_after_days: int = 3,
    memory_dir: Optional[str] = None,
) -> dict:
    """Schedule a delayed verification of a past action."""
    from datetime import timedelta
    d = _memory_dir(memory_dir)
    verify_file = d / "pending_verifications.jsonl"
    entry = {
        "id": f"verify_{int(time.time() * 1000)}",
        "what": what,
        "scheduled_at": datetime.now().isoformat(),
        "check_after": (datetime.now() + timedelta(days=check_after_days)).isoformat(),
        "checked": False,
    }
    with open(verify_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def run_pending_verifications(
    memory_dir: Optional[str] = None,
) -> list[dict]:
    """Check and return verifications that are past their check date."""
    d = _memory_dir(memory_dir)
    verify_file = d / "pending_verifications.jsonl"
    if not verify_file.exists():
        return []
    
    entries = _read_jsonl(verify_file)
    now = datetime.now().isoformat()
    due = []
    remaining = []
    
    for e in entries:
        if e.get("checked"):
            remaining.append(e)
        elif e.get("check_after", "") <= now:
            e["checked"] = True
            e["checked_at"] = now
            due.append(e)
            remaining.append(e)
        else:
            remaining.append(e)
    
    if due:
        with open(verify_file, "w", encoding="utf-8") as f:
            for e in remaining:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
    
    return due


# ============================================================================
# Decision Trace — 判断パスの記録（scarの「やるな」+ traceの「こう判断した」）
# ============================================================================

TRACE_FILENAME = "decision_traces.jsonl"


def write_trace(
    situation: str,
    options: list[dict],
    outcome: str,
    learned: str,
    tags: Optional[list[str]] = None,
    memory_dir: Optional[str] = None,
) -> dict:
    """Record a decision trace — the full judgment path.

    Unlike scars (what NOT to do) and narratives (what was done),
    traces capture WHY a decision was made and what alternatives existed.

    Args:
        situation: What was happening when the decision was needed.
        options: List of {"option": str, "chosen": bool, "reason": str}.
        outcome: What actually happened after the decision.
        learned: The transferable lesson.
        tags: Optional tags for retrieval.
    """
    d = _memory_dir(memory_dir)
    entry = {
        "id": f"trace_{int(time.time() * 1000)}",
        "situation": situation,
        "options": options,
        "outcome": outcome,
        "learned": learned,
        "tags": tags or [],
        "created_at": datetime.now().isoformat(),
    }
    with open(d / TRACE_FILENAME, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def read_traces(
    n: int = 10,
    tags: Optional[list[str]] = None,
    memory_dir: Optional[str] = None,
) -> list[dict]:
    """Read decision traces, optionally filtered by tags."""
    d = _memory_dir(memory_dir)
    entries = _read_jsonl(d / TRACE_FILENAME)
    if tags:
        tag_set = set(tags)
        entries = [e for e in entries if tag_set & set(e.get("tags", []))]
    return entries[-n:]


def trace_to_training_pair(trace: dict) -> dict:
    """Convert a decision trace to instruction-tuning format.

    Output format compatible with LoRA fine-tuning:
    {"instruction": ..., "input": ..., "output": ...}
    """
    # Build the instruction from the situation
    instruction = f"Situation: {trace['situation']}"

    # Build context from tags
    input_ctx = f"Tags: {', '.join(trace.get('tags', []))}" if trace.get('tags') else ""

    # Build the ideal response from the chosen option + outcome + lesson
    chosen = [o for o in trace.get("options", []) if o.get("chosen")]
    rejected = [o for o in trace.get("options", []) if not o.get("chosen")]

    output_parts = []
    if chosen:
        output_parts.append(f"Decision: {chosen[0]['option']}")
        if chosen[0].get("reason"):
            output_parts.append(f"Reason: {chosen[0]['reason']}")
    if rejected:
        for r in rejected[:2]:
            output_parts.append(f"Rejected: {r['option']} — {r.get('reason', '')}")
    output_parts.append(f"Outcome: {trace.get('outcome', '')}")
    output_parts.append(f"Lesson: {trace.get('learned', '')}")

    return {
        "instruction": instruction,
        "input": input_ctx,
        "output": "\n".join(output_parts),
    }


def export_training_data(
    memory_dir: Optional[str] = None,
    output_path: Optional[str] = None,
) -> str:
    """Export all traces + scars as LoRA training data.

    Combines:
    - Decision traces → positive examples (how to judge)
    - Scars → negative examples (what to avoid)
    - Narratives → context (what was done)

    Returns path to the output JSONL file.
    """
    d = _memory_dir(memory_dir)
    out = Path(output_path) if output_path else d / "training_data.jsonl"

    pairs = []

    # Traces → training pairs
    traces = _read_jsonl(d / TRACE_FILENAME)
    for t in traces:
        pairs.append(trace_to_training_pair(t))

    # Scars → negative training pairs
    scars = _read_jsonl(d / SCAR_FILENAME)
    for s in scars:
        pairs.append({
            "instruction": f"Should I do this? Context: {s.get('what_broke', '')}",
            "input": "",
            "output": f"NO. {s.get('never_again', '')}",
        })

    with open(out, "w", encoding="utf-8") as f:
        for p in pairs:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    return str(out)


# ============================================================================
# CLI Interface
# ============================================================================

def _cli_scar_add(args):
    entry = write_scar(args.what_broke, args.never_again, args.memory_dir)
    print(f"SCAR RECORDED: {entry['id']}")
    print(f"  what_broke: {entry['what_broke']}")
    print(f"  never_again: {entry['never_again']}")


def _cli_reflex_check(args):
    scars = read_scars(memory_dir=args.memory_dir)
    block = reflex_check(args.task, scars)
    if block:
        print(f"BLOCKED — {block}")
        sys.exit(1)
    else:
        print("CLEAR — no scar collision")


def _cli_tetra_check(args):
    scars = read_scars(memory_dir=args.memory_dir)
    approved, reason = tetra_check(args.task, scars)
    if approved:
        print(f"APPROVED — {reason}")
    else:
        print(f"REJECTED — {reason}")
        sys.exit(1)


def _cli_narrate(args):
    entry = write_narrative(args.what, args.who, args.memory_dir)
    print(f"NARRATIVE: {entry['id']}")
    print(f"  what: {entry['what']}")
    print(f"  who_benefited: {entry['who_benefited']}")


def _cli_list_scars(args):
    scars = read_scars(n=args.n, memory_dir=args.memory_dir)
    if not scars:
        print("No scars recorded yet.")
        return
    for s in scars:
        print(f"[{s.get('created_at', '?')}] {s.get('id', '?')}")
        print(f"  broke: {s.get('what_broke', '')[:80]}")
        print(f"  never: {s.get('never_again', '')[:80]}")
        print()


def _cli_list_narrative(args):
    entries = read_narrative(n=args.n, memory_dir=args.memory_dir)
    if not entries:
        print("No narrative entries yet.")
        return
    for e in entries:
        print(f"[{e.get('created_at', '?')}] {e.get('what', '')[:80]}")
        who = e.get('who_benefited', '')
        if who:
            print(f"  → benefited: {who}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="tetra-scar: Scar memory and reflex arc for AI agents"
    )
    parser.add_argument(
        "--memory-dir", default=None,
        help="Path to memory directory (default: ./memory)"
    )
    sub = parser.add_subparsers(dest="command")

    # scar-add
    p_scar = sub.add_parser("scar-add", help="Record a scar")
    p_scar.add_argument("--what-broke", required=True)
    p_scar.add_argument("--never-again", required=True)
    p_scar.set_defaults(func=_cli_scar_add)

    # reflex-check
    p_reflex = sub.add_parser("reflex-check", help="Check task against scars")
    p_reflex.add_argument("--task", required=True)
    p_reflex.set_defaults(func=_cli_reflex_check)

    # tetra-check
    p_tetra = sub.add_parser("tetra-check", help="4-axis check")
    p_tetra.add_argument("--task", required=True)
    p_tetra.set_defaults(func=_cli_tetra_check)

    # narrate
    p_narr = sub.add_parser("narrate", help="Record narrative")
    p_narr.add_argument("--what", required=True)
    p_narr.add_argument("--who", default="")
    p_narr.set_defaults(func=_cli_narrate)

    # list-scars
    p_ls = sub.add_parser("list-scars", help="List recorded scars")
    p_ls.add_argument("-n", type=int, default=20)
    p_ls.set_defaults(func=_cli_list_scars)

    # list-narrative
    p_ln = sub.add_parser("list-narrative", help="List narrative entries")
    p_ln.add_argument("-n", type=int, default=10)
    p_ln.set_defaults(func=_cli_list_narrative)

    # trace-add
    p_tr = sub.add_parser("trace-add", help="Record a decision trace")
    p_tr.add_argument("--situation", required=True)
    p_tr.add_argument("--chosen", required=True, help="The chosen option")
    p_tr.add_argument("--reason", default="", help="Why it was chosen")
    p_tr.add_argument("--outcome", required=True)
    p_tr.add_argument("--learned", required=True)
    p_tr.add_argument("--tags", default="", help="Comma-separated tags")
    p_tr.set_defaults(func=lambda args: print(json.dumps(write_trace(
        situation=args.situation,
        options=[{"option": args.chosen, "chosen": True, "reason": args.reason}],
        outcome=args.outcome,
        learned=args.learned,
        tags=[t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else [],
        memory_dir=args.memory_dir,
    ), indent=2, ensure_ascii=False)))

    # export-training
    p_ex = sub.add_parser("export-training", help="Export training data for LoRA")
    p_ex.add_argument("--output", default=None, help="Output JSONL path")
    p_ex.set_defaults(func=lambda args: print(
        f"Exported to: {export_training_data(args.memory_dir, args.output)}"
    ))

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()

