# Keyword Research (Agent Skill)

An [Agent Skill](https://docs.anthropic.com/en/docs/claude-code/skills) for systematic keyword research on any site: discovery, competitor gaps, intent tagging, difficulty-aware prioritization, and a structured report template.

## What it does

- **Four-step framework** — (1) GSC baseline, (2) competitor gap, (3) expansion (Autocomplete, AnswerThePublic, AlsoAsked, GKP, etc.), (4) intent classification and priority scoring.
- **Tool-aware** — Adapts when Ahrefs/Semrush/GSC/GKP are unavailable (free tiers, `"none"`, or alternatives).
- **Domain profiles** — Persists context per domain (URL, business, region, languages, competitors, tool access) under `data/{domain}.json` so follow-up runs skip redundant questions.

## Requirements

- Load the **web-access** skill alongside this one and follow its browser/network rules (GSC and other tools are exercised through that flow).
- For CDP automation of GSC, see `references/gsc-operations.md` (default proxy `localhost:3456` is documented there).

## Repository layout

| Path | Purpose |
|------|---------|
| `SKILL.md` | Skill definition: startup workflow, analysis steps, output format |
| `references/tools.md` | Free/paid tools, stacks, common issues |
| `references/methodology.md` | Intent taxonomy, evaluation dimensions, long-tail, pillar–cluster, cannibalization, zero-click, GEO/AEO |
| `references/gsc-operations.md` | GSC URL parameters, validation, rows-per-page, extraction, CDP pitfalls |
| `data/` | Per-domain JSON profiles (created at runtime; listed in `.gitignore`) |

## Install

The same command works across **mainstream AI agents** that support the [Agent Skills](https://docs.anthropic.com/en/docs/claude-code/skills) layout (e.g. Claude Code, Cursor, and other clients that load `SKILL.md` from a skills directory).

```bash
npx skills add https://github.com/meikidd/keyword-research
```

Domain profiles are written under the skill’s `data/` folder at runtime; agents create it with `mkdir -p` if it does not exist yet.

