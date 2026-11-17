#!/usr/bin/env python3
"""Generate a standalone Signal Scout HTML report from JSON.

Renders three distinct sections: Individuals, Segments, Companies. Each has
its own card layout and scoring dimensions instead of forcing every kind of
lead through one schema. Cards lead with a one-line glance view; full detail
sits behind a single expand toggle so the report reads like a deck, not a
wall of text.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlparse

import diff_reports
from people_filter import strip_people
from signal_scout_core import (
    TIER_BROKEN,
    TIER_DISQUALIFYING,
    TIER_LABELS,
    TIER_LOW_MATCH,
    TIER_UNSUPPORTED,
    TIER_VERIFIED,
    csv_safe,
)

# ── Per-type dimension specs ───────────────────────────────────────────────────

DIMENSION_SPECS: dict[str, list[tuple[str, str]]] = {
    "individual": [
        ("pain_strength", "Pain strength"),
        ("product_fit", "Product fit"),
        ("timing", "Timing"),
        ("reachability", "Reachability"),
        ("evidence_quality", "Evidence quality"),
    ],
    "segment": [
        ("pain_strength", "Pain strength"),
        ("product_fit", "Product fit"),
        ("timing", "Timing"),
        ("evidence_quality", "Evidence quality"),
    ],
    "company": [
        ("strategic_fit", "Strategic fit"),
        ("timing", "Timing"),
        ("execution_ease", "Execution ease"),
        ("evidence_quality", "Evidence quality"),
    ],
}

TYPE_LABEL = {"individual": "Individual", "segment": "Segment", "company": "Company"}
TYPE_ACCENT_CLASS = {"individual": "acc-a", "segment": "acc-b", "company": "acc-c"}


# ── Helpers ───────────────────────────────────────────────────────────────────

def esc(value: Any) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def prose(value: Any) -> str:
    """Escape, then render **bold** markdown so long-form fields can highlight
    the one fact worth catching at a glance instead of reading as flat text."""
    escaped = esc(value)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)


def script_json(value: Any) -> str:
    """JSON for an inline <script>: "</" is escaped so a field containing
    "</script>" cannot end the block."""
    return json.dumps(value).replace("</", "<\\/")


def cc_prompt(label: str, text: str) -> str:
    """Shows the full next-action prompt in the open — never hidden or truncated —
    so whoever reads the report sees exactly what would run before choosing an
    action. Two ways to act on it, either works: a real `claude-cli://open` deep
    link (see https://code.claude.com/docs/en/deep-links) that opens Claude Code
    with the prompt pre-filled but NOT sent — it still has to be reviewed and
    pressed Enter on locally — or a plain copy button for pasting anywhere else."""
    deep_link = f"claude-cli://open?q={quote(text)}"
    return (
        f'<div class="prompt-block">'
        f'<pre class="prompt-text">{esc(text)}</pre>'
        f'<div class="prompt-actions">'
        f'<a class="prompt-btn open-btn" href="{esc(deep_link)}">{esc(label)} ↗</a>'
        f'<button type="button" class="prompt-btn copy-btn">Copy</button>'
        f'</div>'
        f'</div>'
    )


def anchor_id(kind: str, index: int) -> str:
    return f"{kind}-{index}"


def slugify(value: Any) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", str(value or "").strip().lower()).strip("-")
    return slug or "signal-scout"


NEXT_ACTION_FIELD = {"individual": "opener", "segment": "content_angle", "company": "bd_angle"}

CSV_COLUMNS = [
    "type", "name", "domain", "stage", "score", "verification", "pain_signal", "why_fit", "why_now",
    "source_title", "source_url", "source_type", "signal_date", "next_action", "caution",
]


def csv_field(value: Any) -> str:
    text = "" if value is None else str(csv_safe(value))
    text = text.replace('"', '""')
    return f'"{text}"'


def build_csv(individuals: list[dict[str, Any]], segments: list[dict[str, Any]], companies: list[dict[str, Any]]) -> str:
    """Flatten all three prospect types into one CSV for spreadsheet/CRM import.
    Type-specific fields (opener/content_angle/bd_angle) collapse into a single
    `next_action` column since each row is already tagged with `type`."""
    rows = [",".join(csv_field(col) for col in CSV_COLUMNS)]
    for kind, prospects in (("individual", individuals), ("segment", segments), ("company", companies)):
        action_field = NEXT_ACTION_FIELD[kind]
        for item in prospects:
            row = [
                kind,
                item.get("name", ""),
                item.get("domain") or "",
                item.get("stage", ""),
                clamp(item.get("score")),
                TIER_LABELS.get(item.get("verification_tier"), "Unverified"),
                item.get("pain_signal", ""),
                item.get("why_fit", ""),
                item.get("why_now", ""),
                item.get("source_title", ""),
                item.get("source_url", ""),
                item.get("source_type", ""),
                item.get("signal_date", ""),
                item.get(action_field, ""),
                item.get("caution", ""),
            ]
            rows.append(",".join(csv_field(v) for v in row))
    return "\r\n".join(rows) + "\r\n"


def clamp(value: Any, maximum: int = 100) -> int:
    try:
        number = round(float(value))
    except (TypeError, ValueError):
        number = 0
    return max(0, min(maximum, number))


def items(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def dicts(value: Any) -> list[dict[str, Any]]:
    return [x for x in items(value) if isinstance(x, dict)]


def safe_url(value: Any) -> str:
    raw = str(value or "").strip()
    parsed = urlparse(raw)
    return esc(raw) if parsed.scheme in {"http", "https"} and parsed.netloc else "#"


def stage_class(stage: Any) -> str:
    value = str(stage or "").lower()
    if "high" in value:
        return "hot"
    if "problem" in value or "trigger" in value:
        return "warm"
    return "cool"


# ── Cross-run novelty (reuses diff_reports.py rather than reimplementing it) ──

def discover_history(input_path: Path) -> list[Path]:
    """Sibling analysis-*.json snapshots in the same directory as input, per
    the SKILL.md storage convention — input itself excluded. Empty if the
    convention wasn't followed (a one-off file outside that layout), which
    just means novelty badges don't render — the same degrade diff_reports.py
    has when it's given only one snapshot."""
    resolved = input_path.resolve()
    return [p for p in sorted(input_path.parent.glob("analysis-*.json")) if p.resolve() != resolved]


def discover_outcomes(input_path: Path) -> Path | None:
    candidate = input_path.parent / "outcomes.jsonl"
    return candidate if candidate.exists() else None


def compute_novelty(
    data: dict[str, Any], history_paths: list[Path], outcomes_path: Path | None
) -> dict[tuple[str, str, str], dict[str, Any]]:
    """Classify every current prospect as new/recurring against every prior
    snapshot given (not just the last one), and flag recurring prospects that
    already have a logged outcome. Delegates to diff_reports.py's own history
    accumulation and outcome index so a prospect's novelty status here always
    agrees with what `diff_reports.py --outcomes` would print for the same
    files — one definition of "have we seen this," not two."""
    if not history_paths:
        return {}
    loaded = [(p, json.loads(p.read_text(encoding="utf-8"))) for p in history_paths]
    loaded.sort(key=lambda pair: str(pair[1].get("generated_at", "")))
    history_prospects, times_seen, first_seen = diff_reports.accumulate_history(loaded)
    outcomes = diff_reports.OutcomeIndex(outcomes_path)
    curr_prospects = diff_reports.load_prospects(data)

    novelty: dict[tuple[str, str, str], dict[str, Any]] = {}
    for key in curr_prospects:
        is_new = key not in history_prospects
        entry: dict[str, Any] = {"is_new": is_new}
        if not is_new:
            entry["times_seen"] = times_seen.get(key, 0) + 1
            entry["first_seen"] = first_seen.get(key, "")
        record = outcomes.lookup(key[1], key[2])
        if record:
            entry["prior_outcome"] = f"{record.get('outcome', '?')} on {record.get('date', '?')}"
        novelty[key] = entry
    return novelty


def annotate_novelty(data: dict[str, Any], novelty: dict[tuple[str, str, str], dict[str, Any]]) -> None:
    for kind in ("individuals", "segments", "companies"):
        for item in dicts(data.get(kind)):
            key = diff_reports.prospect_key(kind, item)
            if key in novelty:
                item["_novelty"] = novelty[key]


def completeness_score(data: dict[str, Any], total_prospects: int) -> int:
    score = 0
    if data.get("product") and data.get("target_customer"):
        score += 10
    if data.get("methodology"):
        score += 5
    if data.get("search_queries_used"):
        score += 5
    if data.get("sources_consulted"):
        score += 5
    if data.get("verdict"):
        score += 5
    if total_prospects >= 5:
        score += 15
    elif total_prospects >= 1:
        score += total_prospects * 3
    patterns = items(data.get("patterns"))
    if len(patterns) >= 3:
        score += 10
    elif len(patterns) >= 1:
        score += len(patterns) * 3
    plan = data.get("outreach_plan")
    if isinstance(plan, dict) and plan.get("angle") and plan.get("first_step"):
        score += 10
    if data.get("competitive_context"):
        score += 10
    if data.get("limits"):
        score += 5
    if data.get("sources_consulted"):
        score += 10
    return min(100, score)


# ── Shared card sub-renderers ─────────────────────────────────────────────────

def render_dimensions(dimensions: Any, kind: str) -> str:
    dims = dimensions if isinstance(dimensions, dict) else {}
    rows = []
    for key, label in DIMENSION_SPECS[kind]:
        score = clamp(dims.get(key, 0), 5)
        pct = score * 20
        rows.append(
            f'<div class="metric">'
            f'<span>{esc(label)}</span>'
            f'<div class="track"><i style="width:{pct}%"></i></div>'
            f'<b>{score}/5</b>'
            f'</div>'
        )
    return "".join(rows)


def render_novelty_badge(item: dict[str, Any]) -> str:
    """Badge showing whether this prospect is new, recurring, or a recurrence
    of one already decided — absent entirely when no run history was found,
    same as a fresh product's first-ever report renders no badge at all."""
    novelty = item.get("_novelty")
    if not isinstance(novelty, dict):
        return ""
    if novelty.get("prior_outcome"):
        return (
            f'<span class="badge novelty decided" title="Already logged: {esc(novelty["prior_outcome"])}">'
            f'Resurfacing</span>'
        )
    if novelty.get("is_new"):
        return '<span class="badge novelty new">New</span>'
    first_seen = str(novelty.get("first_seen", ""))
    title_attr = f' title="First seen {esc(first_seen)}"' if first_seen else ""
    return f'<span class="badge novelty recurring"{title_attr}>Seen {novelty.get("times_seen", 2)}x</span>'


def render_card_header(item: dict[str, Any], index: int, kind: str, eyebrow_override: str = "") -> tuple[str, int]:
    score = clamp(item.get("score"))
    stage = item.get("stage", "Potential fit")
    eyebrow = eyebrow_override or TYPE_LABEL[kind]
    competitor = item.get("competitor_mentioned", "")
    competitor_badge = f'<span class="badge competitor">Uses {esc(competitor)}</span>' if competitor else ""
    tier = item.get("verification_tier")
    # "Not on page" and a dead link are different failures and must not share a
    # badge with a paraphrase — one means check the wording, the other means the
    # claim isn't real.
    verify_class = {
        TIER_VERIFIED: "verified",
        TIER_LOW_MATCH: "low-match",
        TIER_UNSUPPORTED: "unsupported",
        TIER_BROKEN: "unsupported",
    }.get(tier, "unverified")
    verified_at = str(item.get("verified_at", ""))
    verify_attr = f' data-verified-at="{esc(verified_at)}"' if verified_at else ""
    verify_badge = (
        f'<span class="badge verify {verify_class}"{verify_attr} title="{esc(item.get("verification_note", ""))}">'
        f'{esc(TIER_LABELS.get(tier, "Unverified"))}</span>'
        if tier else ""
    )
    novelty_badge = render_novelty_badge(item)
    header = f"""
      <header class="card-head">
        <div class="rank">{index:02d}</div>
        <div class="identity">
          <span class="eyebrow">{esc(eyebrow)}</span>
          <h3>{esc(item.get('name', f'{TYPE_LABEL[kind]} {index}'))}</h3>
          <div class="badges">
            <span class="stage {stage_class(stage)}">{esc(stage)}</span>
            {competitor_badge}
            {verify_badge}
            {novelty_badge}
          </div>
        </div>
        <div class="score" style="--score:{score}" aria-label="Fit score {score} out of 100">
          <strong>{score}</strong><small>/100</small>
        </div>
        <button type="button" class="link-btn" data-anchor="{anchor_id(kind, index)}" title="Copy link to this card" aria-label="Copy link to this card">↗</button>
      </header>"""
    return header, score


def render_brief_details(item: dict[str, Any], kind: str, rows_html: str, extra_html: str = "") -> str:
    source = safe_url(item.get("source_url"))
    return f"""
      <details class="brief">
        <summary>Full brief</summary>
        <div class="info-grid">{rows_html}</div>
        {extra_html}
        <div class="evidence">
          <div><span>Evidence</span><p>{prose(item.get('evidence', ''))}</p></div>
          <div>
            <span>Source</span>
            <p>{esc(item.get('source_type', 'Public source'))} · {esc(item.get('signal_date', 'Date unavailable'))}</p>
            <a href="{source}" target="_blank" rel="noreferrer">{esc(item.get('source_title', 'Open original source'))} ↗</a>
          </div>
        </div>
        <div class="metrics">{render_dimensions(item.get('dimensions'), kind)}</div>
      </details>"""


# ── Type-specific card renderers ──────────────────────────────────────────────

def render_individual(item: dict[str, Any], index: int) -> str:
    header, score = render_card_header(item, index, "individual")
    channel = item.get("suggested_channel", "")
    opener = item.get("opener", "")

    rows = (
        f'<div><span>Why it fits</span><p>{prose(item.get("why_fit", ""))}</p></div>'
        f'<div><span>Why now</span><p>{prose(item.get("why_now", ""))}</p></div>'
        f'<div><span>Channel</span><p>{esc(channel or "None found")}</p></div>'
        f'<div><span>Caution</span><p>{prose(item.get("caution", "Confirm current relevance before outreach."))}</p></div>'
    )

    opener_prompt = (
        f"Refine this outreach opener to {item.get('name', 'this contact')} on {channel or 'the channel below'}, "
        f"then get it ready for me to review before sending — never send it yourself.\n\n"
        f"Pain signal: {item.get('pain_signal', '')}\n"
        f"Why it fits: {item.get('why_fit', '')}\n"
        f"Why now: {item.get('why_now', '')}\n"
        f"Source: {item.get('source_url', '')}\n\n"
        f"Draft opener:\n{opener}"
    )
    grounding_note = item.get("opener_grounding_note", "")
    grounding_html = f'<p class="opener-warning">{esc(grounding_note)}</p>' if grounding_note else ""
    opener_html = (
        f'<blockquote><span>Suggested opener</span>{prose(opener)}</blockquote>'
        f'{grounding_html}'
        f'{cc_prompt("Open in Claude Code", opener_prompt)}' if opener else
        '<blockquote class="no-channel"><span>Next action</span>No public reply or DM channel exists. Evidence only, not a contactable lead.</blockquote>'
    )

    follow_ups = items(item.get("follow_up_sequence"))
    follow_up_html = ""
    if follow_ups:
        touches = "".join(
            f'<li><span>Follow-up {i}</span><p>{esc(fu)}</p></li>' for i, fu in enumerate(follow_ups, 1)
        )
        follow_up_html = f'<div class="follow-ups"><span>Follow-up sequence</span><ul>{touches}</ul></div>'

    return f"""
    <article id="{anchor_id('individual', index)}" class="card card-individual reveal" data-stage="{stage_class(item.get('stage', ''))}" data-score="{score}">
      {header}
      <p class="glance">{prose(item.get('pain_signal', ''))}</p>
      {render_brief_details(item, "individual", rows, opener_html + follow_up_html)}
    </article>"""


def render_segment(item: dict[str, Any], index: int) -> str:
    header, score = render_card_header(item, index, "segment")
    keywords = items(item.get("target_keywords"))
    channels = items(item.get("suggested_channels"))
    proof_points = items(item.get("proof_points"))

    keyword_html = "".join(f'<span class="chip">{esc(k)}</span>' for k in keywords) or "<span>Not specified</span>"
    channel_html = "".join(f"<li>{esc(c)}</li>" for c in channels) or "<li>Not specified</li>"
    proof_html = "".join(f"<li>{esc(p)}</li>" for p in proof_points)

    rows = (
        f'<div><span>Why it fits</span><p>{prose(item.get("why_fit", ""))}</p></div>'
        f'<div><span>Why now</span><p>{prose(item.get("why_now", ""))}</p></div>'
        f'<div><span>Channels</span><ul>{channel_html}</ul></div>'
        f'<div><span>Caution</span><p>{prose(item.get("caution", "Segment-level evidence, not an individual lead."))}</p></div>'
    )

    content_prompt = (
        f"Draft an SEO-ready page targeting the '{item.get('name', 'this segment')}' segment.\n\n"
        f"Content angle: {item.get('content_angle', '')}\n"
        f"Target keywords: {', '.join(keywords) or 'not specified'}\n"
        f"Proof points: {'; '.join(proof_points) or 'not specified'}\n"
        f"Suggested channels: {', '.join(channels) or 'not specified'}\n\n"
        f"Write a working draft (title, meta description, section outline) I can review before publishing."
    )
    extra = f'<blockquote class="content-angle"><span>Content angle</span>{prose(item.get("content_angle", ""))}</blockquote>'
    extra += cc_prompt("Open in Claude Code", content_prompt)
    extra += f'<div class="keywords"><span>Target keywords</span><div class="chip-row">{keyword_html}</div></div>'
    if proof_points:
        extra += f'<div class="proof-points"><span>Proof points</span><ul>{proof_html}</ul></div>'

    return f"""
    <article id="{anchor_id('segment', index)}" class="card card-segment reveal" data-stage="{stage_class(item.get('stage', ''))}" data-score="{score}">
      {header}
      <p class="glance">{prose(item.get('pain_signal', ''))}</p>
      {render_brief_details(item, "segment", rows, extra)}
    </article>"""


def render_company(item: dict[str, Any], index: int) -> str:
    header, score = render_card_header(item, index, "company", eyebrow_override=item.get("role", "Company"))

    tier_row = (
        f'<div><span>Why this tier</span><p>{prose(item.get("tier_rationale", ""))}</p></div>'
        if item.get("tier_rationale") else ""
    )
    rows = (
        f'<div><span>Combined value</span><p>{prose(item.get("why_fit", ""))}</p></div>'
        f'<div><span>Why now</span><p>{prose(item.get("why_now", ""))}</p></div>'
        f'<div><span>Execution path</span><p>{esc(item.get("execution_path", "Not specified"))}</p></div>'
        f'<div><span>Contact path</span><p>{esc(item.get("contact_path", "Not specified"))}</p></div>'
        f'<div><span>What to propose</span><p>{esc(item.get("what_to_propose", ""))}</p></div>'
        f'{tier_row}'
        f'<div><span>Caution</span><p>{prose(item.get("caution", "Inferred fit, not a stated partnership request."))}</p></div>'
    )
    bd_prompt = (
        f"Prepare a partnership pitch to {item.get('name', 'this company')} via {item.get('contact_path', 'their public contact channel')}.\n\n"
        f"Execution path: {item.get('execution_path', 'not specified')}\n"
        f"Combined value: {item.get('why_fit', '')}\n"
        f"Why now: {item.get('why_now', '')}\n"
        f"What to propose: {item.get('what_to_propose', '')}\n\n"
        f"Draft pitch:\n{item.get('bd_angle', '')}\n\n"
        f"Refine it, keep it under 90 words, and get it ready for me to review before sending — never send it yourself."
    )
    extra = f'<blockquote><span>BD pitch</span>{prose(item.get("bd_angle", ""))}</blockquote>'
    extra += cc_prompt("Open in Claude Code", bd_prompt)

    return f"""
    <article id="{anchor_id('company', index)}" class="card card-company reveal" data-stage="{stage_class(item.get('stage', ''))}" data-score="{score}">
      {header}
      <p class="glance">{prose(item.get('pain_signal', ''))}</p>
      {render_brief_details(item, "company", rows, extra)}
    </article>"""


RENDERERS = {"individual": render_individual, "segment": render_segment, "company": render_company}
SECTION_META = {
    "individual": ("People to message", "Each tied to a public pain, demand, or timing signal with a real reply channel. Open the brief before any outreach."),
    "segment": ("Markets to target", "Audiences and repeated patterns, sized for content, SEO, and ASO. Not a message to send."),
    "company": ("Partners to pitch", "Organizations evaluated as accounts or partners, each with a public contact path and a concrete first ask."),
}


def render_best_card(kind: str, item: dict[str, Any]) -> str:
    if not item:
        return ""
    score = clamp(item.get("score"))
    headline = item.get("why_now") or item.get("pain_signal") or item.get("content_angle") or item.get("bd_angle") or ""
    return f"""
    <div class="best-card {TYPE_ACCENT_CLASS[kind]}">
      <span class="best-label">Best {TYPE_LABEL[kind].lower()}</span>
      <h3>{esc(item.get('name', 'None qualified'))}</h3>
      <p>{esc(headline)}</p>
      <strong>{score}</strong>
    </div>"""


def render_exec_summary(
    data: dict[str, Any],
    all_prospects: list[dict[str, Any]],
    counts: dict[str, int],
    high_intent: int,
    average: int,
) -> str:
    bullets: list[str] = []

    top = max(all_prospects, key=lambda x: clamp(x.get("score")), default=None)
    if top:
        headline = top.get("why_now") or top.get("pain_signal") or ""
        bullets.append(
            f"Strongest signal: <b>{esc(top.get('name', 'Unnamed'))}</b> "
            f"({clamp(top.get('score'))}/100). {esc(headline)}"
        )

    parts = [f"{count} {label}" for label, count in counts.items() if count]
    if parts:
        bullets.append(
            f"{', '.join(parts)} qualified. {high_intent} high-intent. Average fit {average}/100."
        )

    limits = items(data.get("limits"))
    if limits:
        bullets.append(f"Biggest caveat: {esc(limits[0])}")

    if not bullets:
        return ""

    rows = "".join(f"<li>{b}</li>" for b in bullets)
    return f'<ul class="exec-summary">{rows}</ul>'


def render_action_row(plan: dict[str, Any]) -> str:
    channels = items(plan.get("channels_to_prioritize"))[:3]
    if not channels:
        return ""
    cells = "".join(
        f'<div class="action-cell"><span>Move {i}</span><p>{esc(c)}</p></div>'
        for i, c in enumerate(channels, 1)
    )
    return f'<div class="action-row">{cells}</div>'


def render_pattern(pattern: dict[str, Any], index: int) -> str:
    return f"""
    <article class="pattern reveal">
      <span class="pattern-num">{index:02d}</span>
      <div><h3>{esc(pattern.get('title', 'Repeated signal'))}</h3><p>{prose(pattern.get('insight', ''))}</p></div>
      <strong>{clamp(pattern.get('count'), 999)}x</strong>
    </article>"""


def render_growth_playbook(gp: dict[str, Any]) -> str:
    niches = dicts(gp.get("niches"))
    agents = dicts(gp.get("agents"))
    creator = gp.get("creator_program") if isinstance(gp.get("creator_program"), dict) else {}

    niche_html = "".join(
        f'<div class="niche-card"><h4>{esc(n.get("name", ""))}</h4>'
        f'<p><span>Why silent</span>{prose(n.get("why_silent", ""))}</p>'
        f'<p><span>Signal</span>{esc(n.get("signal", ""))}</p></div>'
        for n in niches
    )
    agent_html = "".join(
        f'<div class="agent-card"><span class="agent-num">{i:02d}</span>'
        f'<div><h4>{esc(a.get("name", ""))}</h4><p>{esc(a.get("job", ""))}</p></div></div>'
        for i, a in enumerate(agents, 1)
    )

    creator_html = ""
    if creator:
        creator_html = f"""
        <div class="creator-strip">
          <div><span>B2C creator CPM</span><strong>{esc(creator.get('b2c_cpm', 'Not specified'))}</strong></div>
          <div><span>B2B creator CPM</span><strong>{esc(creator.get('b2b_cpm', 'Not specified'))}</strong></div>
          <div class="creator-angle"><span>Program angle</span><p>{prose(creator.get('angle', ''))}</p></div>
        </div>"""

    if not (niches or agents or creator_html):
        return ""

    return f"""
    <section class="growth">
      <header class="section-head">
        <h2>The invisible-user play</h2>
        <p>{prose(gp.get('thesis', 'High-usage niches with zero public presence are an untapped UGC channel.'))}</p>
      </header>
      {f'<div class="niche-row">{niche_html}</div>' if niche_html else ''}
      {creator_html}
      {f'<div class="agent-row">{agent_html}</div>' if agent_html else ''}
    </section>"""


def verify_badge(item: dict[str, Any]) -> str:
    """The same tier badge cards use, for non-prospect claims (battlecard)."""
    tier = item.get("verification_tier")
    if not tier:
        return ""
    verify_class = {
        TIER_VERIFIED: "verified",
        TIER_LOW_MATCH: "low-match",
        TIER_UNSUPPORTED: "unsupported",
        TIER_BROKEN: "unsupported",
    }.get(tier, "unverified")
    verified_at = str(item.get("verified_at", ""))
    verify_attr = f' data-verified-at="{esc(verified_at)}"' if verified_at else ""
    return (
        f'<span class="badge verify {verify_class}"{verify_attr} title="{esc(item.get("verification_note", ""))}">'
        f'{esc(TIER_LABELS.get(tier, "Unverified"))}</span>'
    )


def render_battlecard(entries: list[dict[str, Any]]) -> str:
    """Per-competitor battlecard: each entry is a verified claim about where a
    competitor's own users complain, plus the counter-angle. Entries whose
    verification failed (Not on page / Broken source) are dropped here, not
    rendered with a red badge — a client deliverable never ships a claim the
    pipeline itself disproved."""
    kept = [e for e in entries if e.get("verification_tier") not in TIER_DISQUALIFYING]
    if not kept:
        return ""
    cards = []
    for entry in kept:
        source = safe_url(entry.get("source_url"))
        corroboration = ""
        if entry.get("corroboration_note"):
            corroboration = f'<span class="badge novelty recurring" title="{esc(entry["corroboration_note"])}">Single-source</span>'
        elif entry.get("corroboration_count"):
            corroboration = f'<span class="badge novelty new">Corroborated by {int(entry["corroboration_count"])} prospect(s)</span>'
        barrier = (
            f'<p><span>Switching barrier</span>{prose(entry.get("switching_barrier", ""))}</p>'
            if entry.get("switching_barrier") else ""
        )
        cards.append(f"""
        <div class="battle-card">
          <div class="battle-head">
            <h4>{esc(entry.get('competitor', 'Competitor'))}</h4>
            <div class="badges">{verify_badge(entry)}{corroboration}</div>
          </div>
          <p><span>Where their users complain</span>{prose(entry.get('claim', ''))}</p>
          <blockquote>{prose(entry.get('evidence', ''))}
            <a href="{source}" target="_blank" rel="noreferrer">{esc(entry.get('source_title', 'Source'))} ↗</a>
          </blockquote>
          {barrier}
          <p><span>Counter-angle</span>{prose(entry.get('counter_angle', ''))}</p>
        </div>""")
    return f'<div class="battle-grid">{"".join(cards)}</div>'


def render_client_summary(summary: dict[str, Any]) -> str:
    """Authored executive summary — the client-facing 'what we did, what we
    found, what to do Monday' block. Synthesis only: SKILL.md requires every
    statement here to trace to a verified prospect's fields, so this renderer
    adds no badges — the claims it summarizes carry theirs on the cards."""
    findings = items(summary.get("key_findings"))
    steps = items(summary.get("next_steps"))
    if not (summary.get("overview") or findings or steps):
        return ""
    findings_html = "".join(f"<li>{prose(f)}</li>" for f in findings)
    steps_html = "".join(f"<li>{prose(s)}</li>" for s in steps)
    return f"""
      <section class="client-summary">
        <header class="section-head">
          <h2>Executive summary</h2>
          <p>{prose(summary.get('overview', ''))}</p>
        </header>
        <div class="summary-grid">
          {f'<div><span>What we found</span><ol>{findings_html}</ol></div>' if findings_html else ''}
          {f'<div><span>Do this Monday</span><ol>{steps_html}</ol></div>' if steps_html else ''}
        </div>
      </section>"""


def render_competitive_context(ctx: dict[str, Any]) -> str:
    competitors = items(ctx.get("top_competitors"))
    comp_list = "".join(f"<li>{esc(c)}</li>" for c in competitors)
    battlecard_html = render_battlecard(dicts(ctx.get("battlecard")))
    return f"""
    <section class="competitive">
      <header class="section-head">
        <h2>The landscape they already live in</h2>
        <p>What prospects currently use, and where this product wins.</p>
      </header>
      <div class="comp-grid">
        <div class="comp-card">
          <span>Top competitors</span>
          <ul>{comp_list or '<li>Not mapped</li>'}</ul>
        </div>
        <div class="comp-card">
          <span>Switching barriers</span>
          <p>{prose(ctx.get('switching_barriers', 'Not specified'))}</p>
        </div>
        <div class="comp-card comp-card--full">
          <span>Where this product wins</span>
          <p>{prose(ctx.get('differentiation_angle', 'Not specified'))}</p>
        </div>
      </div>
      {battlecard_html}
    </section>"""


def render_research_audit(data: dict[str, Any]) -> str:
    queries = items(data.get("search_queries_used"))
    sources = items(data.get("sources_consulted"))
    methodology = data.get("methodology", "")

    query_list = "".join(f"<li><code>{esc(q)}</code></li>" for q in queries[:20])
    source_list = "".join(f"<li><code>{esc(s)}</code></li>" for s in sources[:30])

    return f"""
    <section class="audit">
      <header class="section-head">
        <h2>How this research was done</h2>
        <p>Full audit trail for reproducibility and trust.</p>
      </header>
      <div class="audit-grid">
        <div class="audit-card audit-card--full">
          <span>Methodology</span>
          <p>{prose(methodology or 'Not documented')}</p>
        </div>
        <div class="audit-card">
          <span>Queries issued ({len(queries)})</span>
          <details><summary>Show queries</summary><ul>{query_list or '<li>Not logged</li>'}</ul></details>
        </div>
        <div class="audit-card">
          <span>Sources consulted ({len(sources)})</span>
          <details><summary>Show sources</summary><ul>{source_list or '<li>Not logged</li>'}</ul></details>
        </div>
      </div>
    </section>"""


def render_type_section(kind: str, items_list: list[dict[str, Any]], title: str = "", subtitle: str = "") -> str:
    if not items_list:
        return ""
    default_title, default_subtitle = SECTION_META[kind]
    cards = "".join(RENDERERS[kind](x, i) for i, x in enumerate(items_list, 1))
    return f"""
      <section>
        <header class="section-head">
          <h2>{esc(title) or default_title}</h2>
          <p>{esc(subtitle) or default_subtitle}</p>
        </header>
        <div class="cards">
          {cards}
        </div>
      </section>"""


COMPANY_TIER_META = {
    1: ("Tier 1 — pursue now", "Strongest fit and lowest-friction path; open these conversations this week."),
    2: ("Tier 2 — nurture", "Real fit, but a slower path or weaker trigger; queue behind Tier 1."),
    3: ("Tier 3 — monitor", "Plausible but missing a live trigger; watch for a change before investing time."),
}


def render_companies(companies: list[dict[str, Any]]) -> str:
    """Companies grouped by account tier when any company declares one —
    turning a flat list into an account plan — else the flat section as before."""
    def tier_of(item: dict[str, Any]) -> int:
        try:
            tier = int(item.get("tier", 0))
        except (TypeError, ValueError):
            return 0
        return tier if tier in COMPANY_TIER_META else 0

    if not any(tier_of(c) for c in companies):
        return render_type_section("company", companies)
    sections = []
    for tier in (1, 2, 3):
        group = [c for c in companies if tier_of(c) == tier]
        if group:
            title, subtitle = COMPANY_TIER_META[tier]
            sections.append(render_type_section("company", group, title, subtitle))
    untiered = [c for c in companies if not tier_of(c)]
    if untiered:
        sections.append(render_type_section("company", untiered, "Untiered companies", "Evaluated but not yet placed in the account plan."))
    return "".join(sections)


# ── Main HTML builder ─────────────────────────────────────────────────────────

def build_html(data: dict[str, Any]) -> str:
    individuals = dicts(data.get("individuals"))
    segments = dicts(data.get("segments"))
    companies = dicts(data.get("companies"))
    all_prospects = individuals + segments + companies
    patterns = dicts(data.get("patterns"))

    scores = [clamp(x.get("score")) for x in all_prospects]
    high_intent = sum(1 for x in all_prospects if "high" in str(x.get("stage", "")).lower())
    average = round(sum(scores) / len(scores)) if scores else 0

    best_individual = max(individuals, key=lambda x: clamp(x.get("score")), default={})
    best_segment = max(segments, key=lambda x: clamp(x.get("score")), default={})
    best_company = max(companies, key=lambda x: clamp(x.get("score")), default={})

    plan = data.get("outreach_plan") if isinstance(data.get("outreach_plan"), dict) else {}
    limits = items(data.get("limits"))
    completeness = completeness_score(data, len(all_prospects))
    comp_ctx = data.get("competitive_context") if isinstance(data.get("competitive_context"), dict) else {}
    growth_playbook = data.get("growth_playbook") if isinstance(data.get("growth_playbook"), dict) else {}

    exec_summary_html = render_exec_summary(
        data,
        all_prospects,
        {"individuals": len(individuals), "segments": len(segments), "companies": len(companies)},
        high_intent,
        average,
    )
    action_row_html = render_action_row(plan)

    individuals_html = render_type_section("individual", individuals)
    segments_html = render_type_section("segment", segments)
    companies_html = render_companies(companies)

    client_summary = data.get("executive_summary") if isinstance(data.get("executive_summary"), dict) else {}
    client_summary_html = render_client_summary(client_summary) if client_summary else ""

    # Trust mark: tier counts across every checked claim — prospects plus
    # battlecard entries — rendered in the footer so the report's core promise
    # ("we re-fetched every claim") is stated where a skeptical reader looks.
    battlecard_claims = [
        e for e in dicts(comp_ctx.get("battlecard"))
        if e.get("verification_tier") not in TIER_DISQUALIFYING
    ]
    checked_claims = [x for x in all_prospects + battlecard_claims if x.get("verification_tier")]
    trust_mark_html = ""
    if checked_claims:
        verified_count = sum(1 for x in checked_claims if x.get("verification_tier") == TIER_VERIFIED)
        trust_mark_html = (
            f'<span class="trust-mark"><b>{verified_count} of {len(checked_claims)}</b> claims verified '
            f'against their live or archived source before this report shipped · '
            f'every claim discloses its source</span>'
        )

    best_row = "".join([
        render_best_card("individual", best_individual),
        render_best_card("segment", best_segment),
        render_best_card("company", best_company),
    ])

    product_url = safe_url(data.get("product_url"))
    limits_html = "".join(f"<li>{prose(x)}</li>" for x in limits)
    pattern_html = "".join(render_pattern(x, i) for i, x in enumerate(patterns, 1))

    comp_section = render_competitive_context(comp_ctx) if comp_ctx else ""
    growth_section = render_growth_playbook(growth_playbook) if growth_playbook else ""
    audit_section = render_research_audit(data)
    csv_data = build_csv(individuals, segments, companies)
    csv_filename = f"{slugify(data.get('title'))}-prospects.csv"

    channels = plan.get("channels_to_prioritize")
    channels_html = ""
    if channels:
        channel_list = "".join(
            f'<li>{esc(ch)}</li>' for ch in items(channels)
        )
        channels_html = (
            f'<div class="plan-channels"><span>Channels to prioritize</span>'
            f'<ol>{channel_list}</ol></div>'
        )

    day1_prompt = (
        f"Execute day 1 of the seven-day plan: {plan.get('first_step', '')}\n\n"
        f"Success signal to watch for: {plan.get('success', '')}"
    )
    day1_prompt_html = cc_prompt("Open day-1 prompt in Claude Code", day1_prompt)

    patterns_section = f"""
      <section>
        <header class="section-head">
          <h2>Signals that repeat</h2>
          <p>Patterns across individuals, segments, and companies point at the strongest positioning and outreach angles.</p>
        </header>
        <div class="patterns">
          {pattern_html or '<p>No repeated patterns supplied.</p>'}
        </div>
      </section>""" if patterns else ""

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark light">
  <title>{esc(data.get('title', 'Signal Scout'))} · Signal Scout report</title>
  <meta name="description" content="{esc(data.get('verdict', ''))}">
  <meta property="og:title" content="{esc(data.get('title', 'Signal Scout'))} · Signal Scout report">
  <meta property="og:description" content="{esc(data.get('verdict', ''))}">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Ccircle cx='8' cy='8' r='6' fill='%23d9531f'/%3E%3C/svg%3E">
  <style>
    :root {{
      --bg: #15130f;
      --panel: #1e1a14;
      --panel2: #2b2519;
      --ink: #f5efe2;
      --muted: #b3a68d;
      --line: rgba(245, 239, 226, .16);
      --line-strong: rgba(245, 239, 226, .3);
      --a: #ff7a45;
      --b: #6fb0a0;
      --c: #d7a544;
      --danger: #ff8f7a;
      --radius: 18px;
      --shadow: 0 1px 0 rgba(255, 255, 255, .04) inset, 0 14px 34px rgba(0, 0, 0, .38);
      --fill-a: #ff7a45; --fill-b: #6fb0a0; --fill-c: #d7a544; --fill-ink: #1a1208;
      --on-ink: #1a1208; --ink-soft: #ded4c1;
      --ok: #6fb0a0; --warn: #d7a544;
      /* Display face carries the editorial voice; UI face carries everything
         interactive. Keeping them in variables stops the two from being
         reintroduced as competing `body` rules. */
      --font-display: "Iowan Old Style", Charter, ui-serif, Georgia, "Times New Roman", serif;
      --font-ui: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, sans-serif;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    }}
    :root[data-theme="light"] {{
      --bg: #faf6ee; --panel: #ffffff; --panel2: #f2ece0; --ink: #241d13; --muted: #6d6350;
      --line: rgba(36, 29, 19, .14); --line-strong: rgba(36, 29, 19, .26);
      --a: #d9531f; --b: #2f7d68; --c: #96701c; --danger: #c73f2a;
      --shadow: 0 1px 0 rgba(255, 255, 255, .6) inset, 0 10px 26px rgba(36, 29, 19, .1);
      --on-ink: #faf6ee; --ink-soft: #4a3f2e;
    }}
    @media (prefers-color-scheme: light) {{
      :root:not([data-theme="dark"]) {{
        --bg: #faf6ee; --panel: #ffffff; --panel2: #f2ece0; --ink: #241d13; --muted: #6d6350;
        --line: rgba(36, 29, 19, .14); --line-strong: rgba(36, 29, 19, .26);
        --a: #d9531f; --b: #2f7d68; --c: #96701c; --danger: #c73f2a;
        --shadow: 0 1px 0 rgba(255, 255, 255, .6) inset, 0 10px 26px rgba(36, 29, 19, .1);
        --on-ink: #faf6ee; --ink-soft: #4a3f2e;
      }}
    }}
    *, *::before, *::after {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: var(--font-ui);
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }}
    input, button {{ font-family: var(--font-ui); }}
    /* The editorial face, applied only to display type. Body copy and controls
       stay on the UI face — the contrast between the two is the whole point. */
    h1, h2, h3, .best-card h3, .plan h2, .verdict, blockquote {{ font-family: var(--font-display); }}
    h1, h2, h3 {{ font-weight: 600; }}
    .score strong, .pattern > strong, .best-card strong, .stats strong {{
      font-family: var(--font-display); font-variant-numeric: tabular-nums;
    }}
    a {{ color: inherit; }}
    ul {{ margin: 0; padding-left: 1.2em; }}
    li {{ margin: 2px 0; }}

    .skip {{ position: absolute; left: -9999px; }}
    .skip:focus {{ left: 16px; top: 16px; z-index: 9; background: var(--fill-a); color: var(--fill-ink); padding: 10px; border-radius: 8px; }}
    button:focus-visible, summary:focus-visible, a:focus-visible {{ outline: 3px solid var(--b); outline-offset: 3px; }}

    .shell {{ width: min(1160px, calc(100% - 40px)); margin: auto; position: relative; }}

    .top {{ display: flex; justify-content: space-between; align-items: center; padding: 20px 0; border-bottom: 1px solid var(--line); }}
    .brand {{ font-weight: 800; display: flex; align-items: center; gap: 10px; letter-spacing: -.01em; }}
    .brand i {{ width: 10px; height: 10px; border-radius: 50%; background: var(--a); }}
    .meta {{ display: flex; gap: 8px; align-items: center; }}
    .chip, .badge {{
      border: 1px solid var(--line); border-radius: 999px; padding: 6px 11px; color: var(--muted);
      font: 650 11px inherit; letter-spacing: .02em; display: inline-block;
    }}
    .badge.competitor {{ border-color: var(--danger); color: var(--danger); }}
    /* The verification badge is the one claim this report makes that nothing
       else in the category makes, so it gets real colour, not a grey pill.
       Paraphrase is amber (check the wording), not-on-page is red (the claim
       may be invented) — collapsing those two into one colour was what made
       the badge unreadable at a glance. */
    .badge.verify {{ font-weight: 750; }}
    .badge.verify::before {{ content: ""; width: 6px; height: 6px; border-radius: 50%; display: inline-block; margin-right: 6px; vertical-align: 1px; background: currentColor; }}
    .badge.verify.verified {{ border-color: var(--ok); color: var(--ok); background: color-mix(in srgb, var(--ok) 12%, transparent); }}
    .badge.verify.low-match {{ border-color: var(--warn); color: var(--warn); background: color-mix(in srgb, var(--warn) 12%, transparent); }}
    .badge.verify.unsupported {{ border-color: var(--danger); color: var(--danger); background: color-mix(in srgb, var(--danger) 16%, transparent); font-weight: 800; }}
    .badge.verify.unverified {{ border-color: var(--line); color: var(--muted); }}
    .badge.verify .verify-age {{ opacity: .72; font-weight: 500; margin-left: 2px; }}
    /* Novelty badges answer "have I already seen this" at a glance — new is
       the thing worth looking at, decided is the thing worth NOT re-reading,
       plain recurring is informational and stays muted so it doesn't compete
       with new/decided for attention. Absent entirely with no run history. */
    .badge.novelty {{ font-weight: 700; }}
    .badge.novelty.new {{ border-color: var(--ok); color: var(--ok); background: color-mix(in srgb, var(--ok) 12%, transparent); }}
    .badge.novelty.recurring {{ border-color: var(--line); color: var(--muted); font-weight: 650; }}
    .badge.novelty.decided {{ border-color: var(--warn); color: var(--warn); background: color-mix(in srgb, var(--warn) 12%, transparent); }}
    .opener-warning {{ color: var(--warn); font: 650 12.5px inherit; margin: 6px 0 0; }}
    .completeness-badge {{
      background: var(--fill-a); color: var(--fill-ink); padding: 6px 12px; border-radius: 999px;
      font: 750 12px inherit; display: flex; align-items: center; gap: 6px;
    }}
    button {{ background: var(--ink); color: var(--on-ink); border: 0; border-radius: 999px; padding: 8px 14px; font: 700 13px inherit; cursor: pointer; }}

    .hero {{ padding: 56px 0 30px; }}
    .eyebrow {{ color: var(--a); font: 700 12px inherit; letter-spacing: .04em; }}
    h1 {{ font-size: clamp(38px, 6vw, 64px); line-height: 1; letter-spacing: -.03em; margin: 12px 0 18px; max-width: 780px; }}
    .verdict {{ font-size: clamp(16px, 1.6vw, 19px); color: var(--ink-soft); max-width: 68ch; margin: 0; }}
    .verdict strong, .info-grid strong, .evidence strong, blockquote strong,
    .audit-card strong, .comp-card strong, .glance strong {{ color: var(--ink); font-weight: 800; }}
    .exec-summary {{ list-style: none; margin: 18px 0 0; padding: 0; display: grid; gap: 8px; max-width: 780px; }}
    .exec-summary li {{ font-size: 14px; color: var(--muted); padding-left: 20px; position: relative; }}
    .exec-summary li::before {{ content: "-"; position: absolute; left: 0; color: var(--a); font-weight: 800; }}
    .exec-summary b {{ color: var(--ink); }}

    .action-row {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 24px; }}
    .action-cell {{ border: 1px solid var(--line); border-left: 3px solid var(--a); border-radius: 10px; padding: 14px 16px; background: var(--panel); box-shadow: var(--shadow); }}
    .action-cell span {{ display: block; font: 750 10px inherit; letter-spacing: .06em; text-transform: uppercase; color: var(--a); margin-bottom: 5px; }}
    .action-cell p {{ margin: 0; font-size: 13px; color: var(--ink-soft); }}

    .stats {{ border: 1px solid var(--line); border-radius: var(--radius); overflow: hidden; margin: 30px 0 22px; background: var(--panel); }}
    .stats-product {{ padding: 14px 18px; border-bottom: 1px solid var(--line); }}
    .stats-product p {{ margin: 5px 0 0; font-size: 14px; font-weight: 650; color: var(--ink); line-height: 1.4; }}
    .stats-product a {{ color: var(--a); font-weight: 750; white-space: nowrap; }}
    .stats-metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); }}
    .stats-metrics > div {{ padding: 16px 18px; }}
    .stats-metrics > div + div {{ border-left: 1px solid var(--line); }}
    .stats span, .info-grid span, .glance-label, .evidence span, blockquote span,
    .audit-card span, .comp-card span, .follow-ups span, .keywords span, .proof-points span,
    .battle-card p span, .summary-grid > div > span {{
      display: block; color: var(--muted); font: 700 10px inherit;
      letter-spacing: .06em; text-transform: uppercase; margin-bottom: 6px;
    }}
    .stats strong {{ font-size: 17px; }}

    .filter-bar {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 18px; padding: 14px 0; border-bottom: 1px solid var(--line); }}
    .filter-bar button {{ background: var(--panel); color: var(--muted); border: 1px solid var(--line); padding: 7px 14px; font: 700 12px inherit; transition: all .15s; }}
    .filter-bar button:hover {{ border-color: var(--a); color: var(--ink); }}
    .filter-bar button.active {{ background: var(--fill-a); color: var(--fill-ink); border-color: var(--fill-a); }}
    .filter-bar input {{ background: var(--panel); color: var(--ink); border: 1px solid var(--line); border-radius: 999px; padding: 7px 14px; font: 700 12px inherit; width: 200px; }}
    .filter-bar input::placeholder {{ color: var(--muted); }}

    .best-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 14px; margin-bottom: 56px; }}
    /* Flex column with the score pushed to the bottom, so the three scores sit
       on one line regardless of how long each headline runs. Grid's default
       top-alignment left a dead gap under short cards and made the row
       impossible to compare across. */
    .best-card {{
      display: flex; flex-direction: column; padding: 22px; border-radius: var(--radius);
      box-shadow: var(--shadow); color: var(--fill-ink);
    }}
    .best-card.acc-a {{ background: var(--fill-a); }}
    .best-card.acc-b {{ background: var(--fill-b); }}
    .best-card.acc-c {{ background: var(--fill-c); }}
    .best-label {{ font: 750 11px inherit; letter-spacing: .05em; text-transform: uppercase; opacity: .7; }}
    .best-card h3 {{ font-size: clamp(20px, 2.4vw, 26px); letter-spacing: -.01em; line-height: 1.12; margin: 8px 0; }}
    .best-card p {{ margin: 0 0 14px; font-size: 13px; line-height: 1.5; opacity: .85; }}
    .best-card strong {{
      margin-top: auto; padding-top: 10px; font-size: 34px; line-height: 1;
      border-top: 1px solid color-mix(in srgb, var(--fill-ink) 22%, transparent);
    }}

    .section-head {{ display: flex; justify-content: space-between; align-items: end; gap: 24px; padding-bottom: 16px; border-bottom: 1px solid var(--line); margin-bottom: 18px; }}
    .section-head h2 {{ font-size: clamp(26px, 3.6vw, 40px); line-height: 1.02; letter-spacing: -.025em; margin: 0; }}
    .section-head p {{ color: var(--muted); max-width: 440px; margin: 0; font-size: 14px; }}

    .cards {{ display: grid; gap: 12px; margin-bottom: 60px; }}
    .card {{
      position: relative; background: var(--panel); border: 1px solid var(--line);
      border-radius: var(--radius); padding: 20px 22px 20px 26px; box-shadow: var(--shadow);
      transition: border-color .18s ease, box-shadow .18s ease;
    }}
    /* A colour-coded spine so prospect type is legible while scrolling, without
       reading the eyebrow. Individual/Segment/Company get different next
       actions, so type is the first thing worth knowing about a card. */
    .card::before {{
      content: ""; position: absolute; left: 0; top: 14px; bottom: 14px; width: 3px;
      border-radius: 0 3px 3px 0; background: var(--a);
    }}
    .card-segment::before {{ background: var(--b); }}
    .card-company::before {{ background: var(--c); }}
    .card:hover {{ border-color: var(--line-strong); box-shadow: var(--shadow), 0 0 0 1px var(--line); }}
    .card.hidden {{ display: none; }}
    .card-head {{ display: grid; grid-template-columns: 40px 1fr 76px 30px; gap: 14px; align-items: start; }}
    .link-btn {{
      width: 30px; height: 30px; border: 1px solid var(--line); border-radius: 8px; background: var(--panel2);
      color: var(--muted); font-size: 13px; cursor: pointer; transition: color .15s, border-color .15s;
    }}
    .link-btn:hover {{ color: var(--a); border-color: var(--a); }}
    .prompt-block {{
      margin-top: 10px; border: 1px solid var(--line-strong); border-radius: 12px;
      background: var(--panel2); padding: 12px 13px;
    }}
    .prompt-text {{
      margin: 0 0 10px; padding: 0; background: none; border: 0; white-space: pre-wrap;
      word-break: break-word; max-height: 220px; overflow-y: auto;
      font: 400 12.5px/1.55 ui-monospace, SFMono-Regular, Menlo, monospace; color: var(--ink-soft);
    }}
    .prompt-actions {{ display: flex; gap: 8px; flex-wrap: wrap; }}
    .prompt-btn {{
      display: inline-flex; align-items: center; gap: 5px; background: transparent; color: var(--a);
      border: 1px solid var(--a); border-radius: 8px; padding: 7px 13px; font: 700 12px inherit;
      cursor: pointer; text-decoration: none; transition: background .15s, color .15s;
    }}
    .prompt-btn:hover {{ background: var(--a); color: var(--fill-ink); }}
    .prompt-btn.done {{ background: var(--a); color: var(--fill-ink); border-color: var(--a); }}
    .prompt-btn.open-btn {{ color: var(--b); border-color: var(--b); }}
    .prompt-btn.open-btn:hover {{ background: var(--b); color: var(--fill-ink); }}
    .rank {{ font: 800 19px inherit; color: var(--a); padding-top: 6px; }}
    .identity h3 {{ font-size: 21px; letter-spacing: -.02em; margin: 4px 0 8px; }}
    .badges {{ display: flex; gap: 6px; flex-wrap: wrap; }}
    .stage {{ display: inline-block; border: 1px solid var(--line); border-radius: 999px; padding: 5px 10px; font: 650 11px inherit; }}
    .stage.hot {{ color: var(--a); border-color: var(--a); background: color-mix(in srgb, var(--a) 12%, transparent); }}
    .stage.warm {{ color: var(--c); border-color: var(--c); background: color-mix(in srgb, var(--c) 12%, transparent); }}
    .stage.cool {{ color: var(--b); border-color: var(--b); background: color-mix(in srgb, var(--b) 12%, transparent); }}
    .score {{
      --score: 0; --ring: var(--a);
      width: 68px; height: 68px; border-radius: 50%; display: grid; place-content: center; text-align: center;
      background: radial-gradient(circle, var(--panel) 58%, transparent 60%), conic-gradient(var(--ring) calc(var(--score) * 1%), var(--line) 0);
    }}
    .card-segment .score {{ --ring: var(--b); }}
    .card-company .score {{ --ring: var(--c); }}
    .score strong {{ font-size: 20px; line-height: 1; }}
    .score small {{ color: var(--muted); font-size: 10px; }}
    .glance {{ margin: 14px 0 0; font-size: 15px; color: var(--ink-soft); }}
    .card-segment .glance {{ border-left: 3px solid var(--b); padding-left: 12px; }}
    .card-company .glance {{ border-left: 3px solid var(--c); padding-left: 12px; }}
    .card-individual .glance {{ border-left: 3px solid var(--a); padding-left: 12px; }}

    details.brief {{ margin-top: 12px; }}
    details.brief summary {{ cursor: pointer; color: var(--a); font-weight: 700; font-size: 13px; padding: 8px 0; list-style: none; }}
    details.brief summary::-webkit-details-marker {{ display: none; }}
    details.brief summary::before {{ content: "+ "; }}
    details.brief[open] summary::before {{ content: "- "; }}
    details.brief[open] summary {{ border-bottom: 1px solid var(--line); margin-bottom: 12px; width: 100%; }}

    .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }}
    .info-grid > div, .evidence > div, .comp-card {{ border: 1px solid var(--line-strong); border-radius: 12px; padding: 13px 14px; background: var(--panel2); }}
    .info-grid p {{ margin: 0; font-size: 14px; }}
    .info-grid ul {{ margin: 0; padding-left: 1.1em; font-size: 14px; }}
    blockquote {{ margin: 10px 0 0; padding: 14px; border: 1px solid var(--line-strong); border-left: 3px solid var(--a); border-radius: 12px; background: var(--panel2); color: var(--ink); font-size: 14px; }}
    blockquote.no-channel {{ border-left-color: var(--muted); color: var(--muted); }}
    blockquote.content-angle {{ border-left-color: var(--b); }}
    .card-company blockquote {{ border-left-color: var(--c); }}
    .evidence {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 10px; }}
    .evidence a {{ display: inline-block; color: var(--b); margin-top: 8px; word-break: break-word; font-size: 13px; }}
    .evidence p {{ margin: 0; font-size: 13px; }}
    .metrics {{ display: grid; gap: 8px; margin-top: 14px; }}
    .metric {{ display: grid; grid-template-columns: 135px 1fr 36px; gap: 12px; align-items: center; font-size: 12px; }}
    .track {{ height: 7px; background: var(--line); border-radius: 8px; overflow: hidden; }}
    .track i {{ display: block; height: 100%; background: var(--a); border-radius: 8px; }}
    .follow-ups, .keywords, .proof-points {{ margin-top: 10px; padding: 13px 14px; background: var(--panel2); border: 1px solid var(--line-strong); border-radius: 12px; }}
    .follow-ups ul, .proof-points ul {{ list-style: none; padding: 0; }}
    .follow-ups li, .proof-points li {{ padding: 7px 0; border-bottom: 1px solid var(--line); font-size: 13px; }}
    .follow-ups li:last-child, .proof-points li:last-child {{ border-bottom: 0; }}
    .follow-ups li span {{ font: 700 10px inherit; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); margin-bottom: 3px; display: block; }}
    .follow-ups li p {{ margin: 0; }}
    .chip-row {{ display: flex; flex-wrap: wrap; gap: 6px; }}
    .chip-row .chip {{ color: var(--ink); border-color: var(--line); }}

    .patterns {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 60px; }}
    .pattern {{ display: grid; grid-template-columns: 34px 1fr auto; gap: 13px; align-items: start; padding: 17px; border: 1px solid var(--line); border-radius: 14px; background: var(--panel); box-shadow: var(--shadow); }}
    .pattern-num {{ color: var(--a); font: 750 12px inherit; }}
    .pattern h3 {{ margin: 0 0 5px; font-size: 15px; }}
    .pattern p {{ margin: 0; color: var(--muted); font-size: 13px; }}
    .pattern > strong {{ font-size: 24px; color: var(--a); }}

    .growth {{ margin-bottom: 60px; }}
    .niche-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; margin-bottom: 12px; }}
    .niche-card {{ border: 1px solid var(--line-strong); border-left: 3px solid var(--a); border-radius: 12px; padding: 14px 16px; background: var(--panel); box-shadow: var(--shadow); }}
    .niche-card h4 {{ margin: 0 0 8px; font-size: 15px; }}
    .niche-card p {{ margin: 0 0 6px; font-size: 13px; color: var(--muted); }}
    .niche-card p span {{ display: block; font: 700 10px inherit; letter-spacing: .06em; text-transform: uppercase; color: var(--a); margin-bottom: 2px; }}
    .niche-card p:last-child {{ margin-bottom: 0; }}
    .creator-strip {{ display: grid; grid-template-columns: 1fr 1fr 1.4fr; gap: 16px; border: 1px solid var(--line-strong); border-radius: 12px; padding: 14px 16px; background: var(--panel2); margin-bottom: 12px; align-items: start; }}
    .creator-strip > div {{ padding-right: 16px; border-right: 1px solid var(--line); min-width: 0; }}
    .creator-strip > div:last-child {{ border-right: 0; padding-right: 0; }}
    .creator-strip span {{ display: block; font: 700 10px inherit; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); margin-bottom: 4px; }}
    .creator-strip strong {{ display: block; font-size: 16px; color: var(--a); line-height: 1.3; }}
    .creator-angle p {{ margin: 0; font-size: 13px; color: var(--ink); }}
    .agent-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; }}
    .agent-card {{ display: flex; gap: 10px; align-items: flex-start; border: 1px solid var(--line); border-radius: 12px; padding: 14px 16px; background: var(--panel); }}
    .agent-num {{ font: 800 15px inherit; color: var(--b); }}
    .agent-card h4 {{ margin: 0 0 4px; font-size: 14px; }}
    .agent-card p {{ margin: 0; font-size: 12px; color: var(--muted); }}

    .competitive {{ margin-bottom: 60px; }}
    .battle-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 14px; margin-top: 14px; }}
    .battle-card {{ background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); padding: 18px; box-shadow: var(--shadow); }}
    .battle-head {{ display: flex; justify-content: space-between; align-items: baseline; gap: 10px; margin-bottom: 10px; flex-wrap: wrap; }}
    .battle-head h4 {{ margin: 0; font-family: var(--font-display); font-size: 18px; }}
    .battle-card p {{ margin: 0 0 10px; font-size: 13.5px; color: var(--ink-soft); }}
    .battle-card p span {{ display: block; margin-bottom: 3px; }}
    .battle-card blockquote {{ margin: 0 0 10px; padding: 10px 14px; border-left: 3px solid var(--warn); background: var(--panel2); border-radius: 8px; font-size: 13px; color: var(--muted); }}
    .battle-card blockquote a {{ display: block; margin-top: 6px; color: var(--b); font-size: 12px; }}
    .client-summary {{ background: var(--panel); border: 1px solid var(--line-strong); border-radius: var(--radius); padding: 26px 28px; margin: 0 0 30px; box-shadow: var(--shadow); }}
    .client-summary .section-head {{ margin-bottom: 14px; }}
    .client-summary .section-head p {{ max-width: none; color: var(--ink-soft); }}
    .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 22px; }}
    .summary-grid ol {{ margin: 8px 0 0; padding-left: 20px; display: grid; gap: 7px; font-size: 13.5px; color: var(--ink-soft); }}
    .trust-mark {{ color: var(--ok); font-weight: 650; }}
    .trust-mark b {{ font-weight: 800; }}
    .comp-grid {{ display: grid; grid-template-columns: 1fr 1.3fr; gap: 10px; }}
    .comp-card--full {{ grid-column: 1 / -1; }}
    .comp-card span {{ margin-bottom: 8px; }}
    .comp-card p {{ margin: 0; font-size: 14px; max-width: 78ch; line-height: 1.6; }}
    .comp-card ul {{ margin: 0; padding-left: 1.2em; font-size: 14px; }}

    .plan {{
      display: grid; grid-template-columns: .8fr 1.2fr; gap: 26px; background: var(--panel);
      border: 1px solid var(--line); border-left: 4px solid var(--a); padding: 26px;
      border-radius: var(--radius); margin-bottom: 26px; box-shadow: var(--shadow);
    }}
    .plan-head .eyebrow {{ color: var(--a); }}
    .plan h2 {{ font-size: 26px; line-height: 1.15; letter-spacing: -.02em; margin: 8px 0; color: var(--ink); max-width: 34ch; }}
    .plan-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; align-content: start; }}
    .plan-grid > div {{ border: 1px solid var(--line); border-radius: 11px; padding: 12px; background: var(--panel2); }}
    .plan-grid span {{ display: block; font: 700 10px inherit; letter-spacing: .05em; text-transform: uppercase; margin-bottom: 5px; color: var(--muted); }}
    .plan-grid p {{ margin: 0; font-size: 14px; color: var(--ink-soft); }}
    .plan-channels {{ grid-column: 1 / -1; }}
    .plan-channels ol {{ list-style: none; counter-reset: channel-counter; margin: 6px 0 0; padding: 0; }}
    .plan-channels li {{
      counter-increment: channel-counter; position: relative; padding: 7px 0 7px 26px;
      font-size: 13px; color: var(--ink-soft); border-top: 1px solid var(--line);
    }}
    .plan-channels li:first-child {{ border-top: 0; }}
    .plan-channels li::before {{
      content: counter(channel-counter); position: absolute; left: 0; top: 8px; color: var(--a); font-weight: 800; font-size: 12px;
    }}

    .audit {{ margin-bottom: 60px; }}
    .audit-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
    .audit-card--full {{ grid-column: 1 / -1; }}
    .audit-card {{ border: 1px solid var(--line); border-radius: 14px; padding: 18px; background: var(--panel); box-shadow: var(--shadow); }}
    .audit-card p {{ font-size: 14px; max-width: 78ch; line-height: 1.6; }}
    .audit-card ul {{ list-style: none; padding: 0; max-height: 190px; overflow-y: auto; }}
    .audit-card li {{ font-size: 12px; padding: 3px 0; color: var(--muted); word-break: break-all; }}
    .audit-card code {{ font-size: 12px; color: var(--b); }}
    .audit-card summary {{ cursor: pointer; color: var(--a); font-weight: 700; font-size: 13px; }}

    .limits {{ border: 1px solid var(--line); border-radius: var(--radius); padding: 22px; color: var(--muted); margin-bottom: 50px; font-size: 14px; }}
    .limits h2 {{ color: var(--ink); margin-top: 0; font-size: 20px; }}
    .limits ul {{ list-style: none; margin: 14px 0 0; padding: 0; counter-reset: limit-counter; display: grid; grid-template-columns: 1fr 1fr; gap: 4px 28px; }}
    .limits li {{
      counter-increment: limit-counter; margin-bottom: 10px; padding: 10px 16px 10px 44px; position: relative;
      font-size: 13px; line-height: 1.6; border-left: 2px solid var(--line-strong);
    }}
    .limits li strong {{ color: var(--ink); font-weight: 800; }}
    .limits li::before {{
      content: counter(limit-counter); position: absolute; left: 10px; top: 9px; width: 18px; height: 18px;
      border-radius: 50%; background: var(--panel2); border: 1px solid var(--line-strong); color: var(--muted);
      font: 750 10px inherit; display: flex; align-items: center; justify-content: center;
    }}

    footer {{ display: flex; justify-content: space-between; gap: 20px; border-top: 1px solid var(--line); padding: 20px 0 36px; color: var(--muted); font-size: 12px; }}

    .reveal {{ animation: rise .35s ease both; }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(8px); }} }}

    @media (max-width: 820px) {{
      .shell {{ width: min(100% - 24px, 1160px); }}
      .plan {{ grid-template-columns: 1fr; }}
      .stats-metrics {{ grid-template-columns: 1fr 1fr; }}
      .stats-metrics > div + div {{ border-left: 0; border-top: 1px solid var(--line); }}
      .top {{ flex-wrap: wrap; gap: 12px; }}
      .brand, .meta button, .completeness-badge {{ white-space: nowrap; }}
      .meta {{ flex-wrap: wrap; }}
      .section-head {{ flex-direction: column; align-items: start; gap: 8px; }}
      /* Score ring sits beside the title, not on its own row under it. */
      .card-head {{ grid-template-columns: 1fr 52px; gap: 10px; }}
      .rank {{ display: none; }}
      .identity {{ grid-column: 1; grid-row: 1 / span 2; }}
      .score {{ grid-column: 2; grid-row: 1; width: 52px; height: 52px; }}
      .score strong {{ font-size: 16px; }}
      .link-btn {{ grid-column: 2; grid-row: 2; justify-self: center; }}
      .action-row {{ grid-template-columns: 1fr; }}
      .info-grid, .evidence, .patterns, .plan-grid, .comp-grid, .audit-grid, .niche-row, .agent-row, .limits ul {{ grid-template-columns: 1fr; }}
      .creator-strip {{ grid-template-columns: 1fr; }}
      .creator-strip > div {{ border-right: 0; padding-right: 0; border-bottom: 1px solid var(--line); padding-bottom: 10px; }}
      .creator-strip > div:last-child {{ border-bottom: 0; padding-bottom: 0; }}
      .meta .chip {{ display: none; }}
      .filter-bar input {{ width: 100%; }}
    }}

    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; transition: none !important; scroll-behavior: auto !important; }}
    }}

    @media print {{
      body {{ background: #fff; color: #111; }}
      .top button, .filter-bar {{ display: none; }}
      .shell {{ width: 100%; }}
      .card, .pattern, .limits, .audit-card, .comp-card {{ background: #fff; color: #111; break-inside: avoid; }}
      details.brief {{ display: block; }}
      .card.hidden {{ display: block !important; }}
    }}
  </style>
</head>
<body>
  <a class="skip" href="#main">Skip to report</a>
  <div class="shell">
    <header class="top">
      <div class="brand"><i></i> Signal Scout</div>
      <div class="meta">
        <span class="chip">Public signals only</span>
        <span class="completeness-badge">Completeness {completeness}%</span>
        <button type="button" id="exportCsvBtn">Export CSV</button>
        <button type="button" onclick="window.print()">Print / Save PDF</button>
      </div>
    </header>

    <main id="main">
      <section class="hero">
        <span class="eyebrow">Early-customer report · {esc(data.get('generated_at', ''))}</span>
        <h1>{esc(data.get('title', 'Signal Scout'))}</h1>
        <p class="verdict">{prose(data.get('verdict', 'No verdict supplied.'))}</p>
        {exec_summary_html}
        {action_row_html}
      </section>

      {client_summary_html}

      <section class="stats">
        <div class="stats-product">
          <span>Product</span>
          <p>{esc(data.get('product', 'Not specified'))} <a href="{product_url}" target="_blank" rel="noreferrer">Visit ↗</a></p>
        </div>
        <div class="stats-metrics">
          <div><span>Individuals</span><strong>{len(individuals)}</strong></div>
          <div><span>Segments</span><strong>{len(segments)}</strong></div>
          <div><span>Companies</span><strong>{len(companies)}</strong></div>
          <div><span>Completeness</span><strong>{completeness}%</strong></div>
        </div>
      </section>

      <div class="best-row">
        {best_row}
      </div>

      <div class="filter-bar" id="filterBar">
        <button class="active" data-filter="all">All ({len(all_prospects)})</button>
        <button data-filter="hot">High intent</button>
        <button data-filter="warm">Problem aware / trigger</button>
        <button data-filter="cool">Potential fit</button>
        <input type="text" id="searchInput" placeholder="Search all prospects...">
      </div>

      {individuals_html}
      {segments_html}
      {companies_html}

      {patterns_section}

      {growth_section}

      {comp_section}

      <section class="plan">
        <div class="plan-head">
          <span class="eyebrow">Seven-day manual plan</span>
          <h2>{esc(plan.get('angle', 'Validate the pain before pitching the product.'))}</h2>
        </div>
        <div class="plan-grid">
          <div><span>First step</span><p>{prose(plan.get('first_step', ''))}</p>{day1_prompt_html}</div>
          <div><span>Follow-up</span><p>{prose(plan.get('follow_up', ''))}</p></div>
          <div><span>Success signal</span><p>{prose(plan.get('success', ''))}</p></div>
          <div><span>Research scope</span><p>{esc(data.get('search_scope', 'Not specified'))}</p></div>
          {channels_html}
        </div>
      </section>

      {audit_section}

      <section class="limits">
        <h2>Use this shortlist responsibly</h2>
        <ul>{limits_html or '<li>These are potential customers, markets, and partners inferred from public signals, not confirmed buyers.</li>'}</ul>
      </section>
    </main>

    <footer>
      {trust_mark_html}
      <span>Generated by signal-scout · public signals only, no scraped contact data, no data brokers</span>
      <span>Outreach is never sent automatically.</span>
    </footer>
  </div>

  <script>
    const CSV_DATA = {script_json(csv_data)};
    const CSV_FILENAME = {script_json(csv_filename)};

    document.getElementById('exportCsvBtn').addEventListener('click', (e) => {{
      const blob = new Blob([CSV_DATA], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = CSV_FILENAME;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      flashButton(e.currentTarget, 'Downloaded ✓');
    }});

    document.querySelectorAll('.filter-bar button').forEach(btn => {{
      btn.addEventListener('click', () => {{
        document.querySelectorAll('.filter-bar button').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filter = btn.dataset.filter;
        document.querySelectorAll('.card').forEach(card => {{
          if (filter === 'all' || card.dataset.stage === filter) {{
            card.classList.remove('hidden');
          }} else {{
            card.classList.add('hidden');
          }}
        }});
      }});
    }});

    function flashButton(btn, text) {{
      const original = btn.innerHTML;
      btn.textContent = text;
      btn.classList.add('done');
      setTimeout(() => {{ btn.innerHTML = original; btn.classList.remove('done'); }}, 1800);
    }}

    async function copyText(text) {{
      try {{
        await navigator.clipboard.writeText(text);
        return true;
      }} catch (err) {{
        window.prompt('Copy this manually (clipboard access was blocked):', text);
        return false;
      }}
    }}

    document.addEventListener('click', (e) => {{
      const copyBtn = e.target.closest('.copy-btn');
      if (copyBtn) {{
        const block = copyBtn.closest('.prompt-block');
        const src = block ? block.querySelector('.prompt-text') : copyBtn.previousElementSibling;
        copyText(src.textContent).then((ok) => flashButton(copyBtn, ok ? 'Copied ✓' : 'See prompt'));
        return;
      }}
      const linkBtn = e.target.closest('.link-btn');
      if (linkBtn) {{
        const url = `${{location.origin}}${{location.pathname}}#${{linkBtn.dataset.anchor}}`;
        copyText(url).then(() => flashButton(linkBtn, '✓'));
        location.hash = linkBtn.dataset.anchor;
      }}
    }});

    // Computed against the *viewer's* clock, not the report's generation
    // time — this report is a static file that may be reopened weeks after
    // it was built, and staleness should reflect that, not the day it shipped.
    document.querySelectorAll('.badge.verify[data-verified-at]').forEach(badge => {{
      const verifiedDate = new Date(badge.dataset.verifiedAt);
      if (Number.isNaN(verifiedDate.getTime())) return;
      const days = Math.floor((Date.now() - verifiedDate.getTime()) / 86400000);
      if (days < 1) return;
      const suffix = document.createElement('small');
      suffix.className = 'verify-age';
      suffix.textContent = ` · ${{days}}d ago`;
      badge.appendChild(suffix);
    }});

    document.getElementById('searchInput').addEventListener('input', (e) => {{
      const q = e.target.value.toLowerCase();
      document.querySelectorAll('.card').forEach(card => {{
        const text = card.textContent.toLowerCase();
        card.classList.toggle('hidden', q.length > 0 && !text.includes(q));
      }});
      if (q.length > 0) {{
        document.querySelectorAll('.filter-bar button').forEach(b => b.classList.remove('active'));
      }} else {{
        document.querySelector('.filter-bar button[data-filter="all"]').classList.add('active');
      }}
    }});
  </script>
</body>
</html>"""


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Path to report JSON")
    parser.add_argument("output", type=Path, help="Path to output HTML")
    parser.add_argument(
        "--history", type=Path, nargs="*", default=None,
        help="Prior analysis-*.json snapshots for New/Recurring/Resurfacing badges. "
        "Auto-detected from sibling files (SKILL.md storage convention) if omitted.",
    )
    parser.add_argument(
        "--no-history", action="store_true",
        help="Disable novelty-badge auto-detection even if sibling analysis-*.json snapshots exist.",
    )
    parser.add_argument(
        "--outcomes", type=Path, default=None,
        help="outcomes.jsonl for flagging resurfacing prospects already decided. "
        "Auto-detected as a sibling file if omitted.",
    )
    args = parser.parse_args()

    with args.input.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit("Input JSON must contain an object at the top level.")
    if data.get("people") is False:
        # Belt and braces for direct runs: a file marked no-people never renders a person.
        data, _ = strip_people(data)

    if not any(dicts(data.get(k)) for k in ("individuals", "segments", "companies")):
        raise SystemExit("At least one of individuals, segments, or companies must be a non-empty array.")

    if args.no_history:
        history_paths: list[Path] = []
    elif args.history is not None:
        history_paths = args.history
    else:
        history_paths = discover_history(args.input)
    outcomes_path = args.outcomes if args.outcomes is not None else discover_outcomes(args.input)

    if history_paths:
        novelty = compute_novelty(data, history_paths, outcomes_path)
        annotate_novelty(data, novelty)
        new_count = sum(1 for v in novelty.values() if v.get("is_new"))
        decided_count = sum(1 for v in novelty.values() if v.get("prior_outcome"))
        print(
            f"Novelty: {len(history_paths)} prior snapshot(s) found — {new_count} new, "
            f"{len(novelty) - new_count} recurring ({decided_count} already decided)."
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_html(data), encoding="utf-8")
    print(f"Created report: {args.output.resolve()}")


if __name__ == "__main__":
    main()
