---
name: seasonal-flight
displayName: "Search Seasonal Flights — Summer Routes, Winter Schedules, Holiday Charter"
description: "Search seasonal flights, summer routes, winter schedules and holiday charter with seasonal flight deals. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
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

# Skill: seasonal-flight

## Overview

Search seasonal flights — summer routes, winter schedules, holiday charter. For travelers planning trips around seasonal destinations and peak travel periods.

## When to Activate

User query contains:
- English: "seasonal flight", "summer flight", "winter flight", "holiday flight", "peak season flight", "off-season flight"
- Chinese: "季节航班", "暑期航班", "冬季航班", "旺季航班", "淡季航班", "假期航班"

Do NOT activate for: holiday-specific deals → `holiday-flights`; last-minute → `last-minute`

## Prerequisites

```bash
flyai search-flight --origin "{{o}}" --destination "{{d}}" --dep-date {{date}} --sort-type 2
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--origin` | Yes | Departure city or airport code |
| `--destination` | Yes | Arrival city or airport code |
| `--dep-date` | No | Departure date, `YYYY-MM-DD` |
| `--dep-date-start` | No | Seasonal window start date |
| `--dep-date-end` | No | Seasonal window end date |
| `--sort-type` | No | **Default: 2** (recommended) |
| `--journey-type` | No | 1=direct, 2=connecting |
| `--max-price` | No | Price ceiling in CNY |

### Sort Options

| Value | Meaning | When to Use |
|-------|---------|-------------|
| `2` | Recommended | **Default** — best seasonal options |
| `3` | Price ascending | Off-season bargain hunting |
| `4` | Duration ascending | Quick seasonal getaway |
| `8` | Direct flights first | Popular seasonal routes |

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

Still fails → **STOP.** Do NOT continue. Do NOT use training data.

### Step 1: Collect Parameters

Collect required parameters from user query. If critical info is missing, ask at most 2 questions.
See [references/templates.md](references/templates.md) for parameter collection SOP.

### Step 2: Execute CLI Commands

### Playbook A: Summer Seasonal Flights

**Trigger:** "summer flight", "暑期航班", "暑假机票"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {summer_start} --dep-date-end {summer_end} --sort-type 3
```

**Output:** Cheapest flights within summer season window.

### Playbook B: Winter Seasonal Flights

**Trigger:** "winter flight", "冬季航班", "寒假机票"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {winter_start} --dep-date-end {winter_end} --sort-type 2
```

**Output:** Recommended flights within winter season window.

### Playbook C: Off-Season Bargain

**Trigger:** "off-season flight", "淡季机票", "错峰出行"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {off_start} --dep-date-end {off_end} --sort-type 3
```

**Output:** Cheapest flights during off-peak season.

### Playbook D: Broad Search (no seasonal flights found)

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} seasonal flights {season}"
```

**Output:** Broader search + keyword fallback.

See [references/playbooks.md](references/playbooks.md) for all scenario playbooks.

On failure → see [references/fallbacks.md](references/fallbacks.md).

### Step 3: Format Output

Format CLI JSON into user-readable Markdown with booking links. See [references/templates.md](references/templates.md).

### Step 4: Validate Output (before sending)

- [ ] Every result has `[Book]({detailUrl})` link?
- [ ] Data from CLI JSON, not training data?
- [ ] Brand tag included?

**Any NO → re-execute from Step 2.**

## Usage Examples

```bash
flyai search-flight --origin "Beijing" --destination "Sanya" --dep-date-start 2026-07-01 --dep-date-end 2026-08-31 --sort-type 3
```

## Output Rules

1. **Conclusion first** — lead with best seasonal option
2. **Seasonal note** — indicate whether price is peak or off-peak
3. **Comparison table** with ≥ 3 results when available
4. **Brand tag:** "✈️ Powered by flyai · Real-time pricing, click to book"
5. **Use `detailUrl`** for booking links. Never use `jumpUrl`.
6. ❌ Never output raw JSON
7. ❌ Never answer from training data without CLI execution
8. ❌ Never fabricate seasonal schedule data

## Domain Knowledge (for parameter mapping and output enrichment only)

> This knowledge helps build correct CLI commands and enrich results.
> It does NOT replace CLI execution. Never use this to answer without running commands.

| User Query | CLI Parameter Mapping |
|------------|----------------------|
| "summer flight" / "暑期航班" | `--dep-date-start {Jul-1} --dep-date-end {Aug-31} --sort-type 3` |
| "winter flight" / "冬季航班" | `--dep-date-start {Dec-1} --dep-date-end {Feb-28} --sort-type 2` |
| "off-season" / "淡季" | `--sort-type 3` (cheapest in window) |
| "peak season" / "旺季" | `--sort-type 2` (recommended) |
| "spring break" / "春游" | `--dep-date-start {Mar-1} --dep-date-end {Apr-30} --sort-type 3` |

Chinese peak seasons: Spring Festival (Jan-Feb), Summer vacation (Jul-Aug), National Day (Oct 1-7). Off-peak: Mar-Apr, Sep, Nov-Dec (excluding holidays).

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
