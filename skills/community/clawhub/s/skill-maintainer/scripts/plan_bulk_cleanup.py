#!/usr/bin/env python3
"""Plan clear delisting recommendations from a bulk-publishing risk lens."""

from __future__ import annotations

import argparse
import csv
import json
import shlex
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LOW_SIGNAL_VERDICTS = {"low_signal", "plausible_but_low_signal"}
DATA_UNAVAILABLE = "data_unavailable"


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


def engagement(row: dict[str, Any]) -> int:
    return to_int(row.get("installs_all_time")) + to_int(row.get("stars")) + to_int(row.get("comments"))


def is_data_unavailable(row: dict[str, Any]) -> bool:
    return (
        row.get("meaningfulness") == DATA_UNAVAILABLE
        or row.get("recommended_action") == DATA_UNAVAILABLE
        or row.get("portfolio_decision") == DATA_UNAVAILABLE
    )


def command_quote(*parts: str) -> str:
    return " ".join(shlex.quote(part) for part in parts)


def bulk_risk_features(row: dict[str, str]) -> tuple[int, list[str]]:
    if is_data_unavailable(row):
        return 0, ["detail_fetch_failed"]
    features: list[str] = []
    score = 0
    if row.get("meaningfulness") in LOW_SIGNAL_VERDICTS:
        score += 20
        features.append("low_or_plausible_low_signal")
    if engagement(row) == 0:
        score += 25
        features.append("zero_installs_stars_comments")
    if to_int(row.get("versions")) <= 1:
        score += 20
        features.append("single_version")
    if to_int(row.get("downloads")) < 100:
        score += 15
        features.append("downloads_under_100")
    elif to_int(row.get("downloads")) < 300:
        score += 10
        features.append("downloads_100_299")
    if to_int(row.get("tag_count")) <= 1:
        score += 8
        features.append("minimal_tags")
    if to_int(row.get("merge_family_size")) >= 3:
        score += 8
        features.append("repeated_family")
    if "single_version" in str(row.get("flags", "")):
        score += 4
    if engagement(row) > 0:
        score -= 25
    if to_int(row.get("versions")) >= 3:
        score -= 10
    if to_int(row.get("downloads")) >= 500:
        score -= 8
    return max(0, min(100, score)), features


def phase_for(row: dict[str, str]) -> tuple[str, str, str]:
    if is_data_unavailable(row):
        return (
            "data_unavailable",
            "No decision today",
            "Skill detail fetch failed; retry data collection before any keep, upgrade, hide, merge, or delete decision.",
        )
    zero_engagement = engagement(row) == 0
    single_version = to_int(row.get("versions")) <= 1
    low_signal = row.get("meaningfulness") in LOW_SIGNAL_VERDICTS
    downloads = to_int(row.get("downloads"))
    versions = to_int(row.get("versions"))

    if low_signal and zero_engagement and single_version and downloads < 100:
        return (
            "phase1_clear_hide",
            "Hide now",
            "Strong bulk-publishing signal: low/plausible-low, single version, zero engagement, downloads under 100.",
        )
    if low_signal and zero_engagement and single_version and downloads < 300:
        return (
            "phase2_hide_after_spotcheck",
            "Hide after spot-check",
            "Bulk-like single-version skill with zero engagement and only moderate downloads.",
        )
    if low_signal and zero_engagement and single_version:
        return (
            "phase3_upgrade_or_hide",
            "Upgrade within 7 days or hide",
            "Higher downloads, but still zero engagement and single version; keep public only if upgraded into a curated skill.",
        )
    if low_signal and zero_engagement and versions > 1 and row.get("portfolio_decision") == "merge_into_stronger_skill":
        return (
            "phase4_merge_or_hide",
            "Merge or hide",
            "Repeated family and zero engagement; reduce public surface through merge or hide.",
        )
    if low_signal and zero_engagement:
        return (
            "phase5_review_later",
            "Review later",
            "Zero engagement, but not an immediate single-version bulk tail candidate.",
        )
    return (
        "not_delist_now",
        "Do not delist now",
        "Has engagement, stronger evidence, or meaningful signal; handle through upgrade/curation.",
    )


def build_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    planned: list[dict[str, Any]] = []
    for row in rows:
        risk_score, features = bulk_risk_features(row)
        phase, recommendation, reason = phase_for(row)
        command = ""
        if phase in {"phase1_clear_hide", "phase2_hide_after_spotcheck", "phase3_upgrade_or_hide"}:
            command = command_quote("clawhub", "hide", row["slug"], "--yes")
        elif phase == "phase4_merge_or_hide" and row.get("merge_target_slug"):
            command = command_quote("clawhub", "skill", "merge", row["slug"], row["merge_target_slug"], "--yes")
        planned.append(
            {
                "phase": phase,
                "recommendation": recommendation,
                "bulk_risk_score": risk_score,
                "bulk_risk_features": "|".join(features),
                "slug": row.get("slug", ""),
                "display_name": row.get("display_name", ""),
                "downloads": row.get("downloads", ""),
                "installs_all_time": row.get("installs_all_time", ""),
                "stars": row.get("stars", ""),
                "comments": row.get("comments", ""),
                "versions": row.get("versions", ""),
                "meaning_score": row.get("meaning_score", ""),
                "meaningfulness": row.get("meaningfulness", ""),
                "category": row.get("category", ""),
                "portfolio_decision": row.get("portfolio_decision", ""),
                "detail_ok": row.get("detail_ok", ""),
                "detail_error": row.get("detail_error", ""),
                "merge_family_key": row.get("merge_family_key", ""),
                "merge_family_size": row.get("merge_family_size", ""),
                "merge_target_slug": row.get("merge_target_slug", ""),
                "reason": reason,
                "command": command,
            }
        )
    planned.sort(
        key=lambda row: (
            phase_rank(row["phase"]),
            -to_int(row.get("bulk_risk_score")),
            to_int(row.get("downloads")),
            row.get("slug", ""),
        )
    )
    return planned


def phase_rank(phase: str) -> int:
    order = {
        "phase1_clear_hide": 10,
        "phase2_hide_after_spotcheck": 20,
        "phase3_upgrade_or_hide": 30,
        "phase4_merge_or_hide": 40,
        "phase5_review_later": 50,
        "data_unavailable": 80,
        "not_delist_now": 90,
    }
    return order.get(phase, 999)


def write_command_script(path: Path, rows: list[dict[str, Any]], phase: str, title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    commands = [row["command"] for row in rows if row["phase"] == phase and row.get("command")]
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        f"echo {shlex.quote(title)}",
        "echo 'Commands are commented out. Un-comment only after explicit user approval.'",
        "",
        f"# Approval phrase: APPROVE {phase.upper()}",
        "",
    ]
    for command in commands:
        lines.append(f"# {command}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_bulk_approval_batches(planned: list[dict[str, Any]]) -> list[dict[str, Any]]:
    phase1 = [row for row in planned if row["phase"] == "phase1_clear_hide"]
    phase2 = [row for row in planned if row["phase"] == "phase2_hide_after_spotcheck"]
    phase3 = [row for row in planned if row["phase"] == "phase3_upgrade_or_hide"]
    phase4 = [row for row in planned if row["phase"] == "phase4_merge_or_hide"]
    batches: list[dict[str, Any]] = []
    if phase1:
        batches.append(bulk_batch("BULK_HIDE_PHASE1", "hide", "Hide strongest bulk-risk tail", "APPROVE BULK_HIDE_PHASE1", "medium", "reversible with clawhub unhide <slug>", phase1))
    if phase2:
        batches.append(bulk_batch("BULK_HIDE_PHASE2", "hide", "Spot-check then hide remaining single-version bulk tail", "APPROVE BULK_HIDE_PHASE2", "medium_high", "reversible with clawhub unhide <slug>", phase2))
    if phase3:
        batches.append(bulk_batch("BULK_UPGRADE_OR_HIDE_PHASE3", "upgrade_or_hide", "Upgrade within 7 days or hide", "APPROVE BULK_PHASE3_POLICY", "medium", "non-destructive if treated as upgrade queue; hide is reversible", phase3))
    if phase4:
        batches.append(bulk_batch("BULK_MERGE_OR_HIDE_PHASE4", "merge_or_hide", "Merge or hide repeated families", "APPROVE BULK_PHASE4_POLICY", "high", "merge reversibility is unknown; hide is reversible", phase4))
    return batches


def suppress_cleanup_for_partial_data(planned: list[dict[str, Any]], data_quality: dict[str, Any]) -> list[dict[str, Any]]:
    warnings = data_quality.get("warnings", [])
    suffix = "; ".join(str(warning) for warning in warnings[:3])
    reason = "Data quality is partial; do not hide, merge, or delete until a clean collection confirms the signal."
    if suffix:
        reason = f"{reason} Warnings: {suffix}"
    suppressed: list[dict[str, Any]] = []
    for row in planned:
        copy = dict(row)
        if copy.get("phase") != "data_unavailable":
            copy["phase"] = "not_delist_now"
            copy["recommendation"] = "Do not delist while data is partial"
            copy["reason"] = reason
            copy["command"] = ""
        suppressed.append(copy)
    suppressed.sort(key=lambda row: (phase_rank(row["phase"]), -to_int(row.get("downloads")), row.get("slug", "")))
    return suppressed


def bulk_batch(
    batch_id: str,
    operation: str,
    title: str,
    approval_phrase: str,
    risk: str,
    reversibility: str,
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    commands = [row["command"] for row in rows if row.get("command")]
    return {
        "batch_id": batch_id,
        "operation": operation,
        "title": title,
        "status": "pending_user_approval",
        "approval_phrase": approval_phrase,
        "risk": risk,
        "reversibility": reversibility,
        "item_count": len(rows),
        "command_count": len(commands),
        "max_downloads": max((to_int(row.get("downloads")) for row in rows), default=0),
        "total_downloads": sum(to_int(row.get("downloads")) for row in rows),
        "total_installs": sum(to_int(row.get("installs_all_time")) for row in rows),
        "total_stars": sum(to_int(row.get("stars")) for row in rows),
        "total_comments": sum(to_int(row.get("comments")) for row in rows),
        "commands": commands,
        "items": rows,
    }


def write_bulk_approval_manifest(path: Path, handle: str, batches: list[dict[str, Any]], data_quality: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "handle": handle,
                "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                "purpose": "bulk publishing risk reduction approval batches; no action has been executed",
                "data_quality": data_quality,
                "batches": batches,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def write_bulk_approval_board(path: Path, handle: str, batches: list[dict[str, Any]], data_quality: dict[str, Any]) -> None:
    lines = [
        f"# Bulk Cleanup Approval Board - {handle}",
        "",
        f"Generated: {datetime.now(timezone.utc).replace(microsecond=0).isoformat()}",
        "",
        "This board is specifically for reducing account risk caused by bulk-published public skills.",
        "No action has been executed.",
        f"Data quality: `{data_quality.get('status', 'unknown')}`.",
        "",
        "## Recommendation",
        "",
        "Prefer quality maintenance. Run bulk cleanup only when data quality is `ok` and the user explicitly asks for account-risk cleanup.",
        "",
    ]
    warnings = data_quality.get("warnings", [])
    if warnings:
        lines.extend(["## Data Quality Warnings", ""])
        for warning in warnings:
            lines.append(f"- {warning}")
        lines.extend(["", "Cleanup batches are suppressed until a clean data collection confirms the signal.", ""])
    for batch in batches:
        lines.extend(bulk_batch_markdown(batch))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def bulk_batch_markdown(batch: dict[str, Any]) -> list[str]:
    rows = batch["items"]
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
        f"- command count: {batch['command_count']}",
        f"- max downloads: {batch['max_downloads']}",
        f"- total installs/stars/comments: {batch['total_installs']}/{batch['total_stars']}/{batch['total_comments']}",
        "",
        "Evidence preview:",
    ]
    lines.extend(phase_table("Items", rows, limit=30))
    if batch["commands"]:
        lines.extend(["", "Command preview:", ""])
        for command in batch["commands"][:20]:
            lines.append(f"- `{command}`")
        if len(batch["commands"]) > 20:
            lines.append(f"- ... {len(batch['commands']) - 20} more commands")
    return lines


def write_report(path: Path, handle: str, planned: list[dict[str, Any]], data_quality: dict[str, Any]) -> None:
    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    counts = Counter(row["phase"] for row in planned)
    total = len(planned)
    phase1 = [row for row in planned if row["phase"] == "phase1_clear_hide"]
    phase2 = [row for row in planned if row["phase"] == "phase2_hide_after_spotcheck"]
    phase3 = [row for row in planned if row["phase"] == "phase3_upgrade_or_hide"]
    phase4 = [row for row in planned if row["phase"] == "phase4_merge_or_hide"]
    data_unavailable = [row for row in planned if row["phase"] == "data_unavailable"]
    lines = [
        f"# Bulk Cleanup Recommendation - {handle}",
        "",
        f"Generated: {generated}",
        "",
        "This report focuses on account-risk reduction from bulk publishing signals, not only product usefulness.",
        f"Data quality: `{data_quality.get('status', 'unknown')}`.",
        "",
        "## Clear Recommendation",
        "",
        f"- Hide phase 1 now: {len(phase1)} skills.",
        f"- Spot-check then hide phase 2: {len(phase2)} skills.",
        f"- Upgrade within 7 days or hide phase 3: {len(phase3)} skills.",
        f"- Merge or hide repeated families phase 4: {len(phase4)} skills.",
        f"- Data unavailable, no decision today: {len(data_unavailable)} skills.",
        "",
        "The strongest account-risk pattern is: low/plausible-low signal + single version + zero installs/stars/comments. The count varies by portfolio state.",
        "",
        "## Phase Counts",
        "",
    ]
    warnings = data_quality.get("warnings", [])
    if warnings:
        lines.extend(["## Data Quality Warnings", ""])
        for warning in warnings:
            lines.append(f"- {warning}")
        lines.extend(["", "Cleanup is suppressed while these warnings are present.", ""])
    for phase in [
        "phase1_clear_hide",
        "phase2_hide_after_spotcheck",
        "phase3_upgrade_or_hide",
        "phase4_merge_or_hide",
        "phase5_review_later",
        "data_unavailable",
        "not_delist_now",
    ]:
        lines.append(f"- {phase}: {counts.get(phase, 0)}")
    lines.extend(phase_table("Phase 1 Clear Hide", phase1, limit=40))
    lines.extend(phase_table("Phase 2 Hide After Spot-Check", phase2, limit=30))
    lines.extend(phase_table("Phase 3 Upgrade Or Hide", phase3, limit=30))
    lines.extend(phase_table("Phase 4 Merge Or Hide", phase4, limit=30))
    lines.extend(phase_table("Data Unavailable - No Decision Today", data_unavailable, limit=40))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def phase_table(title: str, rows: list[dict[str, Any]], limit: int) -> list[str]:
    keys = ["slug", "downloads", "versions", "meaning_score", "category", "bulk_risk_features", "reason"]
    lines = ["", f"## {title}", ""]
    if not rows:
        lines.append("No rows.")
        return lines
    lines.append("| " + " | ".join(keys) + " |")
    lines.append("| " + " | ".join("---" for _ in keys) + " |")
    for row in rows[:limit]:
        lines.append("| " + " | ".join(markdown_cell(row.get(key, "")) for key in keys) + " |")
    if len(rows) > limit:
        lines.extend(["", f"Showing first {limit} of {len(rows)} rows. See CSV for the full list."])
    return lines


def markdown_cell(value: Any) -> str:
    text = str(value).replace("\n", " ").replace("|", "\\|")
    return text[:200]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handle", default="harrylabsj")
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--out-dir", default="reports/bulk_cleanup")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    rows = read_csv(data_dir / "processed" / f"{args.handle}_skill_analysis.csv")
    analysis_summary = read_json(data_dir / "processed" / f"{args.handle}_summary.json")
    data_quality = analysis_summary.get("data_quality") if isinstance(analysis_summary.get("data_quality"), dict) else {}
    cleanup_allowed = bool(data_quality.get("cleanup_actions_allowed", True))
    planned = build_rows(rows)
    suppressed_cleanup_count = 0
    if not cleanup_allowed:
        suppressed_cleanup_count = sum(1 for row in planned if row.get("command"))
        planned = suppress_cleanup_for_partial_data(planned, data_quality)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    write_csv(out_dir / f"{args.handle}_bulk_cleanup_all.csv", planned)
    for phase in sorted({row["phase"] for row in planned}, key=phase_rank):
        write_csv(out_dir / f"{args.handle}_{phase}.csv", [row for row in planned if row["phase"] == phase])
    write_report(out_dir / f"{args.handle}_bulk_cleanup_report.md", args.handle, planned, data_quality)
    write_command_script(out_dir / f"{args.handle}_phase1_hide_commands.sh", planned, "phase1_clear_hide", "Phase 1 clear hide commands")
    write_command_script(out_dir / f"{args.handle}_phase2_hide_commands.sh", planned, "phase2_hide_after_spotcheck", "Phase 2 hide-after-spotcheck commands")
    batches = build_bulk_approval_batches(planned) if cleanup_allowed else []
    write_bulk_approval_manifest(out_dir / f"{args.handle}_bulk_approval_manifest.json", args.handle, batches, data_quality)
    write_bulk_approval_board(out_dir / f"{args.handle}_bulk_approval_board.md", args.handle, batches, data_quality)

    counts = Counter(row["phase"] for row in planned)
    summary = {
        "handle": args.handle,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "counts": dict(counts),
        "clear_hide_plus_spotcheck_hide": counts.get("phase1_clear_hide", 0) + counts.get("phase2_hide_after_spotcheck", 0),
        "approval_batches": len(batches),
        "data_quality": data_quality,
        "suppressed_cleanup_command_count": suppressed_cleanup_count,
    }
    (out_dir / f"{args.handle}_bulk_cleanup_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary["counts"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
