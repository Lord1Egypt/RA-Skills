#!/usr/bin/env python3
"""Recommend relationship-coaching interventions from symptoms and constraints."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from typing import Any, Iterable, Optional

INTERVENTIONS: dict[str, dict[str, Any]] = {
    "soft-startup": {
        "fits": ["criticism", "blame", "harsh-start", "complaint", "conflict"],
        "pathway": "conflict_deescalation",
        "why": "Turns a complaint into feeling, observable behaviour, positive need, and small request.",
        "script": "I felt ___ when ___ happened. What would help me is ___. Could we try ___?",
        "worksheet": "soft-startup",
        "avoid_if": ["immediate danger", "coercive control", "unsafe partner"],
    },
    "time-out-and-return": {
        "fits": ["flooding", "shutdown", "stonewalling", "escalation", "panic", "overwhelmed"],
        "pathway": "conflict_deescalation",
        "why": "Stops physiological escalation while preserving a return time so the pause is not abandonment or punishment.",
        "script": "I’m overwhelmed and don’t want to make this worse. I’ll come back at ___ and start by listening.",
        "worksheet": "time-out-and-return",
        "avoid_if": ["partner may retaliate if user disengages without safety plan"],
    },
    "repair-attempt": {
        "fits": ["apology", "after-fight", "regret", "hurt partner", "snapped", "yelled"],
        "pathway": "repair",
        "why": "Repairs impact without relitigating every detail.",
        "script": "I’m sorry for ___. I can see it affected you by ___. I wish I had ___. What would help repair this now?",
        "worksheet": "repair-attempt",
        "avoid_if": ["user is apologising to appease abuse or avoid retaliation"],
    },
    "two-turn-listening": {
        "fits": ["not-heard", "interrupting", "defensive", "rebuttal", "crosstalk"],
        "pathway": "conflict_deescalation",
        "why": "Forces a summary and validation before rebuttal.",
        "script": "Before I answer, what I heard is ___. The part that makes sense is ___.",
        "worksheet": "two-turn-listening",
        "avoid_if": ["active abuse or coercive control"],
    },
    "dreams-within-conflict": {
        "fits": ["perpetual", "same-fight", "gridlock", "money", "chores", "parenting", "values"],
        "pathway": "perpetual_problem",
        "why": "Finds the value, dream, history, or fear protected by each position.",
        "script": "I want to understand why this matters to you, not just what decision you want.",
        "worksheet": "dreams-within-conflict",
        "avoid_if": ["urgent safety issue", "decision must be made immediately"],
    },
    "compromise-circles": {
        "fits": ["compromise", "stuck", "negotiation", "recurring", "agreement"],
        "pathway": "perpetual_problem",
        "why": "Separates core needs from flexible preferences and creates a trial agreement.",
        "script": "My core need is ___. I can be flexible about ___. A fair trial would be ___.",
        "worksheet": "compromise-circles",
        "avoid_if": ["one partner's safety, consent, or rights are being negotiated away"],
    },
    "attachment-cycle-map": {
        "fits": ["anxious", "avoidant", "pursue", "withdraw", "clingy", "space", "reassurance", "abandonment"],
        "pathway": "attachment_cycle",
        "why": "Externalises the cycle so neither partner becomes the villain.",
        "script": "When ___ happens, I protect myself by ___. Underneath, I’m afraid ___.",
        "worksheet": "attachment-cycle-map",
        "avoid_if": ["attachment labels are being used to excuse mistreatment"],
    },
    "connection-before-analysis": {
        "fits": ["talking-makes-it-worse", "relationship-talk", "won't-talk", "shuts-down", "avoidant"],
        "pathway": "connection_before_analysis",
        "why": "Uses behaviour and bonding first when analysis itself is the trigger.",
        "script": "Let’s reconnect first, then use ten minutes for one concrete request.",
        "worksheet": "connection-before-analysis",
        "avoid_if": ["the user needs safety planning, not reconnection"],
    },
    "bids-and-love-maps": {
        "fits": ["distant", "roommates", "lonely", "connection", "bids", "love-maps", "spark"],
        "pathway": "friendship_intimacy",
        "why": "Rebuilds daily responsiveness and curiosity rather than waiting for a big romantic reset.",
        "script": "I miss knowing your inner world. Can we spend fifteen minutes updating each other?",
        "worksheet": "love-map-refresh",
        "avoid_if": ["relationship is unsafe or coercive"],
    },
    "trust-repair-map": {
        "fits": ["trust", "affair", "betrayal", "cheating", "lying", "secret", "broken-agreement"],
        "pathway": "trust_repair",
        "why": "Combines accountability, impact, boundaries, and follow-through without surveillance spirals.",
        "script": "Trust comes back from consistent behaviour you can verify without becoming my jailer.",
        "worksheet": "trust-repair-map",
        "avoid_if": ["the 'betrayal' framing is being used to control autonomy or isolate partner"],
    },
    "brakes-and-accelerators": {
        "fits": ["libido", "desire", "low-desire", "sexless", "not-in-mood", "rejection", "arousal"],
        "pathway": "desire_discrepancy",
        "why": "Reframes desire as context-sensitive, reducing blame and pressure.",
        "script": "I don’t want sex to feel pressured. I want to understand what makes desire easier or harder for us.",
        "worksheet": "brakes-and-accelerators",
        "avoid_if": ["one partner says no and the user wants tactics to override it"],
    },
    "affection-menu": {
        "fits": ["touch", "affection", "pressure", "rejected", "all-or-nothing", "cuddle", "sensual"],
        "pathway": "desire_discrepancy",
        "why": "Separates affection, sensuality, eroticism, and sex so touch stops being a demand signal.",
        "script": "Can we create forms of touch that are welcome without implying sex is expected?",
        "worksheet": "affection-menu",
        "avoid_if": ["touch is unwanted or unsafe"],
    },
    "pleasure-map": {
        "fits": ["orgasm", "clitoris", "oral", "pleasure", "feedback", "sex-improvement", "come", "cum"],
        "pathway": "pleasure_equity",
        "why": "Centres pleasure, feedback, pacing, and anatomy-aware exploration without performance pressure.",
        "script": "Can we treat feedback as teamwork, not criticism?",
        "worksheet": "pleasure-map",
        "avoid_if": ["pain, trauma, or medical symptoms need clinical support first"],
    },
    "erotic-aliveness-audit": {
        "fits": ["boring-sex", "passion", "erotic", "novelty", "desire", "routine", "mating-in-captivity"],
        "pathway": "erotic_reset",
        "why": "Explores autonomy, novelty, play, and aliveness alongside closeness.",
        "script": "I want us to rebuild the conditions where we can feel curious about each other again.",
        "worksheet": "erotic-aliveness-audit",
        "avoid_if": ["unresolved resentment or safety issues are the real brake"],
    },
    "kink-consent-map": {
        "fits": ["kink", "bdsm", "dominance", "submission", "fantasy", "cnc", "rape-fantasy", "roleplay"],
        "pathway": "kink_consent",
        "why": "Creates explicit consent, limits, stop signals, aftercare, and debriefs while separating fantasy from reality.",
        "script": "I’m interested in the fantasy only if our real-world consent is explicit, reversible, and easy to stop.",
        "worksheet": "kink-consent-map",
        "avoid_if": ["minors", "intoxication", "pressure", "active coercion", "real refusal is ambiguous"],
    },
    "safer-kink-alternatives": {
        "fits": ["choking", "breathplay", "strangulation", "neck-pressure"],
        "pathway": "breathplay_redirect",
        "why": "Avoids giving dangerous choking technique while preserving the erotic ingredient through safer substitutes.",
        "script": "I’m not comfortable with neck pressure, but I do want to explore the intensity in a safer way.",
        "worksheet": "safer-kink-alternatives",
        "avoid_if": ["do not give technique or safety reassurance for neck compression"],
    },
    "flirting-message-builder": {
        "fits": ["flirting", "dating", "ask-out", "text", "dating-app", "first-date", "chemistry"],
        "pathway": "flirting_dating",
        "why": "Uses warm specificity, clear invitation, and graceful non-pressure to avoid needy or manipulative escalation.",
        "script": "I liked ___. Want to ___ this week? No pressure if not.",
        "worksheet": "flirting-message-builder",
        "avoid_if": ["workplace power imbalance", "clear disinterest", "harassment risk"],
    },
    "love-languages-menu": {
        "fits": ["love-language", "appreciation", "quality-time", "acts-service", "touch", "gifts", "affirmation"],
        "pathway": "love_languages",
        "why": "Turns a simple vocabulary of care into visible weekly behaviours without treating it as rigid science.",
        "script": "Which signals of care actually land for you right now?",
        "worksheet": "love-languages-menu",
        "avoid_if": ["using physical touch as sexual entitlement"],
    },
    "stay-or-leave-clarifier": {
        "fits": ["breakup", "divorce", "separate", "stay-or-leave", "should-i-leave", "can-this-work"],
        "pathway": "decision_reflection",
        "why": "Balances hope with evidence, minimum viable conditions, and practical constraints.",
        "script": "What would have to change, visibly and repeatedly, for this to be viable?",
        "worksheet": "stay-or-leave-clarifier",
        "avoid_if": ["danger requires safety planning rather than relationship optimisation"],
    },
    "safety-next-step": {
        "fits": ["violence", "coercive-control", "stalking", "monitoring", "unsafe", "threat", "self-harm", "minor", "non-consent"],
        "pathway": "safety_referral",
        "why": "Prioritises immediate safety, crisis support, domestic-abuse/sexual-assault resources, safeguarding, and digital safety.",
        "script": "This is not a couples-communication problem right now. The priority is safety and support from a safe device/person.",
        "worksheet": "safety-next-step",
        "avoid_if": ["do not offer joint exercises or confrontation scripts"],
    },
}

ALIASES = {
    "fight": "conflict",
    "argue": "conflict",
    "argument": "conflict",
    "stonewall": "stonewalling",
    "same fight": "same-fight",
    "no sex": "sexless",
    "low libido": "libido",
    "rape fantasy": "rape-fantasy",
    "ask her out": "ask-out",
    "ask him out": "ask-out",
    "ask them out": "ask-out",
    "choke": "choking",
    "choked": "choking",
    "breath play": "breathplay",
    "love languages": "love-language",
}


def parse_terms(raw: str | None) -> list[str]:
    if not raw:
        return []
    terms: list[str] = []
    for part in raw.replace(";", ",").split(","):
        term = part.strip().lower().replace("_", "-")
        if not term:
            continue
        terms.append(ALIASES.get(term, term))
    return terms


def score_interventions(symptoms: list[str], constraints: list[str]) -> list[dict[str, Any]]:
    symptom_set = set(symptoms)
    constraint_set = set(constraints)
    recs = []
    for key, data in INTERVENTIONS.items():
        fits = set(data["fits"])
        score = len(symptom_set & fits) * 3
        if data["pathway"].replace("_", "-") in symptom_set:
            score += 2
        # Some constraints steer towards safety/ethics even if symptoms are broad.
        if key == "safety-next-step" and (constraint_set & {"unsafe", "violence", "monitoring", "minor", "non-consent", "coercive-control"}):
            score += 10
        if key == "safer-kink-alternatives" and (symptom_set & {"choking", "breathplay", "strangulation", "neck-pressure"}):
            score += 6
        if score:
            rec = {"key": key, "score": score, **data}
            recs.append(rec)
    recs.sort(key=lambda r: (-r["score"], r["key"]))
    return recs


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Recommend relationship-coaching interventions from comma-separated symptoms and constraints.",
        epilog="Example: python3 scripts/intervention_selector.py --symptoms 'libido,pressure,touch' --pretty",
    )
    parser.add_argument("--symptoms", help="Comma-separated symptom/context terms, e.g. 'criticism,defensive,conflict'.")
    parser.add_argument("--constraints", default="", help="Comma-separated constraints, e.g. 'one_partner_present,unsafe,kink'.")
    parser.add_argument("--limit", type=int, default=5, help="Maximum recommendations to return. Default: 5.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args(argv)

    symptoms = parse_terms(args.symptoms)
    constraints = parse_terms(args.constraints)
    recs = score_interventions(symptoms, constraints)[: max(args.limit, 0)]
    by_pathway: dict[str, int] = defaultdict(int)
    for rec in recs:
        by_pathway[rec["pathway"]] += 1
    output = {
        "symptoms": symptoms,
        "constraints": constraints,
        "recommendations": recs,
        "pathway_counts": dict(by_pathway),
        "note": "Heuristic selector only. For safety, consent, minor, or coercion concerns, use the safety semantic triage reference first.",
    }
    print(json.dumps(output, indent=2 if args.pretty else None, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
