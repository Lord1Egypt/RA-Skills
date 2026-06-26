---
name: SkillPick
description: "挑选Skill" — Which AI Skill is Worth Installing? The buying guide for the AI Skill ecosystem. Use when users need to find, compare, or decide which AI Skill to install. Covers 58 categories, 29,000+ skills with dual-scoring (heat score for humans + quality score for agents), search recommendations, similar alternatives, workflow suggestions, and 13-dimension quality analysis.
---

# SkillPick — Which AI Skill is Worth Installing?

> **One-liner**: SkillPick = "What HiEngine Would I Buy?" for AI Skills
> Version: v6.5.0 | Updated: 2026-05-01

---

## Positioning & Boundaries

| You want | Use this | Why |
|----------|----------|-----|
| "I need to find XX skill" | `find-skills` | It's specialized for search |
| "What are everyone else installing?" | skillhub rankings | Follow the crowd, Top10 naturally |
| **"Which one is worth installing?"** | **SkillPick** | **Helps you decide — with reasons and verdicts** |

### What it does NOT do
- No search (find-skills already solves this)
- No rankings (skillhub already solves this)

### What it DOES do (only these 5 things)
- **Track TOP3**: Best-in-category at a glance
- **Search recommendations**: Intent → 1-3 recommendations + reasoning + verdict
- **Similar alternatives**: Compare alternatives with diff analysis
- **Workflow suggestions**: Best skill per role for complex scenarios
- **Quality analysis**: 13-dimension deep scan — GitHub + SkillHub + market validation

---

## Dual-Audience Design

```
┌───────────────────────────────────────┐
│        SkillPick v6.5.0                │
│   "挑选Skill"                          │
│   29,000+ skills · 58 tracks · Top3000 │
├──────────────────┬────────────────────┤
│  For Humans     │  For Agents        │
│                  │                    │
│  Track browsing  │ search / similar   │
│  Heat-score sort │ quality-score sort │
│  "Is it popular?" │ "Is it any good?" │
└──────────────────┴────────────────────┘
```

### Dual-Scoring System

Humans and agents judge skills differently — SkillPick uses two separate scoring systems:

| Dimension | Human Side | Agent Side |
|-----------|-----------|-----------|
| Field | `display_score` (heat) | `quality_score` (quality) |
| Reflects | Stars + chart rankings + community trust | 13-dimension quality depth |
| Used for | TOP3 ranking, frontend display | search/similar ranking |

---

## Six Core Features

### 1. Track TOP3 (Tab 1, human-first)

58 tracks, each showing TOP 3 skills.
Sorted by heat score, quality-gated (B+ or above required for TOP3).

### 2. Search Recommendations (Tab 2, agent-first)

Enter a keyword → returns 1-3 recommendations + comparison + verdict.
35 intent patterns, 13-dimension quality-weighted.

### 3. Similar Alternatives (Tab 3, agent-first)

Specify a skill name → returns 1-3 alternatives + diff analysis.

### 4. Workflow Suggestions (Tab 4, agent-first)

8 predefined scenarios, each role recommends 1 optimal skill.

### 5. Skill Detail (CLI)

Single skill 13-dimension radar + complete scoring.

### 6. Quality Report (CLI)

Global quality distribution (requires full data, run pipeline first).

---

## Agent CLI Interface

```bash
node api.js <command> [args]
```

| Command | Aliases | Args | Function |
|---------|---------|------|----------|
| **top3** | categories, tracks | `[track name]` | View TOP3 |
| **search** | find, s | `<keyword>` | Search recommendations 1-3 |
| **similar** | alt | `<skill name>` | Similar alternatives 1-3 |
| **workflow** | combo, wf | `[scenario]` | Workflow recommendations |
| **detail** | info, d | `<skill name>` | 13-dimension detail |
| **quality** | report, q | none | Global quality report |

```bash
node api.js top3                    # All tracks TOP3
node api.js search PDF              # PDF-related recommendations
node api.js similar pdf             # pdf alternatives
node api.js workflow 短视频带货     # Scenario recommendation (Chinese)
node api.js detail coding-agent    # 13-dimension detail
```

---

## 13-Dimension Quality System

| Dimension | Weight | Data Source |
|-----------|:------:|-------------|
| Description quality | 12% | Metadata |
| Tag completeness | 7% | Metadata |
| Install convenience | 8% | Metadata |
| Safety score | 14% | Metadata (veto) |
| Dependency complexity | 8% | Metadata |
| Documentation structure | 7% | Metadata |
| Error handling | 5% | Metadata |
| Maintenance activity | 10% | GitHub API |
| Test coverage | 5% | GitHub |
| Market validation | 8% | Metadata |
| Market popularity | 8% | SkillHub |

Grades: A+(≥85) · A(70-84) · B+(55-69) · B(45-54) · C(30-44) · D(<30)

---

## Data Scale

- Full: 29,000+ skills / 58 tracks / SkillHub + GitHub + manual 三源
- Release: Top 3000 elite (A+/A grade 96%)
- Workflows: 8 scenarios (short video commerce, e-commerce ops, content marketing, full-stack dev, etc.)

---

## Data Pipeline (auto-update)

```bash
node pipeline/pipeline.js full         # Full crawl + scoring (~6 min)
node pipeline/clean_and_split.js       # Clean + Top3000 split (<3 sec)
node pipeline/pipeline.js status        # View status
```

---

## File Structure

```
skillpick/
├── SKILL_EN.md             ← This file (English version for ClawHub)
├── SKILL.md                ← Chinese version (for SkillHub)
├── api.js                  ← Agent CLI (6 commands)
├── scanner.js              ← 13-dimension scan engine
├── index.html              ← Frontend (4 tabs, bilingual EN/CN)
├── skills_data.js          ← Top 3000 elite data
├── data/
│   ├── quality_map_slim.json
│   └── workflows.json
└── pipeline/               ← Data pipeline
```

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| **v6.5.0** | 2026-05-01 | Brand upgrade: Chinese name officially set to "挑选Skill"; unified version v6.5.0 across all files; release package rebuild |
| **v6.4.0** | 2026-04-30 | English i18n: bilingual UI (EN/CN), SKILL_EN.md for ClawHub |
| **v6.4.0** | 2026-04-27 | Dual scoring: display_score(heat) for humans + quality_score for agents; TOP3 quality gate (B+); C-grade penalty (−50%); track classification fix |
| **v6.2.0** | 2026-04-26 | Auto pipeline: SkillHub 30K + GitHub 680 crawl → merge → 13-dim scoring → build; skill total 954→29526 |
| **v6.1.2** | 2026-04-19 | Layout optimization: 1440px width |
| **v6.1.0** | 2026-04-19 | Pure version: 13-dimension Z-score quality scoring as core engine |
