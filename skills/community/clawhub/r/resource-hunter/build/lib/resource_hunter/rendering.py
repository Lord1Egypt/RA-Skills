from __future__ import annotations

from typing import Any

from .ranking import BUCKET_LABELS
from .video_core import format_video_text


def format_search_text(response: dict[str, Any], max_results: int | None = None) -> str:
    intent = response["intent"]
    plan = response["plan"]
    results = response["results"]
    meta = response.get("meta", {})
    limit = max_results if max_results is not None else meta.get("effective_limit", meta.get("limit", 8))
    selected = results[:limit]

    lines = [
        "Resource Hunter v2",
        f"Query: {response['query']}",
        f"Kind: {intent['kind']} | Channel: {' -> '.join(plan['channels'])}",
    ]
    if plan.get("notes"):
        lines.append("Plan: " + "; ".join(plan["notes"]))
    if meta.get("resolved_titles"):
        lines.append("Resolved titles: " + ", ".join(meta["resolved_titles"][:4]))
    success_estimate = meta.get("success_estimate") or {}
    if success_estimate:
        lines.append(
            "Success estimate: "
            f"direct={success_estimate.get('has_direct')} | "
            f"actionable={success_estimate.get('has_actionable')} | "
            f"clues={success_estimate.get('has_clues')}"
        )
    lines.append("")

    if not selected:
        lines.append("No result matched the current query.")
    else:
        has_confident = any(item.get("match_bucket") in {"exact_title_episode", "title_family_match"} for item in selected)
        if not has_confident:
            lines.append("No confident match")
            lines.append("")
        grouped: dict[str, list[dict[str, Any]]] = {}
        for result in selected:
            grouped.setdefault(result.get("match_bucket", "weak_context_match"), []).append(result)
        seen_labels: set[str] = set()
        for bucket in ("exact_title_episode", "title_family_match", "episode_only_match", "weak_context_match"):
            bucket_items = grouped.get(bucket) or []
            if not bucket_items:
                continue
            label = BUCKET_LABELS[bucket]
            if label not in seen_labels:
                lines.append(label + ":")
                seen_labels.add(label)
            for result in bucket_items:
                summary_bits = [
                    f"{result['channel']}/{result['provider']}",
                    f"via {result['source']}",
                    f"bucket={result.get('match_bucket')}",
                    f"confidence={result.get('confidence')}",
                    f"status={result.get('validation_status')}",
                    f"actionability={result.get('actionability')}",
                ]
                if result.get("cluster_id"):
                    summary_bits.append(f"cluster={result['cluster_id']}")
                if result.get("corroboration_count"):
                    summary_bits.append(f"corroboration={result['corroboration_count']}")
                if result["quality"]:
                    summary_bits.append(result["quality"])
                if result["size"]:
                    summary_bits.append(result["size"])
                if result["seeders"]:
                    summary_bits.append(f"seeders={result['seeders']}")
                summary_bits.append(f"score={result['score']}")
                if result.get("source_degraded"):
                    summary_bits.append("degraded-source")
                lines.append(f"- {result['title']}")
                lines.append("  " + " | ".join(summary_bits))
                lines.append(f"  {result['link_or_magnet']}")
                if result["password"]:
                    lines.append(f"  password: {result['password']}")
                if result.get("source") == "dalipan" and str(result.get("link_or_magnet", "")).startswith("dalipan://"):
                    lines.append("  note: token-only Dalipan clue; final share URL may require follow-up")
                if result.get("validation_signals"):
                    lines.append("  validation: " + ", ".join(result["validation_signals"][:4]))
                if result["reasons"]:
                    lines.append("  why: " + ", ".join(result["reasons"][:4]))
                if result.get("penalties"):
                    lines.append("  penalties: " + ", ".join(result["penalties"][:3]))
            lines.append("")

    if response.get("warnings"):
        lines.append("Warnings:")
        for warning in response["warnings"]:
            lines.append(f"- {warning}")
    if response.get("source_status"):
        lines.append("")
        lines.append("Source status:")
        for status in response["source_status"]:
            state = "ok" if status["ok"] else ("skipped" if status["skipped"] else "fail")
            if status.get("degraded"):
                state += "/degraded"
            detail = f"{status['source']} ({status['channel']}, p{status['priority']}): {state}"
            if status.get("latency_ms") is not None:
                detail += f", {status['latency_ms']}ms"
            if status.get("failure_kind"):
                detail += f", {status['failure_kind']}"
            if status.get("error"):
                detail += f", {status['error']}"
            lines.append(f"- {detail}")
    return "\n".join(lines).strip()


def format_sources_text(payload: dict[str, Any]) -> str:
    lines = ["Resource Hunter sources", ""]
    retrieval_layers = payload.get("meta", {}).get("retrieval_layers") or []
    if retrieval_layers:
        lines.append("Retrieval layers:")
        for layer in retrieval_layers:
            lines.append(f"- {layer['name']} | {layer['role']} | {', '.join(layer.get('sources', [])) or 'reserved'}")
        lines.append("")
    for item in payload["sources"]:
        status = item["recent_status"]
        state = "unknown"
        if status["ok"] is True:
            state = "ok"
        elif status["ok"] is False and status["skipped"]:
            state = "skipped"
        elif status["ok"] is False:
            state = "fail"
        if status.get("degraded"):
            state += "/degraded"
        lines.append(f"- {item['source']} | {item['channel']} | priority={item['priority']} | status={state}")
        if status.get("latency_ms") is not None or status.get("checked_at"):
            lines.append(
                f"  checked_at={status.get('checked_at') or '-'} latency_ms={status.get('latency_ms') or '-'}"
            )
        if status.get("failure_kind"):
            lines.append(f"  failure_kind={status['failure_kind']}")
        if status.get("error"):
            lines.append(f"  error={status['error']}")
    return "\n".join(lines)


__all__ = ["format_search_text", "format_sources_text", "format_video_text"]
