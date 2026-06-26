---
name: recipe-scout
description: >
  Find and normalize Chinese recipes (中餐菜谱) from structured sources first, then export clean recipe notes to Obsidian markdown. Prefer stable recipe sites over social posts; use 小红书 only for inspiration/fallback. Use when user asks for: Chinese recipes / 中餐菜谱, "how to cook X" / 做法, meal ideas, home-style dishes, weeknight cooking, recipe collection / curation, or recipe note creation in Obsidian.
user-invocable: true
metadata: {"openclaw":{"emoji":"🥢","homepage":"https://docs.openclaw.ai/tools/skills"}}
---

# recipe-scout

Source-policy + normalization layer for Chinese recipes. Not a single-site scraper.

## Source Ranking (strict priority)

### Tier A — Structured recipe pages (primary)
- **下厨房** (xiachufang.com) — largest Chinese UGC recipe platform, step-by-step photos, strong search
- **美食天下** (meishichina.com) — broad category coverage, reliable ingredient lists
- **豆果美食** (douguo.com) — large recipe app ecosystem
- **HowToCook** (github.com/Anduin2017/HowToCook) — programmer-authored, precise gram-level measurements, no fluff; raw URLs: `https://raw.githubusercontent.com/Anduin2017/HowToCook/master/dishes/<category>/<dish>/<dish>.md`; categories: `meat_dish`, `aquatic`, `vegetable_dish`, `staple`, `soup`, `dessert`, `condiment`
- Reputable cooking blogs with full recipe text

### Tier B — Video + transcript (secondary)
- YouTube / Bilibili cooking videos with captions or clear on-screen ingredients

### Tier C — Social posts (fallback / inspiration only)
- 小红书, short-post platforms, comment threads
- Mark confidence `low` unless validated by another source
- Do NOT treat as authoritative recipe specs

> **Anti-pattern:** Do not make 小红书 the primary recipe backend. UI changes often, ingredient/timing details are frequently missing, extraction is brittle.

## Retrieval Strategy

1. Parse dish intent + constraints (cuisine, diet, equipment, time, restrictions)
2. Search Tier A first with Chinese queries (see `references/query-examples.md`)
3. Collect 3–7 candidates
4. Deduplicate by core technique + ingredient profile
5. Rank by: completeness → clarity → home-cooking fit → ingredient accessibility
6. Use Tier B/C only to fill gaps or add variants

## Normalization Rules

- **Language:** Chinese default (English if user requests)
- **Units:** metric preferred (g / ml / tbsp / tsp); preserve source units if conversion uncertain
- **Times:** separate prep / cook / total; mark missing estimates as `estimated: true`
- **Seasoning:** keep exact source values; record `适量` as-is with a practical note
- **Heat:** normalize to 小火 / 中小火 / 中火 / 中大火 / 大火
- **Safety:** include basic food safety notes (chicken/pork doneness, etc.) when relevant

## Anti-Hallucination

- Never fabricate ingredient quantities, temperatures, or timings
- Missing fields → `unknown` / `未注明`
- Clearly distinguish: **source facts** vs **inferred estimates** vs **your recommendations**

## Output Modes

| Mode | When | Output |
|------|------|--------|
| Quick answer | Casual ask | Top 3 options, recommended version, concise steps + shopping list |
| Structured pack | User wants detail | Normalized recipe using schema |
| Obsidian export | Collection/save | One `.md` file per recipe → `/home/node/vault/Recipes/Chinese/`; fallback: `{workspace}/exports/recipes/` |

**Schema:** See `references/schema.md`
**Obsidian template:** See `references/obsidian-template.md`

## Execution Playbook

When invoked:
1. Restate target dish + constraints in one line
2. Search Tier A with Chinese queries
3. Return candidate table (3–7): source | completeness | style | confidence
4. Pick one "default cooking path"
5. Normalize into canonical schema
6. Output quick summary in chat
7. If export requested → write Obsidian note(s), return file paths

## Browser vs Web Tools

- **Prefer:** `web_search` (Brave Search API) + `web_fetch` for structured recipe pages — this is the primary retrieval method
- **Brave Search tip:** Use Chinese queries for Tier A sources (下厨房, 豆果, 美食天下); English queries for fallback/Tier B
- **Use browser only when:** page requires JS rendering, login/session, or video transcript interaction
- If Chrome relay is unstable → switch to `openclaw` browser profile

## Hard No's

- No aggressive scraping
- No paywall/login bypass
- No social-media hearsay presented as precise recipe specs
- No invented measurements
