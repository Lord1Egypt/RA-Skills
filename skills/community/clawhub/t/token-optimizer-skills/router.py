"""
router.py — The Synaptic Decision Gate
Part of the Neuromorphic Agent Architecture (v3.0)

The brain's equivalent: the thalamus routing signals to the correct cortex.

Classifies each incoming task as:
  PROCEDURAL → route to a compiled script (zero LLM tokens)
  REASONING  → let the LLM handle it (context window used normally)

Usage:
  python router.py --task "how many tokens are we using?"
  python router.py --task "distill the last conversation"
  python router.py --task "why is my API slow?"  
  python router.py --task "compress this document" --input doc.txt
"""

import sys
import json
import argparse
import os
import re

CONFIG_CANDIDATES = [
    os.path.join(os.path.dirname(__file__), "..", "orchestrator_config.json"),
    os.path.join(os.path.dirname(__file__), "orchestrator_config.json"),
    os.path.expanduser("~/.openclaw/orchestrator_config.json"),
]

def load_config() -> dict:
    for path in CONFIG_CANDIDATES:
        resolved = os.path.abspath(path)
        if os.path.exists(resolved):
            with open(resolved, "r") as f:
                return json.load(f)
    raise FileNotFoundError(
        "orchestrator_config.json not found. Checked:\n" +
        "\n".join(CONFIG_CANDIDATES)
    )

def classify_task(task: str, config: dict) -> dict:
    """
    Three-pass classification:
    Pass 1 — Check procedural signatures (keyword match).
    Pass 2 — Check reasoning keywords. If BOTH procedural AND strong reasoning
              keywords present in the same task, return HYBRID.
    Pass 3 — Default to REASONING (safe fallback).
    """
    task_lower = task.lower().strip()
    signatures = config.get("procedural_signatures", {})
    reasoning_kw = config.get("reasoning_keywords", [])

    # --- Pass 1: Procedural match ---
    best_tool = None
    best_hits = 0
    for tool_name, keywords in signatures.items():
        hits = sum(1 for kw in keywords if kw in task_lower)
        if hits > best_hits:
            best_hits = hits
            best_tool = tool_name

    # --- Detect reasoning keywords alongside procedural ---
    reasoning_hits = [kw for kw in reasoning_kw if kw in task_lower]
    has_strong_reasoning = len(reasoning_hits) >= 1

    # --- Pass 2: HYBRID detection ---
    # If the task has BOTH a procedural match AND a strong reasoning signal,
    # it cannot be silently routed to a script — it needs tool output + LLM interpretation.
    if best_tool and best_hits >= 1 and has_strong_reasoning:
        registry = config.get("tool_registry", {})
        entry = registry.get(best_tool, {})
        guardrail = entry.get("guardrail")
        return {
            "type": "HYBRID",
            "tool": best_tool,
            "script": entry.get("script"),
            "keyword_hits": best_hits,
            "reasoning_keywords_found": reasoning_hits,
            "guardrail": guardrail,
            "warning": (
                f"⚠️  Tool '{best_tool}' has guardrail OFFLINE_ONLY."
                if guardrail == "OFFLINE_ONLY" else None
            ),
            "rationale": (
                f"Mixed task: procedural match '{best_tool}' ({best_hits} hit(s)) "
                f"AND reasoning keywords {reasoning_hits}. "
                "Run the tool first, then pass its output to the LLM for interpretation."
            ),
        }

    # --- Pass 3: Pure procedural ---
    if best_tool and best_hits >= 1:
        # Check if tool has a guardrail
        registry = config.get("tool_registry", {})
        entry = registry.get(best_tool, {})
        guardrail = entry.get("guardrail")
        warning = None
        if guardrail == "OFFLINE_ONLY":
            warning = (
                f"⚠️  Tool '{best_tool}' is OFFLINE_ONLY. "
                "Do not apply to live system prompts, tool schemas, or code."
            )
        return {
            "type": "PROCEDURAL",
            "tool": best_tool,
            "script": registry.get(best_tool, {}).get("script"),
            "keyword_hits": best_hits,
            "guardrail": guardrail,
            "warning": warning,
            "rationale": (
                f"Matched {best_hits} procedural keyword(s) for tool '{best_tool}'. "
                "Routing to compiled script — no LLM tokens consumed."
            ),
        }

    # --- Pass 2: Reasoning keyword check ---
    reasoning_hits = [kw for kw in reasoning_kw if kw in task_lower]
    return {
        "type": "REASONING",
        "tool": None,
        "script": None,
        "keyword_hits": len(reasoning_hits),
        "guardrail": None,
        "warning": None,
        "rationale": (
            f"No procedural match found. Reasoning keywords detected: {reasoning_hits or 'none'}. "
            "Routing to LLM — context window will be used."
        ),
    }

def main():
    parser = argparse.ArgumentParser(
        description="Neuromorphic task router: classifies tasks as PROCEDURAL or REASONING."
    )
    parser.add_argument("--task", required=True,
                        help="The task description to classify.")
    parser.add_argument("--json", action="store_true",
                        help="Output raw JSON (for programmatic use by the orchestrator).")
    args = parser.parse_args()

    try:
        config = load_config()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    result = classify_task(args.task, config)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        icons = {"PROCEDURAL": "⚙️ ", "REASONING": "🧠", "HYBRID": "🔀"}
        icon = icons.get(result["type"], "❓")
        print(f"\n{icon} Classification: {result['type']}")

        if result["tool"]:
            print(f"   Tool    : {result['tool']}")
            print(f"   Script  : {result['script']}")
        if result["type"] == "HYBRID":
            print(f"   Reasoning keywords: {result.get('reasoning_keywords_found', [])}")
            print(f"   Action  : Run tool first → pass output to LLM for interpretation")

        print(f"   Rationale: {result['rationale']}")
        if result["warning"]:
            print(f"   {result['warning']}")

if __name__ == "__main__":
    main()
