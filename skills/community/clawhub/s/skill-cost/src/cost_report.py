"""Generate per-skill token usage and cost reports from OpenClaw session logs."""

import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cost_utils import (
    discover_agents,
    iter_session_files,
    parse_session_file,
    extract_message_data,
    compute_cost,
    get_usage_tokens,
    parse_time_filter,
    format_tokens,
    format_cost,
    CATEGORY_BUILTIN,
    CATEGORY_CONVERSATION,
)


def collect_skill_data(
    agents_dir: Path | None = None,
    cutoff=None,
    agent_filter: str | None = None,
) -> dict:
    """Scan all sessions and aggregate usage by skill.

    Returns dict: {skill_name: {tokens, input, output, cache_read, cache_write, cost, calls, models}}
    """
    agents = discover_agents(agents_dir)
    if not agents:
        print("Error: No agents found. Check agents directory.", file=sys.stderr)
        sys.exit(1)

    stats: dict = defaultdict(lambda: {
        "tokens": 0,
        "input": 0,
        "output": 0,
        "cache_read": 0,
        "cache_write": 0,
        "cost": 0.0,
        "calls": 0,
        "models": defaultdict(int),
        "sessions": set(),
    })
    files_scanned = 0

    for agent_name, sessions_dir in agents:
        if agent_filter and agent_name != agent_filter:
            continue
        files = iter_session_files(sessions_dir, cutoff)
        for fpath in files:
            files_scanned += 1
            session_id = fpath.stem
            entries = parse_session_file(fpath)
            for entry in entries:
                data = extract_message_data(entry)
                if not data:
                    continue

                usage = data["usage"]
                model = data["model"]
                skills = data["skills"]
                total_calls = sum(skills.values())
                msg_cost = compute_cost(usage, model)

                input_t, output_t, cache_r, cache_w = get_usage_tokens(usage)
                total_t = input_t + output_t

                for skill_name, call_count in skills.items():
                    share = call_count / total_calls
                    s = stats[skill_name]
                    s["tokens"] += int(total_t * share)
                    s["input"] += int(input_t * share)
                    s["output"] += int(output_t * share)
                    s["cache_read"] += int(cache_r * share)
                    s["cache_write"] += int(cache_w * share)
                    s["cost"] += msg_cost * share
                    s["calls"] += call_count
                    s["models"][model] += call_count
                    s["sessions"].add(session_id)

    return {"stats": dict(stats), "files_scanned": files_scanned}


def print_text_report(data: dict, top_n: int | None = None) -> None:
    """Print a formatted text report of per-skill costs."""
    stats = data["stats"]
    if not stats:
        print("No usage data found.")
        return

    sorted_skills = sorted(stats.items(), key=lambda x: x[1]["cost"], reverse=True)
    if top_n:
        sorted_skills = sorted_skills[:top_n]

    total_cost = sum(s["cost"] for s in stats.values())
    total_tokens = sum(s["tokens"] for s in stats.values())

    header = f"{'Skill':<25} {'Calls':>6} {'Tokens':>10} {'Cost':>10} {'%':>5}"
    sep = "\u2500" * len(header)

    print(f"\n{sep}")
    print(header)
    print(sep)

    for skill_name, s in sorted_skills:
        pct = (s["cost"] / total_cost * 100) if total_cost > 0 else 0
        print(
            f"{skill_name:<25} "
            f"{s['calls']:>6} "
            f"{format_tokens(s['tokens']):>10} "
            f"{format_cost(s['cost']):>10} "
            f"{pct:>4.0f}%"
        )

    print(sep)
    print(
        f"{'Total':<25} "
        f"{sum(s['calls'] for s in stats.values()):>6} "
        f"{format_tokens(total_tokens):>10} "
        f"{format_cost(total_cost):>10} "
        f"{'100%':>5}"
    )
    print(f"\nFiles scanned: {data['files_scanned']}")


def print_json_report(data: dict, top_n: int | None = None) -> None:
    """Print a JSON report of per-skill costs."""
    stats = data["stats"]
    sorted_skills = sorted(stats.items(), key=lambda x: x[1]["cost"], reverse=True)
    if top_n:
        sorted_skills = sorted_skills[:top_n]

    total_cost = sum(s["cost"] for s in stats.values())
    total_tokens = sum(s["tokens"] for s in stats.values())

    skills_out = []
    for skill_name, s in sorted_skills:
        skills_out.append({
            "skill": skill_name,
            "calls": s["calls"],
            "tokens": {
                "total": s["tokens"],
                "input": s["input"],
                "output": s["output"],
                "cacheRead": s["cache_read"],
                "cacheWrite": s["cache_write"],
            },
            "cost": round(s["cost"], 4),
            "percentage": round(s["cost"] / total_cost * 100, 1) if total_cost > 0 else 0,
            "models": dict(s["models"]),
            "sessions": len(s["sessions"]),
        })

    output = {
        "skills": skills_out,
        "grandTotal": {
            "cost": round(total_cost, 4),
            "tokens": total_tokens,
            "calls": sum(s["calls"] for s in stats.values()),
        },
        "meta": {
            "filesScanned": data["files_scanned"],
        },
    }

    print(json.dumps(output, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Generate per-skill token usage and cost reports."
    )
    parser.add_argument(
        "--days", type=int, default=None,
        help="Only include data from the last N days",
    )
    parser.add_argument(
        "--since", type=str, default=None,
        help="Only include data since this date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--agent", type=str, default=None,
        help="Filter by agent name",
    )
    parser.add_argument(
        "--agents-dir", type=str, default=None,
        help="Custom agents directory (default: ~/.openclaw/agents)",
    )
    parser.add_argument(
        "--top", type=int, default=None,
        help="Show only top N skills by cost",
    )
    parser.add_argument(
        "--format", choices=["text", "json"], default="text",
        help="Output format (default: text)",
    )
    args = parser.parse_args()

    cutoff = parse_time_filter(days=args.days, since=args.since)
    agents_dir = Path(args.agents_dir) if args.agents_dir else None

    data = collect_skill_data(
        agents_dir=agents_dir,
        cutoff=cutoff,
        agent_filter=args.agent,
    )

    for s in data["stats"].values():
        s["sessions"] = s.get("sessions", set())

    if args.format == "json":
        print_json_report(data, top_n=args.top)
    else:
        print_text_report(data, top_n=args.top)


if __name__ == "__main__":
    main()
