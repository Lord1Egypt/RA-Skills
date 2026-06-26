#!/usr/bin/env python3
"""
Resilience Building Architect - Descriptive skill
"""

import json
import sys
import re

def parse_input(user_input: str) -> dict:
    """Parse user input."""
    input_lower = user_input.lower()
    parsed = {
        "input_preview": user_input[:60],
        "word_count": len(user_input.split()),
        "has_goals": "goal" in input_lower,
        "has_challenges": "challenge" in input_lower or "problem" in input_lower,
    }
    
    # Skill-specific detection
    if "resilience-building-architect" == "curiosity-cultivator":
        parsed["curiosity_focus"] = "curiosity" in input_lower or "wonder" in input_lower
    elif "resilience-building-architect" == "resilience-building-architect":
        parsed["resilience_focus"] = "resilience" in input_lower or "stress" in input_lower
    elif "resilience-building-architect" == "intuition-development-guide":
        parsed["intuition_focus"] = "intuition" in input_lower or "gut" in input_lower
    elif "resilience-building-architect" == "personal-ritual-designer":
        parsed["ritual_focus"] = "ritual" in input_lower or "meaning" in input_lower
    elif "resilience-building-architect" == "digital-presence-curator":
        parsed["digital_focus"] = "digital" in input_lower or "online" in input_lower
    elif "resilience-building-architect" == "legacy-thinking-facilitator":
        parsed["legacy_focus"] = "legacy" in input_lower or "impact" in input_lower
    elif "resilience-building-architect" == "sensory-awareness-enhancer":
        parsed["sensory_focus"] = "sensory" in input_lower or "awareness" in input_lower
    elif "resilience-building-architect" == "play-rediscovery-guide":
        parsed["play_focus"] = "play" in input_lower or "fun" in input_lower
    elif "resilience-building-architect" == "cultural-intelligence-builder":
        parsed["cultural_focus"] = "cultural" in input_lower or "diversity" in input_lower
    elif "resilience-building-architect" == "generosity-practice-designer":
        parsed["generosity_focus"] = "generosity" in input_lower or "giving" in input_lower
    
    # Urgency detection
    if "urgent" in input_lower:
        parsed["urgency"] = "high"
    elif "important" in input_lower:
        parsed["urgency"] = "medium"
    
    return parsed

def generate_response(parsed: dict, user_input: str) -> dict:
    """Generate response."""
    response = {
        "skill": "resilience-building-architect",
        "name": "Resilience Building Architect",
        "input_analysis": parsed,
        "analysis": "Analysis based on your input.",
    }
    
    recs = []
    steps = []
    frameworks = []
    
    # Differentiate based on urgency
    urgency = parsed.get("urgency")
    if urgency == "high":
        recs.append("Urgent matters need immediate attention.")
        steps.append("Address within 24-48 hours.")
    elif urgency == "medium":
        recs.append("Important items require structured planning.")
        steps.append("Create timeline with milestones.")
    
    # Differentiate based on word count
    if parsed.get("word_count", 0) > 30:
        recs.append("Detailed input allows for tailored guidance.")
    else:
        recs.append("Consider providing more details for specific advice.")
    
    # Skill-specific recommendations
    if "resilience-building-architect" == "curiosity-cultivator":
        recs.append("Cultivate curiosity through questioning and exploration.")
        frameworks.append("Curiosity assessment framework")
    elif "resilience-building-architect" == "resilience-building-architect":
        recs.append("Build resilience through stress management and recovery practices.")
        frameworks.append("Resilience building framework")
    elif "resilience-building-architect" == "intuition-development-guide":
        recs.append("Develop intuition through awareness and validation practices.")
        frameworks.append("Intuition development framework")
    elif "resilience-building-architect" == "personal-ritual-designer":
        recs.append("Design meaningful rituals for transitions and daily life.")
        frameworks.append("Ritual design framework")
    elif "resilience-building-architect" == "digital-presence-curator":
        recs.append("Curate digital presence with intention and authenticity.")
        frameworks.append("Digital presence framework")
    elif "resilience-building-architect" == "legacy-thinking-facilitator":
        recs.append("Reflect on legacy and align actions with values.")
        frameworks.append("Legacy thinking framework")
    elif "resilience-building-architect" == "sensory-awareness-enhancer":
        recs.append("Enhance sensory awareness for presence and creativity.")
        frameworks.append("Sensory awareness framework")
    elif "resilience-building-architect" == "play-rediscovery-guide":
        recs.append("Rediscover play for joy, creativity, and stress relief.")
        frameworks.append("Play rediscovery framework")
    elif "resilience-building-architect" == "cultural-intelligence-builder":
        recs.append("Build cultural intelligence for diverse environments.")
        frameworks.append("Cultural intelligence framework")
    elif "resilience-building-architect" == "generosity-practice-designer":
        recs.append("Design sustainable generosity practices.")
        frameworks.append("Generosity practice framework")
    
    # Ensure we have content
    if not recs:
        recs = ["Review relevant frameworks.", "Consult professionals if needed."]
    if not steps:
        steps = ["Customize with your context.", "Schedule regular reviews."]
    if not frameworks:
        frameworks = ["Personal growth framework", "Implementation checklist"]
    
    response["recommendations"] = recs
    response["next_steps"] = steps
    response["frameworks"] = frameworks
    response["disclaimer"] = "Descriptive analysis only. No code execution. Consult professionals for serious matters."
    
    return response

def handle(user_input: str) -> str:
    """Main handler."""
    parsed = parse_input(user_input)
    response = generate_response(parsed, user_input)
    return json.dumps(response, indent=2)

if __name__ == "__main__":
    input_text = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(input_text))
