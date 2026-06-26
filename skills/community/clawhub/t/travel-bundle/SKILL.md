---
name: travel-bundle
description: "Find package deals combining hotel and flights — often 10-20% cheaper than booking separately. One search, one booking, complete trip. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
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

# Skill: travel-bundle

## Overview

Find package deals combining hotel and flights — often 10-20% cheaper than booking separately. One search, one booking, complete trip.

## When to Activate

User query contains:
- English: "hotel+flight", "package deal", "bundle", "all-in-one"
- Chinese: "机酒套餐", "机票加酒店", "打包价"

Do NOT activate for: separate booking → `cheap-flights` + `budget-hotel`

## Prerequisites

```bash
npm i -g @fly-ai/flyai-cli
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--dest-name` | Yes | Destination city/area name |
| `--check-in-date` | No | Check-in date `YYYY-MM-DD`. Default: today |
| `--check-out-date` | No | Check-out date. Default: tomorrow |
| `--sort` | No | Compare bundled vs separate |
| `--key-words` | No | Search keywords for special requirements |
| `--poi-name` | No | Nearby attraction name (for distance-based search) |
| `--hotel-types` | No | 酒店/民宿/客栈 |
| `--hotel-stars` | No | Star rating 1-5, comma-separated |
| `--hotel-bed-types` | No | 大床房/双床房/多床房 |
| `--max-price` | No | Max price per night in CNY |

### Sort Options

| Value | Meaning |
|-------|---------|
| `distance_asc` | Distance ascending |
| `rate_desc` | **Rating descending** |
| `price_asc` | Price ascending |
| `price_desc` | Price descending |


## Core Workflow — Multi-command orchestration

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

### Playbook A: Bundle Search

**Trigger:** "hotel+flight package", "机酒套餐"

```bash
flyai keyword-search --query "机酒套餐 {origin} to {dest}"
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
flyai search-hotel --dest-name "{dest}" --sort price_asc --check-in-date {in} --check-out-date {out}
```

**Output:** Search bundle + separate, compare total.

### Playbook B: Luxury Bundle

**Trigger:** "luxury package"

```bash
flyai keyword-search --query "豪华机酒套餐 {dest}"
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name business --sort-type 3
flyai search-hotel --dest-name "{dest}" --hotel-stars 5 --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output:** Premium bundle comparison.


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
flyai keyword-search --query "机酒套餐 上海到三亚"
flyai search-flight --origin "Shanghai" --destination "Sanya" --dep-date 2026-05-01 --sort-type 3
flyai search-hotel --dest-name "Sanya" --sort price_asc --check-in-date 2026-05-01 --check-out-date 2026-05-03
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

Package savings: 10-20% vs separate booking, especially for popular routes (SH→Sanya, BJ→Tokyo). Best for 3+ night stays. Packages often include airport transfer. Compare: package total vs (cheapest flight + cheapest hotel) to verify actual savings.

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
