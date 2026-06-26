#!/usr/bin/env python3
"""
Focus State Assessment Tool

Diagnose current focus state based on the Challenge ≈ Skill framework.
Helps identify whether user is in Anxiety, Boredom, Flow, or Relaxed state.
"""

import sys


def get_challenge_rating():
    """Get challenge level rating from user (1-10)"""
    while True:
        try:
            print("\nOn a scale of 1-10, how challenging is your current main task?")
            print("(1 = trivial, 10 = completely overwhelming)")
            rating = int(input("> "))
            if 1 <= rating <= 10:
                return rating
            print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Please enter a valid number.")


def get_skill_rating():
    """Get skill level rating from user (1-10)"""
    while True:
        try:
            print("\nOn a scale of 1-10, how would you rate your current skill level for this task?")
            print("(1 = complete beginner, 10 = world-class expert)")
            rating = int(input("> "))
            if 1 <= rating <= 10:
                return rating
            print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Please enter a valid number.")


def get_symptoms():
    """Gather symptoms to confirm assessment"""
    print("\nWhich symptoms are you experiencing? (select all that apply)")
    symptoms = {
        "overwhelmed": False,
        "negative_self_talk": False,
        "paralysis": False,
        "restlessness": False,
        "wandering_mind": False,
        "time_flies": False,
        "complete_absorption": False,
        "effortless_performance": False,
        "boredom": False,
        "frustration": False,
    }

    symptom_list = list(symptoms.keys())

    for i, symptom in enumerate(symptom_list, 1):
        print(f"{i}. {symptom.replace('_', ' ').title()}")

    print("\nEnter numbers separated by commas (e.g., 1,3,5), or press Enter for none:")

    try:
        response = input("> ").strip()
        if response:
            indices = [int(x.strip()) for x in response.split(",")]
            for idx in indices:
                if 1 <= idx <= len(symptom_list):
                    symptom = symptom_list[idx - 1]
                    symptoms[symptom] = True
    except ValueError:
        pass

    return symptoms


def analyze_state(challenge, skill, symptoms):
    """Analyze the focus state based on inputs"""

    gap = challenge - skill

    states = {
        "anxiety": {
            "name": "ANXIETY",
            "condition": challenge > skill + 1,
            "indicators": ["overwhelmed", "negative_self_talk", "paralysis", "frustration"],
            "message": "Your challenge level exceeds your skill level. You're attempting a level-100 boss as a level-1 character.",
        },
        "boredom": {
            "name": "BOREDOM",
            "condition": skill > challenge + 1,
            "indicators": ["restlessness", "wandering_mind", "boredom"],
            "message": "Your skill level exceeds the challenge. The task is too easy and isn't stretching you.",
        },
        "flow": {
            "name": "FLOW",
            "condition": abs(gap) <= 1,
            "indicators": ["time_flies", "complete_absorption", "effortless_performance"],
            "message": "Challenge and skill are well-matched. You're in the optimal zone for performance and growth.",
        },
        "relaxed": {
            "name": "RELAXED",
            "condition": False,  # This is a catch-all, handled separately
            "indicators": [],
            "message": "You've mastered this level. It's comfortable but not challenging.",
        },
    }

    # Determine primary state
    if states["anxiety"]["condition"]:
        state = "anxiety"
    elif states["boredom"]["condition"]:
        state = "boredom"
    elif states["flow"]["condition"]:
        state = "flow"
    else:
        state = "relaxed"

    return state, states[state]


def get_recommendations(state, challenge, skill):
    """Get recommendations for the identified state"""
    recommendations = {
        "anxiety": [
            f"Break your task into smaller sub-goals (current challenge: {challenge}, skill: {skill})",
            "Focus only on the very next micro-step, not the entire project",
            "Set a timer for 15 minutes and commit to just 15 minutes of work",
            "Study foundational skills before continuing",
            "Accept that feeling overwhelmed means you're growing—lean into it",
        ],
        "boredom": [
            f"Increase the challenge (current skill: {skill} is too high for challenge: {challenge})",
            "Add a deadline or time constraint",
            "Raise your standards—aim higher than you initially planned",
            "Take on a stretch project that scares you slightly",
            "Compete with yourself or others",
        ],
        "flow": [
            "Protect this state—document what conditions created it",
            "Extend your session if energy allows (max 4 hours)",
            "Take a short break every 60-90 minutes to maintain quality",
            "Capture any insights that emerge—they're valuable",
            "You're in the zone—keep building",
        ],
        "relaxed": [
            "You've mastered this level—time to move up",
            "Find a stretch goal that genuinely challenges you",
            "Review your 10-year vision and raise your targets",
            "Consider taking on a mentorship or teaching role",
        ],
    }

    return recommendations[state]


def main():
    print("=" * 60)
    print("FOCUS STATE ASSESSMENT TOOL")
    print("Based on the Challenge ≈ Skill Framework")
    print("=" * 60)

    challenge = get_challenge_rating()
    skill = get_skill_rating()
    symptoms = get_symptoms()

    state, state_info = analyze_state(challenge, skill, symptoms)

    print("\n" + "=" * 60)
    print(f"ASSESSMENT: {state_info['name']}")
    print("=" * 60)
    print(f"\n{state_info['message']}")
    print(f"\nChallenge Level: {challenge}/10")
    print(f"Skill Level: {skill}/10")
    print(f"Gap: {abs(challenge - skill)}")

    print("\n" + "-" * 60)
    print("RECOMMENDATIONS:")
    print("-" * 60)

    recommendations = get_recommendations(state, challenge, skill)
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")

    print("\n" + "-" * 60)
    print("DEEP WORK CHECKLIST:")
    print("-" * 60)
    checklist = [
        "I know exactly what one task I'm working on",
        "The challenge is just above my current skill level",
        "I understand WHY this matters to my future",
        "Distractions are removed (phone, tabs, notifications)",
        "I have a hard stop time (60 or 90 minutes max)",
    ]
    for item in checklist:
        print(f"[ ] {item}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
