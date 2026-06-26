#!/usr/bin/env python3
"""Generate safe maintenance action plans from scored ClawHub skill analysis."""

from __future__ import annotations

import argparse
import csv
import json
import shlex
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LOW_SIGNAL_VERDICTS = {"low_signal", "plausible_but_low_signal"}
DATA_UNAVAILABLE = "data_unavailable"
PUBLIC_UTILITY_CATEGORIES = {"Developer", "Data", "Knowledge", "Automation", "Shopping"}
DESTRUCTIVE_PLAN_NAMES = {"hide", "merge", "private_backlog"}


def to_int(value: Any) -> int:
    try:
        if value in (None, ""):
            return 0
        return int(float(value))
    except Exception:
        return 0


def to_float(value: Any) -> float:
    try:
        if value in (None, ""):
            return 0.0
        return float(value)
    except Exception:
        return 0.0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text("utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def command_quote(*parts: str) -> str:
    return " ".join(shlex.quote(part) for part in parts)


def engagement(row: dict[str, Any]) -> int:
    return to_int(row.get("installs_all_time")) + to_int(row.get("stars")) + to_int(row.get("comments"))


def is_low_signal(row: dict[str, Any]) -> bool:
    return row.get("meaningfulness") in LOW_SIGNAL_VERDICTS


def is_data_unavailable(row: dict[str, Any]) -> bool:
    return (
        row.get("meaningfulness") == DATA_UNAVAILABLE
        or row.get("recommended_action") == DATA_UNAVAILABLE
        or row.get("portfolio_decision") == DATA_UNAVAILABLE
    )


def maintenance_priority_rank(value: str) -> int:
    return {
        "P0_feedback": 0,
        "P1_maintain": 1,
        "P2_upgrade": 2,
        "P3_watch": 3,
        "P4_low_priority": 4,
        "P5_data_unavailable": 5,
    }.get(value, 9)


def quality_maintenance_plan(rows: list[dict[str, str]], *, limit: int) -> list[dict[str, Any]]:
    candidates = [
        row
        for row in rows
        if not is_data_unavailable(row)
        and (
            row.get("maintenance_priority") in {"P0_feedback", "P1_maintain", "P2_upgrade"}
            or to_float(row.get("quality_score")) >= 55
            or row.get("portfolio_decision") in {"fix_and_reply", "keep_public", "upgrade_public"}
        )
    ]
    candidates.sort(
        key=lambda row: (
            maintenance_priority_rank(row.get("maintenance_priority", "")),
            -to_float(row.get("quality_score")),
            -to_int(row.get("installs_all_time")),
            -to_int(row.get("stars")),
            -to_int(row.get("downloads")),
            row.get("slug", ""),
        )
    )
    return [
        plan_row(
            row,
            operation="maintain",
            command=command_quote("clawhub", "inspect", row["slug"], "--files"),
            risk="low",
        )
        for row in candidates[:limit]
    ]


def hide_plan(rows: list[dict[str, str]], *, limit: int, max_downloads: int) -> list[dict[str, Any]]:
    candidates = [
        row
        for row in rows
        if row.get("portfolio_decision") == "move_private_or_hide"
        and not is_data_unavailable(row)
        and is_low_signal(row)
        and engagement(row) == 0
        and to_int(row.get("downloads")) <= max_downloads
        and row.get("category") not in PUBLIC_UTILITY_CATEGORIES
    ]
    candidates.sort(key=lambda row: (to_int(row.get("downloads")), to_float(row.get("meaning_score")), row.get("slug", "")))
    return [
        plan_row(
            row,
            operation="hide",
            command=command_quote("clawhub", "hide", row["slug"], "--yes"),
            risk="low" if to_int(row.get("downloads")) < 80 else "medium",
        )
        for row in candidates[:limit]
    ]


def private_backlog_plan(rows: list[dict[str, str]], *, limit: int, max_downloads: int) -> list[dict[str, Any]]:
    candidates = [
        row
        for row in rows
        if row.get("portfolio_decision") == "move_private_or_hide"
        and not is_data_unavailable(row)
        and is_low_signal(row)
        and engagement(row) == 0
        and (
            row.get("category") in PUBLIC_UTILITY_CATEGORIES
            or to_int(row.get("downloads")) > max_downloads
        )
    ]
    candidates.sort(key=lambda row: (-to_int(row.get("downloads")), -to_float(row.get("meaning_score")), row.get("slug", "")))
    return [
        plan_row(
            row,
            operation="private_backlog",
            command="",
            risk="review",
        )
        for row in candidates[:limit]
    ]


def merge_plan(rows: list[dict[str, str]], *, limit: int) -> list[dict[str, Any]]:
    families: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if is_data_unavailable(row):
            continue
        family_key = row.get("merge_family_key", "")
        if family_key:
            families[family_key].append(row)

    planned: list[dict[str, Any]] = []
    for family_key, members in families.items():
        mergeable = [
            row
            for row in members
            if row.get("portfolio_decision") == "merge_into_stronger_skill"
            and not is_data_unavailable(row)
            and is_low_signal(row)
            and engagement(row) == 0
        ]
        if not mergeable:
            continue
        target = canonical_merge_target(members)
        target_slug = target.get("slug", "")
        for row in mergeable:
            source_slug = row.get("slug", "")
            if not source_slug or source_slug == target_slug:
                continue
            planned.append(
                plan_row(
                    row,
                    operation="merge",
                    command=command_quote("clawhub", "skill", "merge", source_slug, target_slug, "--yes"),
                    risk="medium",
                    target_slug=target_slug,
                    target_score=target.get("meaning_score", ""),
                    target_downloads=target.get("downloads", ""),
                )
            )
    planned.sort(
        key=lambda row: (
            -to_int(row.get("merge_family_size")),
            to_int(row.get("downloads")),
            row.get("merge_family_key", ""),
            row.get("slug", ""),
        )
    )
    return planned[:limit]


def canonical_merge_target(members: list[dict[str, str]]) -> dict[str, str]:
    return sorted(
        members,
        key=lambda row: (
            engagement(row),
            to_float(row.get("meaning_score")),
            to_int(row.get("downloads")),
            to_int(row.get("versions")),
            row.get("slug", ""),
        ),
        reverse=True,
    )[0]


def upgrade_plan(rows: list[dict[str, str]], *, limit: int) -> list[dict[str, Any]]:
    candidates = [
        row
        for row in rows
        if row.get("portfolio_decision") == "upgrade_public"
        and not is_data_unavailable(row)
        and row.get("meaningfulness") in {"low_signal", "plausible_but_low_signal", "needs_evidence"}
    ]
    candidates.sort(key=lambda row: (-to_int(row.get("downloads")), -to_float(row.get("meaning_score")), row.get("slug", "")))
    return [
        plan_row(
            row,
            operation="upgrade",
            command=command_quote("clawhub", "inspect", row["slug"], "--files"),
            risk="review",
        )
        for row in candidates[:limit]
    ]


def monitor_plan(rows: list[dict[str, str]], *, limit: int) -> list[dict[str, Any]]:
    candidates = [
        row
        for row in rows
        if row.get("portfolio_decision") == "monitor"
        and not is_data_unavailable(row)
        and is_low_signal(row)
    ]
    candidates.sort(key=lambda row: (-to_int(row.get("downloads")), -to_float(row.get("meaning_score")), row.get("slug", "")))
    return [plan_row(row, operation="monitor", command="", risk="watch") for row in candidates[:limit]]


def data_unavailable_plan(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    candidates = [row for row in rows if is_data_unavailable(row)]
    candidates.sort(key=lambda row: (row.get("slug", ""), row.get("display_name", "")))
    return [
        plan_row(
            row,
            operation="data_unavailable",
            command="",
            risk="blocked",
        )
        for row in candidates
    ]


def plan_row(
    row: dict[str, str],
    *,
    operation: str,
    command: str,
    risk: str,
    target_slug: str = "",
    target_score: Any = "",
    target_downloads: Any = "",
) -> dict[str, Any]:
    return {
        "operation": operation,
        "risk": risk,
        "slug": row.get("slug", ""),
        "display_name": row.get("display_name", ""),
        "target_slug": target_slug,
        "target_score": target_score,
        "target_downloads": target_downloads,
        "downloads": row.get("downloads", ""),
        "installs_all_time": row.get("installs_all_time", ""),
        "stars": row.get("stars", ""),
        "comments": row.get("comments", ""),
        "versions": row.get("versions", ""),
        "meaning_score": row.get("meaning_score", ""),
        "meaningfulness": row.get("meaningfulness", ""),
        "quality_score": row.get("quality_score", ""),
        "maintenance_priority": row.get("maintenance_priority", ""),
        "quality_reason": row.get("quality_reason", ""),
        "portfolio_decision": row.get("portfolio_decision", ""),
        "portfolio_reason": row.get("portfolio_reason", ""),
        "detail_ok": row.get("detail_ok", ""),
        "detail_error": row.get("detail_error", ""),
        "merge_family_key": row.get("merge_family_key", ""),
        "merge_family_size": row.get("merge_family_size", ""),
        "category": row.get("category", ""),
        "flags": row.get("flags", ""),
        "command": command,
    }


def write_review_script(path: Path, title: str, commands: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        f"echo {shlex.quote(title)}",
        "echo 'This file is intentionally safe: commands are commented out.'",
        "echo 'Review each line, then un-comment a small batch manually.'",
        "",
    ]
    for command in commands:
        lines.append(f"# {command}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def approval_batches(plans: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    quality_items = plans["quality_maintenance"][:25]
    hide_items = [row for row in plans["hide"] if to_int(row.get("downloads")) < 100][:25]
    merge_items = plans["merge"][:10]
    upgrade_items = plans["upgrade"][:20]
    private_items = plans["private_backlog"][:25]

    batches: list[dict[str, Any]] = []
    if quality_items:
        batches.append(
            approval_batch(
                "QUALITY_MAINTENANCE_001",
                "maintain",
                "Quality maintenance queue",
                "Review these high-quality or high-signal skills first for examples, metadata, and version upgrades.",
                "non-destructive inspection queue",
                "low",
                quality_items,
            )
        )
    if hide_items:
        batches.append(
            approval_batch(
                "HIDE_BATCH_001",
                "hide",
                "Low-risk public cleanup batch",
                "Approve hiding these low-signal, non-utility skills with zero installs, stars, and comments.",
                "reversible with clawhub unhide <slug>",
                "medium",
                hide_items,
            )
        )
    if merge_items:
        batches.append(
            approval_batch(
                "MERGE_BATCH_001",
                "merge",
                "Repeated-family consolidation batch",
                "Approve merging repeated template-family skills into the listed canonical targets.",
                "not known to be automatically reversible; review targets carefully",
                "high",
                merge_items,
            )
        )
    if upgrade_items:
        batches.append(
            approval_batch(
                "UPGRADE_BATCH_001",
                "upgrade",
                "High-download upgrade queue",
                "Approve using these skills as the first public improvement backlog.",
                "non-destructive",
                "low",
                upgrade_items,
            )
        )
    if private_items:
        batches.append(
            approval_batch(
                "PRIVATE_REVIEW_001",
                "private_backlog",
                "Utility-shaped private backlog review",
                "Approve manual review of public-utility shaped low-signal skills before any hide action.",
                "non-destructive review queue",
                "low",
                private_items,
            )
        )
    return batches


def approval_batch(
    batch_id: str,
    operation: str,
    title: str,
    question: str,
    reversibility: str,
    risk: str,
    items: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "batch_id": batch_id,
        "operation": operation,
        "title": title,
        "status": "pending_user_approval",
        "approval_phrase": f"APPROVE {batch_id}",
        "question": question,
        "risk": risk,
        "reversibility": reversibility,
        "item_count": len(items),
        "max_downloads": max((to_int(row.get("downloads")) for row in items), default=0),
        "total_downloads": sum(to_int(row.get("downloads")) for row in items),
        "total_installs": sum(to_int(row.get("installs_all_time")) for row in items),
        "total_stars": sum(to_int(row.get("stars")) for row in items),
        "total_comments": sum(to_int(row.get("comments")) for row in items),
        "commands": [row.get("command", "") for row in items if row.get("command")],
        "items": items,
    }


def write_approval_manifest(path: Path, handle: str, batches: list[dict[str, Any]], data_quality: dict[str, Any]) -> None:
    manifest = {
        "handle": handle,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "purpose": "approval-ready dry-run batches; no action has been executed",
        "data_quality": data_quality,
        "batches": batches,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def write_approval_board(path: Path, handle: str, batches: list[dict[str, Any]], data_quality: dict[str, Any]) -> None:
    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    lines = [
        f"# Approval Board - {handle}",
        "",
        f"Generated: {generated}",
        "",
        "This board is designed for user approval. It is analysis-only: no ClawHub action has been executed.",
        f"Data quality: `{data_quality.get('status', 'unknown')}`.",
        "",
        "## How To Approve",
        "",
        "Approve one batch at a time using the exact approval phrase shown in that section.",
        "Do not approve merge batches unless the canonical targets look right; the CLI does not expose an unmerge command.",
        "",
    ]
    warnings = data_quality.get("warnings", [])
    if warnings:
        lines.extend(["## Data Quality Warnings", ""])
        for warning in warnings:
            lines.append(f"- {warning}")
    for batch in batches:
        lines.extend(approval_batch_markdown(batch))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def approval_batch_markdown(batch: dict[str, Any]) -> list[str]:
    keys = ["slug", "target_slug", "downloads", "quality_score", "maintenance_priority", "category", "quality_reason"]
    rows = batch.get("items", [])
    lines = [
        "",
        f"## {batch['batch_id']} - {batch['title']}",
        "",
        f"- status: `{batch['status']}`",
        f"- approval phrase: `{batch['approval_phrase']}`",
        f"- operation: `{batch['operation']}`",
        f"- risk: `{batch['risk']}`",
        f"- reversibility: {batch['reversibility']}",
        f"- item count: {batch['item_count']}",
        f"- max downloads in batch: {batch['max_downloads']}",
        f"- total installs/stars/comments: {batch['total_installs']}/{batch['total_stars']}/{batch['total_comments']}",
        "",
        f"Decision question: {batch['question']}",
    ]
    if batch.get("commands"):
        lines.extend(["", "Command preview:", ""])
        for command in batch["commands"][:12]:
            lines.append(f"- `{command}`")
        if len(batch["commands"]) > 12:
            lines.append(f"- ... {len(batch['commands']) - 12} more commands")
    lines.extend(markdown_table("Evidence", rows, keys, limit=25))
    return lines


def write_approval_commands(path: Path, batches: list[dict[str, Any]]) -> None:
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        "echo 'Approval commands are commented out by default.'",
        "echo 'Uncomment only after the user gives the exact approval phrase for that batch.'",
        "",
    ]
    for batch in batches:
        lines.append(f"# {batch['batch_id']} - {batch['approval_phrase']}")
        lines.append(f"# Risk: {batch['risk']} | Reversibility: {batch['reversibility']}")
        for command in batch.get("commands", []):
            lines.append(f"# {command}")
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_markdown(path: Path, handle: str, plans: dict[str, list[dict[str, Any]]], data_quality: dict[str, Any]) -> None:
    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    total_quality = len(plans["quality_maintenance"])
    total_hide = len(plans["hide"])
    total_private_backlog = len(plans["private_backlog"])
    total_merge = len(plans["merge"])
    total_upgrade = len(plans["upgrade"])
    total_monitor = len(plans["monitor"])
    total_data_unavailable = len(plans["data_unavailable"])
    quality_status = data_quality.get("status", "unknown")
    quality_warnings = data_quality.get("warnings", [])
    lines = [
        f"# ClawHub Maintenance Action Plan - {handle}",
        "",
        f"Generated: {generated}",
        "",
        "This is a dry-run planning artifact. It does not execute ClawHub changes.",
        "",
        "## Summary",
        "",
        f"- quality maintenance queue: {total_quality}",
        f"- hide candidates: {total_hide}",
        f"- private backlog review: {total_private_backlog}",
        f"- merge commands: {total_merge}",
        f"- upgrade inspection queue: {total_upgrade}",
        f"- monitor queue: {total_monitor}",
        f"- data unavailable: {total_data_unavailable}",
        f"- data quality: {quality_status}",
        "",
        "## Safety Rules",
        "",
        "- Quality maintenance is the default lens; cleanup is secondary.",
        "- Skills with failed detail fetches are separated into `data_unavailable` and receive no decision today.",
        "- When data quality is partial, cleanup plans are suppressed and only non-destructive review queues remain.",
        "- Hide before delete. Current ClawHub CLI exposes `hide/unhide`, not a dedicated skill-private mode.",
        "- Generated shell files keep commands commented out by default.",
        "- Do not batch-hide skills with installs, stars, or comments without manual review.",
        "- Public utility categories go to private backlog review instead of the hide command batch.",
        "- Merge only when the target skill is a better canonical home for the capability family.",
        "",
    ]
    if quality_warnings:
        lines.extend(["## Data Quality Warnings", ""])
        for warning in quality_warnings:
            lines.append(f"- {warning}")
    lines.extend(markdown_table("Quality Maintenance Queue", plans["quality_maintenance"], ["slug", "downloads", "quality_score", "maintenance_priority", "category", "quality_reason"]))
    lines.extend(markdown_table("Hide Candidates", plans["hide"], ["slug", "downloads", "meaning_score", "category", "portfolio_reason"]))
    lines.extend(markdown_table("Private Backlog Review", plans["private_backlog"], ["slug", "downloads", "meaning_score", "category", "portfolio_reason"]))
    lines.extend(markdown_table("Merge Candidates", plans["merge"], ["slug", "target_slug", "merge_family_key", "downloads", "meaning_score"]))
    lines.extend(markdown_table("Upgrade Candidates", plans["upgrade"], ["slug", "downloads", "meaning_score", "category", "portfolio_reason"]))
    lines.extend(markdown_table("Monitor Candidates", plans["monitor"], ["slug", "downloads", "meaning_score", "category", "portfolio_reason"]))
    lines.extend(markdown_table("Data Unavailable - No Decision Today", plans["data_unavailable"], ["slug", "detail_ok", "detail_error", "portfolio_reason"]))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def markdown_table(title: str, rows: list[dict[str, Any]], keys: list[str], limit: int = 20) -> list[str]:
    lines = ["", f"## {title}", ""]
    if not rows:
        lines.append("No rows.")
        return lines
    lines.append("| " + " | ".join(keys) + " |")
    lines.append("| " + " | ".join("---" for _ in keys) + " |")
    for row in rows[:limit]:
        values = [markdown_cell(row.get(key, "")) for key in keys]
        lines.append("| " + " | ".join(values) + " |")
    if len(rows) > limit:
        lines.append("")
        lines.append(f"Showing first {limit} of {len(rows)} rows. See CSV for the full list.")
    return lines


def markdown_cell(value: Any) -> str:
    text = str(value).replace("\n", " ").replace("|", "\\|")
    return text[:180]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handle", default="harrylabsj")
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--out-dir", default="reports/action_plans")
    parser.add_argument("--approval-dir", default="reports/approval_packets")
    parser.add_argument("--hide-limit", type=int, default=200)
    parser.add_argument("--hide-max-downloads", type=int, default=180)
    parser.add_argument("--private-backlog-limit", type=int, default=1000)
    parser.add_argument("--merge-limit", type=int, default=200)
    parser.add_argument("--upgrade-limit", type=int, default=120)
    parser.add_argument("--monitor-limit", type=int, default=120)
    parser.add_argument("--quality-limit", type=int, default=120)
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.out_dir)
    rows = read_csv(data_dir / "processed" / f"{args.handle}_skill_analysis.csv")
    analysis_summary = read_json(data_dir / "processed" / f"{args.handle}_summary.json")
    data_quality = analysis_summary.get("data_quality") if isinstance(analysis_summary.get("data_quality"), dict) else {}
    destructive_allowed = bool(data_quality.get("destructive_actions_allowed", True))

    plans = {
        "quality_maintenance": quality_maintenance_plan(rows, limit=args.quality_limit),
        "hide": hide_plan(rows, limit=args.hide_limit, max_downloads=args.hide_max_downloads),
        "private_backlog": private_backlog_plan(rows, limit=args.private_backlog_limit, max_downloads=args.hide_max_downloads),
        "merge": merge_plan(rows, limit=args.merge_limit),
        "upgrade": upgrade_plan(rows, limit=args.upgrade_limit),
        "monitor": monitor_plan(rows, limit=args.monitor_limit),
        "data_unavailable": data_unavailable_plan(rows),
    }
    suppressed_counts = {name: len(plans[name]) for name in DESTRUCTIVE_PLAN_NAMES}
    if not destructive_allowed:
        for name in DESTRUCTIVE_PLAN_NAMES:
            plans[name] = []

    out_dir.mkdir(parents=True, exist_ok=True)
    for name, plan_rows in plans.items():
        write_csv(out_dir / f"{args.handle}_{name}_plan.csv", plan_rows)

    batches = approval_batches(plans)
    approval_dir = Path(args.approval_dir)
    write_approval_manifest(approval_dir / f"{args.handle}_approval_manifest.json", args.handle, batches, data_quality)
    write_approval_board(approval_dir / f"{args.handle}_approval_board.md", args.handle, batches, data_quality)
    write_approval_commands(approval_dir / f"{args.handle}_approval_commands.sh", batches)

    write_review_script(
        out_dir / f"{args.handle}_hide_review_commands.sh",
        f"Review hide candidates for {args.handle}",
        [row["command"] for row in plans["hide"] if row.get("command")],
    )
    write_review_script(
        out_dir / f"{args.handle}_merge_review_commands.sh",
        f"Review merge candidates for {args.handle}",
        [row["command"] for row in plans["merge"] if row.get("command")],
    )
    write_markdown(out_dir / f"{args.handle}_action_plan.md", args.handle, plans, data_quality)

    summary = {name: len(plan_rows) for name, plan_rows in plans.items()}
    summary["approval_batches"] = len(batches)
    summary["data_quality_status"] = data_quality.get("status", "unknown")
    if not destructive_allowed:
        summary["suppressed_cleanup_counts"] = suppressed_counts
    (out_dir / f"{args.handle}_action_plan_summary.json").write_text(
        json.dumps({"handle": args.handle, "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(), "data_quality": data_quality, "counts": summary}, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
