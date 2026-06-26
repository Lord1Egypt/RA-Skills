# SEOwlsClaw — SEO Plan Workflow
# File: SEO_PLANS/plan_workflow.md
# Loaded by: BRAIN_ARCHITECTURE.md Step 2e — ONLY when /seoplan command is active
# Purpose: Full processing logic for the /seoplan brain pipeline (Steps A–G)

---

## When This File Is Loaded

This file is loaded ONLY when the `/seoplan` command is issued.
It is NEVER loaded during `/write`, `/writehtml`, `/seobrief`, `/research`, or `/checks`.
This keeps the standard content generation brain lean and fast.

---

## /seoplan Brain Pipeline — Overview

`/seoplan` replaces Steps 3–7 of the standard brain workflow.
Once Step 2e confirms this is a `/seoplan` command, execute Steps A–G below in order.

```
seoplan-Step A    Niche + Market Research
seoplan-Step B    Cluster Architecture Design
seoplan-Step C    Node Tiering + Priority Assignment
seoplan-Step D    Internal Link Matrix
seoplan-Step E    Execution Order
seoplan-Step F    Plan Quality Check
seoplan-Step G    Output + Save
```

---

## seoplan-Step A — Niche + Market Research

**Input:** `niche_prompt`, `plan_lang`, `plan_brand`, `plan_mode`

**Actions:**

1. Run keyword research for the niche (equivalent to `/research` internally):
   - Identify 3–5 primary keyword families in the niche
   - For each family: estimate volume + difficulty
   - Detect dominant SERP features (comparison tables, PAA-heavy, image packs, shopping results)
   - Identify top 3–5 competitor domains in the niche

2. Identify niche characteristics:
   - Commercial niche (product sales) vs. informational (publishing)?
   - Average difficulty range across the keyword families → sets the Quick Win threshold
   - Dominant content formats currently ranking → sets page type defaults for nodes

3. Calculate the Quick Win threshold for this specific niche:
   - Default threshold: Difficulty < 25
   - If niche average difficulty > 50 → lower threshold to Difficulty < 20
   - If niche average difficulty < 30 → raise threshold to Difficulty < 30

---

## seoplan-Step B — Cluster Architecture Design

**Input:** Research data from Step A

### Mode: cluster (default)

Build one cluster around the strongest primary keyword family:

1. **Pillar topic:** The highest-volume + commercial/commercial-investigation intent keyword in the niche
2. **Supporting nodes** generated from:
   - Long-tail variations of the pillar keyword (informational angles → FOUNDATION candidates)
   - Question-style queries from PAA data (→ FAQ candidates)
   - Commercial comparison queries (buyer intent → STRATEGIC candidates)
   - How-to and tutorial queries below the QW threshold (→ QUICKWIN candidates)
3. **Target node count by `--depth`:**
   - `--depth light` → 4–6 nodes total
   - `--depth standard` → 8–14 nodes total (default)
   - `--depth deep` → 15–25 nodes total
   - `--pages <n>` → exact override of depth (ignores --depth if both set)

### Mode: site

Build a full site architecture across multiple clusters:

1. Identify 3–5 major keyword families in the niche → one cluster per family
2. For each cluster: identify its pillar keyword + 3 example node topics (summary level only)
3. Output: cluster overview table — no deep node detail per node
4. Each cluster row ends with the drill-down command:
   `/seoplan "[cluster topic]" --mode cluster --lang [lang]`

---

## seoplan-Step C — Node Tiering + Priority Assignment

**Input:** All candidate nodes from Step B

Assign each node to a tier using these exact criteria:

### PILLAR
- Highest volume keyword in the cluster
- Commercial or commercial-investigation intent
- Difficulty may be high (40–70) — this is a long-term investment
- Always exactly **1 PILLAR** per cluster in `--mode cluster`
- Usually: Blogpost (comparison/buyer guide) or Landingpage

### QUICKWIN
- Difficulty: **below the niche threshold** calculated in Step A
- Clear search intent matching an executable page type
- SERP currently shows thin, outdated, or poorly structured content
- Can realistically rank within 4–8 weeks
- Usually: Blogpost (how-to, guide) or FAQ

### FOUNDATION
- Supports the pillar with informational depth
- Difficulty between the QW threshold and ~40
- Informational or educational intent
- Builds topical authority and supplies internal link anchors to the pillar
- Usually: Blogpost (guide/explainer) or FAQ

### STRATEGIC
- High volume AND high difficulty (difficulty > 40)
- High conversion value: transactional or strong commercial intent
- Requires internal link support from Pillar + Quick Wins before ranking realistically
- Long-term investment: 6–12 months to rank
- Usually: Blogpost (comparison), Productused, Landingpage

### Persona Assignment Per Tier

| Tier | Zone A Persona | Zone B Persona | Rationale |
|------|---------------|---------------|-----------|
| PILLAR | researcher | ecommerce-manager | Hub page: authority body + conversion CTA |
| QUICKWIN | blogger or researcher | none | Fast informational — no hard sell |
| FOUNDATION | blogger or vintage-expert | none | Deep educational — purely Zone A |
| STRATEGIC | researcher | ecommerce-manager | High-value: depth + conversion |
| FAQ | researcher | none | Factual Q&A — always Zone A |

**Brand override:** If an active brand profile (Step 2d) has a `default_persona` set,
use it for Zone A on FOUNDATION and FAQ nodes instead of the tier default.

---

## seoplan-Step D — Internal Link Matrix

**Input:** All tiered nodes from Step C

**Linking rules — enforce without exception:**

1. Every QUICKWIN node → links UP to PILLAR (outbound link to pillar)
2. Every FOUNDATION node → links UP to PILLAR
3. Every STRATEGIC node → links UP to PILLAR
4. PILLAR → links DOWN to ALL QUICKWIN + FOUNDATION + STRATEGIC nodes
5. QUICKWIN nodes may cross-link to thematically related FOUNDATION nodes
6. STRATEGIC nodes may cross-link to related QUICKWIN or FOUNDATION nodes
7. FAQ nodes → always link to PILLAR + most relevant FOUNDATION or STRATEGIC node
8. **No orphan nodes** — every node must have at least 1 inbound + 1 outbound link

**Matrix format:**
- Rows = "linking FROM" pages
- Columns = "linking TO" pages
- Mark with ✅ where a link should exist

---

## seoplan-Step E — Execution Order

**Input:** All tiered nodes + link matrix from Step D

Generate a numbered execution order following this priority logic:

### `--priority balanced` (default)
```
1. All QUICKWIN nodes  → ordered by ascending difficulty
2. FOUNDATION nodes    → ordered by ascending difficulty
3. PILLAR node         → after QW + FND nodes are indexed
4. STRATEGIC nodes     → ordered by: conversion value > volume > ascending difficulty
```

### `--priority quickwins`
- Output QUICKWIN nodes only in the plan body
- Add note at bottom: "Run `/seoplan "[niche]" --priority strategic` for the full cluster"

### `--priority strategic`
- Output all nodes but place PILLAR + STRATEGIC first in the execution list
- Add note at bottom: "Quick Wins deprioritised. Run `/seoplan "[niche]" --priority quickwins` for fast traffic"

**Add timeline estimates per tier group:**

| Tier | Estimated Time to Rank |
|------|----------------------|
| QUICKWIN | 4–8 weeks |
| FOUNDATION | 8–16 weeks (depends on internal link coverage) |
| PILLAR | 3–6 months (needs Quick Wins + Foundation live first) |
| STRATEGIC | 6–12 months (needs full cluster indexed) |

---

## seoplan-Step F — Plan Quality Check

Before outputting, verify all of the following:

```
[ ] Every node has: node-id, tier, slug, primary_kw, page_type, intent, difficulty, persona fields
[ ] Exactly 1 PILLAR node per cluster (--mode cluster)
[ ] At least 2 QUICKWIN nodes present (--mode cluster, --depth standard or deep)
[ ] No orphan nodes (every node: >= 1 inbound link AND >= 1 outbound link)
[ ] PILLAR has inbound links from ALL other nodes
[ ] PILLAR has outbound links to ALL other nodes
[ ] Execution order is consistent (QW and FND before PILLAR; STRATEGIC last)
[ ] All seobrief_cmd values are valid commands (correct syntax, correct --plan reference)
[ ] If --brand is active: brand persona defaults applied to applicable node tiers
```

If any check fails → fix the relevant nodes before output.

---

## seoplan-Step G — Output + Save

### Display Output

Output the full plan in the format defined in `SEO_PLANS/plan-template.md`:

```
1. Plan header (plan_id, niche, mode, lang, brand, date, priority_focus, total_nodes)
2. Topical Map text overview (tree showing pillar → tiers)
3. PILLAR node card (full detail)
4. QUICKWIN node cards (full detail each)
5. FOUNDATION node cards (full detail each)
6. STRATEGIC node cards (full detail each)
7. Internal Link Matrix table
8. Execution Order (numbered, with timeline note per tier group)
9. Next Step (the first /seobrief command to run — always the lowest-difficulty QUICKWIN)
```

### Save

1. Generate `plan_id` from niche + lang:
   - Lowercase, hyphens for spaces, lang suffix
   - Example: "Vintage analog cameras Germany" + de → `vintage-analog-cameras-de`
2. Save full plan to `SEO_PLANS/<plan-id>.md`
3. Add a row to `SEO_PLANS/_index.md`

### After Output — Offer the User

```
"show me only quick wins"         → reprint QUICKWIN section only
"generate brief for [node-id]"    → immediately run /seobrief for that node
"show link matrix"                → reprint internal link matrix only
"export execution order"          → print numbered execution list only
"drill down [cluster-topic]"      → run /seoplan for that cluster (--mode site only)
```

---

*Last updated: 2026-04-05 (v0.1)*
*Maintainer: Chris — full /seoplan pipeline logic*
