---
name: skill-net
description: >
  Analyze OpenClaw skill ecosystem — dependencies, orphan detection, ecosystem health score,
  impact analysis, and skill relationships. Use when the user asks about skill relationships,
  "what depends on X", "if I delete Y what breaks", ecosystem health, or wants to find
  skills without trigger conditions (orhpans).
license: MIT
metadata:
  version: "3.1"
  category: skill-development
  author: wangjipeng
---

# OpenClaw Skill Net

Analyze, map, and diagnose the OpenClaw skill ecosystem — not a skill creator, a diagnostic lens.

---

## Core Positioning

This skill answers: **how does my skill ecosystem actually work?**

It scans every SKILL.md, detects dependency relationships, scores ecosystem health, and finds orhpans.

---

## Modes

### Mode 1: Full Analyze (default)

Run the complete ecosystem scan and produce a full diagnostic report.

**Trigger:** "analyze ecosystem", "full scan", "ecosystem health", "skill health", "技能生态", "生态报告"

**Language options (CLI flags):**
```bash
python3 scripts/analyze_deps.py              # default: ZH then EN
python3 scripts/analyze_deps.py --lang=ZH   # Chinese only
python3 scripts/analyze_deps.py --lang=EN   # English only
python3 scripts/analyze_deps.py --lang=BOTH  # ZH then EN (default)
```

**Output sections:**
1. 🌡️ Ecosystem Health Score (0–100) — 生态健康分
2. 📊 Health Breakdown — 健康度明细 (trigger coverage, metadata, cross-references)
3. 🔵 Core Hubs — 核心枢纽 (referenced by 3+ skills)
4. 🟡 Bridge Connectors — 桥接技能
5. 🟢 Leaf Skills — 叶节点技能
6. ⚪ Isolated Skills — 孤立技能
7. ⚠️ Orphan Skills — 孤儿技能 (have SKILL.md but no trigger conditions)
8. 🗑️ Impact Analysis — 删除影响分析 (who breaks what)
9. 📋 ASCII Ecosystem Map — 技能生态地图

> All sections rendered in the requested language (ZH/EN) with full bilingual labels.

### Mode 2: Query

Answer specific questions from cached or fresh data.

**Trigger:** "what depends on X", "if I delete Y", "who references Z", "core skills", "most connected skill"

**Execution:** Answer from `data/ecosystem.json` or run fresh scan.

### Mode 3: Orphan Scan

Find all skills with SKILL.md but missing trigger conditions.

**Trigger:** "find orphans", "skills without triggers", "dead skills", "missing triggers"

**Output:** List of orphan skills with line count and frontmatter name.

### Mode 4: Compare

Compare two skills side-by-side.

**Trigger:** "compare X and Y", "X vs Y dependencies", "skill X relationship to Y"

**Output:** Shared mentions, relationship type, overlap analysis.

---

## Key Findings From Real Data

> The ecosystem reveals structural patterns invisible from casual observation:

| Finding | Evidence |
|---------|----------|
| **True core hub: `review`** | 53 skills reference `/review` — by far the most connected |
| **`qa` is a secondary hub** | 9 skills reference `/qa` |
| **`/summarize`, `/weather`** | Referenced by 2+ skills each — utility anchors |
| **100/123 skills lack triggers** | Many use `/protocol` style instead of "use when" |
| **Ecosystem Health: 22.6/100** | Most skills missing metadata and trigger conditions |
| **`review` and `qa` are invisible hubs** | They don't use `skill-` prefix — protocol commands |

---

## Execution Steps (Full Analyze)

1. **Scan** — walk `~/.openclaw/skills/` and `~/.openclaw/workspace/skills/`, read every SKILL.md
2. **Extract** — for each skill:
   - Frontmatter fields (name, version, license, metadata)
   - Trigger presence (`use when` / `trigger` / `/protocol`)
   - ALL cross-skill name mentions (full scan, not just known slugs)
   - Metadata blocks
3. **Build graph** — `mentions` (outgoing) + `referenced_by` (incoming) for each skill
4. **Classify** — Core (≥3 incoming) → Bridge → Leaf → Isolated
5. **Detect orhpans** — has SKILL.md but no trigger phrase detected
6. **Score health** — weighted formula across 4 dimensions
7. **Render** — bilingual ASCII report (ZH/EN) + save `data/ecosystem.json` + `data/report.md`

---

## Ecosystem Health Formula

```
Health Score = (
  trigger_coverage   × 30%  +
  metadata_complete  × 20%  +
  cross_reference     × 20%  +
  ecosystem_cohesion  × 30%
)
```

Your ecosystem: **22.6/100** — healthy room for improvement.

---

## What the Real Data Reveals

**Surprising insight:** The most-connected nodes are protocol commands (`/review`, `/qa`), not `skill-*` named skills. These protocol skills are referenced by code patterns like:

```python
# Many skills open with this:
# /review — Structured Code Review Protocol
# /qa — Quality Assurance Execution Protocol
```

This means traditional dependency detection (looking for `skill-X` mentions) **severely underestimates** real relationships.

**True dependency types:**
1. **Named skill mentions** — `skill-factory`, `gupiao`, `bazi`
2. **Protocol command references** — `/review`, `/qa`, `/careful`, `/cso`
3. **CLI tool references** — `clawhub`, `mmx`, `summarize`, `weather`

---

## Do not

- Do not modify any skill based on the analysis without explicit user request
- Do not publish the ecosystem map without context — it's a diagnostic tool
- Do not call skills "broken" just because they lack trigger phrases — many use protocol-style activation
- Do not include `.git/`, `.venv/`, `__pycache__/` in scans

---

## Quality Bar

The output must:
- Scan both `~/.openclaw/skills/` and `~/.openclaw/workspace/skills/`
- Correctly identify incoming + outgoing references per skill
- Detect orhpans (has SKILL.md, no trigger phrase)
- Compute ecosystem health score (0–100)
- Complete full scan in < 15 seconds for 120+ skills
- Save structured data to `data/ecosystem.json` + `data/report.md`
- Support bilingual output (ZH/EN) via `--lang` flag

---

## Good vs Bad Examples

**Good:**
> "🔵 review (Core Hub, 53 incoming): /review is referenced by 53 skills. If deleted, these skills lose their review protocol: gupiao, proactive-agent, skill-vetter..."

**Bad:**
> "Here are all skills listed alphabetically"

**Good Orphan Report:**
> "⚠️  Found 100 orhpans — most are protocol-style skills (review, qa, careful, cso) that use `/command` activation instead of 'use when' phrases. These are not broken, just designed differently."

**Good Query:**
> "DELETE review → Breaks 53 skills including: gupiao, marketing-*, engineering-*, testing-*, project-*. This is the most critical skill in the ecosystem."