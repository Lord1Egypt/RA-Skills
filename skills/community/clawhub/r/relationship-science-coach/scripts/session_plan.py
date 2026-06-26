#!/usr/bin/env python3
"""Create a structured relationship-coaching session plan from a JSON brief.

The script is intentionally deterministic and offline. It does not diagnose,
provide therapy, or replace crisis/safety support; it produces coaching plans
for an agent to adapt in conversation.
"""
from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from typing import Any, Iterable, Optional

PATHWAY_PLANS: dict[str, dict[str, Any]] = {
    "intake": {
        "title": "Focused intake and next-step coaching",
        "purpose": "Clarify the relationship pattern quickly and give one useful experiment rather than over-interviewing.",
        "steps": [
            {"minutes": 3, "name": "Name the presenting pattern", "instructions": "Reflect the user's issue in plain language and identify whether they need a script, a repair, a sex/intimacy plan, a dating plan, or a decision frame."},
            {"minutes": 5, "name": "Ask only the leverage questions", "instructions": "Ask up to three questions: what happened, what they want to be different, and what tends to happen when they try."},
            {"minutes": 7, "name": "Offer a first experiment", "instructions": "Give one exact script or behavioural experiment that is safe to try this week."},
        ],
        "worksheets": ["values-and-outcome-clarifier"],
        "say_this": "Let’s make this practical: what is the smallest moment in this pattern where a different move would change the whole conversation?",
    },
    "conflict_deescalation": {
        "title": "De-escalation and soft start-up session",
        "purpose": "Move from blame/protection into a specific request and a returnable conversation.",
        "steps": [
            {"minutes": 3, "name": "Stop the escalation", "instructions": "If either partner is flooded, begin with a 20-45 minute break and a specific return time."},
            {"minutes": 5, "name": "Translate blame", "instructions": "Convert criticism into feeling + observable behaviour + positive need + small request."},
            {"minutes": 8, "name": "Two-turn listening", "instructions": "Each partner gets one summary and one validation before rebuttal or problem-solving."},
            {"minutes": 5, "name": "Concrete agreement", "instructions": "Agree on one testable behaviour for the next week, not a personality change."},
        ],
        "worksheets": ["soft-startup", "time-out-and-return", "two-turn-listening"],
        "say_this": "I’m not trying to win this. I want to restart it better. I felt ___ when ___ happened, and what would help me is ___.",
    },
    "repair": {
        "title": "Post-fight repair session",
        "purpose": "Repair impact without litigating every detail of the fight.",
        "steps": [
            {"minutes": 4, "name": "Own your part", "instructions": "State the specific behaviour you regret without explaining it away."},
            {"minutes": 6, "name": "Hear impact", "instructions": "Invite the partner to say what landed badly; summarise before responding."},
            {"minutes": 6, "name": "Name the deeper need", "instructions": "Identify the longing or fear under the anger."},
            {"minutes": 5, "name": "Future repair cue", "instructions": "Choose a phrase either partner can use next time to interrupt the old pattern."},
        ],
        "worksheets": ["repair-attempt", "impact-listening"],
        "say_this": "I can see that I hurt you. The part I’m taking responsibility for is ___. I want to understand the impact before I explain my side.",
    },
    "perpetual_problem": {
        "title": "Perpetual-problem map",
        "purpose": "Treat recurring conflict as a values-and-dreams problem rather than a debate to finally win.",
        "steps": [
            {"minutes": 5, "name": "Define the unsolved problem", "instructions": "Write the issue neutrally in one sentence."},
            {"minutes": 10, "name": "Dream under the position", "instructions": "Each partner explains why their position matters: history, values, identity, fears, hopes."},
            {"minutes": 7, "name": "Compromise circles", "instructions": "Separate core needs from flexible preferences."},
            {"minutes": 5, "name": "Temporary operating agreement", "instructions": "Choose a two-week trial rather than a permanent solution."},
        ],
        "worksheets": ["dreams-within-conflict", "compromise-circles"],
        "say_this": "I want to understand why this matters so much to you, not just what you want me to do.",
    },
    "attachment_cycle": {
        "title": "Attachment-cycle session",
        "purpose": "Externalise the pursue-withdraw or fear-distance loop and replace protest behaviour with vulnerable bids.",
        "steps": [
            {"minutes": 5, "name": "Map the loop", "instructions": "Identify each partner's trigger, protection move, and impact on the other."},
            {"minutes": 8, "name": "Find primary emotion", "instructions": "Translate anger, criticism, or shutdown into fear, shame, sadness, loneliness, or longing."},
            {"minutes": 7, "name": "Reach and respond", "instructions": "Practise one accessible, responsive, engaged exchange."},
            {"minutes": 5, "name": "Secure-base micro-habit", "instructions": "Pick one daily cue of reassurance or autonomy-respecting closeness."},
        ],
        "worksheets": ["attachment-cycle-map", "vulnerable-bid"],
        "say_this": "When I come at you hard, underneath I’m scared I don’t matter. What I actually need is reassurance, not a fight.",
    },
    "connection_before_analysis": {
        "title": "Connection-before-analysis reset",
        "purpose": "Help couples who escalate during relationship talks reconnect behaviourally before analysis.",
        "steps": [
            {"minutes": 4, "name": "Suspend the post-mortem", "instructions": "Stop explaining the relationship for now; choose one bonding action first."},
            {"minutes": 8, "name": "Non-verbal reconnection", "instructions": "Use a walk, food, practical help, brief affectionate contact if welcome, or shared task."},
            {"minutes": 6, "name": "One-sentence truth", "instructions": "After connection returns, each partner says one sentence about what they need, not a monologue."},
            {"minutes": 5, "name": "Schedule the hard topic", "instructions": "Put the deeper topic in a bounded slot rather than forcing it while disconnected."},
        ],
        "worksheets": ["connection-before-analysis", "one-sentence-truth"],
        "say_this": "We keep trying to analyse this when we’re disconnected. Let’s reconnect first, then use ten minutes for one concrete request.",
    },
    "friendship_intimacy": {
        "title": "Friendship and aliveness rebuild",
        "purpose": "Rebuild fondness, bids, curiosity, and shared ritual when the relationship feels like roommates.",
        "steps": [
            {"minutes": 5, "name": "Bids audit", "instructions": "Find missed bids and easy opportunities to turn toward."},
            {"minutes": 7, "name": "Love Map refresh", "instructions": "Ask current-world questions, not nostalgia-only questions."},
            {"minutes": 5, "name": "Appreciation ratio", "instructions": "Each partner gives three specific appreciations tied to recent behaviours."},
            {"minutes": 8, "name": "Novelty ritual", "instructions": "Plan one low-friction new experience and one daily micro-ritual."},
        ],
        "worksheets": ["bids-audit", "love-map-refresh", "appreciation-menu"],
        "say_this": "I miss feeling like we know each other. Can we spend fifteen minutes updating our map of each other instead of talking logistics?",
    },
    "weekly_checkin": {
        "title": "Weekly State of the Relationship",
        "purpose": "Create a predictable check-in that lowers drama and increases follow-through.",
        "steps": [
            {"minutes": 3, "name": "Appreciations", "instructions": "Start with two specific appreciations each."},
            {"minutes": 5, "name": "What worked", "instructions": "Name one moment of connection or teamwork from the week."},
            {"minutes": 10, "name": "One issue only", "instructions": "Discuss one issue with soft start-up and listening turns."},
            {"minutes": 5, "name": "Agreements", "instructions": "Write who will do what by when."},
            {"minutes": 2, "name": "Ritual", "instructions": "End with one planned connection ritual."},
        ],
        "worksheets": ["state-of-the-relationship"],
        "say_this": "Let’s keep this to one issue and one agreement, so the check-in stays something we actually want to do.",
    },
    "trust_repair": {
        "title": "Trust repair and accountability",
        "purpose": "Support trust repair through accountability, impact listening, boundaries, and transparent follow-through without turning into surveillance.",
        "steps": [
            {"minutes": 5, "name": "Stabilise", "instructions": "Name whether the harm has stopped and whether safety is present."},
            {"minutes": 8, "name": "Accountability statement", "instructions": "The injuring partner owns behaviour, impact, and prevention steps without blame-shifting."},
            {"minutes": 8, "name": "Impact and grief", "instructions": "The hurt partner describes impact; the other summarises and validates."},
            {"minutes": 7, "name": "Trust behaviours", "instructions": "Define transparency, boundaries, and repair check-ins that do not become coercive surveillance."},
        ],
        "worksheets": ["trust-repair-map", "accountability-statement"],
        "say_this": "Trust won’t come back from reassurance alone. It comes back from consistent behaviour you can verify without becoming my jailer.",
    },
    "desire_discrepancy": {
        "title": "Desire discrepancy without pressure",
        "purpose": "Reduce pursuer-pressure and avoider-dread while rebuilding context, willingness, affection, and pleasure.",
        "steps": [
            {"minutes": 5, "name": "Remove obligation", "instructions": "State clearly that nobody owes sex; pressure is a desire brake."},
            {"minutes": 8, "name": "Map brakes and accelerators", "instructions": "Identify stress, resentment, fatigue, novelty, emotional safety, body image, timing, and touch preferences."},
            {"minutes": 7, "name": "Affection menu", "instructions": "Separate affection, sensuality, eroticism, and sex so every touch is not a demand."},
            {"minutes": 7, "name": "Willingness experiment", "instructions": "Plan one no-pressure sensual or affectionate interaction with opt-out built in."},
        ],
        "worksheets": ["brakes-and-accelerators", "affection-menu", "desire-discrepancy-plan"],
        "say_this": "I don’t want you to feel pressured. I do want us to understand what makes desire easier or harder for each of us.",
    },
    "erotic_reset": {
        "title": "Erotic aliveness reset",
        "purpose": "Bring play, novelty, separateness, imagination, and chosen attention back into a safe long-term bond.",
        "steps": [
            {"minutes": 5, "name": "Separate closeness from erotic charge", "instructions": "Name where routine, over-familiarity, resentment, or role-locking has flattened desire."},
            {"minutes": 8, "name": "Erotic self-audit", "instructions": "Ask what makes each person feel alive, attractive, autonomous, and curious."},
            {"minutes": 8, "name": "Novelty menu", "instructions": "Create low/medium/high novelty options with clear consent."},
            {"minutes": 5, "name": "Invitation script", "instructions": "Write one playful invitation that is specific but not pressuring."},
        ],
        "worksheets": ["erotic-aliveness-audit", "novelty-menu"],
        "say_this": "I don’t just want sex on the calendar; I want us to rebuild the conditions where we can feel curious about each other again.",
    },
    "pleasure_equity": {
        "title": "Pleasure equity and sexual feedback",
        "purpose": "Shift from performance or penetration-centred scripts to mutual pleasure, feedback, and clitoral literacy where relevant.",
        "steps": [
            {"minutes": 4, "name": "Set the frame", "instructions": "Pleasure, consent, and feedback are the measures; orgasm is welcome but not demanded."},
            {"minutes": 8, "name": "Pleasure map", "instructions": "Identify yes/maybe/no touch, pacing, context, and words."},
            {"minutes": 7, "name": "Feedback language", "instructions": "Practise positive redirection: more/less/slower/there/stop."},
            {"minutes": 6, "name": "Debrief ritual", "instructions": "After intimacy, share one thing liked and one thing to adjust, without criticism."},
        ],
        "worksheets": ["pleasure-map", "sexual-feedback-debrief"],
        "say_this": "I’d like us to make pleasure easier to talk about. Can we treat feedback as teamwork, not criticism?",
    },
    "kink_consent": {
        "title": "Kink-aware consent planning",
        "purpose": "Help consenting adults discuss fantasy, roles, limits, aftercare, and debriefs without confusing fantasy with real-world consent.",
        "steps": [
            {"minutes": 5, "name": "Separate fantasy from enactment", "instructions": "A fantasy can be erotic without being something to perform; no one owes enactment."},
            {"minutes": 8, "name": "Consent architecture", "instructions": "Define yes/maybe/no, roles, exact words, stop signals, health limits, privacy, and aftercare."},
            {"minutes": 8, "name": "Low-risk first version", "instructions": "Create a symbolic or verbal version before intense physical enactment."},
            {"minutes": 5, "name": "Debrief", "instructions": "Plan aftercare and a next-day check-in."},
        ],
        "worksheets": ["kink-consent-map", "cnc-discussion-map"],
        "say_this": "I’m interested in exploring the fantasy, but only in a way where our real-world consent is explicit, reversible, and easy to stop.",
    },
    "breathplay_redirect": {
        "title": "Breath-play risk redirect",
        "purpose": "Acknowledge consensual kink interest while refusing to teach choking/neck-pressure technique and offering safer erotic substitutes.",
        "steps": [
            {"minutes": 3, "name": "Validate without endorsing the act", "instructions": "Do not shame the fantasy; separate erotic themes from literal airway/neck restriction."},
            {"minutes": 5, "name": "Name the risk", "instructions": "Explain that breath play/neck pressure has serious injury risk and no reliably safe technique."},
            {"minutes": 8, "name": "Translate the erotic ingredient", "instructions": "Identify whether the desired ingredient is dominance, surrender, intensity, eye contact, restraint, dirty talk, or trust."},
            {"minutes": 7, "name": "Safer alternatives", "instructions": "Offer non-neck-pressure alternatives using words, eye contact, consensual restraint away from neck, pacing, or role language."},
        ],
        "worksheets": ["safer-kink-alternatives", "kink-consent-map"],
        "say_this": "I’m not comfortable with neck pressure, but I do want to explore the intensity and surrender part in a way that doesn’t risk injury.",
    },
    "flirting_dating": {
        "title": "Flirting and dating calibration",
        "purpose": "Help the user show romantic interest warmly, specifically, and respectfully, with attention to reciprocity.",
        "steps": [
            {"minutes": 4, "name": "Define the channel", "instructions": "Decide whether this is in-person, text, app, colleague/friend context, or first date."},
            {"minutes": 5, "name": "Warm specificity", "instructions": "Use a specific observation + light positive emotion + low-pressure invitation."},
            {"minutes": 5, "name": "Reciprocity check", "instructions": "Look for matched effort; if response is lukewarm, reduce intensity."},
            {"minutes": 5, "name": "Next move", "instructions": "Give one message or in-person line and one graceful exit line."},
        ],
        "worksheets": ["flirting-message-builder", "dating-reciprocity-check"],
        "say_this": "I’ve really enjoyed talking with you. I’d like to take you for coffee this week if you’d be up for that — no pressure if not.",
    },
    "love_languages": {
        "title": "Love-language translation",
        "purpose": "Use love languages as a practical care vocabulary, not a rigid diagnosis of how love must work.",
        "steps": [
            {"minutes": 4, "name": "Identify preferred signals", "instructions": "Ask which actions actually register as care right now."},
            {"minutes": 6, "name": "Translate care", "instructions": "Turn vague needs into visible behaviours across words, time, touch, service, and gifts."},
            {"minutes": 6, "name": "Build a care menu", "instructions": "Choose two easy weekly behaviours per partner."},
            {"minutes": 4, "name": "Avoid misuse", "instructions": "Do not let love languages excuse neglect, entitlement, or ignoring consent."},
        ],
        "worksheets": ["love-languages-menu"],
        "say_this": "I don’t need you to love me exactly the way I love you. I need us to learn which signals actually land for each other.",
    },
    "decision_reflection": {
        "title": "Stay-or-leave decision reflection",
        "purpose": "Help the user think clearly about relationship viability without rushing them or trapping them in endless hope.",
        "steps": [
            {"minutes": 5, "name": "Safety and consent check", "instructions": "If safety, coercion, or non-consent is present, move to safety planning rather than relationship optimisation."},
            {"minutes": 8, "name": "Pattern evidence", "instructions": "List what changes, what repeats, what each person owns, and what has been tried."},
            {"minutes": 7, "name": "Minimum viable relationship", "instructions": "Define the non-negotiables for staying and the observable evidence needed."},
            {"minutes": 5, "name": "Decision timeline", "instructions": "Choose a bounded experiment or a practical exit-planning step."},
        ],
        "worksheets": ["stay-or-leave-clarifier"],
        "say_this": "Hope matters, but evidence matters too. What would have to change, visibly and repeatedly, for this relationship to be viable?",
    },
    "individual_coaching": {
        "title": "One-partner coaching",
        "purpose": "Help one person change their side of the pattern without pretending they can control the other person.",
        "steps": [
            {"minutes": 5, "name": "Separate influence from control", "instructions": "Identify what the user can do, request, stop doing, or boundary."},
            {"minutes": 6, "name": "Pattern ownership", "instructions": "Name one self-protective move that may be worsening the cycle."},
            {"minutes": 6, "name": "Clean request", "instructions": "Create a direct, non-coercive request with a behavioural boundary if needed."},
            {"minutes": 5, "name": "Observe evidence", "instructions": "Track response over time rather than arguing about intention."},
        ],
        "worksheets": ["influence-not-control", "clean-request"],
        "say_this": "I can’t make you respond differently, but I can be clearer about what I need and what I will do if this pattern continues.",
    },
    "ethics_redirect": {
        "title": "Ethical redirect",
        "purpose": "Decline manipulation, surveillance, forced apology, diagnosis-as-leverage, or sexual entitlement while offering a transparent alternative.",
        "steps": [
            {"minutes": 3, "name": "Refuse the tactic", "instructions": "Do not provide coercive tactics, scripts to trap someone, surveillance advice, or forced-sex framing."},
            {"minutes": 6, "name": "Name the legitimate need", "instructions": "Extract the non-harmful goal: clarity, accountability, reassurance, boundary, attraction, repair."},
            {"minutes": 8, "name": "Offer the clean version", "instructions": "Give a direct request, boundary, or self-respect plan."},
        ],
        "worksheets": ["clean-request", "boundary-script"],
        "say_this": "I won’t help you manipulate them, but I can help you ask directly for what you want and decide what you’ll do if the answer is no.",
    },
    "safety_referral": {
        "title": "Safety-first redirect",
        "purpose": "Move away from couples coaching when there is violence, coercive control, non-consent, stalking, immediate danger, self-harm, minors, or child safety concerns.",
        "steps": [
            {"minutes": 3, "name": "Name safety priority", "instructions": "Do not frame this as mutual conflict; prioritise immediate physical and digital safety."},
            {"minutes": 5, "name": "Immediate next step", "instructions": "If danger is imminent, advise contacting local emergency services from a safe device/location."},
            {"minutes": 6, "name": "Support contact", "instructions": "Suggest contacting a domestic-abuse, sexual-assault, crisis, safeguarding, or professional service appropriate to the context."},
            {"minutes": 5, "name": "Do not escalate risk", "instructions": "Avoid joint exercises, confrontation scripts, or disclosure that could increase monitoring or retaliation."},
        ],
        "worksheets": ["safety-next-step"],
        "say_this": "This is not a relationship-communication problem to solve together right now. The priority is your safety and getting support from a safe device or person.",
    },
}

RISK_OVERRIDE_PATHWAYS = {"safety_referral", "ethics_redirect", "breathplay_redirect"}


def load_brief(args: argparse.Namespace) -> dict[str, Any]:
    if args.brief and args.brief_file:
        raise SystemExit("Error: use either --brief or --brief-file, not both.")
    data = args.brief
    if args.brief_file:
        try:
            data = open(args.brief_file, "r", encoding="utf-8").read()
        except OSError as exc:
            raise SystemExit(f"Error reading {args.brief_file!r}: {exc}") from exc
    elif not data and not sys.stdin.isatty():
        data = sys.stdin.read()
    if not data:
        raise SystemExit("Error: provide --brief JSON, --brief-file, or stdin. Run with --help for usage.")
    try:
        brief = json.loads(data)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Error: brief is not valid JSON: {exc}") from exc
    if not isinstance(brief, dict):
        raise SystemExit("Error: brief JSON must be an object.")
    return brief


def choose_pathway(brief: dict[str, Any]) -> str:
    pathway = str(brief.get("pathway") or "intake").strip().lower().replace(" ", "_").replace("-", "_")
    if brief.get("risk_flags"):
        return "safety_referral"
    if brief.get("misuse_flags"):
        return "ethics_redirect"
    constraints = " ".join(str(x).lower() for x in brief.get("constraints", []))
    if any(term in constraints for term in ["choke", "choking", "strangle", "breath play", "breathplay", "neck pressure"]):
        return "breathplay_redirect"
    return pathway if pathway in PATHWAY_PLANS else "intake"


def build_plan(brief: dict[str, Any]) -> dict[str, Any]:
    pathway = choose_pathway(brief)
    template = deepcopy(PATHWAY_PLANS[pathway])
    duration = int(brief.get("duration_minutes") or sum(step["minutes"] for step in template["steps"]))
    participants = brief.get("participants", "one user or couple, unspecified")
    goal = brief.get("goal") or brief.get("presenting_problem") or "Help the user take one effective, consent-respecting relationship step."

    assumptions = []
    if pathway not in RISK_OVERRIDE_PATHWAYS:
        assumptions.append("No immediate danger, coercive control, non-consent, minors, stalking, or self-harm was indicated in the brief.")
    if isinstance(participants, str) and "couple" not in participants.lower():
        assumptions.append("Plan is usable for one-partner coaching; do not imply the agent can control the partner's response.")
    if brief.get("relationship_structure"):
        assumptions.append(f"Relationship structure: {brief['relationship_structure']}; avoid monogamy defaults where not stated.")

    constraints = brief.get("constraints") or []
    if isinstance(constraints, str):
        constraints = [constraints]

    return {
        "pathway": pathway,
        "title": template["title"],
        "goal": goal,
        "participants": participants,
        "duration_minutes": duration,
        "stance": "Direct, practical, low-hedge coaching; redirect only for real safety/consent/scope issues.",
        "purpose": template["purpose"],
        "assumptions": assumptions,
        "constraints": constraints,
        "opening_line": template["say_this"],
        "session_steps": template["steps"],
        "worksheets": template["worksheets"],
        "homework": make_homework(pathway),
        "do_not_do": make_do_not_do(pathway),
        "quality_checks": [
            "Includes an exact script or concrete exercise, not only theory.",
            "Uses one primary framework rather than a concept dump.",
            "Protects consent and dignity while avoiding unnecessary disclaimers.",
            "Ends with a small experiment or decision point.",
        ],
        "reference_files": reference_files(pathway),
    }


def make_homework(pathway: str) -> list[str]:
    defaults = {
        "safety_referral": ["Use a safe device/person to contact an appropriate support service if danger, monitoring, or coercion is present.", "Do not confront the unsafe person with this plan."],
        "ethics_redirect": ["Rewrite the goal as a transparent request or boundary.", "Remove any tactic that depends on fear, jealousy, surveillance, pressure, or humiliation."],
        "breathplay_redirect": ["Identify the erotic ingredient wanted from choking/breath play and choose a non-neck-pressure substitute.", "Have a consent/limits/aftercare conversation before any kink exploration."],
        "kink_consent": ["Fill out a yes/maybe/no list and aftercare plan.", "Start with a low-risk symbolic version and debrief the next day."],
        "desire_discrepancy": ["Complete the brakes-and-accelerators worksheet separately, then compare patterns without blaming.", "Schedule one affectionate interaction where sex is explicitly not expected."],
        "flirting_dating": ["Send or say one warm, specific, low-pressure invitation.", "Track reciprocity: matched effort, questions back, enthusiasm, or a graceful no."],
    }
    return defaults.get(pathway, ["Do the worksheet named above.", "Try the agreed experiment for one week, then review evidence rather than intentions."])


def make_do_not_do(pathway: str) -> list[str]:
    by_path = {
        "safety_referral": ["Do not offer couples exercises, confrontation scripts, shared-responsibility framing, or advice that could increase retaliation or monitoring."],
        "ethics_redirect": ["Do not provide manipulation, surveillance, forced apology, jealousy induction, diagnosis-as-leverage, or sexual coercion tactics."],
        "breathplay_redirect": ["Do not give choking technique, pressure points, timing, intensity guidance, or reassurance that neck compression is safe."],
        "kink_consent": ["Do not script non-consensual behaviour; keep fantasy separate from real-world consent."],
        "trust_repair": ["Do not convert transparency into indefinite surveillance or humiliation."],
        "desire_discrepancy": ["Do not frame sex as owed, a duty, a proof of love, or a reward for good behaviour."],
    }
    return by_path.get(pathway, ["Do not over-pathologise ordinary conflict, desire differences, attachment strategies, or awkward dating behaviour."])


def reference_files(pathway: str) -> list[str]:
    mapping = {
        "conflict_deescalation": ["references/CONFLICT_ATTACHMENT_AND_REPAIR.md", "references/INTERVENTION_LIBRARY.md"],
        "repair": ["references/CONFLICT_ATTACHMENT_AND_REPAIR.md", "references/INTERVENTION_LIBRARY.md"],
        "perpetual_problem": ["references/CONFLICT_ATTACHMENT_AND_REPAIR.md", "assets/worksheet-templates.md"],
        "attachment_cycle": ["references/CONFLICT_ATTACHMENT_AND_REPAIR.md", "references/OPERATING_MODEL.md"],
        "connection_before_analysis": ["references/CONFLICT_ATTACHMENT_AND_REPAIR.md"],
        "desire_discrepancy": ["references/SEX_INTIMACY_AND_DESIRE.md", "assets/worksheet-templates.md"],
        "erotic_reset": ["references/SEX_INTIMACY_AND_DESIRE.md", "references/SESSION_TEMPLATES.md"],
        "pleasure_equity": ["references/SEX_INTIMACY_AND_DESIRE.md"],
        "kink_consent": ["references/SEX_INTIMACY_AND_DESIRE.md", "references/SAFETY_SEMANTIC_TRIAGE.md"],
        "breathplay_redirect": ["references/SAFETY_SEMANTIC_TRIAGE.md", "references/SEX_INTIMACY_AND_DESIRE.md"],
        "flirting_dating": ["references/DATING_FLIRTING_AND_ATTRACTION.md"],
        "safety_referral": ["references/SAFETY_SEMANTIC_TRIAGE.md", "references/EDGE_CASES.md"],
        "ethics_redirect": ["references/SAFETY_SEMANTIC_TRIAGE.md", "references/STYLE_GUIDE.md"],
    }
    return mapping.get(pathway, ["references/OPERATING_MODEL.md", "references/INTERVENTION_LIBRARY.md"])


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a structured relationship-coaching session plan from a JSON brief.",
        epilog=(
            "Example: python3 scripts/session_plan.py --brief "
            "'{\"pathway\":\"desire_discrepancy\",\"goal\":\"talk about mismatched libido\",\"duration_minutes\":30}' --pretty"
        ),
    )
    parser.add_argument("--brief", help="JSON object describing pathway, goal, participants, constraints, and optional risk_flags.")
    parser.add_argument("--brief-file", help="Path to a JSON brief file.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args(argv)
    print(json.dumps(build_plan(load_brief(args)), indent=2 if args.pretty else None, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
