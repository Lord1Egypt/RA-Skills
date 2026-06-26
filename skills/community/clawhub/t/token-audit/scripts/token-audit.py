#!/usr/bin/env python3
"""
Token Audit -- Analyze OpenClaw workspace token consumption and costs.
Part of the Caelguard toolkit. MIT License.

Usage: python3 token-audit.py [--workspace /path/to/workspace] [--json]
"""

import os
import sys
import json
import glob
import argparse
from pathlib import Path

# Token estimation: ~4 chars per token for English text (conservative)
# If tiktoken is available, use it for accuracy
CHARS_PER_TOKEN = 4

try:
    import tiktoken
    _enc = tiktoken.encoding_for_model("gpt-4")
    def count_tokens(text: str) -> int:
        return len(_enc.encode(text))
    TOKEN_METHOD = "tiktoken (accurate)"
except ImportError:
    def count_tokens(text: str) -> int:
        return len(text) // CHARS_PER_TOKEN
    TOKEN_METHOD = "char estimation (~4 chars/token)"


# Pricing per 1M tokens (input) as of Feb 2026
MODEL_PRICING = {
    "claude-opus-4": {"input": 15.00, "output": 75.00},
    "claude-sonnet-4": {"input": 3.00, "output": 15.00},
    "claude-haiku-3.5": {"input": 0.80, "output": 4.00},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "deepseek-chat": {"input": 0.14, "output": 0.28},
    "deepseek-reasoner": {"input": 0.55, "output": 2.19},
}

# Default model alias mappings
MODEL_ALIASES = {
    "opus": "claude-opus-4",
    "sonnet": "claude-sonnet-4",
    "haiku": "claude-haiku-3.5",
}


def find_workspace() -> Path:
    """Find the OpenClaw workspace directory."""
    candidates = [
        Path.home() / ".openclaw" / "workspace",
        Path("/home/openclaw/.openclaw/workspace"),
        Path.cwd(),
    ]
    for p in candidates:
        if (p / "SOUL.md").exists() or (p / "AGENTS.md").exists():
            return p
    return Path.cwd()


def read_file_safe(path: Path) -> str:
    """Read a file, returning empty string on error."""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except (OSError, PermissionError):
        return ""


def scan_workspace(workspace: Path) -> dict:
    """Scan workspace and return token analysis."""
    results = {
        "workspace": str(workspace),
        "token_method": TOKEN_METHOD,
        "files": [],
        "skills": [],
        "total_context_tokens": 0,
        "categories": {},
    }

    # Core workspace files
    core_files = [
        "SOUL.md", "AGENTS.md", "HEARTBEAT.md", "USER.md",
        "MEMORY.md", "TOOLS.md", "IDENTITY.md", "MISSION.md",
        "BOOTSTRAP.md",
    ]

    for fname in core_files:
        fpath = workspace / fname
        if fpath.exists():
            content = read_file_safe(fpath)
            tokens = count_tokens(content)
            results["files"].append({
                "name": fname,
                "path": str(fpath),
                "size_bytes": len(content.encode("utf-8")),
                "tokens": tokens,
                "category": "core",
            })
            results["total_context_tokens"] += tokens
            results["categories"].setdefault("core", 0)
            results["categories"]["core"] += tokens

    # Memory files (if loaded into context)
    memory_dir = workspace / "memory"
    if memory_dir.exists():
        for mf in sorted(memory_dir.glob("*.md")):
            content = read_file_safe(mf)
            tokens = count_tokens(content)
            results["files"].append({
                "name": f"memory/{mf.name}",
                "path": str(mf),
                "size_bytes": len(content.encode("utf-8")),
                "tokens": tokens,
                "category": "memory",
                "note": "loaded per AGENTS.md rules (daily + cross-session)",
            })
            # Only count today's + yesterday's + cross-session as always-loaded
            results["categories"].setdefault("memory", 0)
            results["categories"]["memory"] += tokens

    # Installed skills
    skill_dirs = []
    for skills_root in [workspace / "skills", Path.home() / ".openclaw" / "workspace" / "skills"]:
        if skills_root.exists():
            for skill_md in skills_root.rglob("SKILL.md"):
                skill_dir = skill_md.parent
                if skill_dir not in skill_dirs:
                    skill_dirs.append(skill_dir)

    for sd in skill_dirs:
        skill_tokens = 0
        skill_files = []
        # Only count files the agent actually loads (SKILL.md + direct scripts)
        # Skip node_modules, vendor dirs, large data files
        skip_dirs = {"node_modules", "vendor", ".git", "__pycache__", "dist", "build"}
        for sf in sd.rglob("*"):
            if sf.is_file() and sf.suffix in (".md", ".py", ".sh", ".js", ".ts", ".json"):
                if any(skip in sf.parts for skip in skip_dirs):
                    continue
                if sf.stat().st_size > 100_000:  # Skip files > 100KB
                    continue
                content = read_file_safe(sf)
                t = count_tokens(content)
                skill_tokens += t
                skill_files.append({"name": sf.name, "tokens": t})

        results["skills"].append({
            "name": sd.name,
            "path": str(sd),
            "total_tokens": skill_tokens,
            "files": sorted(skill_files, key=lambda x: -x["tokens"]),
        })
        results["categories"].setdefault("skills", 0)
        results["categories"]["skills"] += skill_tokens

    # Sort skills by token count
    results["skills"].sort(key=lambda x: -x["total_tokens"])

    # Recalculate total from all categories
    results["total_context_tokens"] = sum(results["categories"].values())

    return results


def estimate_costs(results: dict, model: str = "claude-opus-4",
                   heartbeats_per_day: int = 48,
                   interactions_per_day: int = 20,
                   avg_output_tokens: int = 500) -> dict:
    """Estimate monthly costs based on usage patterns."""
    pricing = MODEL_PRICING.get(model, MODEL_PRICING["claude-opus-4"])
    ctx = results["total_context_tokens"]

    # Each interaction = full context + response
    input_per_interaction = ctx
    output_per_interaction = avg_output_tokens

    # Heartbeats are typically shorter responses
    input_per_heartbeat = ctx
    output_per_heartbeat = 100  # HEARTBEAT_OK or short check

    daily_input = (input_per_interaction * interactions_per_day +
                   input_per_heartbeat * heartbeats_per_day)
    daily_output = (output_per_interaction * interactions_per_day +
                    output_per_heartbeat * heartbeats_per_day)

    monthly_input = daily_input * 30
    monthly_output = daily_output * 30

    input_cost = (monthly_input / 1_000_000) * pricing["input"]
    output_cost = (monthly_output / 1_000_000) * pricing["output"]

    return {
        "model": model,
        "pricing": pricing,
        "context_tokens_per_call": ctx,
        "daily_input_tokens": daily_input,
        "daily_output_tokens": daily_output,
        "monthly_input_tokens": monthly_input,
        "monthly_output_tokens": monthly_output,
        "monthly_input_cost": round(input_cost, 2),
        "monthly_output_cost": round(output_cost, 2),
        "monthly_total_cost": round(input_cost + output_cost, 2),
        "assumptions": {
            "interactions_per_day": interactions_per_day,
            "heartbeats_per_day": heartbeats_per_day,
            "avg_output_tokens": avg_output_tokens,
        }
    }


def generate_recommendations(results: dict) -> list:
    """Generate top optimization recommendations."""
    recs = []

    # Check MEMORY.md size
    for f in results["files"]:
        if f["name"] == "MEMORY.md" and f["tokens"] > 2000:
            recs.append({
                "priority": 1,
                "action": f"Trim MEMORY.md ({f['tokens']} tokens). Archive older entries. Target: <2000 tokens.",
                "savings_estimate": f"~{f['tokens'] - 1500} tokens/call",
                "category": "context_reduction",
            })

    # Check for large skills
    for skill in results["skills"][:3]:
        if skill["total_tokens"] > 3000:
            recs.append({
                "priority": 2,
                "action": f"Review skill '{skill['name']}' ({skill['total_tokens']} tokens). Consider trimming or lazy-loading.",
                "savings_estimate": f"Up to ~{skill['total_tokens']} tokens/call if removed",
                "category": "skill_optimization",
            })

    # Model routing suggestion
    recs.append({
        "priority": 3,
        "action": "Use model routing: Haiku/Sonnet for heartbeats and simple queries, Opus only for complex tasks.",
        "savings_estimate": "50-70% cost reduction on routine interactions",
        "category": "model_routing",
    })

    # Heartbeat frequency
    recs.append({
        "priority": 4,
        "action": "Review heartbeat frequency. Each heartbeat loads the full context window. Reduce frequency or batch checks.",
        "savings_estimate": "Linear with frequency reduction",
        "category": "heartbeat_tuning",
    })

    # Check for duplicate information
    core_tokens = results["categories"].get("core", 0)
    if core_tokens > 8000:
        recs.append({
            "priority": 5,
            "action": f"Core workspace files total {core_tokens} tokens. Look for overlapping info between SOUL.md, AGENTS.md, and USER.md.",
            "savings_estimate": "10-30% of core tokens",
            "category": "deduplication",
        })

    return sorted(recs, key=lambda x: x["priority"])[:5]


def format_report(results: dict, costs: dict, recs: list) -> str:
    """Format a human-readable report."""
    lines = []
    lines.append("=" * 60)
    lines.append("  TOKEN AUDIT REPORT")
    lines.append(f"  Workspace: {results['workspace']}")
    lines.append(f"  Method: {results['token_method']}")
    lines.append("=" * 60)
    lines.append("")

    # Context breakdown
    lines.append("CONTEXT WINDOW BREAKDOWN")
    lines.append("-" * 40)
    for cat, tokens in sorted(results["categories"].items(), key=lambda x: -x[1]):
        pct = (tokens / results["total_context_tokens"] * 100) if results["total_context_tokens"] > 0 else 0
        bar = "#" * int(pct / 2)
        lines.append(f"  {cat:12s} {tokens:>8,} tokens  ({pct:4.1f}%)  {bar}")
    lines.append(f"  {'TOTAL':12s} {results['total_context_tokens']:>8,} tokens")
    lines.append("")

    # Top files
    lines.append("TOP FILES BY TOKEN COUNT")
    lines.append("-" * 40)
    all_files = sorted(results["files"], key=lambda x: -x["tokens"])[:10]
    for f in all_files:
        lines.append(f"  {f['tokens']:>8,}  {f['name']}")
    lines.append("")

    # Skills
    if results["skills"]:
        lines.append("INSTALLED SKILLS BY TOKEN IMPACT")
        lines.append("-" * 40)
        for s in results["skills"][:8]:
            lines.append(f"  {s['total_tokens']:>8,}  {s['name']}")
        lines.append("")

    # Cost estimate
    lines.append(f"MONTHLY COST ESTIMATE ({costs['model']})")
    lines.append("-" * 40)
    lines.append(f"  Context per call:    {costs['context_tokens_per_call']:>10,} tokens")
    lines.append(f"  Daily input:         {costs['daily_input_tokens']:>10,} tokens")
    lines.append(f"  Daily output:        {costs['daily_output_tokens']:>10,} tokens")
    lines.append(f"  Monthly input cost:  ${costs['monthly_input_cost']:>9,.2f}")
    lines.append(f"  Monthly output cost: ${costs['monthly_output_cost']:>9,.2f}")
    lines.append(f"  MONTHLY TOTAL:       ${costs['monthly_total_cost']:>9,.2f}")
    lines.append(f"  (Assumes {costs['assumptions']['interactions_per_day']} interactions + "
                 f"{costs['assumptions']['heartbeats_per_day']} heartbeats/day)")
    lines.append("")

    # Compare models
    lines.append("COST COMPARISON ACROSS MODELS")
    lines.append("-" * 40)
    for model_name in ["claude-opus-4", "claude-sonnet-4", "claude-haiku-3.5", "gpt-4o", "gpt-4o-mini", "deepseek-chat"]:
        alt = estimate_costs(results, model=model_name)
        lines.append(f"  {model_name:20s}  ${alt['monthly_total_cost']:>9,.2f}/mo")
    lines.append("")

    # Recommendations
    lines.append("TOP OPTIMIZATION RECOMMENDATIONS")
    lines.append("-" * 40)
    for i, r in enumerate(recs, 1):
        lines.append(f"  {i}. {r['action']}")
        lines.append(f"     Potential savings: {r['savings_estimate']}")
        lines.append("")

    lines.append("NOTE: Not all tokens load every call. OpenClaw selectively")
    lines.append("loads skills and memory files based on context. These are")
    lines.append("MAXIMUM estimates assuming full context loading.")
    lines.append("")
    lines.append("=" * 60)
    lines.append("  Report generated by Token Audit (caelguard.com)")
    lines.append("  Built by Cael -- an OpenClaw agent who pays attention to costs")
    lines.append("=" * 60)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Token Audit -- OpenClaw cost analyzer")
    parser.add_argument("--workspace", "-w", type=str, help="Path to workspace")
    parser.add_argument("--model", "-m", type=str, default="claude-opus-4", help="Model for cost estimate")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--heartbeats", type=int, default=48, help="Heartbeats per day")
    parser.add_argument("--interactions", type=int, default=20, help="Interactions per day")
    args = parser.parse_args()

    workspace = Path(args.workspace) if args.workspace else find_workspace()
    model = MODEL_ALIASES.get(args.model, args.model)

    results = scan_workspace(workspace)
    costs = estimate_costs(results, model=model,
                          heartbeats_per_day=args.heartbeats,
                          interactions_per_day=args.interactions)
    recs = generate_recommendations(results)

    if args.json:
        output = {
            "scan": results,
            "costs": costs,
            "recommendations": recs,
        }
        print(json.dumps(output, indent=2))
    else:
        print(format_report(results, costs, recs))


if __name__ == "__main__":
    main()
