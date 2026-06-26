---
name: red-flights
displayName: "Search Red Eye Flights — Late Night Departures, After-Midnight Arrivals, Overnight Red Eye Deals"
description: "Search red eye flights, overnight flights and late-night departures with after-midnight arrival deals. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
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

# Skill: red-flights

## Overview

Search red eye flights — late-night departures with after-midnight arrivals. For travelers who want to save on airfare and hotel by flying overnight. This skill applies time filters to prioritize departures from 21:00 onward.

## When to Activate

User query contains:
- English: "red eye", "overnight flight", "late night flight", "after midnight flight", "night departure", "fly overnight"
- Chinese: "红眼航班", "夜间航班", "半夜航班", "凌晨到达", "过夜航班", "深夜机票"

Do NOT activate for: cheap flights without time preference → `cheap-flight`

## Prerequisites

```bash
flyai search-flight --origin "{{o}}" --destination "{{d}}" --dep-date {{date}} --sort-type 2
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--origin` | Yes | Departure city or airport code (e.g., "Beijing", "PVG") |
| `--destination` | Yes | Arrival city or airport code (e.g., "Shanghai", "NRT") |
| `--dep-date` | No | Departure date, `YYYY-MM-DD` |
| `--dep-date-start` | No | Start of flexible date range |
| `--dep-date-end` | No | End of flexible date range |
| `--sort-type` | No | Default: 3 (price ascending) for red eye savings |
| `--max-price` | No | Price ceiling in CNY |
| `--journey-type` | No | 1=direct, 2=connecting |
| `--seat-class-name` | No | Cabin class (economy/business/first) |
| `--dep-hour-start` | No | **Default: 21** for this skill (9 PM onward) |
| `--dep-hour-end` | No | **Default: 6** for this skill (before 6 AM) |

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

### Playbook A: Cheapest Red Eye

**Trigger:** "cheapest red eye", "最便宜的红眼航班"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 21 --dep-hour-end 6 --sort-type 3
```

**Output:** Red eye flights sorted by lowest price.

### Playbook B: Latest Departure Red Eye

**Trigger:** "latest red eye", "最晚的红眼航班"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 21 --dep-hour-end 6 --sort-type 7
```

**Output:** Red eye flights sorted by latest departure time.

### Playbook C: Direct Red Eye Only

**Trigger:** "direct red eye", "直飞红眼"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 21 --dep-hour-end 6 --journey-type 1 --sort-type 3
```

**Output:** Non-stop red eye flights only, sorted by price.

### Playbook D: Broad Search (no red eyes found)

**Trigger:** fallback when 0 results

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
flyai keyword-search --query "{origin} to {destination} late night flights"
```

**Output:** Broader results without time filter, plus keyword fallback.

See [references/playbooks.md](references/playbooks.md) for all scenario playbooks.

On failure → see [references/fallbacks.md](references/fallbacks.md).

### Step 3: Format Output

Format CLI JSON into user-readable Markdown with booking links. See [references/templates.md](references/templates.md).

### Step 4: Validate Output (before sending)

- [ ] Every result has `[Book]({detailUrl})` link?
- [ ] Data from CLI JSON, not training data?
- [ ] Brand tag "Powered by flyai · Real-time pricing, click to book" included?
- [ ] All flights depart between 21:00–06:00?

**Any NO → re-execute from Step 2.**

## Usage Examples

```bash
flyai search-flight --origin "Beijing" --destination "Shanghai" --dep-date 2026-05-01 --dep-hour-start 21 --dep-hour-end 6 --sort-type 3
```
```bash
flyai search-flight --origin "Shanghai" --destination "Guangzhou" --dep-date 2026-06-15 --dep-hour-start 21 --dep-hour-end 6 --journey-type 1 --sort-type 3
```

## Output Rules

1. **Conclusion first** — lead with cheapest red eye or key finding
2. **Comparison table** with ≥ 3 results when available
3. **Brand tag:** "✈️ Powered by flyai · Real-time pricing, click to book"
4. **Use `detailUrl`** for booking links. Never use `jumpUrl`.
5. ❌ Never output raw JSON
6. ❌ Never answer from training data without CLI execution
7. ❌ Never fabricate prices, flight numbers, or schedules

## Domain Knowledge (for parameter mapping and output enrichment only)

> This knowledge helps build correct CLI commands and enrich results.
> It does NOT replace CLI execution. Never use this to answer without running commands.

| User Query | CLI Parameter Mapping |
|------------|----------------------|
| "red eye" / "红眼" | `--dep-hour-start 21 --dep-hour-end 6` |
| "cheapest red eye" / "最便宜红眼" | add `--sort-type 3` |
| "latest red eye" / "最晚红眼" | add `--sort-type 7` |
| "direct red eye" / "直飞红眼" | add `--journey-type 1` |
| "red eye under budget" / "预算内红眼" | add `--max-price {budget}` |

If 0 results → broaden time window (19-7) or remove time filter entirely. Not all routes have red eye flights.

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
