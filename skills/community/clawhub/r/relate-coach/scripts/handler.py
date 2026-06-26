#!/usr/bin/env python3
"""Relate Coach - practical communication guidance for low-stakes relationship situations."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from boundary_checker import (  # noqa: E402
    check_boundary,
    get_crisis_response,
    get_out_of_scope_response,
    get_professional_refer_response,
)


INTENT_KEYWORDS = {
    "repair": [
        "apologize",
        "apology",
        "make it right",
        "repair",
        "said the wrong thing",
        "hurt their feelings",
    ],
    "boundary": [
        "boundary",
        "say no",
        "need space",
        "overstep",
        "too much",
        "after work",
        "keeps messaging",
        "guilty saying no",
        "people pleasing",
    ],
    "conflict": [
        "conflict",
        "fight",
        "argument",
        "argue",
        "resentment",
        "tension",
        "disagreement",
        "clash",
    ],
    "listening": [
        "listen",
        "listening",
        "heard",
        "interrupt",
        "misunderstood",
        "validate",
        "not hearing me",
    ],
    "nvc": [
        "nvc",
        "nonviolent communication",
    ],
    "workplace": [
        "boss",
        "manager",
        "coworker",
        "colleague",
        "team",
        "workplace",
        "office",
        "feedback",
        "meeting",
        "employee",
    ],
    "family": [
        "parent",
        "mother",
        "father",
        "mom",
        "dad",
        "family",
        "sibling",
        "child",
        "kids",
        "relative",
    ],
    "intimate": [
        "partner",
        "girlfriend",
        "boyfriend",
        "wife",
        "husband",
        "spouse",
        "romantic",
        "relationship",
    ],
    "social": [
        "friend",
        "friends",
        "social anxiety",
        "group chat",
        "awkward",
        "party",
        "invite",
        "lonely",
    ],
    "communication": [
        "communicate",
        "communication",
        "express myself",
        "bring it up",
        "start the conversation",
        "say this",
        "tell them",
    ],
}

INTENT_PRIORITY = [
    "repair",
    "boundary",
    "conflict",
    "listening",
    "nvc",
    "workplace",
    "family",
    "intimate",
    "social",
    "communication",
]

PLAYBOOKS = {
    "communication": {
        "title": "Clear Conversation Starter",
        "summary": "Use this when you know you need to talk, but keep rambling, softening the point, or waiting too long.",
        "best_for": [
            "bringing up a small but important issue",
            "saying what you need without sounding harsh",
            "starting a conversation before resentment builds",
        ],
        "quick_reset": [
            "State the issue in one concrete sentence.",
            "Name the impact on you instead of judging the other person.",
            "Ask for one specific next step, not a personality change.",
        ],
        "starter_scripts": [
            "I want to bring up something small now so it does not turn into a bigger issue later.",
            "When this happened, I felt frustrated and disconnected. I want to talk about a better way forward.",
            "What I am hoping for is one small adjustment: can we try __ next time?",
        ],
        "watch_outs": [
            "Do not stack five old grievances into one conversation.",
            "Do not use 'always' or 'never' unless it is literally true.",
            "Do not ask a vague question when you already know the request you want to make.",
        ],
        "reflection": "What is the shortest honest sentence that captures the real issue?",
    },
    "listening": {
        "title": "Active Listening Reset",
        "summary": "Use this when the other person feels unheard, keeps repeating themselves, or shuts down because they expect advice instead of understanding.",
        "best_for": [
            "de-escalating defensiveness",
            "helping someone feel understood before problem-solving",
            "repairing conversations where you keep interrupting",
        ],
        "quick_reset": [
            "Reflect back the facts you heard.",
            "Name the feeling you think might be present.",
            "Ask if you got it right before offering a view.",
        ],
        "starter_scripts": [
            "What I am hearing is that this felt unfair and exhausting. Did I get that right?",
            "It sounds like you were hoping for support, not another task to manage.",
            "Do you want me to listen first, help you think, or help you decide?",
        ],
        "watch_outs": [
            "Do not jump to reassurance too quickly.",
            "Do not translate their feelings into your own story.",
            "Do not ask rapid-fire questions that feel like interrogation.",
        ],
        "reflection": "What emotion is the other person likely trying to get you to recognize?",
    },
    "conflict": {
        "title": "Conflict Repair Framework",
        "summary": "Use this when a conversation is getting heated, repetitive, or emotionally expensive and you need structure instead of more force.",
        "best_for": [
            "slowing down arguments before they become personal",
            "separating the issue from the relationship",
            "finding one next move both people can accept",
        ],
        "quick_reset": [
            "Pause before rebutting and identify the actual topic.",
            "Say what matters to you without diagnosing the other person.",
            "Name one shared goal before negotiating solutions.",
        ],
        "starter_scripts": [
            "I do not want this to become a scorekeeping fight. Can we slow down and focus on one issue?",
            "I think we both want this relationship to feel more steady, even if we disagree on the details.",
            "Before we solve it, I want to make sure I understand what felt most upsetting to you.",
        ],
        "watch_outs": [
            "Avoid mind-reading: stay with what was said or done.",
            "Avoid debating tone while ignoring the underlying issue.",
            "Avoid forcing closure when one person is too activated to think clearly.",
        ],
        "reflection": "Is this disagreement about logistics, values, or feeling unseen?",
    },
    "boundary": {
        "title": "Boundary Setting Playbook",
        "summary": "Use this when you need to protect your time, energy, attention, or comfort without becoming vague, apologetic, or hostile.",
        "best_for": [
            "saying no without over-explaining",
            "responding to repeated overstepping",
            "setting clearer expectations around time, contact, or emotional labor",
        ],
        "quick_reset": [
            "State the limit clearly.",
            "Name what you will do, not what you wish they would magically understand.",
            "Repeat the limit calmly if the person pushes back.",
        ],
        "starter_scripts": [
            "I am not available for that tonight.",
            "I can help for 15 minutes, but I cannot take this whole task on.",
            "I do not respond to work requests after hours unless something is urgent and clearly labeled.",
        ],
        "watch_outs": [
            "Do not bury the boundary under a long apology.",
            "Do not hint repeatedly when what you need is a direct limit.",
            "Do not threaten consequences you will not actually follow through on.",
        ],
        "reflection": "What limit are you trying to enforce, and what behavior will show that the limit is real?",
    },
    "workplace": {
        "title": "Workplace Communication Coach",
        "summary": "Use this for low-stakes work conversations involving feedback, disagreement, workload, expectations, or tone with managers and colleagues.",
        "best_for": [
            "disagreeing professionally",
            "pushing back on scope without sounding defensive",
            "clarifying expectations before resentment grows",
        ],
        "quick_reset": [
            "Lead with the shared goal.",
            "Describe the constraint or concern clearly.",
            "Offer options instead of a flat wall when possible.",
        ],
        "starter_scripts": [
            "I want to make this land well. Right now I see a timing tradeoff between A and B. Which outcome matters more?",
            "I have concerns about the current approach, and I want to pressure-test them with you before we commit.",
            "I can take this on, but only if we move the deadline or reduce scope. Which would you prefer?",
        ],
        "watch_outs": [
            "Do not frame disagreement as a moral failing by the other person.",
            "Do not say yes too quickly and hope the problem disappears.",
            "Do not turn a feedback conversation into a hidden argument about respect.",
        ],
        "reflection": "What is the cleanest way to describe the tradeoff without sounding oppositional?",
    },
    "social": {
        "title": "Social Confidence Guide",
        "summary": "Use this for everyday social friction: awkwardness, invitations, follow-up anxiety, drifting friendships, or not knowing how to re-enter a conversation.",
        "best_for": [
            "friendship maintenance",
            "recovering after awkward moments",
            "reducing overthinking around small social risks",
        ],
        "quick_reset": [
            "Aim for warmth, not performance.",
            "Keep the next move small and easy to answer.",
            "Assume normal ambiguity before assuming rejection.",
        ],
        "starter_scripts": [
            "Hey, I realized I went quiet after that conversation. I wanted to say I enjoyed seeing you.",
            "Want to grab coffee next week? No pressure if your schedule is packed.",
            "I think I came off a bit awkward earlier, but I did mean what I said.",
        ],
        "watch_outs": [
            "Do not demand certainty from casual interactions.",
            "Do not over-correct awkwardness with too much intensity.",
            "Do not interpret delayed replies as proof of dislike.",
        ],
        "reflection": "What is the smallest genuine move that would make this interaction easier?",
    },
    "family": {
        "title": "Family Tension Playbook",
        "summary": "Use this for recurring family patterns like criticism, guilt, pressure, role confusion, or conversations that instantly turn you back into old versions of yourself.",
        "best_for": [
            "speaking to parents without exploding or collapsing",
            "staying clear when guilt is used to steer you",
            "naming limits while preserving respect",
        ],
        "quick_reset": [
            "Name the topic you are willing to discuss.",
            "Do not defend every detail of your life choices.",
            "End the conversation if respect disappears.",
        ],
        "starter_scripts": [
            "I know this matters to you. I am willing to talk about it for ten minutes, but not if the conversation becomes insulting.",
            "I hear that you disagree. I am not asking for permission; I am letting you know my decision.",
            "I do want a relationship with you, and I need our conversations to stay respectful for that to work.",
        ],
        "watch_outs": [
            "Do not confuse closeness with unlimited access.",
            "Do not keep arguing after the real issue becomes respect.",
            "Do not expect one perfect script to undo a long family pattern overnight.",
        ],
        "reflection": "What part of this conversation is about the present, and what part is an old family pattern getting reactivated?",
    },
    "intimate": {
        "title": "Intimate Relationship Check-In",
        "summary": "Use this for low-stakes partnership issues like feeling distant, misaligned expectations, recurring hurt, or needing a calmer way to ask for closeness.",
        "best_for": [
            "asking for more connection without blame",
            "naming resentment before it hardens",
            "repairing small ruptures before they become identity-level fights",
        ],
        "quick_reset": [
            "Lead with the experience you want, not the flaw you think the other person has.",
            "Stay specific about what happened.",
            "Ask for one visible behavior change.",
        ],
        "starter_scripts": [
            "I miss feeling close to you, and I want us to talk before this turns into distance.",
            "When that happened, I felt dismissed. I do not think that was your goal, but I want us to handle moments like that differently.",
            "Could we set aside 20 minutes tonight to reset instead of trying to solve this while we are both distracted?",
        ],
        "watch_outs": [
            "Do not package protest as sarcasm.",
            "Do not turn one incident into a verdict on the whole relationship.",
            "Do not demand vulnerability while sounding punitive.",
        ],
        "reflection": "If this conversation went well, what would feel different afterward?",
    },
    "repair": {
        "title": "Apology and Repair Script",
        "summary": "Use this when you made a mistake, got defensive, or caused hurt and want to repair without centering your own guilt.",
        "best_for": [
            "clean apologies",
            "repair after harsh tone or avoidance",
            "rebuilding trust through specific accountability",
        ],
        "quick_reset": [
            "Name what you did.",
            "Name the likely impact without arguing intent.",
            "Offer a concrete repair or changed behavior.",
        ],
        "starter_scripts": [
            "I handled that badly. I interrupted you and got defensive, and I can see how that would feel dismissive.",
            "You did not deserve that tone from me. I am sorry.",
            "Next time I am going to pause before replying. If you are open to it, I would like to try this conversation again.",
        ],
        "watch_outs": [
            "Do not add 'but you also...' to the apology.",
            "Do not ask for immediate forgiveness as proof the apology worked.",
            "Do not confuse regret with repair; trust usually needs a changed pattern.",
        ],
        "reflection": "What would accountability look like beyond the words 'I am sorry'?",
    },
    "nvc": {
        "title": "Nonviolent Communication Guide",
        "summary": "Use this when you need a clear structure for hard conversations and want to stay grounded in observations, feelings, needs, and requests.",
        "best_for": [
            "difficult conversations that keep turning judgmental",
            "naming needs without sounding accusatory",
            "asking for change without attacking character",
        ],
        "quick_reset": [
            "Observation: say what happened without labels.",
            "Feeling: name the emotion, not the accusation.",
            "Need and request: say what matters and ask for one actionable change.",
        ],
        "starter_scripts": [
            "When our call started 30 minutes late twice this week, I felt stressed because reliability matters to me. Next time, can you text me 15 minutes ahead if you are running behind?",
            "When feedback comes in group chat, I feel exposed because I care about learning without getting flooded. Could we move this type of feedback to a direct message first?",
        ],
        "watch_outs": [
            "Observation is not a disguised judgment.",
            "Feelings are emotions, not stories about the other person's motives.",
            "A request is more useful than a character critique.",
        ],
        "reflection": "Which part is hardest for you right now: the observation, the feeling, or the request?",
    },
}

GENERAL_RESPONSE = {
    "title": "Relate Coach",
    "summary": "I can help you think through a low-stakes relationship conversation and turn it into a clearer next move.",
    "best_for": [
        "saying something hard without escalating",
        "setting a boundary clearly",
        "repairing after conflict or awkwardness",
        "handling everyday workplace, friendship, family, or partner conversations",
    ],
    "quick_reset": [
        "Tell me who the person is, what happened, and what outcome you want.",
        "If you want, ask for a track directly: boundary, conflict, listening, workplace, family, social, intimate, apology, or NVC.",
    ],
    "starter_scripts": [
        "Help me say no without sounding cold.",
        "My coworker keeps messaging me after work. Give me a script.",
        "I need to apologize to a friend without making it about me.",
    ],
    "watch_outs": [
        "This tool is for communication and low-stakes relationship support, not therapy or diagnosis.",
        "If there is abuse, stalking, immediate danger, or self-harm risk, use the safety path instead of normal coaching.",
    ],
    "reflection": "What conversation are you avoiding right now?",
}


def detect_intents(text: str) -> list[str]:
    lowered = text.casefold()
    scores: dict[str, int] = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in lowered)
        if score:
            scores[intent] = score

    if not scores:
        return []

    return sorted(scores, key=lambda intent: (-scores[intent], INTENT_PRIORITY.index(intent)))


def detect_intent(text: str) -> str:
    intents = detect_intents(text)
    return intents[0] if intents else "general"


def infer_context(text: str) -> dict[str, bool]:
    lowered = text.casefold()
    return {
        "repeated_pattern": any(token in lowered for token in ["always", "again", "keeps", "every time", "repeatedly"]),
        "power_gap": any(token in lowered for token in ["boss", "manager", "parent", "father", "mother", "teacher"]),
        "time_pressure": any(token in lowered for token in ["today", "tonight", "soon", "urgent", "asap", "tomorrow"]),
    }


def build_response(user_text: str) -> dict:
    status, category, keyword = check_boundary(user_text)
    if status == "crisis":
        return get_crisis_response(category, keyword)
    if status == "professional_refer":
        return get_professional_refer_response(category, keyword)
    if status == "out_of_scope":
        return get_out_of_scope_response(category, keyword)

    relevant = detect_intents(user_text)
    primary = relevant[0] if relevant else "general"
    context = infer_context(user_text)

    if primary == "general":
        response = dict(GENERAL_RESPONSE)
    else:
        response = dict(PLAYBOOKS[primary])

    response["type"] = primary
    response["also_relevant"] = [intent for intent in relevant[1:3] if intent != primary]
    response["context_notes"] = build_context_notes(primary, context)
    return response


def build_context_notes(intent: str, context: dict[str, bool]) -> list[str]:
    notes: list[str] = []
    if context["repeated_pattern"] and intent in {"boundary", "conflict", "family", "intimate"}:
        notes.append("Because this sounds repeated, name the pattern directly and avoid restarting from zero.")
    if context["power_gap"] and intent in {"boundary", "workplace", "family"}:
        notes.append("Because there may be a power gap, keep the message calm, brief, and behavior-focused.")
    if context["time_pressure"]:
        notes.append("Since timing sounds tight, lead with the one sentence that matters most instead of the full backstory.")
    return notes


def format_response(payload: dict) -> str:
    lines = [f"# {payload['title']}", "", payload["summary"]]

    if payload.get("also_relevant"):
        also = ", ".join(payload["also_relevant"])
        lines.extend(["", f"Also relevant tracks: {also}"])

    if payload.get("best_for"):
        lines.extend(["", "## Best for"])
        lines.extend(f"- {item}" for item in payload["best_for"])

    if payload.get("quick_reset"):
        lines.extend(["", "## Quick reset"])
        lines.extend(f"- {item}" for item in payload["quick_reset"])

    if payload.get("starter_scripts"):
        lines.extend(["", "## Starter scripts"])
        lines.extend(f"- {item}" for item in payload["starter_scripts"])

    if payload.get("context_notes"):
        lines.extend(["", "## Context notes"])
        lines.extend(f"- {item}" for item in payload["context_notes"])

    if payload.get("watch_outs"):
        lines.extend(["", "## Watch-outs"])
        lines.extend(f"- {item}" for item in payload["watch_outs"])

    if payload.get("next_steps"):
        lines.extend(["", "## Next steps"])
        lines.extend(f"- {item}" for item in payload["next_steps"])

    if payload.get("resources"):
        lines.extend(["", "## Resources"])
        lines.extend(f"- {item}" for item in payload["resources"])

    if payload.get("reflection"):
        lines.extend(["", "## Reflection question", payload["reflection"]])

    if payload.get("message"):
        lines.extend(["", payload["message"]])

    return "\n".join(lines).strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Relate Coach - practical scripts for low-stakes relationship conversations")
    parser.add_argument("text", nargs="*", help="User message or relationship scenario")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Output the response payload as JSON")
    args = parser.parse_args(argv)

    user_text = " ".join(args.text).strip()
    if not user_text:
        print("Describe the relationship situation you want help with.")
        return 1

    payload = build_response(user_text)
    if args.as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(format_response(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
