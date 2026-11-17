---
name: smart-followups
version: 2.2.0
description: Generate contextual follow-up suggestions after AI responses. Offers three next questions (Quick, Deep Dive, Related) when the user runs /smart-followups or asks for suggestions.
metadata:
  openclaw:
    requires:
      bins: ["node"]
    note: "No API keys needed. The slash command is /smart-followups, derived from the skill name."
---

# Smart Follow-ups Skill

Generate contextual follow-up suggestions for OpenClaw conversations.

## Slash Command

The command name is derived from the skill's `name` field:

```
/smart-followups
```

OpenClaw 2.0 registers no aliases (`/fu`, `/suggestions`, and `/next` do not work), and separate `commands:`, `triggers:`, or `channels:` frontmatter fields are ignored.

When you run `/smart-followups`, the skill generates 3 contextual follow-up questions based on the conversation:

1. ⚡ **Quick** — Clarification or immediate next step
2. 🧠 **Deep Dive** — Technical depth or detailed exploration
3. 🔗 **Related** — Connected topic or broader context

---

## How to Trigger

| Method | Example |
|--------|---------|
| Slash command | `/smart-followups` |
| Natural language | "give me suggestions" |
| After any answer | "what should I ask next?" |

## Usage

Say "followups" in any conversation:

```
You: What is Docker?
Bot: Docker is a containerization platform...

You: /smart-followups

Bot: 💡 What would you like to explore next?
[⚡ How do I install Docker?]
[🧠 Explain container architecture]
[🔗 Docker vs Kubernetes?]
```

The skill produces the 3 suggestions. How they are rendered depends on the channel: the agent can show buttons only on channels that support interactive buttons, and only if it builds them there. Otherwise it posts a numbered text list — reply with 1, 2, or 3.

## Categories

Each generation produces 3 suggestions:

| Category | Emoji | Purpose |
|----------|-------|---------|
| **Quick** | ⚡ | Clarifications, definitions, immediate next steps |
| **Deep Dive** | 🧠 | Technical depth, advanced concepts, thorough exploration |
| **Related** | 🔗 | Connected topics, broader context, alternatives |

## Authentication

**Default:** Uses OpenClaw's existing auth — same login and model as your current chat.

**Optional providers:**
- `openrouter` — Requires `OPENROUTER_API_KEY`
- `anthropic` — Requires `ANTHROPIC_API_KEY`

## Configuration

```json
{
  "skills": {
    "entries": {
      "smart-followups": {
        "enabled": true,
        "provider": "openclaw",
        "model": null
      }
    }
  }
}
```

| Option | Default | Description |
|--------|---------|-------------|
| `provider` | `"openclaw"` | Auth provider: `openclaw`, `openrouter`, `anthropic` |
| `model` | `null` | Model override (null = inherit from session) |
| `apiKey` | — | API key for non-openclaw providers |

## Channel Support

The skill generates the suggestions; the agent decides how to render them within each channel's capabilities.

| Channel | Rendering |
|---------|-----------|
| Telegram | Buttons possible (agent-built) |
| Discord | Buttons possible (agent-built) |
| Slack | Buttons possible (agent-built) |
| Signal | Numbered text |
| WhatsApp | Numbered text |
| iMessage | Numbered text |
| SMS | Numbered text |
| Matrix | Numbered text |
| Email | Numbered text |

See [CHANNELS.md](CHANNELS.md) for detailed channel documentation.

## How It Works

1. User runs `/smart-followups`
2. The agent gathers recent conversation context (OpenClaw does not load `handler.js`; skills are instruction packs)
3. The agent generates 3 contextual questions (using the current model/auth)
4. The agent renders them as buttons or as a numbered text list, depending on what the channel supports
5. User taps a button or replies with a number
6. OpenClaw answers that question

## Files

| File | Purpose |
|------|---------|
| `handler.js` | Formatting helper; OpenClaw does not load it as a command handler |
| `cli/followups-cli.js` | Standalone CLI for testing/scripting |
| `README.md` | Full documentation |
| `CHANNELS.md` | Channel-specific guide |
| `FAQ.md` | Common questions |

## Credits

Inspired by [Chameleon AI Chat](https://github.com/robbyczgw-cla/Chameleon-AI-Chat)'s smart follow-up feature.
