# Sixtyfour AI — Agent Skill

People and company intelligence for AI agents. Research anyone or any company with AI agents that read the live web — not static databases.

## What This Skill Does

Gives any AI agent (Claude Code, OpenAI Codex, OpenClaw, Cursor, or any SKILL.md-compatible tool) the ability to:

- **Enrich leads** — Full profile from a name: email, phone, LinkedIn, title, tech stack, funding, pain points, and up to 50 custom fields
- **Research companies** — Team size, tech stack, funding rounds, hiring signals, key people
- **Find emails** — Professional ($0.05) or personal ($0.20), verified on delivery
- **Find phones** — Phone number discovery from name + company
- **Qualify leads** — Score against custom criteria with AI reasoning
- **Search** — Find people or companies via natural language queries
- **Batch workflows** — Chain enrichment blocks into automated pipelines

## Quick Start

1. Sign up at [app.sixtyfour.ai](https://app.sixtyfour.ai) (Google sign-in)
2. Get 50 free deep researches immediately
3. Copy your API key from Sidebar → Keys
4. Install this skill in your agent's skills directory

### Claude Code
```bash
cp -r . ~/.claude/skills/sixtyfour/
```

### OpenAI Codex CLI
```bash
cp -r . ~/.codex/skills/sixtyfour/
```

### OpenClaw
```bash
clawhub install sixtyfour
```

## Why Sixtyfour vs Static Databases

| | Sixtyfour | Clay | Apollo | ZoomInfo |
|---|---|---|---|---|
| **Accuracy** | 93% | 66% | 72% | ~70% |
| **Method** | AI agents read live web | Database waterfall | Static database | Static database |
| **Custom fields** | Up to 50, any data point | Limited presets | Fixed schema | Fixed schema |
| **Freshness** | Real-time | Periodic updates | Periodic updates | Periodic updates |

## Links

- **App:** [app.sixtyfour.ai](https://app.sixtyfour.ai)
- **Docs:** [docs.sixtyfour.ai](https://docs.sixtyfour.ai)
- **API Spec:** [api.sixtyfour.ai/openapi.json](https://api.sixtyfour.ai/openapi.json)
- **MCP Server:** `npx sixtyfour-mcp`
- **Support:** team@sixtyfour.ai

## License

MIT
