"""Pipeline orchestrator — runs the full deterministic processing pipeline."""

from __future__ import annotations

import os

from .extractor import build_timeline, extract_env_facts, extract_error_codes, find_user_agents
from .models import EnvironmentFacts
from .packager.builder import PackBuilder, PackResult
from .parser import extract_stack_traces, parse_log, parse_ticket
from .redactor import RedactionEngine, report_to_json


def run_pipeline(
    ticket_path: str | None = None,
    log_paths: list[str] | None = None,
    output_dir: str = "repro_output",
) -> PackResult:
    """Run the full deterministic pipeline.

    Args:
        ticket_path: Path to the support ticket file.
        log_paths: Paths to log files.
        output_dir: Directory to write outputs to.

    Returns:
        PackResult with list of created files and validation status.
    """
    builder = PackBuilder(output_dir)
    engine = RedactionEngine()
    all_text_parts: list[str] = []

    # 1. Process ticket
    if ticket_path and os.path.exists(ticket_path):
        with open(ticket_path, "r", encoding="utf-8") as f:
            ticket_raw = f.read()
        all_text_parts.append(ticket_raw)

        # Parse ticket structure
        ticket_info = parse_ticket(ticket_raw)

        # Redact PII
        sanitized_ticket = engine.redact(ticket_raw)
        builder.write_sanitized_ticket(sanitized_ticket)
    else:
        builder.write_sanitized_ticket("No ticket provided.")

    # 2. Process logs
    all_log_entries = []
    all_log_text: list[str] = []

    for log_path in (log_paths or []):
        if not os.path.exists(log_path):
            continue
        with open(log_path, "r", encoding="utf-8") as f:
            log_raw = f.read()
        all_text_parts.append(log_raw)
        all_log_text.append(log_raw)

        # Parse log entries
        entries = parse_log(log_raw)
        all_log_entries.extend(entries)

    # Redact all logs together
    combined_logs = "\n".join(all_log_text)
    if combined_logs.strip():
        sanitized_logs = engine.redact(combined_logs)
        builder.write_sanitized_logs(sanitized_logs)
    else:
        builder.write_sanitized_logs("No logs provided.")

    # 3. Extract facts from all text
    combined_text = "\n".join(all_text_parts)
    facts = extract_env_facts(combined_text)

    # Enrich facts with UA parsing
    ua_results = find_user_agents(combined_text)
    if ua_results:
        ua = ua_results[0]
        if ua.browser:
            facts.browser = ua.browser
            facts.browser_version = ua.browser_version
        if ua.os:
            facts.os = ua.os

    # Enrich with error codes
    error_codes = extract_error_codes(combined_text)
    for ec in error_codes:
        if ec.code not in facts.error_codes:
            facts.error_codes.append(ec.code)

    builder.write_facts(facts)

    # 4. Build timeline
    timeline_events = build_timeline(all_log_entries)
    builder.write_timeline(timeline_events)

    # 5. Extract stack traces
    traces = extract_stack_traces(combined_text)
    builder.write_stack_traces(traces)

    # 6. Generate placeholder documents (to be filled by Claude via SKILL.md)
    eng_issue = _generate_engineering_issue_stub(facts, traces, timeline_events)
    builder.write_engineering_issue(eng_issue)

    escalation = _generate_escalation_stub(facts)
    builder.write_internal_escalation(escalation)

    reply = _generate_customer_reply_stub()
    builder.write_customer_reply(reply)

    # 7. Write redaction report
    report = engine.get_report()
    builder.write_redaction_report(report)

    # 8. Finalize
    return builder.finalize()


def _generate_engineering_issue_stub(
    facts: EnvironmentFacts,
    traces: list,
    timeline: list,
) -> str:
    """Generate engineering issue with deterministic fields filled, AI fields marked."""
    lines = ["## Problem Summary", "[NEEDS_AI_REVIEW: Summarize the issue]", ""]

    # Environment table
    lines.append("## Environment")
    lines.append("| Field | Value |")
    lines.append("|-------|-------|")
    if facts.environment:
        lines.append(f"| Environment | {facts.environment} |")
    if facts.app_version:
        lines.append(f"| Version | {facts.app_version} |")
    if facts.build_number:
        lines.append(f"| Build | {facts.build_number} |")
    if facts.browser:
        ver = f" {facts.browser_version}" if facts.browser_version else ""
        lines.append(f"| Browser | {facts.browser}{ver} |")
    if facts.os:
        lines.append(f"| OS | {facts.os} |")
    if facts.region:
        lines.append(f"| Region | {facts.region} |")
    if facts.user_role:
        lines.append(f"| User Role | {facts.user_role} |")
    if facts.feature_flags:
        for k, v in facts.feature_flags.items():
            lines.append(f"| Feature Flag: {k} | {v} |")
    lines.append("")

    # Error info
    if facts.error_codes:
        lines.append("## Error Codes")
        lines.append(", ".join(facts.error_codes))
        lines.append("")

    # Stack traces
    if traces:
        lines.append("## Stack Trace")
        for t in traces:
            lines.append(f"**{t.language}**: `{t.exception_type}: {t.exception_message}`")
            for f in t.frames[:5]:
                loc = f":{f.line_number}" if f.line_number else ""
                func = f" in {f.function_name}" if f.function_name else ""
                lines.append(f"  - `{f.file_path}{loc}`{func}")
        lines.append("")

    # Timeline
    if timeline:
        lines.append("## Event Timeline")
        lines.append("| Timestamp | Event |")
        lines.append("|-----------|-------|")
        for ev in timeline[:15]:
            lines.append(f"| {ev.timestamp} | {ev.event[:100]} |")
        lines.append("")

    lines.append("## Reproduction Steps")
    lines.append("[NEEDS_AI_REVIEW: Generate minimal reproduction steps]")
    lines.append("")
    lines.append("## Root Cause Hypothesis")
    lines.append("[NEEDS_AI_REVIEW: Analyze and suggest root cause]")

    return "\n".join(lines)


def _generate_escalation_stub(facts: EnvironmentFacts) -> str:
    lines = [
        "## Escalation Summary",
        "[NEEDS_AI_REVIEW: Summarize for support/PM]",
        "",
        "## Impact",
        f"- Environment: {facts.environment or 'unknown'}",
        f"- Version: {facts.app_version or 'unknown'}",
        f"- Error codes: {', '.join(facts.error_codes) if facts.error_codes else 'none'}",
        "",
        "## Severity",
        "[NEEDS_AI_REVIEW: Assess severity level P0-P4]",
        "",
        "## Recommended Actions",
        "[NEEDS_AI_REVIEW: Suggest next steps]",
    ]
    return "\n".join(lines)


def _generate_customer_reply_stub() -> str:
    return "\n".join([
        "[NEEDS_AI_REVIEW: Generate a professional, empathetic customer reply]",
        "",
        "Key requirements:",
        "- Acknowledge the issue",
        "- Do NOT expose internal details",
        "- Provide next steps or workaround if available",
        "- Set expectations for follow-up timeline",
    ])
