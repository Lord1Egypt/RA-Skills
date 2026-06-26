# x402geo-skill

GEO + SEO (Generative Engine Optimization) skill for running paid audits through `x402geo.com`, with support for a manual checkout flow or silent payment via an agentic wallet.

## What this skill does

- Creates a GEO/SEO audit request for a target website
- Handles **payment_required** (either returns a checkout URL to the user, or pays silently if an agentic wallet is available)
- Tracks job progress until completion
- Returns a concise summary and a public report link

The main instructions live in `SKILL.md`.

## Install

### Claude Code

Clone this repo and copy it into either:

- Personal skills: `~/.claude/skills/x402geo-skills/`
- Project skills: `.claude/skills/x402geo-skills/`

### OpenAI Codex CLI

Clone this repo and copy it into:

- `~/.codex/skills/x402geo-skills/`

## Repo structure

- `SKILL.md`: primary skill definition and audit/payment workflow
- `marketplace.json`: ecosystem metadata for skills directories/marketplaces
- `.claude-plugin/plugin.json`: Claude plugin metadata
- `agents/openai.yaml`: lightweight agent UI metadata

## Usage

In your agent/assistant, ask for a GEO/SEO audit of a URL. The skill will prompt for required inputs (`email`, `url`) and run the audit workflow.

## License

MIT (see `marketplace.json` / `.claude-plugin/plugin.json`).

