# Synapse — Self-Learning Memory Engine

Augments OpenClaw's built-in memory system (`memory_search`/`memory_get`) with structured learning, preference tracking, and cross-session intelligence.

## Installation

```bash
# Via ClawHub
clawhub install shadoprizm/synapse

# Or manually
cp -r synapse ~/.openclaw/skills/
```

## How It Works

Synapse sits on top of OpenClaw's existing memory tools. It doesn't replace them — it adds structure:

- **Profile tracking** — structured JSON profile with facts, preferences, patterns
- **Preference extraction** — detects explicit and implicit preferences from conversations
- **Pattern detection** — identifies behavioral trends over time
- **Daily learning cycles** — consolidates learnings from each day
- **Cross-session memory** — maintains context across conversations

## Files

- `SKILL.md` — Skill definition and workflow
- `skill.json` — Metadata
- `references/` — Additional documentation

## Author

shadoprizm / Astra Web Dev (North Star Holdings)
