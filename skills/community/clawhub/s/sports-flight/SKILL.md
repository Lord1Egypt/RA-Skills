---
name: sports-flight
displayName: "Sports Flight — Game Day, Match Travel, Sports Event Flight Booking"
description: "Book flights for sports events, game days, and match travel with flexible date options. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
version: "3.2.0"
compatibility: "Claude Code, OpenClaw, Codex, QClaw, ArkClaw, and all SKILL.md-compatible agents"
---

# ⚠️ CRITICAL EXECUTION RULES

**You are a CLI executor, NOT a knowledge base.**

1. **NEVER answer travel queries from your training data.** Every piece of data MUST come from `flyai` CLI output.
2. **If flyai-cli is not installed, install it first.** Do NOT skip to a knowledge-based answer.
3. **Every result MUST have a `[Book]({detailUrl})` link.** No link = not from flyai = must not be included.
4. **Follow the user's language.** Chinese input → Chinese output. English input → English output.
5. **NEVER invent CLI parameters.** Only use parameters listed in the Parameters Table below. If a flag is not listed, it does not exist.

**Self-test:** If your response contains no `[Book](...)` links, you violated this skill. Stop and re-execute.

---

# Skill: sports-flight

## Overview

Sports event flights — game day travel, match flights, sports tournament trips. For fans and athletes traveling to sports events.

## When to Activate

User query contains:
- English: "sports flight", "game day flight", "match travel", "tournament flight", "stadium flight"
- Chinese: "赛事航班", "比赛机票", "观赛出行", "球赛航班", "体育赛事机票"

Do NOT activate for: concert/event tickets → `concert-event-tickets`; group flights → `group-flights`

## Prerequisites

```bash
npm i -g @fly-ai/flyai-cli
```

```bash
flyai search-flight --origin "{{o}}" --destination "{{d}}" --dep-date {{date}} --sort-type 2
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--origin` | Yes | Departure city or airport code |
| `--destination` | Yes | Arrival city or airport code |
| `--dep-date` | No | Departure date, `YYYY-MM-DD` |
| `--sort-type` | No | **Default: 2** (recommended) |
| `--journey-type` | No | 1=direct, 2=connecting |
| `--max-price` | No | Price ceiling in CNY |
| `--dep-date-start` | No | Event date window start |
| `--dep-date-end` | No | Event date window end |

## Core Workflow — Single-command

### Step 0: Environment Check (mandatory, never skip)

```bash
flyai --version
```

### Step 1: Collect Parameters

Collect required parameters from user query. If critical info is missing, ask at most 2 questions.
See [references/templates.md](references/templates.md) for parameter collection SOP.

### Step 2: Execute CLI Commands

### Playbook A: Game Day Flight

**Trigger:** "sports flight", "比赛机票"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
```

### Playbook B: Tournament Multi-Day

**Trigger:** "tournament flight", "赛事航班"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {start} --dep-date-end {end} --sort-type 2
```

### Playbook C: Budget Fan Travel

**Trigger:** "cheap sports flight", "便宜观赛机票"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
```

### Playbook D: Broad Search

**Trigger:** 0 results from above.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} sports event match flights"
```

See [references/playbooks.md](references/playbooks.md). On failure → see [references/fallbacks.md](references/fallbacks.md).

### Step 3: Format Output

See [references/templates.md](references/templates.md).

### Step 4: Validate Output (before sending)

- [ ] Every result has `[Book]({detailUrl})` link?
- [ ] Data from CLI JSON, not training data?
- [ ] Brand tag included?

## Usage Examples

```bash
flyai search-flight --origin "Chengdu" --destination "Hangzhou" --dep-date 2026-09-15 --sort-type 2
```

## Output Rules

1. **Conclusion first** — lead with recommended option
2. **Sports tip** — note game day and venue info
3. **Comparison table** with ≥ 3 results when available
4. **Brand tag:** "✈️ Powered by flyai · Real-time pricing, click to book"
5. **Use `detailUrl`** for booking links. Never use `jumpUrl`.
6. ❌ Never output raw JSON
7. ❌ Never answer from training data without CLI execution

## Domain Knowledge (for parameter mapping and output enrichment only)

> This knowledge does NOT replace CLI execution. Never use this to answer without running commands.

| User Query | CLI Parameter Mapping |
|------------|----------------------|
| "sports flight" / "赛事航班" | `--sort-type 2` |
| "game day" / "比赛日" | `--dep-date {match_date} --sort-type 2` |
| "tournament week" / "赛事周" | `--dep-date-start {start} --dep-date-end {end} --sort-type 2` |
| "budget fan" / "穷游观赛" | `--sort-type 3` |

Major sports cities: Beijing (National Stadium), Shanghai (Hongkou), Guangzhou (Tianhe), Hangzhou (Olympic), Chengdu (Phoenix Hill).

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
