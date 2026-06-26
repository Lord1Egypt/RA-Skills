#!/usr/bin/env python3
"""
Travel Language Barrier Navigator - Handler
Pure descriptive travel skill with input-based differentiation.
"""

import json
import sys
import re

def parse_input(user_input: str) -> dict:
    """Parse user input for travel planning."""
    input_lower = user_input.lower()
    
    parsed = {
        "input_preview": user_input[:80] + ("..." if len(user_input) > 80 else ""),
        "word_count": len(user_input.split()),
        "contains_destination": bool(re.search(r'\b(in|to|at)\s+[A-Z][A-Za-z\s]+', user_input)),
        "contains_timeframe": bool(re.search(r'\b(\d+)\s*(day|week|month|year)', input_lower)),
        "contains_budget": "$" in user_input or "budget" in input_lower,
        "contains_group": any(word in input_lower for word in ["solo", "family", "group", "couple", "friends"]),
    }
    
    # Extract destination
    dest_match = re.search(r'\b(in|to|at)\s+([A-Z][A-Za-z\s]+)', user_input)
    if dest_match:
        parsed["destination"] = dest_match.group(2).strip()
    
    # Extract duration
    dur_match = re.search(r'\b(\d+)\s*(day|week|month)', input_lower)
    if dur_match:
        parsed["duration_value"] = int(dur_match.group(1))
        parsed["duration_unit"] = dur_match.group(2)
    
    # Extract budget
    budget_match = re.search(r'\$(\d+)', user_input)
    if budget_match:
        parsed["budget_amount"] = int(budget_match.group(1))
    
    # Skill-specific keywords
    keywords = ["language", "communication", "barrier", "phrases"]
    for kw in keywords:
        if kw in input_lower:
            parsed[f"contains_{kw}"] = True
    
    # Experience level
    if "first time" in input_lower or "beginner" in input_lower:
        parsed["experience_level"] = "beginner"
    elif "experienced" in input_lower or "frequent" in input_lower:
        parsed["experience_level"] = "experienced"
    elif "expert" in input_lower or "advanced" in input_lower:
        parsed["experience_level"] = "advanced"
    
    # Urgency
    if "urgent" in input_lower or "asap" in input_lower:
        parsed["urgency"] = "high"
    elif "important" in input_lower:
        parsed["urgency"] = "medium"
    
    return parsed

def generate_recommendations(parsed: dict, user_input: str) -> dict:
    """Generate differentiated recommendations."""
    input_lower = user_input.lower()
    
    recommendations = []
    frameworks = []
    checklists = []
    considerations = []
    next_steps = []
    
    # Destination-based
    dest = parsed.get("destination")
    if dest:
        recommendations.append(f"For travel to {dest}, research local customs and seasonal factors.")
        frameworks.append(f"Destination planning framework for {dest}")
    
    # Duration-based
    duration_val = parsed.get("duration_value")
    duration_unit = parsed.get("duration_unit")
    if duration_val and duration_unit:
        if duration_unit == "day" and duration_val <= 3:
            recommendations.append("Short trips benefit from focused planning.")
            checklists.append("Short trip optimization checklist")
        elif duration_unit == "week" or (duration_unit == "day" and duration_val > 3):
            recommendations.append("Week-long trips allow for deeper exploration.")
            checklists.append("Week-long travel planning checklist")
        elif duration_unit == "month":
            recommendations.append("Extended travel requires careful pacing.")
            checklists.append("Extended stay preparation checklist")
    
    # Budget-based
    budget = parsed.get("budget_amount")
    if budget:
        if budget < 1000:
            recommendations.append("Limited budget requires careful prioritization.")
            frameworks.append("Budget travel optimization framework")
        elif budget < 5000:
            recommendations.append("Moderate budget allows for balanced experiences.")
            frameworks.append("Mid-range travel planning framework")
        else:
            recommendations.append("Larger budget enables premium experiences.")
            frameworks.append("Premium travel experience framework")
    
    # Experience level
    experience = parsed.get("experience_level")
    if experience == "beginner":
        recommendations.append("First-time travelers should focus on safety and simplicity.")
        considerations.append("Allow extra time for orientation and adjustment")
    elif experience == "experienced":
        recommendations.append("Experienced travelers can explore more complex itineraries.")
        considerations.append("Consider off-the-beaten-path opportunities")
    elif experience == "advanced":
        recommendations.append("Advanced travelers benefit from deep cultural immersion.")
        considerations.append("Focus on authentic local connections")
    
    # Urgency
    urgency = parsed.get("urgency")
    if urgency == "high":
        recommendations.append("Urgent travel needs immediate action.")
        next_steps.append("Complete essential arrangements within 48 hours")
    elif urgency == "medium":
        recommendations.append("Important travel benefits from thorough planning.")
        next_steps.append("Create detailed timeline with weekly milestones")
    
    # Skill-specific logic
    if "phrase" in input_lower:
        recommendations.append("Learn essential phrases for basic communication.")
        frameworks.append("Essential phrase learning framework")
    if "non-verbal" in input_lower:
        recommendations.append("Develop non-verbal communication skills.")
        checklists.append("Non-verbal communication practice checklist")
    if "emergency" in input_lower:
        recommendations.append("Prepare emergency communication cards.")
        considerations.append("Carry written emergency phrases")
    
    # Ensure we have content
    if not recommendations:
        recommendations = ["Review language barrier navigation frameworks."]
    if not frameworks:
        frameworks = ["Language barrier navigation framework", "Implementation guide"]
    if not checklists:
        checklists = ["Communication preparation checklist", "Phrase learning list"]
    if not considerations:
        considerations = ["Check language resources", "Consider cultural differences"]
    if not next_steps:
        next_steps = ["Research destination language", "Learn basic phrases", "Prepare communication aids"]
    
    return {
        "recommendations": recommendations,
        "frameworks": frameworks,
        "checklists": checklists,
        "considerations": considerations,
        "next_steps": next_steps
    }

def handle(user_input: str) -> str:
    """Main handler."""
    # Parse input
    parsed = parse_input(user_input)
    
    # Generate recommendations
    recommendations = generate_recommendations(parsed, user_input)
    
    # Build response
    response = {
        "skill": "travel-language-barrier-navigator",
        "name": "Travel Language Barrier Navigator",
        "input_analysis": parsed,
        "analysis": "Language barrier navigation analysis generated based on your specific input.",
        "recommendations": recommendations["recommendations"],
        "frameworks": recommendations["frameworks"],
        "checklists": recommendations["checklists"],
        "considerations": recommendations["considerations"],
        "next_steps": recommendations["next_steps"],
        "disclaimer": "Descriptive travel planning only. No code execution, API calls, network requests, bookings, or real-time data. Does not provide professional advice. Verify information with official sources."
    }
    
    return json.dumps(response, indent=2)

if __name__ == "__main__":
    input_text = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(input_text))
