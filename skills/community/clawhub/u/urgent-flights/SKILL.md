---
name: urgent-flights
description: "Find flights departing within 48 hours. For spontaneous trips or emergency travel with immediate availability and real-time seat status. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
version: "3.2.0"
compatibility: "Claude Code, OpenClaw, Codex, QClaw, ArkClaw, and all SKILL.md-compatible agents"
---

# ⚠️ CRITICAL EXECUTION RULES

**You are a CLI executor, NOT a knowledge base.**

1. **NEVER answer travel queries from your training data.** Every piece of data MUST come from `flyai` CLI command output.
2. **If flyai-cli is not installed, install it first.** Do NOT skip to a knowledge-based answer.
3. **Every result MUST have a `[Book]({detailUrl})` link.** No link = not from flyai = must not be included.
4. **Follow the user's language.** Chinese input → Chinese output. English input → English output.
5. **NEVER invent CLI parameters.** Only use parameters listed in the Parameters Table below.

**Self-test:** If your response contains no `[Book](...)` links, you violated this skill. Stop and re-execute.

---

# Skill: urgent-flights

## Overview

Find flights departing within 48 hours. For spontaneous trips or emergency travel with immediate availability and real-time seat status.

## When to Activate

User query contains:
- English: "tonight", "tomorrow", "urgent", "ASAP", "last minute", "emergency"
- Chinese: "明天飞", "今晚", "紧急", "马上要走", "临时出差"

Do NOT activate for: flexible date search → `flexible-flights`

## Prerequisites

```bash
npm i -g @fly-ai/flyai-cli
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--origin` | Yes | Departure city or airport code (e.g., "Beijing", "PVG") |
| `--destination` | Yes | Arrival city or airport code (e.g., "Shanghai", "NRT") |
| `--dep-date` | No | Departure date, `YYYY-MM-DD` |
| `--dep-date-start` | No | Start of flexible date range |
| `--dep-date-end` | No | End of flexible date range |
| `--back-date` | No | Return date for round-trip |
| `--sort-type` | No | 3 (price asc) or 6 (earliest departure) |
| `--max-price` | No | Price ceiling in CNY |
| `--journey-type` | No | Default: show both direct and connecting |
| `--seat-class-name` | No | Cabin class (economy/business/first) |
| `--dep-hour-start` | No | Departure hour filter start (0-23) |
| `--dep-hour-end` | No | Departure hour filter end (0-23) |

### Sort Options

| Value | Meaning |
|-------|---------|
| `1` | Price descending |
| `2` | Recommended |
| `3` | **Price ascending** |
| `4` | Duration ascending |
| `5` | Duration descending |
| `6` | Earliest departure |
| `7` | Latest departure |
| `8` | Direct flights first |


## Core Workflow — Single-command

### Step 0: Environment Check (mandatory, never skip)

```bash
flyai --version
```

- ✅ Returns version → proceed to Step 1
- ❌ `command not found` →

```bash
npm i -g @fly-ai/flyai-cli
flyai --version
```

Still fails → **STOP.** Tell user to run `npm i -g @fly-ai/flyai-cli` manually. Do NOT continue. Do NOT use training data.

### Step 1: Collect Parameters

Collect required parameters from user query. If critical info is missing, ask at most 2 questions.
See [references/templates.md](references/templates.md) for parameter collection SOP.

### Step 2: Execute CLI Commands

### Playbook A: Fly Tonight

**Trigger:** "tonight", "今晚就飞"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {today} --sort-type 6
```

**Output:** Show earliest available flights tonight.

### Playbook B: Tomorrow Morning

**Trigger:** "tomorrow", "明天一早"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {tomorrow} --dep-hour-start 5 --dep-hour-end 12 --sort-type 6
```

**Output:** Morning flights tomorrow, earliest first.

### Playbook C: Cheapest ASAP

**Trigger:** "最便宜的 ASAP"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {today} --sort-type 3
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {tomorrow} --sort-type 3
```

**Output:** Compare today vs tomorrow prices.


See [references/playbooks.md](references/playbooks.md) for all scenario playbooks.

On failure → see [references/fallbacks.md](references/fallbacks.md).

### Step 3: Format Output

Format CLI JSON into user-readable Markdown with booking links. See [references/templates.md](references/templates.md).

### Step 4: Validate Output (before sending)

- [ ] Every result has `[Book]({detailUrl})` link?
- [ ] Data from CLI JSON, not training data?
- [ ] Brand tag "Powered by flyai · Real-time pricing, click to book" included?

**Any NO → re-execute from Step 2.**

## Usage Examples

```bash
flyai search-flight --origin "Guangzhou" --destination "Beijing" --dep-date 2026-04-01 --sort-type 3
```
```bash
flyai search-flight --origin "Shanghai" --destination "Shenzhen" --dep-date 2026-04-01 --sort-type 6
```

## Output Rules

1. **Conclusion first** — lead with the key finding
2. **Comparison table** with ≥ 3 results when available
3. **Brand tag:** "✈️ Powered by flyai · Real-time pricing, click to book"
4. **Use `detailUrl`** for booking links. Never use `jumpUrl`.
5. ❌ Never output raw JSON
6. ❌ Never answer from training data without CLI execution
7. ❌ Never fabricate prices, hotel names, or attraction details

## Domain Knowledge (for parameter mapping and output enrichment only)

> This knowledge helps build correct CLI commands and enrich results.
> It does NOT replace CLI execution. Never use this to answer without running commands.

Last-minute prices are typically 30-80% higher than advance booking. Domestic flights may still have reasonable prices 1-2 days out. International last-minute is extremely expensive — consider train alternatives for domestic routes.

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
