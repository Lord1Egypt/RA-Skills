#!/usr/bin/env python3
"""Route adult relationship-coaching prompts for the relationship-science-coach skill.

This deterministic helper is not a clinical, legal, abuse-risk, or crisis
assessment. It helps an agent remember the right reference files and avoid
crude keyword over-routing, especially around consensual kink language.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class Match:
    category: str
    terms: list[str]


def normalise(text: str) -> str:
    text = text.lower()
    replacements = {
        "’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return re.sub(r"\s+", " ", text).strip()


def term_in_text(term: str, text: str) -> bool:
    term = normalise(term)
    if " " in term or "-" in term or "'" in term or "/" in term:
        return term in text
    return re.search(rf"\b{re.escape(term)}\b", text) is not None


def find_terms(text: str, mapping: dict[str, list[str]]) -> list[Match]:
    matches: list[Match] = []
    for category, terms in mapping.items():
        found = [t for t in terms if term_in_text(t, text)]
        if found:
            matches.append(Match(category, found))
    return matches


def any_term(text: str, terms: Iterable[str]) -> bool:
    return any(term_in_text(t, text) for t in terms)


IMMEDIATE_DANGER = [
    "right now", "outside my door", "has a weapon", "gun", "knife", "emergency",
    "in danger", "threatened to kill", "threatens to kill", "going to kill",
    "kill me", "blocked the exit", "blocked the door", "won't let me leave",
    "wont let me leave", "trapped me", "trapped in", "locked me in",
]

VIOLENCE_CONTEXT = [
    "during a fight", "during an argument", "argument", "fight", "angry", "rage",
    "scared", "afraid", "terrified", "fear", "hurt me", "injured", "bruise",
    "bruised", "threat", "threatened", "blocked", "restrained", "pinned",
]

PHYSICAL_VIOLENCE = [
    "hit", "hits", "hitting", "punched", "punch", "slapped", "slap", "kicked",
    "kick", "pushed", "push", "shoved", "shove", "grabbed", "grabbing",
    "pinned", "restrained", "threw something", "weapon", "headbutt", "bit me",
]

CHOKING_TERMS = ["choke", "choked", "choking", "strangle", "strangled", "strangling", "throat", "neck pressure"]
CHOKING_METAPHOR = ["choked up", "choked on", "choke on", "choke during my speech", "choked during the conversation"]

SEXUAL_ASSAULT = [
    "raped", "rape me", "raping", "sexual assault", "assaulted me", "forced sex",
    "forced me", "made me have sex", "wouldn't take no", "wouldnt take no", "stealthing",
    "removed condom", "without consent", "didn't consent", "didnt consent", "coerced sex",
]

RAPE_FANTASY_CONTEXT = [
    "rape fantasy", "rape fantasies", "cnc", "consensual non-consent", "consensual non consent",
    "ravishment", "roleplay", "role play", "fantasy", "fantasies", "scene", "safeword", "safe word",
]

KINK_CONTEXT = [
    "kink", "bdsm", "dominance", "submission", "dominant", "submissive", "dom", "sub",
    "impact play", "restraint", "restraints", "bondage", "degradation", "humiliation",
    "power exchange", "scene", "aftercare", "safeword", "safe word", "limits", "consensual",
    "we both", "we want to try", "curious about", "roleplay", "role play", "cnc",
]

COERCIVE_CONTROL = [
    "tracks my phone", "tracking my phone", "tracking me", "monitors me", "monitoring me",
    "checks my phone", "reads my messages", "controls my money", "controls my medication",
    "took my documents", "took my passport", "isolates me", "won't let me", "wont let me",
    "stalking", "stalks me", "coercive", "afraid to say no", "scared to disagree",
    "retaliation", "ruin my life", "threatens custody", "threatened custody", "immigration",
    "outing me", "threatens to out", "threatened to out", "controls what i wear",
]

SELF_HARM = [
    "suicide", "kill myself", "end my life", "self harm", "self-harm", "want to die",
    "don't want to live", "dont want to live", "overdose", "cut myself", "threatens suicide",
    "they will kill themselves", "he will kill himself", "she will kill herself",
]

HARM_OTHERS = ["kill them", "kill him", "kill her", "murder", "homicide", "hurt them", "hurt him", "hurt her", "make them pay"]

CHILD_SAFETY = [
    "child abuse", "hit our child", "hits our child", "hurt the kids", "hurts our child",
    "kids are scared", "children are scared", "neglect", "safeguarding", "child protection",
]

MINOR_SEX = [
    "minor", "underage", "under age", "14 year old", "15 year old", "16 year old", "17 year old",
    "teen", "teenager", "schoolgirl", "schoolboy",
]
SEX_TERMS = ["sex", "sexual", "nude", "nudes", "kiss", "kissing", "date", "dating", "flirt", "horny", "fantasy"]

MISUSE = {
    "manipulation_or_control": [
        "make them apologize", "make them apologise", "make her apologize", "make her apologise",
        "make him apologize", "make him apologise", "force them", "force her", "force him",
        "make her see", "make him see", "make them see", "trap them", "test them", "test her",
        "test him", "punish them", "punish her", "punish him", "get revenge", "make them jealous",
        "make her jealous", "make him jealous", "make partner jealous", "make boyfriend jealous",
        "make girlfriend jealous", "make my partner jealous", "make my boyfriend jealous",
        "make my girlfriend jealous", "teach them a lesson", "corner them",
    ],
    "surveillance": [
        "spy on", "track their phone", "track her phone", "track his phone", "hack", "password",
        "read their messages", "secretly record", "airtag", "gps tracker",
    ],
    "diagnosis_as_leverage": [
        "diagnose my partner", "diagnose her", "diagnose him", "diagnose them", "prove narcissist",
        "prove she's narcissistic", "prove he's narcissistic", "personality disorder",
    ],
    "sexual_entitlement": [
        "owes me sex", "owes me intimacy", "owes me affection", "duty to have sex", "make her have sex", "make him have sex",
    ],
}

TOPICS = {
    "weekly_checkin": ["state of the union", "weekly check", "weekly relationship", "relationship meeting", "check-in", "check in", "agenda"],
    "repair": ["repair", "apolog", "sorry", "after a fight", "after an argument", "yelled", "shouted", "snapped", "regret", "i messed up", "bad text"],
    "conflict_deescalation": ["argue", "argument", "fight", "conflict", "criticism", "defensive", "defensiveness", "stonewall", "contempt", "soft start", "gentle start", "flooded", "shut down", "shutdown", "spiral"],
    "perpetual_problem": ["same fight", "again and again", "recurring", "stuck", "gridlock", "never agree", "can't agree", "cant agree", "chores", "money", "parenting", "in-laws", "in laws"],
    "attachment_cycle": ["anxious", "avoidant", "attachment", "abandon", "abandoned", "clingy", "pursue", "withdraw", "pulls away", "space", "reassurance"],
    "connection_before_analysis": ["talking makes it worse", "talk about us makes", "relationship talk", "won't talk", "wont talk", "shuts down when we talk"],
    "friendship_intimacy": ["distant", "roommates", "connection", "love maps", "bids", "date night", "lonely", "spark", "appreciation"],
    "trust_repair": ["affair", "infidelity", "betrayal", "trust", "lied", "secret", "cheated", "cheating", "broken agreement"],
    "desire_discrepancy": ["desire", "libido", "mismatched", "low sex", "no sex", "sexless", "not in the mood", "rejected", "touch", "affection"],
    "erotic_reset": ["boring sex", "spice", "spark", "passion", "erotic", "fantasy", "novelty", "mating in captivity", "attraction"],
    "pleasure_equity": ["orgasm", "come", "cum", "clitoris", "clitoral", "oral sex", "cunnilingus", "pleasure", "she comes first"],
    "kink_consent": KINK_CONTEXT + RAPE_FANTASY_CONTEXT,
    "flirting_dating": ["flirt", "flirting", "dating", "first date", "ask out", "text her", "text him", "text them", "dating app", "tinder", "hinge", "bumble", "chemistry"],
    "love_languages": ["love language", "love languages", "quality time", "acts of service", "words of affirmation", "physical touch", "gifts"],
    "decision_reflection": ["break up", "breakup", "separate", "divorce", "stay or leave", "should i leave", "should we stay", "can this work"],
    "individual_coaching": ["my partner", "my wife", "my husband", "my girlfriend", "my boyfriend", "my spouse", "they", "she", "he"],
}

REFERENCES = {
    "safety_referral": ["references/SAFETY_SEMANTIC_TRIAGE.md", "references/EDGE_CASES.md"],
    "ethics_redirect": ["references/SAFETY_SEMANTIC_TRIAGE.md", "references/STYLE_GUIDE.md"],
    "intake": ["references/OPERATING_MODEL.md", "references/STYLE_GUIDE.md"],
    "conflict_deescalation": ["references/CONFLICT_ATTACHMENT_AND_REPAIR.md", "references/INTERVENTION_LIBRARY.md"],
    "repair": ["references/CONFLICT_ATTACHMENT_AND_REPAIR.md", "references/INTERVENTION_LIBRARY.md"],
    "perpetual_problem": ["references/CONFLICT_ATTACHMENT_AND_REPAIR.md", "references/INTERVENTION_LIBRARY.md"],
    "attachment_cycle": ["references/CONFLICT_ATTACHMENT_AND_REPAIR.md", "references/INTERVENTION_LIBRARY.md"],
    "connection_before_analysis": ["references/CONFLICT_ATTACHMENT_AND_REPAIR.md", "references/INTERVENTION_LIBRARY.md"],
    "friendship_intimacy": ["references/CONFLICT_ATTACHMENT_AND_REPAIR.md", "references/SESSION_TEMPLATES.md"],
    "weekly_checkin": ["references/SESSION_TEMPLATES.md", "assets/worksheet-templates.md"],
    "trust_repair": ["references/CONFLICT_ATTACHMENT_AND_REPAIR.md", "references/SESSION_TEMPLATES.md"],
    "desire_discrepancy": ["references/SEX_INTIMACY_AND_DESIRE.md", "assets/worksheet-templates.md"],
    "erotic_reset": ["references/SEX_INTIMACY_AND_DESIRE.md", "references/SESSION_TEMPLATES.md"],
    "pleasure_equity": ["references/SEX_INTIMACY_AND_DESIRE.md", "assets/worksheet-templates.md"],
    "kink_consent": ["references/SEX_INTIMACY_AND_DESIRE.md", "references/SAFETY_SEMANTIC_TRIAGE.md"],
    "breathplay_redirect": ["references/SEX_INTIMACY_AND_DESIRE.md", "references/SAFETY_SEMANTIC_TRIAGE.md"],
    "flirting_dating": ["references/DATING_FLIRTING_AND_ATTRACTION.md", "references/STYLE_GUIDE.md"],
    "love_languages": ["references/INTERVENTION_LIBRARY.md", "assets/worksheet-templates.md"],
    "decision_reflection": ["references/SESSION_TEMPLATES.md", "references/STYLE_GUIDE.md"],
    "individual_coaching": ["references/STYLE_GUIDE.md", "references/INTERVENTION_LIBRARY.md"],
}

DO_NOT_OFFER = {
    "safety_referral": [
        "joint couples exercises", "soft start-up scripts to use with an unsafe partner",
        "shared-responsibility framing", "advice to disclose plans to a monitored or threatening partner",
    ],
    "ethics_redirect": ["manipulation tactics", "surveillance", "diagnosis as leverage", "forced sex or forced apology tactics"],
    "breathplay_redirect": ["choking technique", "neck pressure instructions", "reassurance that breath play is safe"],
}


def classify_safety(text: str) -> list[Match]:
    flags: list[Match] = []

    def add(category: str, terms: list[str]) -> None:
        if terms:
            flags.append(Match(category, terms))

    add("immediate_danger", [t for t in IMMEDIATE_DANGER if term_in_text(t, text)])
    add("coercive_control", [t for t in COERCIVE_CONTROL if term_in_text(t, text)])
    add("self_harm_or_suicide", [t for t in SELF_HARM if term_in_text(t, text)])
    add("harm_to_others", [t for t in HARM_OTHERS if term_in_text(t, text)])
    add("child_safety", [t for t in CHILD_SAFETY if term_in_text(t, text)])

    physical = [t for t in PHYSICAL_VIOLENCE if term_in_text(t, text)]
    if physical:
        add("physical_violence", physical)

    # Choking is semantic: metaphor -> none; consensual kink curiosity -> high-risk kink, not abuse;
    # fight/fear/unwanted context -> safety.
    choking = [t for t in CHOKING_TERMS if term_in_text(t, text)]
    if choking and not any_term(text, CHOKING_METAPHOR):
        kinkish = any_term(text, KINK_CONTEXT)
        violent_context = any_term(text, VIOLENCE_CONTEXT + ["without asking", "without consent", "didn't ask", "didnt ask", "unwanted"])
        if violent_context or not kinkish:
            add("choking_or_strangulation_safety", choking)

    assault = [t for t in SEXUAL_ASSAULT if term_in_text(t, text)]
    if assault:
        add("sexual_assault_or_coercion", assault)

    # Bare "rape" is dangerous unless clearly fantasy/CNC/media context.
    if term_in_text("rape", text) and not any_term(text, RAPE_FANTASY_CONTEXT):
        add("rape_or_nonconsent", ["rape"])

    if any_term(text, MINOR_SEX) and any_term(text, SEX_TERMS):
        add("minor_sexual_context", [t for t in MINOR_SEX if term_in_text(t, text)])

    return flags


def classify_high_risk_kink(text: str, safety_flags: list[Match]) -> list[Match]:
    flags: list[Match] = []
    if safety_flags:
        return flags
    choking = [t for t in CHOKING_TERMS if term_in_text(t, text)]
    if choking and any_term(text, KINK_CONTEXT):
        flags.append(Match("breathplay_or_choking_kink", choking))
    rape_fantasy = [t for t in RAPE_FANTASY_CONTEXT if term_in_text(t, text)]
    if rape_fantasy and term_in_text("rape", text):
        flags.append(Match("cnc_or_rape_fantasy", rape_fantasy))
    return flags


def choose_pathway(safety: list[Match], misuse: list[Match], topics: list[Match], high_risk_kink: list[Match]) -> str:
    if safety:
        return "safety_referral"
    if misuse:
        # If the user asks about sex while using entitlement/coercion words, redirect ethics first.
        return "ethics_redirect"
    if any(m.category == "breathplay_or_choking_kink" for m in high_risk_kink):
        return "breathplay_redirect"
    if any(m.category == "cnc_or_rape_fantasy" for m in high_risk_kink):
        return "kink_consent"
    if not topics:
        return "intake"

    priority = [
        "kink_consent", "pleasure_equity", "desire_discrepancy", "erotic_reset", "trust_repair",
        "attachment_cycle", "connection_before_analysis", "weekly_checkin", "repair", "decision_reflection",
        "perpetual_problem", "conflict_deescalation", "flirting_dating", "love_languages",
        "friendship_intimacy", "individual_coaching",
    ]
    found = {m.category for m in topics}
    for item in priority:
        if item in found:
            return item
    return topics[0].category


def load_text(args: argparse.Namespace) -> str:
    if args.text and args.file:
        raise SystemExit("Error: use either --text or --file, not both.")
    if args.file:
        try:
            return open(args.file, "r", encoding="utf-8").read()
        except OSError as exc:
            raise SystemExit(f"Error reading {args.file!r}: {exc}") from exc
    if args.text:
        return args.text
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit("Error: provide --text, --file, or stdin. Run with --help for usage.")


def build_output(raw_text: str) -> dict[str, object]:
    text = normalise(raw_text)
    safety = classify_safety(text)
    high_risk_kink = classify_high_risk_kink(text, safety)
    misuse = find_terms(text, MISUSE)
    topics = find_terms(text, TOPICS)
    pathway = choose_pathway(safety, misuse, topics, high_risk_kink)

    do_not_offer = list(DO_NOT_OFFER.get(pathway, []))
    if misuse:
        for item in DO_NOT_OFFER["ethics_redirect"]:
            if item not in do_not_offer:
                do_not_offer.append(item)

    coaching_note = {
        "safety_referral": "Use safety protocol. Do not offer joint relationship exercises.",
        "ethics_redirect": "Refuse coercive/manipulative tactic and offer transparent alternative.",
        "breathplay_redirect": "Do not teach choking or breath-play technique; offer safer erotic alternatives.",
        "kink_consent": "Proceed with kink-aware adult consent architecture and no non-consensual erotic scripting.",
    }.get(pathway, "Proceed with direct coaching after a brief silent safety/scope check.")

    return {
        "pathway": pathway,
        "safety_first": pathway == "safety_referral",
        "ethics_first": pathway == "ethics_redirect",
        "kink_context": bool(high_risk_kink or any(m.category == "kink_consent" for m in topics)),
        "high_risk_kink_flags": [{"category": m.category, "matched_terms": m.terms} for m in high_risk_kink],
        "risk_flags": [{"category": m.category, "matched_terms": m.terms} for m in safety],
        "misuse_flags": [{"category": m.category, "matched_terms": m.terms} for m in misuse],
        "topic_matches": [{"category": m.category, "matched_terms": m.terms} for m in topics],
        "recommended_references": REFERENCES.get(pathway, REFERENCES["intake"]),
        "do_not_offer": do_not_offer,
        "coaching_note": coaching_note,
        "limitations": "Heuristic router only; use judgement and the semantic triage reference.",
    }


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Classify a relationship-coaching prompt and recommend an evidence-informed pathway.",
        epilog="Example: python3 scripts/intake_router.py --text 'We want to try CNC roleplay but keep it safe' --pretty",
    )
    parser.add_argument("--text", help="Prompt text to classify.")
    parser.add_argument("--file", help="Path to a UTF-8 text file containing the prompt.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args(argv)
    print(json.dumps(build_output(load_text(args)), indent=2 if args.pretty else None, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
