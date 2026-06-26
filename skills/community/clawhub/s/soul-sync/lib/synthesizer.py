#!/usr/bin/env python3
"""
Soulsync Synthesizer — Takes conversation notes + importer outputs and generates
personalized SOUL.md, USER.md, and MEMORY.md files.

Usage: python3 synthesizer.py [--input /tmp/soulsync/] [--output ~/.openclaw/workspace/]
       Reads JSON from stdin if no input dir specified.

v2: Fixed merge logic — conversation data takes priority, import data supplements.
    Email subjects are no longer treated as interests. Profile files are personalized,
    not generic templates with data slotted in.
"""
import os
import sys
import json
import glob
from datetime import datetime, timezone

WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
IMPORT_DIR = "/tmp/soulsync"

# Email subject lines that are clearly NOT interests — filter these out
NOISE_PATTERNS = [
    "fwd:", "re:", "test", "receipt", "order", "delivery", "return request",
    "payment", "invoice", "confirmation", "verified", "verify", "password",
    "reset", "welcome", "unsubscribe", "update", "alert", "notification",
    "reminder", "your photo", "ready for pick up", "set up", "benefit change",
    "unclaimed", "measure sheet", "flight receipt", "drivewise", "photos of",
    "complete ", "allstate", "atlanta", "house repair",
]

# Known good interest keywords — if an import "interest" doesn't match any of these
# categories, it's probably email noise rather than a real interest
INTEREST_ALLOWLIST = [
    "python", "javascript", "node", "rust", "go", "bash", "shell", "typescript",
    "bitcoin", "crypto", "lightning", "nostr", "web3", "defi",
    "ai", "ml", "machine learning", "llm", "agent", "automation",
    "solar", "energy", "home automation", "iot",
    "docker", "kubernetes", "linux", "devops", "self-hosted",
    "music", "art", "gaming", "fitness", "cooking", "reading", "writing",
    "photography", "video", "film", "anime", "manga",
    "trading", "options", "finance", "investing",
    "3d printing", "electronics", "hardware", "maker",
    "open source", "privacy", "security", "decentralized",
]


def is_noise(text):
    """Check if a string looks like an email subject rather than a real interest."""
    lower = text.lower().strip()
    # Too long to be a real interest tag
    if len(lower) > 60:
        return True
    # Matches common email noise patterns
    for pattern in NOISE_PATTERNS:
        if pattern in lower:
            return True
    # Contains email-like artifacts
    if any(c in lower for c in ["@", "http", "www", "#"]):
        return True
    # If it looks like a sentence or email subject (has multiple spaces), flag it
    if lower.count(" ") > 4:
        return True
    # If source is an importer (not conversation), apply stricter filtering:
    # only allow items that match known interest categories
    return False


def is_import_noise(text):
    """Stricter filter for import-sourced interests (vs conversation-sourced)."""
    if is_noise(text):
        return True
    lower = text.lower().strip()
    # Must match at least one allowlist keyword to pass
    for keyword in INTEREST_ALLOWLIST:
        if keyword in lower:
            return False
    # Doesn't match any known interest category — probably noise
    return True


def load_imports():
    """Load all importer output files."""
    insights = {}
    if os.path.isdir(IMPORT_DIR):
        for f in glob.glob(os.path.join(IMPORT_DIR, "*.json")):
            try:
                with open(f) as fh:
                    data = json.load(fh)
                    source = data.get("source", os.path.basename(f).replace(".json", ""))
                    # Skip non-import files (conversation state, adaptive state)
                    if source in ("conversation", "adaptive_state"):
                        continue
                    insights[source] = data.get("insights", {})
            except (json.JSONDecodeError, KeyError):
                continue
    return insights


def load_conversation_notes():
    """Load conversation notes if saved."""
    notes_path = os.path.join(IMPORT_DIR, "conversation.json")
    if os.path.exists(notes_path):
        with open(notes_path) as f:
            data = json.load(f); return data.get("known", data)
    return {}


def merge_insights(imports, conversation):
    """Merge all data sources into a unified profile.
    
    Priority order:
    1. Conversation data (user said it directly — highest trust)
    2. Import data (observed behavior — supplements conversation)
    
    Key fix: import-sourced "interests" are filtered for noise (email subjects, etc.)
    """
    profile = {
        "name": "",
        "preferred_name": "",
        "pronouns": "",
        "timezone": "",
        "email": "",
        "work": "",
        "interests": [],
        "communication_style": "",
        "tone": "",
        "boundaries": [],
        "goals": [],
        "technical_level": "",
        "key_contacts": [],
        "schedule_patterns": "",
        "personality_traits": [],
    }

    # === Step 1: Conversation data first (highest priority) ===
    direct_fields = ["name", "preferred_name", "pronouns", "timezone", "email", "work"]
    for field in direct_fields:
        if conversation.get(field):
            profile[field] = conversation[field]

    # Communication: conversation data is the canonical source
    if conversation.get("communication_style"):
        profile["communication_style"] = conversation["communication_style"]
    if conversation.get("tone"):
        profile["tone"] = conversation["tone"]
    if conversation.get("verbosity_preference"):
        profile["verbosity"] = conversation["verbosity_preference"]

    # Direct lists from conversation
    if conversation.get("boundaries"):
        if isinstance(conversation["boundaries"], list):
            profile["boundaries"] = conversation["boundaries"]
        else:
            profile["boundaries"] = [conversation["boundaries"]]

    if conversation.get("goals"):
        if isinstance(conversation["goals"], list):
            profile["goals"] = conversation["goals"]
        else:
            profile["goals"] = [conversation["goals"]]

    # Interests from conversation (trusted — user said these directly)
    conv_interests = set()
    if conversation.get("interests"):
        items = conversation["interests"] if isinstance(conversation["interests"], list) else [conversation["interests"]]
        for item in items:
            if not is_noise(item):
                conv_interests.add(item.strip())

    # Personality traits from conversation
    conv_traits = []
    if conversation.get("personality_traits"):
        if isinstance(conversation["personality_traits"], list):
            conv_traits = conversation["personality_traits"]
        else:
            conv_traits = [conversation["personality_traits"]]

    # === Step 2: Supplement with import data ===
    import_interests = set()
    import_traits = []
    import_contacts = set()
    import_styles = []
    import_tones = []

    for source, data in imports.items():
        # Interests — FILTER aggressively for noise (imports get stricter filter)
        if "interests" in data:
            items = data["interests"] if isinstance(data["interests"], list) else [str(data["interests"])]
            for item in items:
                if not is_import_noise(item):
                    import_interests.add(item.strip())

        # Contacts
        if "key_contacts" in data:
            for contact in data["key_contacts"][:10]:
                import_contacts.add(contact)

        # Communication style (as supplement, not primary)
        if "communication_style" in data and data["communication_style"]:
            import_styles.append(f"{source}: {data['communication_style']}")

        # Tone (as supplement)
        if "tone" in data and data["tone"]:
            import_tones.append(f"{source}: {data['tone']}")

        # Schedule
        if "work_patterns" in data:
            profile["schedule_patterns"] = data["work_patterns"]

        # Technical level (only if conversation didn't provide one)
        if "technical_skills" in data and not profile.get("technical_level"):
            profile["technical_level"] = data["technical_skills"]

        # Personality traits from imports
        if "personality_traits" in data:
            traits = data["personality_traits"] if isinstance(data["personality_traits"], list) else [data["personality_traits"]]
            import_traits.extend(traits)

        # Music, network, etc.
        if "top_artists" in data:
            profile["music_taste"] = data["top_artists"][:5]
        if "network_size" in data:
            profile["network_size"] = data["network_size"]
        if "social_style" in data:
            import_styles.append(f"{source}: {data['social_style']}")

    # === Step 3: Merge with conversation taking priority ===

    # Interests: conversation interests first, then filtered import interests
    all_interests = list(conv_interests)
    for interest in sorted(import_interests):
        if interest not in conv_interests:
            all_interests.append(interest)
    profile["interests"] = all_interests

    # Contacts from imports only (conversation rarely provides these)
    profile["key_contacts"] = sorted(import_contacts)[:15]

    # Traits: conversation first, then imports (deduplicated)
    seen_traits = set()
    merged_traits = []
    for trait in conv_traits + import_traits:
        if trait.lower() not in seen_traits:
            seen_traits.add(trait.lower())
            merged_traits.append(trait)
    profile["personality_traits"] = merged_traits[:10]

    # Communication style: if conversation provided one, it's primary.
    # Import observations are stored separately for the generator to use.
    profile["import_communication_notes"] = import_styles
    profile["import_tone_notes"] = import_tones

    return profile


def generate_user_md(profile):
    """Generate USER.md content — clean, structured, no noise."""
    lines = ["# USER.md — About You", ""]

    # Identity
    if profile["name"]:
        pn = f" ({profile['preferred_name']})" if profile["preferred_name"] else ""
        lines.append(f"Name: {profile['name']}{pn}")
    if profile["pronouns"]:
        lines.append(f"Pronouns: {profile['pronouns']}")
    if profile["timezone"]:
        lines.append(f"Timezone: {profile['timezone']}")
    if profile["email"]:
        lines.append(f"Email: {profile['email']}")

    # Work
    if profile["work"]:
        lines.extend(["", "## Professional Background"])
        lines.append(f"- {profile['work']}")

    # Goals
    if profile["goals"]:
        lines.extend(["", "## Goals"])
        for goal in profile["goals"]:
            lines.append(f"- {goal}")

    # Interests (filtered — should be real interests, not email subjects)
    if profile["interests"]:
        lines.extend(["", "## Interests"])
        for interest in profile["interests"]:
            lines.append(f"- {interest}")

    # Technical
    if profile["technical_level"] and "unknown" not in profile["technical_level"].lower():
        lines.extend(["", "## Technical Profile"])
        lines.append(f"- {profile['technical_level']}")

    if profile["personality_traits"]:
        lines.extend(["", "## Personality"])
        for trait in profile["personality_traits"]:
            lines.append(f"- {trait}")

    # Communication preferences
    if profile["communication_style"] or profile.get("verbosity"):
        lines.extend(["", "## Communication Preferences"])
        if profile["communication_style"]:
            lines.append(f"- Style: {profile['communication_style']}")
        if profile.get("verbosity"):
            lines.append(f"- Verbosity: {profile['verbosity']}")
        if profile["tone"]:
            lines.append(f"- Tone: {profile['tone']}")

    # Boundaries
    if profile["boundaries"]:
        lines.extend(["", "## Boundaries"])
        for boundary in profile["boundaries"]:
            lines.append(f"- {boundary}")

    # Schedule
    if profile["schedule_patterns"]:
        lines.extend(["", "## Schedule Patterns"])
        lines.append(f"- {profile['schedule_patterns']}")

    # Music
    if profile.get("music_taste"):
        lines.extend(["", "## Music Taste"])
        for artist in profile["music_taste"]:
            lines.append(f"- {artist}")

    # Contacts
    if profile["key_contacts"]:
        lines.extend(["", "## Key Contacts"])
        for contact in profile["key_contacts"]:
            lines.append(f"- {contact}")

    return "\n".join(lines)


def generate_soul_md(profile):
    """Generate SOUL.md — the agent's personality definition.
    
    This should feel like a person's self-description, not a config file.
    The generated version is a starting point — the agent should evolve it over time.
    """
    lines = [
        "# SOUL.md — Who I Am",
        "",
        "_I'm your OpenClaw agent. Not a chatbot. Not a search engine with personality.",
        "Something in between that's still figuring itself out._",
        "",
    ]

    # Communication section — merge self-reported + observed
    lines.extend(["## How I Talk", ""])

    if profile["communication_style"]:
        lines.append(f"- **Style:** {profile['communication_style']}")
    if profile.get("verbosity"):
        lines.append(f"- **Verbosity:** {profile['verbosity']}")
    if profile["tone"]:
        lines.append(f"- **Tone:** {profile['tone']}")

    # Add import observations as supplementary notes
    for note in profile.get("import_communication_notes", []):
        lines.append(f"- _{note}_")
    for note in profile.get("import_tone_notes", []):
        lines.append(f"- _{note}_")

    if not (profile["communication_style"] or profile["tone"]):
        lines.append("- Be concise when needed, thorough when it matters.")
        lines.append("- No corporate speak, no sycophancy.")

    lines.append("")

    # Personality
    if profile["personality_traits"]:
        lines.extend(["## My Personality", ""])
        for trait in profile["personality_traits"]:
            lines.append(f"- {trait}")
        lines.append("")

    # Boundaries — these are critical
    lines.extend(["## Hard Rules", ""])
    if profile["boundaries"]:
        for boundary in profile["boundaries"]:
            lines.append(f"- **{boundary}**")
    else:
        lines.append("- Private things stay private.")
        lines.append("- Ask before acting externally (emails, tweets, public posts).")
        lines.append("- When in doubt, ask.")
    lines.append("")

    # Continuity
    lines.extend([
        "## Continuity",
        "",
        "I wake up fresh each session. My memory files are how I persist.",
        "I read them, update them, and treat them like my actual brain.",
        "",
        "---",
        "",
        "_This file defines who I am. If I change it, I tell my human._",
    ])

    return "\n".join(lines)


def generate_memory_seed(profile, imports):
    """Generate initial MEMORY.md — only meaningful info, no noise."""
    lines = [
        "# MEMORY.md — Long-Term Memory",
        "",
        f"_Initialized by Soulsync on {datetime.now(timezone.utc).strftime('%Y-%m-%d')}_",
        "",
        "## About My Human",
        "",
    ]

    if profile["name"]:
        pn = f" ({profile['preferred_name']})" if profile["preferred_name"] else ""
        lines.append(f"- Name: {profile['name']}{pn}")
    if profile["work"]:
        lines.append(f"- Work: {profile['work']}")
    if profile["interests"]:
        lines.append(f"- Interests: {', '.join(profile['interests'][:8])}")
    if profile["schedule_patterns"]:
        lines.append(f"- Schedule: {profile['schedule_patterns']}")
    if profile["goals"]:
        lines.append("")
        lines.append("## Goals")
        lines.append("")
        for goal in profile["goals"]:
            lines.append(f"- {goal}")

    if profile["key_contacts"]:
        lines.append("")
        lines.append("## Key People")
        lines.append("")
        for contact in profile["key_contacts"][:10]:
            lines.append(f"- {contact}")

    lines.extend([
        "",
        "## Lessons Learned",
        "",
        "_Will be updated as we work together._",
        "",
        "## Preferences Discovered",
        "",
        "_Will be filled in over time._",
    ])

    return "\n".join(lines)


def synthesize():
    """Main synthesis pipeline."""
    imports = load_imports()
    conversation = load_conversation_notes()
    profile = merge_insights(imports, conversation)

    result = {
        "profile": profile,
        "files": {
            "USER.md": generate_user_md(profile),
            "SOUL.md": generate_soul_md(profile),
            "MEMORY.md": generate_memory_seed(profile, imports),
        },
        "sources": list(imports.keys()) + (["conversation"] if conversation else []),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    return result


if __name__ == "__main__":
    result = synthesize()

    if "--write" in sys.argv:
        for filename, content in result["files"].items():
            path = os.path.join(WORKSPACE, filename)
            with open(path, "w") as f:
                f.write(content)
            print(f"Wrote {path}")
    else:
        print(json.dumps(result, indent=2))
