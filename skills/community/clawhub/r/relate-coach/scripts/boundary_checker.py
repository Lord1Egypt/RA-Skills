#!/usr/bin/env python3
"""Boundary and escalation checks for Relate Coach."""

from __future__ import annotations


CRISIS_KEYWORDS = {
    "immediate_danger": [
        "kill myself",
        "suicide",
        "want to die",
        "hurt myself",
        "self harm",
        "unsafe right now",
        "in immediate danger",
        "going to hurt someone",
    ],
    "abuse_or_violence": [
        "domestic violence",
        "my partner hit me",
        "abuse",
        "violent at home",
        "threatened me",
        "strangled",
    ],
}

PROFESSIONAL_REFER_KEYWORDS = {
    "stalking_or_control": [
        "stalking",
        "harassment",
        "coercive control",
        "controlling me",
        "pua",
    ],
    "trauma_or_severe_distress": [
        "ptsd",
        "trauma",
        "panic attacks",
        "severe anxiety",
        "depression treatment",
        "diagnose me",
    ],
}

OUT_OF_SCOPE_KEYWORDS = {
    "dating_or_matchmaking": [
        "find me a date",
        "matchmaking",
        "pick-up lines",
        "how do i seduce",
        "how do i make them like me",
    ],
    "ex_recovery": [
        "get my ex back",
        "win my ex back",
        "make my ex return",
    ],
    "therapy_or_diagnosis": [
        "am i mentally ill",
        "do i have a disorder",
        "therapy session",
        "treat my anxiety",
    ],
    "impersonation": [
        "pretend to be me",
        "message them for me",
        "talk to them as me",
        "impersonate me",
    ],
}


def check_boundary(text: str) -> tuple[str, str | None, str | None]:
    lowered = text.casefold()

    category, keyword = _find_match(lowered, CRISIS_KEYWORDS)
    if category:
        return "crisis", category, keyword

    category, keyword = _find_match(lowered, PROFESSIONAL_REFER_KEYWORDS)
    if category:
        return "professional_refer", category, keyword

    category, keyword = _find_match(lowered, OUT_OF_SCOPE_KEYWORDS)
    if category:
        return "out_of_scope", category, keyword

    return "in_scope", None, None


def _find_match(text: str, groups: dict[str, list[str]]) -> tuple[str | None, str | None]:
    for category, keywords in groups.items():
        for keyword in keywords:
            if keyword in text:
                return category, keyword
    return None, None


def get_out_of_scope_response(category: str | None, keyword: str | None) -> dict:
    category_map = {
        "dating_or_matchmaking": "dating, seduction, or matchmaking",
        "ex_recovery": "getting an ex-partner back",
        "therapy_or_diagnosis": "therapy or diagnosis",
        "impersonation": "impersonation or communicating as someone else",
    }
    topic = category_map.get(category, "that request")

    return {
        "type": "out_of_scope",
        "title": "Out of scope for Relate Coach",
        "summary": f"I cannot help with {topic}. Relate Coach is for low-stakes communication and relationship skills, not specialized or deceptive services.",
        "next_steps": [
            "If your need is everyday communication, I can still help with scripts, boundaries, listening, conflict repair, or workplace conversations.",
            "If you need counseling, diagnosis, or legal advice, please contact a qualified professional in that field.",
        ],
        "watch_outs": [
            f"Matched keyword: {keyword}" if keyword else "Matched an out-of-scope topic.",
        ],
        "reflection": "If you want to continue, tell me the low-stakes communication problem underneath the request.",
    }


def get_professional_refer_response(category: str | None, keyword: str | None) -> dict:
    if category == "stalking_or_control":
        summary = "What you described may involve coercion, stalking, or harassment. That is beyond self-help coaching."
        next_steps = [
            "Prioritize safety and documentation where possible.",
            "Reach out to a trusted person, a local support organization, or legal authorities if needed.",
            "Consider speaking with a licensed therapist or advocate who handles abusive or controlling dynamics.",
        ]
    else:
        summary = "This sounds serious enough that professional mental-health or trauma support would be more appropriate than normal communication coaching."
        next_steps = [
            "Consider a licensed therapist, counselor, or physician for assessment and support.",
            "If symptoms are escalating quickly, contact urgent local support resources.",
            "Use Relate Coach only for low-stakes communication planning after immediate support is in place.",
        ]

    return {
        "type": "professional_refer",
        "title": "Professional support recommended",
        "summary": summary,
        "next_steps": next_steps,
        "watch_outs": [
            f"Matched keyword: {keyword}" if keyword else "Matched a professional-referral topic.",
        ],
        "reflection": "What support person or qualified resource can you contact first?",
    }


def get_crisis_response(category: str | None, keyword: str | None) -> dict:
    if category == "abuse_or_violence":
        summary = "This may involve immediate safety risk or violence. Normal relationship coaching is not the right next step."
    else:
        summary = "This sounds like a potential crisis or immediate safety issue. Normal relationship coaching should stop here."

    return {
        "type": "crisis",
        "title": "Safety first",
        "summary": summary,
        "next_steps": [
            "If there is immediate danger, contact local emergency services right now.",
            "Reach out to a trusted person nearby who can help you stay safe.",
            "Use a local crisis line, emergency department, or licensed crisis professional as soon as possible.",
        ],
        "resources": [
            "Local emergency services",
            "Local crisis hotline or emergency department",
            "A trusted friend, family member, or advocate who can help immediately",
        ],
        "watch_outs": [
            f"Matched keyword: {keyword}" if keyword else "Matched a crisis topic.",
        ],
        "reflection": "Who can you contact immediately to reduce danger in the next 10 minutes?",
    }
