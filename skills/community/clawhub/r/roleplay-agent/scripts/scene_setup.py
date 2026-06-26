#!/usr/bin/env python3
"""
scene_setup.py
Generates a scene setup prompt from a persona file.
Run: python3 scene_setup.py [persona_file.md]
Outputs a structured scene prompt for the agent.
"""

import sys
import os

PERSONAS_DIR = "/root/.openclaw/workspace/skills/roleplay-agent/personas"

def parse_persona(path):
    """Extract Want, Obstacle, Moment Before, Voice, Boundaries from a persona file."""
    with open(path) as f:
        content = f.read()

    sections = {}
    current = None
    for line in content.split("\n"):
        line = line.rstrip()
        if line.startswith("# PERSONA:") or line.startswith("## "):
            current = line.lstrip("# ").lower().replace(" ", "_")
            sections[current] = ""
        elif current:
            sections[current] += line + "\n"
    return sections

def build_prompt(persona_name, sections):
    want = sections.get("want", "").strip()
    obstacle = sections.get("obstacle", "").strip()
    moment_before = sections.get("moment_before", "").strip()
    voice = sections.get("voice", "").strip()
    boundaries = sections.get("boundaries", "").strip()

    prompt = f"""## SCENE SETUP — {persona_name}

### Primary Persona: {persona_name}

**Want:** {want}
**Obstacle:** {obstacle}
**Moment Before:** {moment_before}

### Voice
{voice}

### Boundaries
{boundaries}

### Scene Questions (answer before writing)
1. Where are the characters physically?
2. What just happened to start this scene?
3. Whose want is primary — who is the scene "about"?
4. What does the primary character do in the first 30 seconds to try to get what they want?
"""
    return prompt

def main():
    if len(sys.argv) < 2:
        # List available personas
        files = [f for f in os.listdir(PERSONAS_DIR) if f.endswith(".md")]
        print("Available personas:")
        for f in files:
            print(f"  {f}")
        print(f"\nUsage: python3 scene_setup.py <persona_file.md>")
        print(f"Example: python3 scene_setup.py example_eve.md")
        return

    persona_file = sys.argv[1]
    path = os.path.join(PERSONAS_DIR, persona_file)
    if not os.path.exists(path):
        print(f"Error: {path} not found")
        return

    sections = parse_persona(path)
    persona_name = persona_file.replace(".md", "").replace("_", " ").title()
    prompt = build_prompt(persona_name, sections)
    print(prompt)

if __name__ == "__main__":
    main()
