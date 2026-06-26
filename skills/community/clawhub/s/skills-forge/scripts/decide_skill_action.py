#!/usr/bin/env python3
"""Route a detected opportunity: evolve an existing skill or forge a new one.

Inputs:
  - An opportunity (CLI args, JSON file, or stdin) — the same shape that
    detect_skill_opportunities.py emits.
  - The installed skill manifest under <target_root>/.skill-forge-installs.json
    plus each installed skill's SKILL.md.

Decision:
  - For every active installed skill, compute a fitness score against the
    opportunity. Profile mismatch is a hard gate (score = 0.0). Otherwise:
        score = 0.4 * trigger_overlap
              + 0.4 * topic_overlap
              + 0.2 * name_overlap
    where each overlap is a Jaccard index over relevant token sets.
  - decision = "evolve" when the top score >= --evolve-threshold AND the
    second-best score is at least --ambiguous-margin lower.
  - decision = "ambiguous" when the top two scores are both above the
    threshold but tied within --ambiguous-margin (the caller decides).
  - decision = "forge" otherwise.

The point of the gate isn't to be "right" in some abstract sense — it's to
prevent skill sprawl when a request is really just a new trigger surface for
an existing skill. The replay non-regression gate is the safety net that
catches bad evolution outcomes downstream.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional


DEFAULT_TARGET_ROOT = Path.home() / ".openclaw" / "workspace" / "skills"
DEFAULT_EVOLVE_THRESHOLD = 0.45
DEFAULT_AMBIGUOUS_MARGIN = 0.1

# Fitness weights — calibrated so that 6/8 trigger overlap with same profile
# crosses the threshold even when SKILL.md boilerplate dilutes topic overlap.
WEIGHT_TRIGGER = 0.7
WEIGHT_TOPIC = 0.2
WEIGHT_NAME = 0.1

STOPWORDS = {
    "the", "and", "for", "that", "with", "from", "this", "have", "your", "will",
    "skill", "agent", "user", "users", "openclaw", "task", "tasks",
    "use", "uses", "when", "what", "into", "they", "them", "than", "need", "needs",
    "should", "could", "make", "creates", "create", "support", "helper", "guidance",
    "output", "outputs", "workflow", "workflows", "able", "ability", "feature",
    # Generic / structural words also filtered by generate_skill_scaffold so the
    # router sees the same trigger surface that the scaffold treats as noise.
    "reusable", "structure", "reminders", "recurring", "process", "repeatable",
    "notes", "generic", "simple", "basic", "common",
}

PROFILE_KEYWORDS = {
    "academic": {"citation", "bibliography", "reference", "apa", "mla", "harvard",
                 "chicago", "essay", "paper", "assignment", "source metadata"},
    "product": {"prd", "mvp", "roadmap", "acceptance criteria", "user story",
                "requirements", "dev handoff", "competitive"},
    "integration": {"api", "oauth", "webhook", "token", "credential", "telegram",
                    "notion", "connector", "health check"},
    "script": {"script", "cli", "batch", "parse", "validate", "export",
               "convert", "exit code", "dry-run"},
}


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-{2,}", "-", value).strip("-")


def name_tokens(name: str) -> set:
    parts = slugify(name).split("-")
    return {p for p in parts if len(p) >= 3 and p not in STOPWORDS}


def trigger_tokens(triggers: list) -> set:
    tokens = set()
    for trigger in triggers:
        for word in re.findall(r"[a-zA-Z][a-zA-Z0-9]{2,}", trigger.lower()):
            if word not in STOPWORDS:
                tokens.add(word)
    return tokens


def topic_tokens(text: str, limit: int = 80) -> set:
    # 3+ char tokens so acronyms (APA, MLA, CSV, SQL, JWT, …) survive — those
    # are usually the high-signal terms that distinguish skills.
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9]{2,}", text.lower())
    counts = {}
    for word in words:
        if word in STOPWORDS:
            continue
        counts[word] = counts.get(word, 0) + 1
    sorted_words = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return {word for word, _ in sorted_words[:limit]}


def jaccard(a: set, b: set) -> float:
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


def parse_frontmatter(content: str) -> dict:
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    result = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip('"')
    return result


def extract_triggers_from_skill_md(content: str) -> list:
    match = re.search(r"(?ms)^## Trigger Cues\s*\n(.*?)(?=^## |\Z)", content)
    if not match:
        return []
    triggers = []
    for line in match.group(1).splitlines():
        item = re.match(r"\s*-\s+`?([^`\n]+?)`?\s*$", line)
        if item:
            triggers.append(item.group(1).strip())
    return triggers


def infer_profile_from_skill_md(content: str) -> str:
    text = content.lower()
    scores = {p: sum(1 for kw in kws if kw in text) for p, kws in PROFILE_KEYWORDS.items()}
    profile, score = max(scores.items(), key=lambda item: item[1])
    return profile if score >= 2 else "workflow"


def load_manifest(target_root: Path) -> dict:
    path = target_root / ".skill-forge-installs.json"
    if not path.exists():
        return {"installs": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"installs": {}}


def installed_skills(target_root: Path) -> list:
    manifest = load_manifest(target_root)
    skills = []
    for name, record in manifest.get("installs", {}).items():
        if record.get("active") is False:
            continue
        source = record.get("source") or record.get("target")
        if not source:
            continue
        skill_md = Path(source).expanduser() / "SKILL.md"
        if not skill_md.is_file():
            continue
        try:
            content = skill_md.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        frontmatter = parse_frontmatter(content)
        triggers = extract_triggers_from_skill_md(content)
        profile = infer_profile_from_skill_md(content)
        skills.append({
            "name": frontmatter.get("name", name),
            "manifest_name": name,
            "source_dir": str(source),
            "profile": profile,
            "triggers": triggers,
            "name_tokens": name_tokens(name),
            "trigger_tokens": trigger_tokens(triggers),
            "topic_tokens": topic_tokens(content),
        })
    return skills


def fitness(opp_profile: str, opp_name: str, opp_name_toks: set, opp_trigger_toks: set,
            opp_topic_toks: set, existing: dict) -> tuple:
    if opp_profile != existing["profile"]:
        return 0.0, {
            "profile_match": False,
            "exact_name_match": False,
            "trigger_overlap": 0.0,
            "name_overlap": 0.0,
            "topic_overlap": 0.0,
        }
    # Exact-name match short-circuit: when the user (or detect) names the
    # opportunity identically to an installed skill, profile already matches,
    # this is a near-certain evolve signal regardless of trigger phrasing.
    exact_name_match = bool(opp_name) and slugify(opp_name) == slugify(existing.get("manifest_name", existing["name"]))
    trigger_overlap = jaccard(opp_trigger_toks, existing["trigger_tokens"])
    name_overlap = jaccard(opp_name_toks, existing["name_tokens"])
    topic_overlap = jaccard(opp_topic_toks, existing["topic_tokens"])
    if exact_name_match:
        score = 1.0
    else:
        score = (WEIGHT_TRIGGER * trigger_overlap
                 + WEIGHT_TOPIC * topic_overlap
                 + WEIGHT_NAME * name_overlap)
    return round(score, 3), {
        "profile_match": True,
        "exact_name_match": exact_name_match,
        "trigger_overlap": round(trigger_overlap, 3),
        "name_overlap": round(name_overlap, 3),
        "topic_overlap": round(topic_overlap, 3),
    }


def opportunity_topic_text(opportunity: dict) -> str:
    parts = [opportunity.get("suggested_skill_name", "")]
    parts.extend(opportunity.get("triggers", []) or [])
    parts.append(opportunity.get("reason", ""))
    for evidence in opportunity.get("evidence", []) or []:
        parts.append(evidence.get("snippet", ""))
    return " ".join(parts)


def decide(opportunity: dict, target_root: Path,
           threshold: float, ambiguous_margin: float) -> dict:
    opp_profile = opportunity.get("recommended_template") or "workflow"
    opp_name = opportunity.get("suggested_skill_name", "")
    opp_triggers = opportunity.get("triggers", []) or []
    opp_name_toks = name_tokens(opp_name)
    opp_trigger_toks = trigger_tokens(opp_triggers)
    opp_topic_toks = topic_tokens(opportunity_topic_text(opportunity))

    candidates = []
    for skill in installed_skills(target_root):
        score, reasoning = fitness(
            opp_profile, opp_name, opp_name_toks, opp_trigger_toks, opp_topic_toks, skill
        )
        candidates.append({
            "skill": skill["name"],
            "fitness": score,
            "profile": skill["profile"],
            "source_dir": skill["source_dir"],
            "reasoning": reasoning,
        })

    candidates.sort(key=lambda item: item["fitness"], reverse=True)

    base = {
        "threshold": threshold,
        "ambiguous_margin": ambiguous_margin,
        "opportunity_profile": opp_profile,
        "opportunity_name": opp_name,
        "candidates_evaluated": len(candidates),
        "alternatives": candidates[:3],
    }

    if not candidates or candidates[0]["fitness"] < threshold:
        return {
            "decision": "forge",
            "target_skill": None,
            "fitness": candidates[0]["fitness"] if candidates else 0.0,
            **base,
        }

    top = candidates[0]
    second = candidates[1] if len(candidates) > 1 else None
    if (second
            and second["fitness"] >= threshold
            and (top["fitness"] - second["fitness"]) < ambiguous_margin):
        return {
            "decision": "ambiguous",
            "target_skill": None,
            "fitness": top["fitness"],
            **base,
        }

    return {
        "decision": "evolve",
        "target_skill": top["skill"],
        "fitness": top["fitness"],
        "reasoning": top["reasoning"],
        **base,
    }


def load_opportunity(args: argparse.Namespace) -> dict:
    if args.opportunity_stdin:
        return json.load(sys.stdin)
    if args.opportunity_json:
        return json.loads(Path(args.opportunity_json).expanduser().read_text(encoding="utf-8"))
    return {
        "suggested_skill_name": args.skill_name,
        "recommended_template": args.template,
        "triggers": [t.strip() for t in args.triggers.split(",") if t.strip()],
        "reason": args.reason,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Decide whether to evolve an existing installed skill or forge a new one."
    )
    parser.add_argument("--opportunity-json", default="",
                        help="Path to JSON file with the opportunity dict.")
    parser.add_argument("--opportunity-stdin", action="store_true",
                        help="Read opportunity JSON from stdin.")
    parser.add_argument("--skill-name", default="",
                        help="Inline opportunity: suggested skill name.")
    parser.add_argument("--triggers", default="",
                        help="Inline opportunity: comma-separated trigger phrases.")
    parser.add_argument("--template",
                        choices=["academic", "product", "integration", "script", "workflow"],
                        default="workflow",
                        help="Inline opportunity: recommended template profile.")
    parser.add_argument("--reason", default="",
                        help="Inline opportunity: reason / evidence snippet.")
    parser.add_argument("--target-root", default=str(DEFAULT_TARGET_ROOT),
                        help="OpenClaw skills root containing the install manifest.")
    parser.add_argument("--evolve-threshold", type=float, default=DEFAULT_EVOLVE_THRESHOLD,
                        help=f"Top-candidate fitness >= this routes to evolve. Default {DEFAULT_EVOLVE_THRESHOLD}.")
    parser.add_argument("--ambiguous-margin", type=float, default=DEFAULT_AMBIGUOUS_MARGIN,
                        help="Top-vs-second-fitness margin within which the result is ambiguous.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    opportunity = load_opportunity(args)
    target_root = Path(args.target_root).expanduser().resolve()
    result = decide(opportunity, target_root, args.evolve_threshold, args.ambiguous_margin)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"decision: {result['decision']}")
        if result.get("target_skill"):
            print(f"target_skill: {result['target_skill']}")
        print(f"fitness: {result['fitness']}")
        print(f"candidates_evaluated: {result['candidates_evaluated']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
