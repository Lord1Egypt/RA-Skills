"""Query detailed cost data for individual skills or compare two skills."""

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


def collect_skill_detail(
    skill_name: str,
    agents_dir: Path | None = None,
    cutoff=None,
    agent_filter: str | None = None,
) -> dict:
    """Collect detailed usage data for a single skill, broken down by model and day."""
    agents = discover_agents(agents_dir)
    if not agents:
        print("Error: No agents found.", file=sys.stderr)
        sys.exit(1)

    by_model: dict = defaultdict(lambda: {
        "tokens": 0, "input": 0, "output": 0,
        "cache_read": 0, "cache_write": 0,
        "cost": 0.0, "calls": 0,
    })
    by_day: dict = defaultdict(lambda: {"tokens": 0, "cost": 0.0, "calls": 0})
    total = {"tokens": 0, "cost": 0.0, "calls": 0, "sessions": set()}

    for agent_name, sessions_dir in agents:
        if agent_filter and agent_name != agent_filter:
            continue
        files = iter_session_files(sessions_dir, cutoff)
        for fpath in files:
            session_id = fpath.stem
            entries = parse_session_file(fpath)
            for entry in entries:
                data = extract_message_data(entry)
                if not data:
                    continue

                skills = data["skills"]
                if skill_name not in skills:
                    continue

                usage = data["usage"]
                model = data["model"]
                ts = data["timestamp"]

                total_calls = sum(skills.values())
                share = skills[skill_name] / total_calls
                msg_cost = compute_cost(usage, model)

                input_t, output_t, cache_r, cache_w = get_usage_tokens(usage)
                total_t = input_t + output_t

                m = by_model[model]
                m["tokens"] += int(total_t * share)
                m["input"] += int(input_t * share)
                m["output"] += int(output_t * share)
                m["cache_read"] += int(cache_r * share)
                m["cache_write"] += int(cache_w * share)
                m["cost"] += msg_cost * share
                m["calls"] += skills[skill_name]

                day = ts[:10] if len(ts) >= 10 else "unknown"
                d = by_day[day]
                d["tokens"] += int(total_t * share)
                d["cost"] += msg_cost * share
                d["calls"] += skills[skill_name]

                total["tokens"] += int(total_t * share)
                total["cost"] += msg_cost * share
                total["calls"] += skills[skill_name]
                total["sessions"].add(session_id)

    return {
        "skill": skill_name,
        "by_model": dict(by_model),
        "by_day": dict(sorted(by_day.items())),
        "total": total,
    }


def print_detail_text(detail: dict) -> None:
    """Print detailed text report for a single skill."""
    skill = detail["skill"]
    total = detail["total"]
    by_model = detail["by_model"]
    by_day = detail["by_day"]

    if not by_model:
        print(f"No usage data found for skill '{skill}'.")
        return

    print(f"\n=== Skill Detail: {skill} ===")
    print(f"Total cost: {format_cost(total['cost'])}")
    print(f"Total tokens: {format_tokens(total['tokens'])}")
    print(f"Total calls: {total['calls']}")
    print(f"Sessions: {len(total['sessions'])}")

    header = f"\n{'Model':<40} {'Calls':>6} {'Tokens':>10} {'Cost':>10}"
    sep = "\u2500" * len(header.strip())
    print(header)
    print(sep)
    for model, m in sorted(by_model.items(), key=lambda x: x[1]["cost"], reverse=True):
        print(
            f"{model:<40} "
            f"{m['calls']:>6} "
            f"{format_tokens(m['tokens']):>10} "
            f"{format_cost(m['cost']):>10}"
        )

    if by_day:
        print(f"\n{'Date':<12} {'Calls':>6} {'Tokens':>10} {'Cost':>10}")
        print(sep[:44])
        for day, d in by_day.items():
            print(
                f"{day:<12} "
                f"{d['calls']:>6} "
                f"{format_tokens(d['tokens']):>10} "
                f"{format_cost(d['cost']):>10}"
            )


def print_detail_json(detail: dict) -> None:
    """Print JSON detail for a single skill."""
    total = detail["total"]
    output = {
        "skill": detail["skill"],
        "total": {
            "cost": round(total["cost"], 4),
            "tokens": total["tokens"],
            "calls": total["calls"],
            "sessions": len(total["sessions"]),
        },
        "byModel": {
            model: {
                "calls": m["calls"],
                "tokens": m["tokens"],
                "input": m["input"],
                "output": m["output"],
                "cacheRead": m["cache_read"],
                "cacheWrite": m["cache_write"],
                "cost": round(m["cost"], 4),
            }
            for model, m in sorted(detail["by_model"].items(), key=lambda x: x[1]["cost"], reverse=True)
        },
        "byDay": {
            day: {"calls": d["calls"], "tokens": d["tokens"], "cost": round(d["cost"], 4)}
            for day, d in detail["by_day"].items()
        },
    }
    print(json.dumps(output, indent=2))


def compare_skills(
    skill1: str, skill2: str,
    agents_dir: Path | None = None,
    cutoff=None,
    agent_filter: str | None = None,
    fmt: str = "text",
) -> None:
    """Compare two skills side by side."""
    d1 = collect_skill_detail(skill1, agents_dir, cutoff, agent_filter)
    d2 = collect_skill_detail(skill2, agents_dir, cutoff, agent_filter)

    if fmt == "json":
        output = {
            "comparison": [
                {
                    "skill": d1["skill"],
                    "cost": round(d1["total"]["cost"], 4),
                    "tokens": d1["total"]["tokens"],
                    "calls": d1["total"]["calls"],
                },
                {
                    "skill": d2["skill"],
                    "cost": round(d2["total"]["cost"], 4),
                    "tokens": d2["total"]["tokens"],
                    "calls": d2["total"]["calls"],
                },
            ]
        }
        print(json.dumps(output, indent=2))
        return

    header = f"\n{'Metric':<20} {skill1:<20} {skill2:<20}"
    sep = "\u2500" * len(header.strip())
    print(header)
    print(sep)

    t1, t2 = d1["total"], d2["total"]
    rows = [
        ("Cost", format_cost(t1["cost"]), format_cost(t2["cost"])),
        ("Tokens", format_tokens(t1["tokens"]), format_tokens(t2["tokens"])),
        ("Calls", str(t1["calls"]), str(t2["calls"])),
        ("Sessions", str(len(t1["sessions"])), str(len(t2["sessions"]))),
    ]
    for label, v1, v2 in rows:
        print(f"{label:<20} {v1:<20} {v2:<20}")


def main():
    parser = argparse.ArgumentParser(
        description="Query skill-level cost details or compare skills."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    detail_p = sub.add_parser("detail", help="Show detailed cost data for a skill")
    detail_p.add_argument("skill", help="Skill name to query")
    detail_p.add_argument("--days", type=int, default=None)
    detail_p.add_argument("--since", type=str, default=None)
    detail_p.add_argument("--agent", type=str, default=None)
    detail_p.add_argument("--agents-dir", type=str, default=None)
    detail_p.add_argument("--format", choices=["text", "json"], default="text")

    compare_p = sub.add_parser("compare", help="Compare two skills side by side")
    compare_p.add_argument("skill1", help="First skill name")
    compare_p.add_argument("skill2", help="Second skill name")
    compare_p.add_argument("--days", type=int, default=None)
    compare_p.add_argument("--since", type=str, default=None)
    compare_p.add_argument("--agent", type=str, default=None)
    compare_p.add_argument("--agents-dir", type=str, default=None)
    compare_p.add_argument("--format", choices=["text", "json"], default="text")

    args = parser.parse_args()
    cutoff = parse_time_filter(days=args.days, since=args.since)
    agents_dir = Path(args.agents_dir) if args.agents_dir else None

    if args.command == "detail":
        detail = collect_skill_detail(
            args.skill, agents_dir=agents_dir, cutoff=cutoff, agent_filter=args.agent,
        )
        if args.format == "json":
            print_detail_json(detail)
        else:
            print_detail_text(detail)

    elif args.command == "compare":
        compare_skills(
            args.skill1, args.skill2,
            agents_dir=agents_dir, cutoff=cutoff,
            agent_filter=args.agent, fmt=args.format,
        )


if __name__ == "__main__":
    main()
