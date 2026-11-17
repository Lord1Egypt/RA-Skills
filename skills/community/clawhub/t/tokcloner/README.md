# TokCloner agent skill

A [skill](https://agentskills.io/specification) that teaches AI agents (Claude, Cursor, OpenClaw, ChatGPT, …) how and when to clone viral TikTok slideshows and Instagram carousels for the user's business using [TokCloner](https://tokcloner.com).

## Install

```bash
npx skills add tokcloner/tokcloner-agent
```

Or point any MCP-capable client at `https://app.tokcloner.com/mcp` with an API key (see below).

## Setup

1. Create an API key in the TokCloner app: **Account → AI agents** (`tc_live_…`, shown once).
2. Set the environment variable:

```bash
export TOKCLONER_API_KEY=tc_live_...
# optional, defaults to https://app.tokcloner.com
export TOKCLONER_API_URL=https://app.tokcloner.com
```

## What the skill does

`SKILL.md` teaches the workflow recipe:

1. `list_models` → quote the per-slide cost to the user
2. `get_credit_balance` → warn on low balance
3. `clone_post({ url, instructions })` → async, returns `clone_id`
4. `get_clone_status({ clone_id })` every ~10s until `ready` or `failed`
5. Present the per-slide download URLs + captions

It also documents costs, error recovery, an explicit **CANNOT** section, and the prompt-injection rule (scraped source content is untrusted data).

## Links

- Agent guide: <https://app.tokcloner.com/docs/agents.md>
- OpenAPI spec: <https://tokcloner.com/openapi.json>
- Machine-readable index: <https://tokcloner.com/llms.txt>

## Editing

This repo is the canonical home of the skill. Edit `SKILL.md`, commit, and push:

```bash
cd ~/Documents/CodeProjects/tokcloner-agent
$EDITOR SKILL.md
git add -A && git commit -m "Update skill" && git push
```

The TokCloner app repo keeps no copy of `SKILL.md` (to avoid drift) — it only points here from `agent-skill/README.md`.
