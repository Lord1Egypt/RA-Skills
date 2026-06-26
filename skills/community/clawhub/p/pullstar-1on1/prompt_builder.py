"""
prompt_builder.py — Prompt construction and LLM input serialization for PullStar 1-on-1

Design philosophy:
  Python packages bounded raw context — the LLM is responsible for extracting meaning.
  Bounds exist for stability and cost control, not to pre-summarize or filter content.

Public API:
  build_user_message(score, ingest)   — construct the user turn for the brief prompt
  build_llm_input_payload(...)        — assemble a serializable LLM input artifact
  write_llm_input(payload, output_dir)— write payload to .pullstar/llm_input_{login}.json

LLM input payload schema (version 1.0):
  {
    "version":        "1.0",
    "engineer_login": str,
    "mode":           "ai" | "stub",
    "system":         str,
    "user":           str,
    "metadata": {
      "generated_at":  ISO-8601 str,
      "lookback_days": int,
      "provider":      str | null,
      "model":         str | null,
      "total_score":   int,
      "confidence":    "high" | "medium" | "low",
      "has_insights":  bool
    }
  }

PR insights mode (when ingest contains discussion_summary_stats fields):
  Two additional sections are appended to the user message:
    1. === PR DISCUSSION SUMMARY === — lightweight counts, no interpretation
    2. === PR CONTEXT (OPT-IN) === — bounded raw review/comment text, labeled by source
"""

import json
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Bounds — PR context packaging (applies only when PR insights data is present)
# ---------------------------------------------------------------------------
#
# These limits control how much raw content is packaged into the prompt.
# They exist for stability and cost control, NOT to pre-summarize or rank.
# All items are taken in original ingest order — no reordering or selection.
#
_CONTEXT_PR_CAP        = 5    # max authored PRs included in the PR CONTEXT block
_CONTEXT_MAX_REVIEWS   = 3    # max reviews per PR (original order, non-empty body only)
_CONTEXT_MAX_COMMENTS  = 3    # max comments per PR (original order, non-empty body only)
_CONTEXT_REVIEW_CHARS  = 600  # backstop truncation for review body text
_CONTEXT_COMMENT_CHARS = 500  # backstop truncation for comment body text


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_bot(login: str | None) -> bool:
    """Return True if the login is a GitHub bot account (contains '[bot]')."""
    return bool(login and "[bot]" in login)


def _truncate_to(text: str, limit: int) -> str:
    """
    Truncate text to at most `limit` characters, appending ' [...]' if cut.
    Preserves readable, meaningful content — truncation is a size backstop only.
    """
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + " [...]"


def _short_date(iso: str) -> str:
    """Return YYYY-MM-DD from an ISO timestamp string."""
    return iso[:10] if iso else ""


# ---------------------------------------------------------------------------
# Section 1 — PR Discussion Summary (lightweight counts, no interpretation)
# ---------------------------------------------------------------------------

def _build_pr_summary_section(ingest: dict) -> str | None:
    """
    Build a lightweight structured summary of PR discussion activity.

    Reads discussion_summary_stats from prs_authored entries.
    Returns None if no insight data is present.
    """
    prs = ingest.get("prs_authored", [])
    sample = [p for p in prs if "discussion_summary_stats" in p]
    if not sample:
        return None

    n = len(sample)
    total_reviews  = sum(p["discussion_summary_stats"]["review_count"]   for p in sample)
    prs_reviewed   = sum(1 for p in sample
                         if p["discussion_summary_stats"]["review_count"] > 0)
    prs_with_cr    = sum(1 for p in sample
                         if p["discussion_summary_stats"]["changes_requested_count"] > 0)
    prs_approved   = sum(1 for p in sample
                         if p["discussion_summary_stats"]["approved_count"] > 0)
    total_comments = sum(p["discussion_summary_stats"]["comment_count"] for p in sample)
    prs_with_comments = sum(1 for p in sample
                            if p["discussion_summary_stats"]["comment_count"] > 0)

    # Unique reviewer counts per PR
    reviewer_counts = []
    for p in sample:
        logins = {
            r["reviewer_login"]
            for r in p.get("reviews_received_detail", [])
            if r.get("reviewer_login")
        }
        reviewer_counts.append(len(logins))
    avg_reviewers = sum(reviewer_counts) / n if n else 0

    # Revision cycles: approved review followed a changes_requested in submission order
    revision_cycles = 0
    for p in sample:
        pending_cr = False
        for r in p.get("reviews_received_detail", []):
            if r["state"] == "changes_requested":
                pending_cr = True
            elif r["state"] == "approved" and pending_cr:
                revision_cycles += 1
                break

    lines = [
        f"=== PR DISCUSSION SUMMARY ===",
        f"Based on {n} authored PR{'s' if n != 1 else ''} with review/comment data:",
        f"- Reviews received: {total_reviews} total "
        f"({prs_reviewed} of {n} PRs had at least 1 review)",
        f"- Change requests: {prs_with_cr} PR{'s' if prs_with_cr != 1 else ''} "
        f"had at least one change request",
        f"- Approvals: {prs_approved} PR{'s' if prs_approved != 1 else ''} "
        f"received a formal approval",
        f"- Visible revision cycles: {revision_cycles} "
        f"(changes_requested followed by approval on same PR)",
        f"- Avg distinct reviewers per PR: {avg_reviewers:.1f}",
        f"- PRs with issue comments: {prs_with_comments} of {n} "
        f"({total_comments} comments total)",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Section 2 — PR Context (bounded raw text, labeled by source)
# ---------------------------------------------------------------------------

def _build_pr_context_section(ingest: dict) -> str | None:
    """
    Package bounded raw PR context for the LLM to interpret.

    Includes PR titles, review bodies, and comment bodies — labeled clearly
    as (human) or (bot). Takes items in original ingest order.

    - Max PRs: _CONTEXT_PR_CAP
    - Max reviews per PR: _CONTEXT_MAX_REVIEWS (non-empty body, original order)
    - Max comments per PR: _CONTEXT_MAX_COMMENTS (non-empty body, original order)
    - Review body truncated to _CONTEXT_REVIEW_CHARS
    - Comment body truncated to _CONTEXT_COMMENT_CHARS

    Returns None if no insight data is present.
    """
    prs = ingest.get("prs_authored", [])
    sample = [p for p in prs if "discussion_summary_stats" in p][:_CONTEXT_PR_CAP]
    if not sample:
        return None

    header_lines = [
        "=== PR CONTEXT (OPT-IN) ===",
        "The following PR titles, reviews, and comments are included because PR insights "
        "mode is enabled.",
        "Use them to understand engineering behavior and collaboration patterns.",
        "Do NOT quote them directly in the final brief.",
        "",
    ]

    pr_blocks: list[str] = []

    for pr in sample:
        repo    = pr.get("repository", "")
        status  = pr.get("status", "")
        lines_added   = pr.get("lines_added", 0)
        lines_deleted = pr.get("lines_deleted", 0)
        desc_len      = pr.get("description_length", 0)

        block: list[str] = [
            f"PR #{pr['number']} — \"{pr['title']}\" "
            f"({repo}, {status}, +{lines_added}/-{lines_deleted} lines)",
        ]

        # Description body is not stored in ingest — show length as context
        if desc_len > 0:
            block.append(f"Description: {desc_len} chars (body not captured in ingest)")
        else:
            block.append("Description: (empty)")

        # Reviews — in original order, non-empty body only, capped at _CONTEXT_MAX_REVIEWS
        reviews = [
            r for r in pr.get("reviews_received_detail", [])
            if (r.get("body_excerpt") or "").strip()
        ][:_CONTEXT_MAX_REVIEWS]

        for r in reviews:
            login     = r.get("reviewer_login") or "unknown"
            state     = r.get("state", "commented")
            date      = _short_date(r.get("submitted_at", ""))
            label     = "bot" if _is_bot(login) else "human"
            body      = _truncate_to(r.get("body_excerpt", "").strip(), _CONTEXT_REVIEW_CHARS)
            block.append(f"\nReview ({label}) — {login} [{state}, {date}]:")
            block.append(body)

        # Comments — in original order, non-empty body only, capped at _CONTEXT_MAX_COMMENTS
        comments = [
            c for c in pr.get("comments_detail", [])
            if (c.get("body_excerpt") or "").strip()
        ][:_CONTEXT_MAX_COMMENTS]

        for c in comments:
            login = c.get("author_login") or "unknown"
            date  = _short_date(c.get("created_at", ""))
            label = "bot" if _is_bot(login) else "human"
            body  = _truncate_to(c.get("body_excerpt", "").strip(), _CONTEXT_COMMENT_CHARS)
            block.append(f"\nComment ({label}) — {login} [{date}]:")
            block.append(body)

        pr_blocks.append("\n".join(block))

    return "\n".join(header_lines) + "\n---\n\n".join(pr_blocks)


# ---------------------------------------------------------------------------
# User message builder
# ---------------------------------------------------------------------------

def build_user_message(score: dict, ingest: dict | None) -> str:
    """
    Construct the user turn for the brief prompt.

    In normal mode (no PR insights): includes dimension scores, raw stats, flags.
    In PR insights mode: also appends a PR Discussion Summary and PR Context block.
    """
    login = score["engineer_login"]
    name  = (ingest or {}).get("engineer_name") or "no display name"
    org   = (ingest or {}).get("org") or "not specified"
    days  = score["lookback_days"]

    lines = [
        f"Engineer: {login} ({name})",
        f"Period: Last {days} days",
        f"Org: {org}",
        f"Overall confidence: {score['confidence']}",
    ]
    note = score.get("data_volume_note")
    if note:
        lines.append(f"Data note: {note}")

    lines.append("\n=== DIMENSION SCORES ===")
    for dim_name, dim in score["dimensions"].items():
        label = dim_name.replace("_", " ").title()
        lines.append(f"{label}: {dim['score']}/{dim['max']} ({dim['confidence']} confidence)")
        for s in dim["signals"]:
            lines.append(f"  - {s}")
        for f in dim["flags"]:
            lines.append(f"  [flag] {f}")

    total  = score["total_score"]
    n_dims = len(score["dimensions"])
    lines.append(f"\nTotal: {total}/{n_dims * 20} (all {n_dims} dimensions scored)")

    if ingest and ingest.get("summary_stats"):
        s = ingest["summary_stats"]
        lines += [
            "\n=== RAW STATS ===",
            f"PRs authored: {s['total_prs_authored']} ({s['prs_merged']} merged, "
            f"{s['prs_open']} open, {s['prs_closed_unmerged']} closed unmerged)",
            f"Reviews given: {s['total_reviews_given']}",
            f"Code volume: +{s['total_lines_added']} / -{s['total_lines_deleted']} lines",
            f"Avg PR size: {s['avg_pr_size_lines']} lines",
            f"Active weeks: {s['active_weeks']} of {s['total_weeks']}",
        ]

    flags = score.get("flags", [])
    if flags:
        lines.append("\n=== FLAGS (highest severity first) ===")
        for flag in flags:
            lines.append(f"[{flag['severity'].upper()}] {flag['dimension']}: {flag['message']}")

    # PR insights mode: append structured summary + bounded raw context
    if ingest:
        summary_block = _build_pr_summary_section(ingest)
        if summary_block:
            lines.append(f"\n{summary_block}")

        context_block = _build_pr_context_section(ingest)
        if context_block:
            lines.append(f"\n{context_block}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# LLM input payload
# ---------------------------------------------------------------------------

def build_llm_input_payload(
    score: dict,
    ingest: dict | None,
    system_prompt: str,
    *,
    model: str | None,
    provider: str | None,
    mode: str = "ai",
) -> dict:
    """
    Assemble a serializable LLM input payload.

    Parameters
    ----------
    score         : scored profile dict (from score_{login}.json)
    ingest        : ingest profile dict or None
    system_prompt : the loaded system prompt text
    model         : resolved model name, or None for stub mode
    provider      : resolved provider name, or None for stub mode
    mode          : "ai" when a provider is configured, "stub" otherwise
    """
    user_message = build_user_message(score, ingest)

    has_insights = any(
        "discussion_summary_stats" in p
        for p in (ingest or {}).get("prs_authored", [])
    )

    return {
        "version":        "1.0",
        "engineer_login": score["engineer_login"],
        "mode":           mode,
        "system":         system_prompt,
        "user":           user_message,
        "metadata": {
            "generated_at":  datetime.now(timezone.utc).isoformat(),
            "lookback_days": score["lookback_days"],
            "provider":      provider,
            "model":         model,
            "total_score":   score["total_score"],
            "confidence":    score["confidence"],
            "has_insights":  has_insights,
        },
    }


def write_llm_input(payload: dict, output_dir: Path) -> Path:
    """
    Write an LLM input payload to .pullstar/llm_input_{login}.json.

    Uses an atomic write (write to .tmp, then replace).
    Returns the final file path.
    """
    login    = payload["engineer_login"]
    out_path = output_dir / f"llm_input_{login}.json"
    tmp_path = out_path.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp_path.replace(out_path)
    return out_path
