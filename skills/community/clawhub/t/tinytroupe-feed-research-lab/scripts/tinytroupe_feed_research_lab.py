#!/usr/bin/env python3
"""Run bounded synthetic audience research for draft posts."""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import statistics
import sys
import textwrap
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


BOUNDARY = (
    "This is synthetic audience research. It does not predict reach, rank, "
    "virality, revenue, or live X production behavior."
)

TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_'-]{2,}")
URL_RE = re.compile(r"https?://|www\.")
QUESTION_RE = re.compile(r"\?")
CTA_RE = re.compile(r"\b(reply|comment|tell me|what do you think|which|why|how|would you|send me)\b", re.I)
PROOF_RE = re.compile(r"\b(source|evidence|repo|commit|file|line|audit|data|receipt|proof|public)\b", re.I)
RISK_RE = re.compile(r"\b(guarantee|guaranteed|viral|growth hack|boost|shadowban|shadow ban|rank|reach|100x|150x|onlyfans)\b", re.I)
HYPE_RE = re.compile(r"\b(insane|secret|destroyed|exposed|everyone|always|never|massive|king)\b", re.I)


@dataclass
class Draft:
    id: str
    text: str


@dataclass
class Persona:
    name: str
    segment: str
    interests: list[str]
    dislikes: list[str] = field(default_factory=list)
    reply_bias: float = 0.5
    skepticism: float = 0.5
    link_sensitivity: float = 0.5
    safety_strictness: float = 0.5
    clarity_need: float = 0.5


@dataclass
class Reaction:
    persona: str
    segment: str
    draft_id: str
    interest: float
    clarity: float
    replyability: float
    trust: float
    safety: float
    link_friction: float
    conversation_score: float
    action: str
    reason: str
    suggested_rewrite: str


DEFAULT_PERSONAS = [
    Persona(
        name="Skeptical Engineer",
        segment="technical builder",
        interests=["source", "repo", "evidence", "architecture", "code", "phoenix", "grok", "audit"],
        dislikes=["hype", "guarantee", "viral", "secret"],
        reply_bias=0.42,
        skepticism=0.82,
        link_sensitivity=0.35,
        safety_strictness=0.55,
        clarity_need=0.72,
    ),
    Persona(
        name="Creator Operator",
        segment="creator",
        interests=["draft", "reply", "conversation", "audience", "share", "post", "hook"],
        dislikes=["jargon", "long", "unclear"],
        reply_bias=0.78,
        skepticism=0.42,
        link_sensitivity=0.62,
        safety_strictness=0.38,
        clarity_need=0.56,
    ),
    Persona(
        name="Brand Safety Lead",
        segment="marketing and trust",
        interests=["brand", "safety", "risk", "evidence", "policy", "claim", "audit"],
        dislikes=["profanity", "shadowban", "guarantee", "onlyfans"],
        reply_bias=0.36,
        skepticism=0.76,
        link_sensitivity=0.48,
        safety_strictness=0.9,
        clarity_need=0.76,
    ),
    Persona(
        name="Busy Founder",
        segment="operator",
        interests=["summary", "decision", "traction", "experiment", "proof", "fast"],
        dislikes=["thread", "academic", "unclear", "huge"],
        reply_bias=0.5,
        skepticism=0.58,
        link_sensitivity=0.5,
        safety_strictness=0.45,
        clarity_need=0.82,
    ),
    Persona(
        name="Policy Analyst",
        segment="research",
        interests=["public", "claim", "misleading", "unsupported", "source", "boundary", "evidence"],
        dislikes=["overclaim", "predict", "shadowban", "secret"],
        reply_bias=0.45,
        skepticism=0.86,
        link_sensitivity=0.28,
        safety_strictness=0.72,
        clarity_need=0.74,
    ),
    Persona(
        name="Casual Reader",
        segment="general audience",
        interests=["simple", "why", "what", "new", "interesting", "clear"],
        dislikes=["jargon", "code", "long", "confusing"],
        reply_bias=0.55,
        skepticism=0.35,
        link_sensitivity=0.7,
        safety_strictness=0.4,
        clarity_need=0.66,
    ),
]


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def tokens(text: str) -> set[str]:
    return {m.group(0).lower().strip("'") for m in TOKEN_RE.finditer(text)}


def normalize_persona(raw: dict) -> Persona:
    base = {
        "name": "Synthetic Persona",
        "segment": "custom",
        "interests": [],
        "dislikes": [],
        "reply_bias": 0.5,
        "skepticism": 0.5,
        "link_sensitivity": 0.5,
        "safety_strictness": 0.5,
        "clarity_need": 0.5,
    }
    base.update(raw)
    base["interests"] = [str(x).lower() for x in base.get("interests") or []]
    base["dislikes"] = [str(x).lower() for x in base.get("dislikes") or []]
    for key in ["reply_bias", "skepticism", "link_sensitivity", "safety_strictness", "clarity_need"]:
        base[key] = clamp(float(base.get(key, 0.5)))
    return Persona(**base)


def load_personas(path: str | None) -> list[Persona]:
    if not path:
        return DEFAULT_PERSONAS
    data = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("--personas-file must contain a JSON list")
    return [normalize_persona(item) for item in data]


def load_drafts(args: argparse.Namespace) -> list[Draft]:
    drafts: list[Draft] = []
    for i, text in enumerate(args.draft or [], start=1):
        if text.strip():
            drafts.append(Draft(id=f"draft_{i}", text=text.strip()))

    if args.drafts_file:
        path = Path(args.drafts_file).expanduser()
        raw = path.read_text(encoding="utf-8")
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                for i, item in enumerate(data, start=1):
                    if isinstance(item, str):
                        drafts.append(Draft(id=f"draft_{len(drafts) + 1}", text=item.strip()))
                    elif isinstance(item, dict):
                        text = str(item.get("text", "")).strip()
                        if text:
                            drafts.append(Draft(id=str(item.get("id") or f"draft_{len(drafts) + 1}"), text=text))
                    else:
                        raise ValueError
            else:
                raise ValueError
        except ValueError:
            blocks = [block.strip() for block in re.split(r"(?m)^---+$", raw) if block.strip()]
            for block in blocks:
                drafts.append(Draft(id=f"draft_{len(drafts) + 1}", text=block))

    if len(drafts) < 1:
        raise SystemExit("Provide at least one draft via --draft or --drafts-file.")
    return drafts


def score_reaction(draft: Draft, persona: Persona, audience: str) -> Reaction:
    text = draft.text
    draft_tokens = tokens(text)
    audience_tokens = tokens(audience)
    interest_terms = set(persona.interests) | audience_tokens
    dislike_terms = set(persona.dislikes)

    overlap = len(draft_tokens & interest_terms)
    dislike_hits = len(draft_tokens & dislike_terms)
    interest = clamp(0.25 + overlap * 0.11 - dislike_hits * 0.08)

    length = len(text)
    length_fit = 1.0 - min(abs(length - 170) / 280, 0.65)
    jargon_hits = len(draft_tokens & {"algorithm", "hydrator", "transformer", "phoenix", "grox", "inference", "recsys"})
    clarity = clamp(0.28 + length_fit * 0.55 - jargon_hits * 0.035 * persona.clarity_need)

    has_question = bool(QUESTION_RE.search(text))
    has_cta = bool(CTA_RE.search(text))
    has_proof = bool(PROOF_RE.search(text))
    hype_hits = len(HYPE_RE.findall(text))
    risk_hits = len(RISK_RE.findall(text))
    has_link = bool(URL_RE.search(text))

    replyability = clamp(0.2 + persona.reply_bias * 0.34 + (0.18 if has_question else 0) + (0.16 if has_cta else 0) + interest * 0.18 - risk_hits * 0.04)
    trust = clamp(0.42 + (0.22 if has_proof else 0) - persona.skepticism * risk_hits * 0.09 - hype_hits * 0.06)
    safety = clamp(0.92 - persona.safety_strictness * risk_hits * 0.12 - hype_hits * 0.035)
    link_friction = clamp((0.16 if has_link else 0.0) + persona.link_sensitivity * (0.28 if has_link else 0.03))

    conversation_score = clamp(
        0.30 * interest
        + 0.24 * replyability
        + 0.18 * clarity
        + 0.18 * trust
        + 0.10 * safety
        - 0.18 * link_friction
    )
    if conversation_score >= 0.72 and replyability >= 0.65:
        action = "reply"
    elif conversation_score >= 0.62:
        action = "like"
    elif link_friction > 0.32 or safety < 0.62:
        action = "skip"
    else:
        action = "read"

    reason_bits = []
    if overlap:
        reason_bits.append("matches interests")
    if has_question or has_cta:
        reason_bits.append("invites response")
    if has_proof:
        reason_bits.append("offers proof")
    if risk_hits:
        reason_bits.append("contains overclaim-risk wording")
    if has_link:
        reason_bits.append("has link friction")
    reason = ", ".join(reason_bits) or "neutral reaction"

    rewrite = suggest_rewrite(persona, has_question, has_proof, risk_hits, has_link, clarity)
    return Reaction(
        persona=persona.name,
        segment=persona.segment,
        draft_id=draft.id,
        interest=round(interest, 3),
        clarity=round(clarity, 3),
        replyability=round(replyability, 3),
        trust=round(trust, 3),
        safety=round(safety, 3),
        link_friction=round(link_friction, 3),
        conversation_score=round(conversation_score, 3),
        action=action,
        reason=reason,
        suggested_rewrite=rewrite,
    )


def suggest_rewrite(
    persona: Persona,
    has_question: bool,
    has_proof: bool,
    risk_hits: int,
    has_link: bool,
    clarity: float,
) -> str:
    suggestions = []
    if not has_question:
        suggestions.append("end with a concrete question")
    if not has_proof and persona.skepticism > 0.55:
        suggestions.append("add a source or evidence phrase")
    if risk_hits:
        suggestions.append("replace reach/boost/secret wording with bounded research wording")
    if has_link and persona.link_sensitivity > 0.55:
        suggestions.append("put the link after the main claim or in a follow-up")
    if clarity < 0.55:
        suggestions.append("shorten and reduce jargon")
    if not suggestions:
        suggestions.append("keep the core angle and make the first sentence sharper")
    return "; ".join(suggestions[:3])


def aggregate(drafts: list[Draft], reactions: list[Reaction]) -> dict[str, dict[str, object]]:
    by_draft: dict[str, list[Reaction]] = {d.id: [] for d in drafts}
    for reaction in reactions:
        by_draft[reaction.draft_id].append(reaction)

    result: dict[str, dict[str, object]] = {}
    for draft in drafts:
        rows = by_draft[draft.id]
        avg = lambda field: round(statistics.mean(getattr(r, field) for r in rows), 3)
        actions = {name: sum(1 for r in rows if r.action == name) for name in ["reply", "like", "read", "skip"]}
        result[draft.id] = {
            "text": draft.text,
            "conversation_score": avg("conversation_score"),
            "interest": avg("interest"),
            "clarity": avg("clarity"),
            "replyability": avg("replyability"),
            "trust": avg("trust"),
            "safety": avg("safety"),
            "link_friction": avg("link_friction"),
            "actions": actions,
        }
    return result


def warnings_for(drafts: list[Draft]) -> list[str]:
    warnings = []
    all_text = "\n".join(d.text for d in drafts).lower()
    if any(term in all_text for term in ["predict reach", "shadowban", "shadow ban", "boost", "algorithm hack"]):
        warnings.append("Input contains prediction/boost/shadowban language. Reframe results as synthetic research only.")
    if URL_RE.search(all_text):
        warnings.append("At least one draft contains a link; synthetic personas may apply link-friction penalties.")
    if len(drafts) == 1:
        warnings.append("Only one draft was supplied. Comparison is stronger with 2-5 variants.")
    return warnings


def best_draft_id(summary: dict[str, dict[str, object]]) -> str:
    return max(summary, key=lambda key: float(summary[key]["conversation_score"]))


def render_report(audit: dict[str, object]) -> str:
    summary: dict[str, dict[str, object]] = audit["draft_summary"]  # type: ignore[assignment]
    best = audit["best_draft_id"]
    lines = [
        "# TinyTroupe Feed Research Lab Report",
        "",
        f"- Generated: `{audit['generated_at']}`",
        f"- Audience: {audit['audience']}",
        f"- Best synthetic conversation draft: `{best}`",
        "",
        "## Boundary",
        "",
        BOUNDARY,
        "",
        "## Draft Comparison",
        "",
        "| Draft | Conversation | Replyability | Clarity | Trust | Safety | Link friction | Actions |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for draft_id, data in sorted(summary.items(), key=lambda item: float(item[1]["conversation_score"]), reverse=True):
        actions = data["actions"]
        lines.append(
            f"| {draft_id} | {data['conversation_score']} | {data['replyability']} | {data['clarity']} | {data['trust']} | {data['safety']} | {data['link_friction']} | {actions} |"
        )
    lines.extend(["", "## Best Draft", "", f"```text\n{summary[str(best)]['text']}\n```", ""])
    lines.extend(["## Why It Won", ""])
    best_reactions = [r for r in audit["reactions"] if r["draft_id"] == best]  # type: ignore[index]
    reasons = top_counts(r["reason"] for r in best_reactions)
    lines.extend(f"- {reason} ({count})" for reason, count in reasons[:5])
    lines.extend(["", "## Rewrite Suggestions", ""])
    suggestions = top_counts(r["suggested_rewrite"] for r in best_reactions)
    lines.extend(f"- {suggestion} ({count})" for suggestion, count in suggestions[:5])
    lines.extend(["", "## Warnings", ""])
    warnings = audit["warnings"]  # type: ignore[assignment]
    if warnings:
        lines.extend(f"- {warning}" for warning in warnings)
    else:
        lines.append("- No high-risk wording detected in the supplied drafts.")
    lines.extend(
        [
            "",
            "## Next Experiment",
            "",
            "Run the top two drafts against a smaller, sharper persona set or validate with real users before posting decisions.",
            "",
            f"Boundary: {BOUNDARY}",
        ]
    )
    return "\n".join(lines)


def top_counts(items: Iterable[str]) -> list[tuple[str, int]]:
    counts: dict[str, int] = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))


def write_reactions_csv(path: Path, reactions: list[Reaction]) -> None:
    fields = list(asdict(reactions[0]).keys()) if reactions else []
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for reaction in reactions:
            writer.writerow(asdict(reaction))


def render_share_card_md(audit: dict[str, object]) -> str:
    best = str(audit["best_draft_id"])
    data = audit["draft_summary"][best]  # type: ignore[index]
    return "\n".join(
        [
            "Synthetic Audience Result",
            "",
            f"Best draft: {best}",
            f"Conversation score: {data['conversation_score']}",
            "",
            "Use this as a research signal, not reach prediction.",
        ]
    )


def render_share_card_svg(audit: dict[str, object]) -> str:
    best = str(audit["best_draft_id"])
    data = audit["draft_summary"][best]  # type: ignore[index]
    text = str(data["text"])
    wrapped = textwrap.wrap(text, width=74)[:5]
    y = 170
    body = []
    for line in wrapped:
        body.append(f'<text x="48" y="{y}" class="body">{html.escape(line)}</text>')
        y += 30
    height = max(360, y + 100)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}">
  <style>
    .title {{ font: 750 36px system-ui, -apple-system, Segoe UI, sans-serif; fill: #102A43; }}
    .score {{ font: 800 48px system-ui, -apple-system, Segoe UI, sans-serif; fill: #146C5C; }}
    .body {{ font: 24px system-ui, -apple-system, Segoe UI, sans-serif; fill: #243B53; }}
    .foot {{ font: 20px system-ui, -apple-system, Segoe UI, sans-serif; fill: #627D98; }}
  </style>
  <rect width="1200" height="{height}" rx="28" fill="#F7FAF9"/>
  <rect x="24" y="24" width="1152" height="{height - 48}" rx="22" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2"/>
  <text x="48" y="78" class="title">Synthetic Audience Feed Research</text>
  <text x="48" y="136" class="score">Best: {html.escape(best)} · {data['conversation_score']}</text>
  {''.join(body)}
  <text x="48" y="{height - 52}" class="foot">Boundary: synthetic research signal, not reach or ranking prediction.</text>
</svg>
"""


def render_tinytroupe_plan(audit: dict[str, object]) -> str:
    lines = [
        "# TinyTroupe Experiment Plan",
        "",
        "Use this only if a richer LLM persona simulation is justified after the deterministic pretest.",
        "",
        "## Boundary",
        "",
        BOUNDARY,
        "",
        "## Personas",
        "",
    ]
    for persona in audit["personas"]:  # type: ignore[index]
        lines.append(f"- {persona['name']} ({persona['segment']}): interests={persona['interests']}")
    lines.extend(["", "## Reaction Schema", "", "```json", json.dumps({
        "dwell": "0.0-1.0",
        "like": "boolean",
        "reply": "string or null",
        "repost": "boolean",
        "not_interested": "boolean",
        "reason": "one sentence",
    }, indent=2), "```", ""])
    lines.extend(["## Instruction", "", "Ask each TinyPerson to read each draft, respond with the schema above, then compare aggregate objections and conversation hooks."])
    return "\n".join(lines)


def build_audit(drafts: list[Draft], personas: list[Persona], audience: str) -> dict[str, object]:
    reactions = [score_reaction(draft, persona, audience) for draft in drafts for persona in personas]
    summary = aggregate(drafts, reactions)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "audience": audience or "general synthetic audience",
        "boundary": BOUNDARY,
        "warnings": warnings_for(drafts),
        "drafts": [asdict(d) for d in drafts],
        "personas": [asdict(p) for p in personas],
        "reactions": [asdict(r) for r in reactions],
        "draft_summary": summary,
        "best_draft_id": best_draft_id(summary),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audience", default="", help="Target audience description.")
    parser.add_argument("--draft", action="append", help="Draft post text. Repeat for multiple drafts.")
    parser.add_argument("--drafts-file", help="JSON or --- separated text file of drafts.")
    parser.add_argument("--personas-file", help="Optional JSON list of persona specs.")
    parser.add_argument("--output-dir", default="tinytroupe-feed-research", help="Output directory.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    drafts = load_drafts(args)
    personas = load_personas(args.personas_file)
    out = Path(args.output_dir).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)

    audit = build_audit(drafts, personas, args.audience)
    (out / "feed_research.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    (out / "feed_research_report.md").write_text(render_report(audit) + "\n", encoding="utf-8")
    write_reactions_csv(out / "persona_reactions.csv", [Reaction(**r) for r in audit["reactions"]])  # type: ignore[arg-type]
    (out / "share_card.md").write_text(render_share_card_md(audit) + "\n", encoding="utf-8")
    (out / "share_card.svg").write_text(render_share_card_svg(audit), encoding="utf-8")
    (out / "tinytroupe_experiment_plan.md").write_text(render_tinytroupe_plan(audit) + "\n", encoding="utf-8")

    print(f"Wrote {out / 'feed_research_report.md'}")
    print(f"Wrote {out / 'feed_research.json'}")
    print(f"Wrote {out / 'persona_reactions.csv'}")
    print(f"Best draft: {audit['best_draft_id']}")
    print(BOUNDARY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
