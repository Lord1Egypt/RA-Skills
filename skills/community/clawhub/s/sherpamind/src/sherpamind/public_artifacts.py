from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from .analysis import (
    get_dataset_summary,
    get_enrichment_coverage,
    list_open_ticket_ages,
    list_recent_account_activity,
    list_recent_tickets,
    list_technician_recent_load,
    list_ticket_attachment_summary,
    list_ticket_counts_by_status,
)
from .freshness import get_sync_freshness
from .paths import ensure_path_layout
from .summaries import (
    get_account_summary,
    get_technician_summary,
    get_ticket_summary,
    list_account_artifact_summaries,
    list_technician_artifact_summaries,
    list_ticket_artifact_summaries,
)
from .vector_exports import get_retrieval_readiness_summary
from .vector_index import get_vector_index_status


def _markdown_table(rows: list[dict], columns: list[tuple[str, str]]) -> str:
    if not rows:
        return "_No data available._"
    header = "| " + " | ".join(label for _, label in columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(key, "")) for key, _ in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def _safe_doc_name(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in name)[:80]


def _cleanup_stale_entity_docs(directory: Path, desired_paths: set[Path]) -> list[str]:
    removed: list[str] = []
    desired_names = {path.name for path in desired_paths}
    for existing in sorted(directory.glob("*.md")):
        if existing.name == "index.md":
            continue
        if existing.name in desired_names:
            continue
        existing.unlink()
        removed.append(str(existing))
    return removed


def _format_ratio(value: Any) -> str:
    if value is None:
        return ""
    try:
        return f"{float(value) * 100:.1f}%"
    except (TypeError, ValueError):
        return str(value)


def _format_number(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.1f}" if not value.is_integer() else str(int(value))
    return str(value)


def _top_metadata_gaps(coverage: dict[str, dict[str, Any]], *, count_key: str, limit: int = 12) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for field, stats in coverage.items():
        ratio = stats.get("ratio")
        rows.append({
            "field": field,
            count_key: stats.get(count_key, 0),
            "ratio": _format_ratio(ratio),
            "missing_ratio_value": 1.0 - float(ratio or 0.0),
        })
    rows.sort(key=lambda row: (-row["missing_ratio_value"], row["field"]))
    return [{k: v for k, v in row.items() if k != "missing_ratio_value"} for row in rows[:limit]]


def _source_materialization_gap_rows(coverage: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for field, stats in coverage.items():
        status = str(stats.get("status") or "")
        if status not in {"partial_materialization", "missing_materialization"}:
            continue
        rows.append({
            "field": field,
            "status": status,
            "source_documents": stats.get("source_documents", 0),
            "materialized_documents": stats.get("materialized_documents", 0),
            "promotion_gap": stats.get("promotion_gap_documents", 0),
            "materialized_ratio": _format_ratio(stats.get("materialized_document_ratio")),
        })
    rows.sort(key=lambda row: (-int(row["promotion_gap"] or 0), row["field"]))
    return rows


def _invalid_source_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in summary.get("fields_with_invalid_source") or []:
        rows.append({
            "field": item.get("field", "unknown"),
            "raw_ticket_rows": item.get("raw_ticket_rows", 0),
            "raw_detail_rows": item.get("raw_detail_rows", 0),
            "invalid_ticket_rows": item.get("invalid_ticket_rows", 0),
            "invalid_detail_rows": item.get("invalid_detail_rows", 0),
            "source_documents": item.get("source_documents", 0),
        })
    rows.sort(key=lambda row: (-(int(row["invalid_ticket_rows"] or 0) + int(row["invalid_detail_rows"] or 0)), row["field"]))
    return rows


def _upstream_absent_rows(coverage: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for field, stats in coverage.items():
        if str(stats.get("status") or "") != "upstream_absent":
            continue
        rows.append({
            "field": field,
            "ticket_rows": stats.get("ticket_rows", 0),
            "detail_rows": stats.get("detail_rows", 0),
            "source_documents": stats.get("source_documents", 0),
            "materialized_documents": stats.get("materialized_documents", 0),
        })
    rows.sort(key=lambda row: row["field"])
    return rows


def _entity_label_quality_rows(entity_quality: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for entity, stats in entity_quality.items():
        rows.append({
            "entity": entity,
            "readable_ratio": _format_ratio(stats.get("readable_ratio")),
            "identifier_like_ratio": _format_ratio(stats.get("identifier_like_ratio")),
            "fallback_source_ratio": _format_ratio(stats.get("fallback_source_ratio")),
            "sample_identifier_values": ", ".join(stats.get("identifier_like_distinct_value_sample", [])[:3]),
        })
    return rows


def _retrieval_signal_pressure_rows(summary: dict[str, Any], dimension: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in ((summary.get("retrieval_signal_pressure") or {}).get(dimension) or {}).get("rows", []):
        rows.append({
            "label": row.get("label", "unknown"),
            "documents": row.get("total_documents", 0),
            "richness_ratio": _format_ratio(row.get("richness_ratio")),
            "detail_ratio": _format_ratio(row.get("detail_ratio")),
            "action_ratio": _format_ratio(row.get("action_ratio")),
            "activity_ratio": _format_ratio(row.get("activity_ratio")),
            "resolution_ratio": _format_ratio(row.get("resolution_ratio")),
            "attachment_ratio": _format_ratio(row.get("attachment_ratio")),
            "lagging_ratio": _format_ratio(row.get("lagging_ratio")),
            "low_richness_backlog": row.get("low_richness_backlog", 0),
            "latest_activity_at": row.get("latest_activity_at", ""),
        })
    return rows


def _detail_gap_rows(coverage: dict[str, Any], dimension: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in ((coverage.get("detail_gap_pressure") or {}).get(dimension) or {}).get("rows", []):
        rows.append({
            "label": row.get("label", "unknown"),
            "tickets": row.get("total_tickets", 0),
            "detail_tickets": row.get("detail_tickets", 0),
            "detail_ratio": _format_ratio(row.get("detail_ratio")),
            "detail_backlog": row.get("detail_backlog", 0),
            "open_without_detail": row.get("open_without_detail", 0),
            "warm_closed_without_detail": row.get("warm_closed_without_detail", 0),
            "latest_activity_at": row.get("latest_activity_at", ""),
        })
    return rows


def _source_breakdown_rows(source_counts: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source, stats in source_counts.items():
        rows.append({
            "source": source,
            "chunks": stats.get("chunks", 0),
            "ratio": _format_ratio(stats.get("ratio")),
        })
    rows.sort(key=lambda row: (-int(row["chunks"] or 0), row["source"]))
    return rows


def _freshness_status_rows(freshness: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for status, stats in (freshness.get("status_breakdown") or {}).items():
        rows.append({
            "status": status,
            "documents": stats.get("documents", 0),
            "lagging_documents": stats.get("lagging_documents", 0),
            "lagging_ratio": _format_ratio(stats.get("lagging_ratio")),
        })
    rows.sort(key=lambda row: row["status"])
    return rows


def _freshness_bucket_rows(freshness: dict[str, Any]) -> list[dict[str, Any]]:
    labels = {
        "lag_le_15m": "<=15m",
        "lag_le_1h": "<=1h",
        "lag_le_6h": "<=6h",
        "lag_le_24h": "<=24h",
        "lag_gt_24h": ">24h",
    }
    rows: list[dict[str, Any]] = []
    for bucket_name, stats in (freshness.get("lag_buckets") or {}).items():
        rows.append({
            "bucket": labels.get(bucket_name, bucket_name),
            "documents": stats.get("documents", 0),
            "ratio": _format_ratio(stats.get("ratio")),
            "bucket_sort": ["lag_le_15m", "lag_le_1h", "lag_le_6h", "lag_le_24h", "lag_gt_24h"].index(bucket_name) if bucket_name in labels else 999,
        })
    rows.sort(key=lambda row: row["bucket_sort"])
    return [{k: v for k, v in row.items() if k != "bucket_sort"} for row in rows]


def _top_lagging_document_rows(freshness: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in freshness.get("top_lagging_documents") or []:
        rows.append({
            "ticket_id": item.get("ticket_id", ""),
            "status": item.get("status", ""),
            "account": item.get("account", ""),
            "technician": item.get("technician", ""),
            "lag_minutes": _format_number(item.get("lag_minutes")),
        })
    return rows


def _entity_retrieval_health_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    return [{
        "detail_coverage": _format_ratio(summary.get("detail_coverage_ratio")),
        "document_coverage": _format_ratio(summary.get("document_coverage_ratio")),
        "action_cue_coverage": _format_ratio(summary.get("action_cue_ratio")),
        "resolution_summary_coverage": _format_ratio(summary.get("resolution_summary_ratio")),
        "multi_chunk_ratio": _format_ratio(summary.get("multi_chunk_ratio")),
        "lagging_ratio": _format_ratio(summary.get("lagging_ratio")),
        "avg_lag_minutes": _format_number(summary.get("avg_lag_minutes")),
        "max_lag_minutes": _format_number(summary.get("max_lag_minutes")),
        "latest_chunk_synced_at": summary.get("latest_chunk_synced_at") or "",
    }]


def _entity_lag_bucket_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    labels = {
        "current_or_ahead": "Current/Ahead",
        "lag_le_15m": "<=15m",
        "lag_le_1h": "<=1h",
        "lag_le_6h": "<=6h",
        "lag_le_24h": "<=24h",
        "lag_gt_24h": ">24h",
        "missing_chunk_synced_at": "Missing Chunk Sync",
        "missing_updated_at": "Missing Updated At",
    }
    order = list(labels.keys())
    rows: list[dict[str, Any]] = []
    buckets = summary.get("lag_buckets") or {}
    total = sum(int(value or 0) for value in buckets.values())
    for key in order:
        count = int(buckets.get(key) or 0)
        rows.append({
            "bucket": labels[key],
            "tickets": count,
            "ratio": _format_ratio((count / total) if total else 0.0),
        })
    return rows


def _entity_metadata_coverage_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for field, stats in (summary.get("metadata_coverage") or {}).items():
        rows.append({
            "field": field,
            "tickets": stats.get("tickets", 0),
            "ratio": _format_ratio(stats.get("ratio")),
        })
    rows.sort(key=lambda row: (-float(str(row["ratio"]).rstrip('%') or 0), row["field"]))
    return rows


def _vector_drift_chunk_rows(rows: list[dict[str, Any]], *, count_key: str | None = None) -> list[dict[str, Any]]:
    formatted: list[dict[str, Any]] = []
    for item in rows:
        row = {
            "ticket_id": item.get("ticket_id", ""),
            "chunk_id": item.get("chunk_id", ""),
            "chunk_index": item.get("chunk_index", ""),
            "status": item.get("status", ""),
            "account": item.get("account", ""),
            "technician": item.get("technician", ""),
        }
        if count_key:
            row[count_key] = item.get(count_key, 0)
        formatted.append(row)
    return formatted


def _vector_drift_dangling_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "ticket_id": item.get("ticket_id", ""),
            "chunk_id": item.get("chunk_id", ""),
            "dims": item.get("dims", ""),
            "index_synced_at": item.get("index_synced_at", ""),
        }
        for item in rows
    ]


def generate_public_snapshot(db_path: Path) -> dict:
    paths = ensure_path_layout()
    generated_at = datetime.now(timezone.utc).isoformat()

    dataset_summary = get_dataset_summary(db_path)
    enrichment_coverage = get_enrichment_coverage(db_path)
    sync_freshness = get_sync_freshness(db_path)
    status_counts = list_ticket_counts_by_status(db_path)
    open_ages = list_open_ticket_ages(db_path, limit=10)
    account_activity = list_recent_account_activity(db_path, days=7, limit=10)
    technician_load = list_technician_recent_load(db_path, days=7, limit=10)
    attachment_summary = list_ticket_attachment_summary(db_path, limit=10)
    recent_tickets = list_recent_tickets(db_path, limit=10)
    account_summaries = list_account_artifact_summaries(db_path)
    technician_summaries = list_technician_artifact_summaries(db_path)
    ticket_summaries = list_ticket_artifact_summaries(db_path)
    retrieval_readiness = get_retrieval_readiness_summary(db_path)
    vector_index_status = get_vector_index_status(db_path)

    account_dir = paths.docs_root / "accounts"
    technician_dir = paths.docs_root / "technicians"
    ticket_dir = paths.docs_root / "tickets"
    account_dir.mkdir(parents=True, exist_ok=True)
    technician_dir.mkdir(parents=True, exist_ok=True)
    ticket_dir.mkdir(parents=True, exist_ok=True)

    snapshot_path = paths.docs_root / "insight-snapshot.md"
    snapshot_md = [
        "# SherpaMind Public Insight Snapshot",
        "",
        f"Generated: `{generated_at}`",
        "",
        "## Dataset summary",
        "",
        "```json",
        json.dumps(dataset_summary, indent=2),
        "```",
        "",
        "## Enrichment coverage",
        "",
        "```json",
        json.dumps(enrichment_coverage, indent=2),
        "```",
        "",
        "## Enrichment pressure — under-covered accounts",
        "",
        _markdown_table(_detail_gap_rows(enrichment_coverage, "accounts"), [
            ("label", "Account"),
            ("tickets", "Tickets"),
            ("detail_tickets", "Detail Tickets"),
            ("detail_ratio", "Detail Coverage"),
            ("detail_backlog", "Backlog"),
            ("open_without_detail", "Open Missing Detail"),
            ("warm_closed_without_detail", "Warm Closed Missing Detail"),
        ]),
        "",
        "## Enrichment pressure — under-covered categories",
        "",
        _markdown_table(_detail_gap_rows(enrichment_coverage, "categories"), [
            ("label", "Category"),
            ("tickets", "Tickets"),
            ("detail_tickets", "Detail Tickets"),
            ("detail_ratio", "Detail Coverage"),
            ("detail_backlog", "Backlog"),
            ("open_without_detail", "Open Missing Detail"),
            ("warm_closed_without_detail", "Warm Closed Missing Detail"),
        ]),
        "",
        "## Enrichment pressure — under-covered technicians",
        "",
        _markdown_table(_detail_gap_rows(enrichment_coverage, "technicians"), [
            ("label", "Technician"),
            ("tickets", "Tickets"),
            ("detail_tickets", "Detail Tickets"),
            ("detail_ratio", "Detail Coverage"),
            ("detail_backlog", "Backlog"),
            ("open_without_detail", "Open Missing Detail"),
            ("warm_closed_without_detail", "Warm Closed Missing Detail"),
        ]),
        "",
        "## Sync freshness",
        "",
        "```json",
        json.dumps(sync_freshness, indent=2),
        "```",
        "",
        "## Status counts",
        "",
        _markdown_table(status_counts, [("status", "Status"), ("ticket_count", "Ticket Count")]),
        "",
        "## Oldest open tickets",
        "",
        _markdown_table(open_ages, [
            ("id", "Ticket ID"),
            ("subject", "Subject"),
            ("account", "Account"),
            ("technician", "Technician"),
            ("age_days", "Age Days"),
            ("days_since_update", "Days Since Update"),
        ]),
        "",
        "## Recent account activity (7d)",
        "",
        _markdown_table(account_activity, [
            ("account", "Account"),
            ("ticket_count", "Tickets"),
            ("open_count", "Open"),
            ("closed_count", "Closed"),
            ("latest_activity_at", "Latest Activity"),
        ]),
        "",
        "## Recent technician load (7d)",
        "",
        _markdown_table(technician_load, [
            ("technician", "Technician"),
            ("ticket_count", "Tickets"),
            ("open_count", "Open"),
            ("closed_count", "Closed"),
            ("latest_activity_at", "Latest Activity"),
        ]),
        "",
        "## Retrieval metadata readiness",
        "",
        "```json",
        json.dumps(enrichment_coverage.get("metadata", {}), indent=2),
        "```",
        "",
        "## Account artifact coverage",
        "",
        _markdown_table(account_summaries[:10], [
            ("account", "Account"),
            ("total_tickets", "Tickets"),
            ("detail_tickets", "Detail Tickets"),
            ("log_tickets", "Log Tickets"),
            ("attachment_tickets", "Attachment Tickets"),
            ("document_tickets", "Document Tickets"),
            ("chunk_count", "Chunks"),
        ]),
        "",
        "## Technician artifact coverage",
        "",
        _markdown_table(technician_summaries[:10], [
            ("technician", "Technician"),
            ("total_tickets", "Tickets"),
            ("detail_tickets", "Detail Tickets"),
            ("log_tickets", "Log Tickets"),
            ("attachment_tickets", "Attachment Tickets"),
            ("document_tickets", "Document Tickets"),
            ("chunk_count", "Chunks"),
        ]),
        "",
        "## Ticket artifact coverage",
        "",
        _markdown_table(ticket_summaries[:10], [
            ("ticket_id", "Ticket ID"),
            ("ticket_number", "Ticket #"),
            ("status", "Status"),
            ("account", "Account"),
            ("technician", "Technician"),
            ("detail_available", "Detail"),
            ("log_count", "Logs"),
            ("attachment_count", "Attachments"),
            ("chunk_count", "Chunks"),
        ]),
        "",
        "## Attachment metadata summary",
        "",
        _markdown_table(attachment_summary, [
            ("ticket_id", "Ticket ID"),
            ("subject", "Subject"),
            ("attachment_count", "Attachments"),
            ("total_attachment_bytes", "Total Bytes"),
            ("latest_attachment_at", "Latest Attachment"),
        ]),
        "",
        "## Recent tickets",
        "",
        _markdown_table(recent_tickets, [
            ("id", "Ticket ID"),
            ("subject", "Subject"),
            ("status", "Status"),
            ("account", "Account"),
            ("technician", "Technician"),
            ("updated_at", "Updated"),
        ]),
        "",
        "## Notes",
        "",
        "- This file is a derived public artifact for OpenClaw-friendly consumption.",
        "- Canonical truth remains in `.SherpaMind/private/data/sherpamind.sqlite3`.",
        "- Attachment bodies are not downloaded by default; this snapshot reflects metadata only.",
    ]
    snapshot_path.write_text("\n".join(snapshot_md) + "\n")

    retrieval_path = paths.docs_root / "retrieval-readiness.md"
    retrieval_md = [
        "# SherpaMind Retrieval Readiness",
        "",
        f"Generated: `{generated_at}`",
        "",
        "## Summary",
        "",
        f"- Documents: `{retrieval_readiness.get('document_count', 0)}`",
        f"- Chunks: `{retrieval_readiness.get('chunk_count', 0)}`",
        f"- Indexed chunks: `{vector_index_status.get('indexed_chunks', 0)}` / `{vector_index_status.get('total_chunk_rows', 0)}`",
        f"- Vector ready ratio: `{_format_ratio(vector_index_status.get('ready_ratio'))}`",
        f"- Materialization version: `{retrieval_readiness.get('materialization', {}).get('current_version')}`",
        f"- Current-version chunk ratio: `{_format_ratio(retrieval_readiness.get('materialization', {}).get('chunk_rows_at_current_version_ratio'))}`",
        "",
        "## Chunk quality",
        "",
        _markdown_table([
            {
                "avg_chunk_chars": _format_number(retrieval_readiness.get("chunk_quality", {}).get("avg_chunk_chars")),
                "min_chunk_chars": retrieval_readiness.get("chunk_quality", {}).get("min_chunk_chars", 0),
                "max_chunk_chars": retrieval_readiness.get("chunk_quality", {}).get("max_chunk_chars", 0),
                "tiny_chunk_count": retrieval_readiness.get("chunk_quality", {}).get("tiny_chunk_count", 0),
                "over_target_chunk_count": retrieval_readiness.get("chunk_quality", {}).get("over_target_chunk_count", 0),
            }
        ], [
            ("avg_chunk_chars", "Avg Chunk Chars"),
            ("min_chunk_chars", "Min"),
            ("max_chunk_chars", "Max"),
            ("tiny_chunk_count", "Tiny Chunks"),
            ("over_target_chunk_count", "Over Target"),
        ]),
        "",
        "## Document chunk topology",
        "",
        _markdown_table([
            {
                "avg_chunks_per_document": _format_number(retrieval_readiness.get("document_chunk_topology", {}).get("avg_chunks_per_document")),
                "single_chunk_document_count": retrieval_readiness.get("document_chunk_topology", {}).get("single_chunk_document_count", 0),
                "multi_chunk_document_count": retrieval_readiness.get("document_chunk_topology", {}).get("multi_chunk_document_count", 0),
                "multi_chunk_document_ratio": _format_ratio(retrieval_readiness.get("document_chunk_topology", {}).get("multi_chunk_document_ratio")),
                "max_chunks_per_document": retrieval_readiness.get("document_chunk_topology", {}).get("max_chunks_per_document", 0),
            }
        ], [
            ("avg_chunks_per_document", "Avg Chunks / Doc"),
            ("single_chunk_document_count", "Single-Chunk Docs"),
            ("multi_chunk_document_count", "Multi-Chunk Docs"),
            ("multi_chunk_document_ratio", "Multi-Chunk Ratio"),
            ("max_chunks_per_document", "Max Chunks / Doc"),
        ]),
        "",
        "## Freshness windows",
        "",
        _markdown_table([
            {
                "earliest_updated_at": retrieval_readiness.get("freshness", {}).get("earliest_updated_at", ""),
                "latest_updated_at": retrieval_readiness.get("freshness", {}).get("latest_updated_at", ""),
                "earliest_chunk_synced_at": retrieval_readiness.get("freshness", {}).get("earliest_chunk_synced_at", ""),
                "latest_chunk_synced_at": retrieval_readiness.get("freshness", {}).get("latest_chunk_synced_at", ""),
            }
        ], [
            ("earliest_updated_at", "Earliest Ticket Update"),
            ("latest_updated_at", "Latest Ticket Update"),
            ("earliest_chunk_synced_at", "Chunk Sync Started"),
            ("latest_chunk_synced_at", "Chunk Sync Finished"),
        ]),
        "",
        "## Materialization lag summary",
        "",
        _markdown_table([
            {
                "documents_with_timestamps": retrieval_readiness.get("freshness", {}).get("document_count_with_timestamps", 0),
                "documents_materialized_behind": retrieval_readiness.get("freshness", {}).get("documents_materialized_behind", 0),
                "lagging_document_ratio": _format_ratio(retrieval_readiness.get("freshness", {}).get("lagging_document_ratio")),
                "avg_lag_minutes": _format_number(retrieval_readiness.get("freshness", {}).get("avg_lag_minutes")),
                "max_lag_minutes": _format_number(retrieval_readiness.get("freshness", {}).get("max_lag_minutes")),
                "documents_missing_any_timestamp": retrieval_readiness.get("freshness", {}).get("documents_missing_any_timestamp", 0),
            }
        ], [
            ("documents_with_timestamps", "Docs With Timestamps"),
            ("documents_materialized_behind", "Lagging Docs"),
            ("lagging_document_ratio", "Lagging Ratio"),
            ("avg_lag_minutes", "Avg Lag Minutes"),
            ("max_lag_minutes", "Max Lag Minutes"),
            ("documents_missing_any_timestamp", "Missing Any Timestamp"),
        ]),
        "",
        "## Materialization lag by ticket status",
        "",
        _markdown_table(
            _freshness_status_rows(retrieval_readiness.get("freshness", {})),
            [("status", "Status"), ("documents", "Documents"), ("lagging_documents", "Lagging Docs"), ("lagging_ratio", "Lagging Ratio")],
        ),
        "",
        "## Materialization lag buckets",
        "",
        _markdown_table(
            _freshness_bucket_rows(retrieval_readiness.get("freshness", {})),
            [("bucket", "Lag Bucket"), ("documents", "Documents"), ("ratio", "Coverage")],
        ),
        "",
        "## Top lagging documents",
        "",
        _markdown_table(
            _top_lagging_document_rows(retrieval_readiness.get("freshness", {})),
            [("ticket_id", "Ticket ID"), ("status", "Status"), ("account", "Account"), ("technician", "Technician"), ("lag_minutes", "Lag Minutes")],
        ),
        "",
        "## Materialization and vector status",
        "",
        _markdown_table([
            {
                "stale_docs": retrieval_readiness.get("materialization", {}).get("stale_docs", 0),
                "unversioned_docs": retrieval_readiness.get("materialization", {}).get("unversioned_docs", 0),
                "missing_index_rows": vector_index_status.get("missing_index_rows", 0),
                "dangling_index_rows": vector_index_status.get("dangling_index_rows", 0),
                "outdated_content_rows": vector_index_status.get("outdated_content_rows", 0),
            }
        ], [
            ("stale_docs", "Stale Docs"),
            ("unversioned_docs", "Unversioned Docs"),
            ("missing_index_rows", "Missing Index Rows"),
            ("dangling_index_rows", "Dangling Index Rows"),
            ("outdated_content_rows", "Outdated Index Rows"),
        ]),
        "",
        "## Missing vector chunk samples",
        "",
        _markdown_table(
            _vector_drift_chunk_rows((vector_index_status.get("drift_samples") or {}).get("missing_chunks", [])),
            [("ticket_id", "Ticket ID"), ("chunk_id", "Chunk ID"), ("chunk_index", "Chunk #"), ("status", "Status"), ("account", "Account"), ("technician", "Technician")],
        ),
        "",
        "## Documents with missing vector chunks",
        "",
        _markdown_table(
            _vector_drift_chunk_rows((vector_index_status.get("drift_samples") or {}).get("missing_documents", []), count_key="missing_chunks"),
            [("ticket_id", "Ticket ID"), ("missing_chunks", "Missing Chunks"), ("status", "Status"), ("account", "Account"), ("technician", "Technician")],
        ),
        "",
        "## Outdated vector chunk samples",
        "",
        _markdown_table(
            _vector_drift_chunk_rows((vector_index_status.get("drift_samples") or {}).get("outdated_chunks", [])),
            [("ticket_id", "Ticket ID"), ("chunk_id", "Chunk ID"), ("chunk_index", "Chunk #"), ("status", "Status"), ("account", "Account"), ("technician", "Technician")],
        ),
        "",
        "## Documents with outdated vector chunks",
        "",
        _markdown_table(
            _vector_drift_chunk_rows((vector_index_status.get("drift_samples") or {}).get("outdated_documents", []), count_key="outdated_chunks"),
            [("ticket_id", "Ticket ID"), ("outdated_chunks", "Outdated Chunks"), ("status", "Status"), ("account", "Account"), ("technician", "Technician")],
        ),
        "",
        "## Dangling vector index samples",
        "",
        _markdown_table(
            _vector_drift_dangling_rows((vector_index_status.get("drift_samples") or {}).get("dangling_index_rows", [])),
            [("ticket_id", "Ticket ID"), ("chunk_id", "Chunk ID"), ("dims", "Dims"), ("index_synced_at", "Indexed At")],
        ),
        "",
        "## Lowest chunk-level metadata coverage",
        "",
        _markdown_table(
            _top_metadata_gaps(retrieval_readiness.get("metadata_coverage", {}), count_key="chunks"),
            [("field", "Field"), ("chunks", "Chunks"), ("ratio", "Coverage")],
        ),
        "",
        "## Lowest document-level metadata coverage",
        "",
        _markdown_table(
            _top_metadata_gaps(retrieval_readiness.get("document_metadata_coverage", {}), count_key="documents"),
            [("field", "Field"), ("documents", "Documents"), ("ratio", "Coverage")],
        ),
        "",
        "## Follow-up cue source coverage",
        "",
        _markdown_table(
            _source_breakdown_rows(retrieval_readiness.get("label_source_summary", {}).get("followup_note_source", {})),
            [("source", "Source"), ("chunks", "Chunks"), ("ratio", "Coverage")],
        ),
        "",
        "## Action cue source coverage",
        "",
        _markdown_table(
            _source_breakdown_rows(retrieval_readiness.get("label_source_summary", {}).get("action_cue_source", {})),
            [("source", "Source"), ("chunks", "Chunks"), ("ratio", "Coverage")],
        ),
        "",
        "## Source-backed metadata promotion gaps",
        "",
        _markdown_table(
            _source_materialization_gap_rows(retrieval_readiness.get("source_metadata_coverage", {})),
            [
                ("field", "Field"),
                ("status", "Status"),
                ("source_documents", "Source Docs"),
                ("materialized_documents", "Materialized Docs"),
                ("promotion_gap", "Gap"),
                ("materialized_ratio", "Materialized Ratio"),
            ],
        ),
        "",
        "## Source-backed metadata invalid-source hygiene",
        "",
        _markdown_table(
            _invalid_source_rows(retrieval_readiness.get("source_backed_metadata", {})),
            [
                ("field", "Field"),
                ("raw_ticket_rows", "Raw Ticket Rows"),
                ("raw_detail_rows", "Raw Detail Rows"),
                ("invalid_ticket_rows", "Invalid Ticket Rows"),
                ("invalid_detail_rows", "Invalid Detail Rows"),
                ("source_documents", "Source Docs"),
            ],
        ),
        "",
        "## Source-backed metadata still upstream-absent",
        "",
        _markdown_table(
            _upstream_absent_rows(retrieval_readiness.get("source_metadata_coverage", {})),
            [
                ("field", "Field"),
                ("ticket_rows", "Ticket Rows"),
                ("detail_rows", "Detail Rows"),
                ("source_documents", "Source Docs"),
                ("materialized_documents", "Materialized Docs"),
            ],
        ),
        "",
        "## Entity label quality",
        "",
        _markdown_table(
            _entity_label_quality_rows(retrieval_readiness.get("entity_label_quality", {})),
            [
                ("entity", "Entity"),
                ("readable_ratio", "Readable"),
                ("identifier_like_ratio", "Identifier-Like"),
                ("fallback_source_ratio", "Fallback Source"),
                ("sample_identifier_values", "Identifier Samples"),
            ],
        ),
        "",
        "## Retrieval signal pressure — under-covered accounts",
        "",
        _markdown_table(
            _retrieval_signal_pressure_rows(retrieval_readiness, "accounts"),
            [
                ("label", "Account"),
                ("documents", "Docs"),
                ("richness_ratio", "Richness"),
                ("detail_ratio", "Detail"),
                ("action_ratio", "Action"),
                ("activity_ratio", "Activity"),
                ("resolution_ratio", "Resolution"),
                ("attachment_ratio", "Attachment"),
                ("lagging_ratio", "Lagging"),
                ("low_richness_backlog", "Backlog"),
                ("latest_activity_at", "Latest Activity"),
            ],
        ),
        "",
        "## Retrieval signal pressure — under-covered categories",
        "",
        _markdown_table(
            _retrieval_signal_pressure_rows(retrieval_readiness, "categories"),
            [
                ("label", "Category"),
                ("documents", "Docs"),
                ("richness_ratio", "Richness"),
                ("detail_ratio", "Detail"),
                ("action_ratio", "Action"),
                ("activity_ratio", "Activity"),
                ("resolution_ratio", "Resolution"),
                ("attachment_ratio", "Attachment"),
                ("lagging_ratio", "Lagging"),
                ("low_richness_backlog", "Backlog"),
                ("latest_activity_at", "Latest Activity"),
            ],
        ),
        "",
        "## Retrieval signal pressure — under-covered technicians",
        "",
        _markdown_table(
            _retrieval_signal_pressure_rows(retrieval_readiness, "technicians"),
            [
                ("label", "Technician"),
                ("documents", "Docs"),
                ("richness_ratio", "Richness"),
                ("detail_ratio", "Detail"),
                ("action_ratio", "Action"),
                ("activity_ratio", "Activity"),
                ("resolution_ratio", "Resolution"),
                ("attachment_ratio", "Attachment"),
                ("lagging_ratio", "Lagging"),
                ("low_richness_backlog", "Backlog"),
                ("latest_activity_at", "Latest Activity"),
            ],
        ),
        "",
        "## Raw retrieval readiness JSON",
        "",
        "```json",
        json.dumps(retrieval_readiness, indent=2),
        "```",
        "",
        "## Notes",
        "",
        "- This file is a derived public artifact for OpenClaw-friendly inspection of retrieval quality and drift.",
        "- Canonical truth remains in `.SherpaMind/private/data/sherpamind.sqlite3`.",
        "- Materialized docs, chunks, vector rows, and Markdown outputs remain replaceable caches.",
    ]
    retrieval_path.write_text("\n".join(retrieval_md) + "\n")

    stale_open_path = paths.docs_root / "stale-open-tickets.md"
    stale_open_md = [
        "# SherpaMind Stale Open Tickets",
        "",
        f"Generated: `{generated_at}`",
        "",
        _markdown_table(open_ages, [
            ("id", "Ticket ID"),
            ("subject", "Subject"),
            ("account", "Account"),
            ("technician", "Technician"),
            ("age_days", "Age Days"),
            ("days_since_update", "Days Since Update"),
        ]),
        "",
        "- Derived from the canonical SQLite store under `.SherpaMind/private/data/`.",
    ]
    stale_open_path.write_text("\n".join(stale_open_md) + "\n")

    account_activity_path = paths.docs_root / "recent-account-activity.md"
    account_activity_md = [
        "# SherpaMind Recent Account Activity",
        "",
        f"Generated: `{generated_at}`",
        "",
        _markdown_table(account_activity, [
            ("account", "Account"),
            ("ticket_count", "Tickets"),
            ("open_count", "Open"),
            ("closed_count", "Closed"),
            ("latest_activity_at", "Latest Activity"),
        ]),
    ]
    account_activity_path.write_text("\n".join(account_activity_md) + "\n")

    technician_load_path = paths.docs_root / "recent-technician-load.md"
    technician_load_md = [
        "# SherpaMind Recent Technician Load",
        "",
        f"Generated: `{generated_at}`",
        "",
        _markdown_table(technician_load, [
            ("technician", "Technician"),
            ("ticket_count", "Tickets"),
            ("open_count", "Open"),
            ("closed_count", "Closed"),
            ("latest_activity_at", "Latest Activity"),
        ]),
    ]
    technician_load_path.write_text("\n".join(technician_load_md) + "\n")

    account_index_path = account_dir / "index.md"
    account_index_md = [
        "# SherpaMind Account Artifact Index",
        "",
        f"Generated: `{generated_at}`",
        "",
        f"Total account docs: `{len(account_summaries)}`",
        "",
        _markdown_table(account_summaries, [
            ("account", "Account"),
            ("total_tickets", "Tickets"),
            ("open_tickets", "Open"),
            ("closed_tickets", "Closed"),
            ("detail_tickets", "Detail Tickets"),
            ("document_tickets", "Document Tickets"),
            ("chunk_count", "Chunks"),
            ("detail_coverage_ratio", "Detail Coverage"),
            ("latest_activity_at", "Latest Activity"),
        ]),
        "",
        "These are derived per-account retrieval/support artifacts, not canonical truth.",
    ]
    account_index_path.write_text("\n".join(account_index_md) + "\n")

    technician_index_path = technician_dir / "index.md"
    technician_index_md = [
        "# SherpaMind Technician Artifact Index",
        "",
        f"Generated: `{generated_at}`",
        "",
        f"Total technician docs: `{len(technician_summaries)}`",
        "",
        _markdown_table(technician_summaries, [
            ("technician", "Technician"),
            ("total_tickets", "Tickets"),
            ("open_tickets", "Open"),
            ("closed_tickets", "Closed"),
            ("detail_tickets", "Detail Tickets"),
            ("document_tickets", "Document Tickets"),
            ("chunk_count", "Chunks"),
            ("detail_coverage_ratio", "Detail Coverage"),
            ("latest_activity_at", "Latest Activity"),
        ]),
        "",
        "These are derived per-technician retrieval/support artifacts, not canonical truth.",
    ]
    technician_index_path.write_text("\n".join(technician_index_md) + "\n")

    ticket_index_path = ticket_dir / "index.md"
    ticket_index_md = [
        "# SherpaMind Ticket Artifact Index",
        "",
        f"Generated: `{generated_at}`",
        "",
        f"Total ticket docs: `{len(ticket_summaries)}`",
        "",
        _markdown_table(ticket_summaries, [
            ("ticket_id", "Ticket ID"),
            ("ticket_number", "Ticket #"),
            ("status", "Status"),
            ("priority", "Priority"),
            ("account", "Account"),
            ("technician", "Technician"),
            ("detail_available", "Detail"),
            ("document_available", "Doc"),
            ("chunk_count", "Chunks"),
            ("indexed_chunk_count", "Indexed Chunks"),
            ("vector_ready", "Vector Ready"),
            ("lag_minutes", "Lag Minutes"),
            ("updated_at", "Updated"),
        ]),
        "",
        "These are derived per-ticket inspection artifacts, not canonical truth.",
    ]
    ticket_index_path.write_text("\n".join(ticket_index_md) + "\n")

    generated_files = [
        str(snapshot_path),
        str(retrieval_path),
        str(stale_open_path),
        str(account_activity_path),
        str(technician_load_path),
        str(account_index_path),
        str(technician_index_path),
        str(ticket_index_path),
    ]
    account_docs_written = 0
    technician_docs_written = 0
    ticket_docs_written = 0
    desired_account_paths: set[Path] = set()
    desired_technician_paths: set[Path] = set()
    desired_ticket_paths: set[Path] = set()

    for account_row in account_summaries:
        account_name = account_row["account"]
        summary = get_account_summary(db_path, str(account_row["account_ref"] or account_name))
        if summary.get("status") != "ok":
            continue
        path = account_dir / f"{_safe_doc_name(account_name)}.md"
        lines = [
            f"# Account Summary: {summary['account']['name']}",
            "",
            f"Generated: `{generated_at}`",
            "",
            "## Stats",
            "",
            "```json",
            json.dumps(summary["stats"], indent=2),
            "```",
            "",
            "## Status breakdown",
            "",
            _markdown_table(summary["status_breakdown"], [("status", "Status"), ("ticket_count", "Ticket Count")]),
            "",
            "## Priority breakdown",
            "",
            _markdown_table(summary["priority_breakdown"], [("priority", "Priority"), ("ticket_count", "Ticket Count")]),
            "",
            "## Category breakdown",
            "",
            _markdown_table(summary["category_breakdown"], [("category", "Category"), ("ticket_count", "Ticket Count")]),
            "",
            "## Retrieval health",
            "",
            _markdown_table(_entity_retrieval_health_rows(summary["retrieval_health"]), [
                ("detail_coverage", "Detail Coverage"),
                ("document_coverage", "Document Coverage"),
                ("action_cue_coverage", "Action Cue Coverage"),
                ("resolution_summary_coverage", "Resolution Coverage"),
                ("multi_chunk_ratio", "Multi-Chunk Ratio"),
                ("lagging_ratio", "Lagging Ratio"),
                ("avg_lag_minutes", "Avg Lag Minutes"),
                ("max_lag_minutes", "Max Lag Minutes"),
            ]),
            "",
            "## Retrieval lag buckets",
            "",
            _markdown_table(_entity_lag_bucket_rows(summary["retrieval_health"]), [
                ("bucket", "Bucket"),
                ("tickets", "Tickets"),
                ("ratio", "Coverage"),
            ]),
            "",
            "## Retrieval metadata coverage",
            "",
            _markdown_table(_entity_metadata_coverage_rows(summary["retrieval_health"]), [
                ("field", "Field"),
                ("tickets", "Tickets"),
                ("ratio", "Coverage"),
            ]),
            "",
            "## Open tickets",
            "",
            _markdown_table(summary["open_tickets"], [
                ("id", "Ticket ID"),
                ("subject", "Subject"),
                ("priority", "Priority"),
                ("category", "Category"),
                ("updated_at", "Updated"),
            ]),
            "",
            "## Recent tickets",
            "",
            _markdown_table(summary["recent_tickets"], [
                ("id", "Ticket ID"),
                ("subject", "Subject"),
                ("status", "Status"),
                ("priority", "Priority"),
                ("category", "Category"),
                ("updated_at", "Updated"),
            ]),
            "",
            "## Recent log types",
            "",
            _markdown_table(summary["recent_log_types"], [("log_type", "Log Type"), ("log_count", "Count")]),
        ]
        path.write_text("\n".join(lines) + "\n")
        desired_account_paths.add(path)
        generated_files.append(str(path))
        account_docs_written += 1

    for technician_row in technician_summaries:
        technician_name = technician_row["technician"]
        summary = get_technician_summary(db_path, str(technician_row["technician_ref"] or technician_name))
        if summary.get("status") != "ok":
            continue
        path = technician_dir / f"{_safe_doc_name(technician_name)}.md"
        lines = [
            f"# Technician Summary: {summary['technician']['display_name']}",
            "",
            f"Generated: `{generated_at}`",
            "",
            "## Stats",
            "",
            "```json",
            json.dumps(summary["stats"], indent=2),
            "```",
            "",
            "## Status breakdown",
            "",
            _markdown_table(summary["status_breakdown"], [("status", "Status"), ("ticket_count", "Ticket Count")]),
            "",
            "## Priority breakdown",
            "",
            _markdown_table(summary["priority_breakdown"], [("priority", "Priority"), ("ticket_count", "Ticket Count")]),
            "",
            "## Category breakdown",
            "",
            _markdown_table(summary["category_breakdown"], [("category", "Category"), ("ticket_count", "Ticket Count")]),
            "",
            "## Retrieval health",
            "",
            _markdown_table(_entity_retrieval_health_rows(summary["retrieval_health"]), [
                ("detail_coverage", "Detail Coverage"),
                ("document_coverage", "Document Coverage"),
                ("action_cue_coverage", "Action Cue Coverage"),
                ("resolution_summary_coverage", "Resolution Coverage"),
                ("multi_chunk_ratio", "Multi-Chunk Ratio"),
                ("lagging_ratio", "Lagging Ratio"),
                ("avg_lag_minutes", "Avg Lag Minutes"),
                ("max_lag_minutes", "Max Lag Minutes"),
            ]),
            "",
            "## Retrieval lag buckets",
            "",
            _markdown_table(_entity_lag_bucket_rows(summary["retrieval_health"]), [
                ("bucket", "Bucket"),
                ("tickets", "Tickets"),
                ("ratio", "Coverage"),
            ]),
            "",
            "## Retrieval metadata coverage",
            "",
            _markdown_table(_entity_metadata_coverage_rows(summary["retrieval_health"]), [
                ("field", "Field"),
                ("tickets", "Tickets"),
                ("ratio", "Coverage"),
            ]),
            "",
            "## Open tickets",
            "",
            _markdown_table(summary["open_tickets"], [
                ("id", "Ticket ID"),
                ("subject", "Subject"),
                ("priority", "Priority"),
                ("category", "Category"),
                ("updated_at", "Updated"),
            ]),
            "",
            "## Recent tickets",
            "",
            _markdown_table(summary["recent_tickets"], [
                ("id", "Ticket ID"),
                ("subject", "Subject"),
                ("status", "Status"),
                ("priority", "Priority"),
                ("category", "Category"),
                ("updated_at", "Updated"),
            ]),
            "",
            "## Recent log types",
            "",
            _markdown_table(summary["recent_log_types"], [("log_type", "Log Type"), ("log_count", "Count")]),
        ]
        path.write_text("\n".join(lines) + "\n")
        desired_technician_paths.add(path)
        generated_files.append(str(path))
        technician_docs_written += 1

    for ticket_row in ticket_summaries:
        ticket_id = ticket_row["ticket_id"]
        summary = get_ticket_summary(db_path, str(ticket_id))
        if summary.get("status") != "ok":
            continue
        path = ticket_dir / f"ticket_{ticket_id}.md"
        lines = [
            f"# Ticket Summary: {summary['ticket']['ticket_number'] or summary['ticket']['id']} — {summary['ticket']['subject'] or '(no subject)'}",
            "",
            f"Generated: `{generated_at}`",
            "",
            "## Ticket identity",
            "",
            "```json",
            json.dumps(summary["ticket"], indent=2),
            "```",
            "",
            "## Artifact stats",
            "",
            "```json",
            json.dumps(summary["artifact_stats"], indent=2),
            "```",
            "",
            "## Retrieval health",
            "",
            _markdown_table([
                {
                    "document_synced_at": summary["retrieval_health"].get("document_synced_at"),
                    "materialization_version": summary["retrieval_health"].get("materialization_version"),
                    "is_current_materialization_version": summary["retrieval_health"].get("is_current_materialization_version"),
                    "lag_minutes": _format_number(summary["retrieval_health"].get("lag_minutes")),
                    "chunk_count": summary["retrieval_health"].get("chunk_count"),
                    "indexed_chunk_count": summary["retrieval_health"].get("indexed_chunk_count"),
                    "vector_ready": summary["retrieval_health"].get("vector_ready"),
                    "all_chunk_hashes_present": summary["retrieval_health"].get("all_chunk_hashes_present"),
                }
            ], [
                ("document_synced_at", "Doc Synced"),
                ("materialization_version", "Doc Version"),
                ("is_current_materialization_version", "Current Version"),
                ("lag_minutes", "Lag Minutes"),
                ("chunk_count", "Chunks"),
                ("indexed_chunk_count", "Indexed Chunks"),
                ("vector_ready", "Vector Ready"),
                ("all_chunk_hashes_present", "All Chunk Hashes"),
            ]),
            "",
            "## Chunk section inventory",
            "",
            _markdown_table(
                summary["chunk_inventory"],
                [
                    ("chunk_index", "Chunk #"),
                    ("chunk_chars", "Chars"),
                    ("chunk_primary_section", "Primary Section"),
                    ("chunk_section_labels", "Section Labels"),
                    ("vector_indexed", "Vector Indexed"),
                    ("vector_dims", "Vector Dims"),
                    ("content_hash_present", "Content Hash"),
                    ("chunk_synced_at", "Chunk Synced"),
                ],
            ),
            "",
            "## Retrieval metadata",
            "",
            "```json",
            json.dumps(summary["retrieval_metadata"], indent=2),
            "```",
            "",
            "## Recent logs",
            "",
            _markdown_table(summary["recent_logs"], [
                ("id", "Log ID"),
                ("log_type", "Type"),
                ("record_date", "Recorded"),
                ("actor", "Actor"),
                ("is_tech_only", "Internal"),
                ("note", "Note"),
            ]),
            "",
            "## Attachments",
            "",
            _markdown_table(summary["attachments"], [
                ("id", "Attachment ID"),
                ("name", "Name"),
                ("size", "Size"),
                ("recorded_at", "Recorded"),
                ("url", "URL"),
            ]),
        ]
        path.write_text("\n".join(lines) + "\n")
        desired_ticket_paths.add(path)
        generated_files.append(str(path))
        ticket_docs_written += 1

    removed_account_docs = _cleanup_stale_entity_docs(account_dir, desired_account_paths)
    removed_technician_docs = _cleanup_stale_entity_docs(technician_dir, desired_technician_paths)
    removed_ticket_docs = _cleanup_stale_entity_docs(ticket_dir, desired_ticket_paths)

    index_path = paths.docs_root / "index.md"
    index_md = [
        "# SherpaMind Public Docs Index",
        "",
        f"Generated: `{generated_at}`",
        "",
        "Available derived artifacts:",
        "- `insight-snapshot.md`",
        "- `retrieval-readiness.md`",
        "- `stale-open-tickets.md`",
        "- `recent-account-activity.md`",
        "- `recent-technician-load.md`",
        "- `accounts/index.md`",
        "- `technicians/index.md`",
        "- `tickets/index.md`",
        f"- account docs directory: `{account_dir}` ({account_docs_written} docs)",
        f"- technician docs directory: `{technician_dir}` ({technician_docs_written} docs)",
        f"- ticket docs directory: `{ticket_dir}` ({ticket_docs_written} docs)",
        "",
        "These are derived/public artifacts for OpenClaw-friendly access. Canonical truth remains in `.SherpaMind/private/data/`.",
        "The matching vector-ready export lives under `.SherpaMind/public/exports/embedding-ticket-chunks.jsonl` when generated.",
        "The matching vector export manifest lives under `.SherpaMind/public/exports/embedding-ticket-chunks.manifest.json` when generated.",
    ]
    index_path.write_text("\n".join(index_md) + "\n")
    generated_files.insert(0, str(index_path))

    return {
        "status": "ok",
        "output_path": str(snapshot_path),
        "generated_at": generated_at,
        "generated_files": generated_files,
        "account_docs_generated": account_docs_written,
        "technician_docs_generated": technician_docs_written,
        "ticket_docs_generated": ticket_docs_written,
        "account_artifact_candidates": len(account_summaries),
        "technician_artifact_candidates": len(technician_summaries),
        "ticket_artifact_candidates": len(ticket_summaries),
        "stale_account_docs_removed": len(removed_account_docs),
        "stale_technician_docs_removed": len(removed_technician_docs),
        "stale_ticket_docs_removed": len(removed_ticket_docs),
        "removed_files": removed_account_docs + removed_technician_docs + removed_ticket_docs,
    }
