# Scenario-First Thinking

> Let AI use the right tool, at the right time, for the right problem.

---

## ⚡ Install

```bash
npx clawhub install scenario-first-thinking
```

---

**Author**: WH laowu
**Version**: 1.0.2
**Category**: Task Routing Layer — Thinking Framework

---

## One-Line Summary

When a task comes in, first identify the scenario (1 of 6), then apply 8 thinking tools (2-3 at a time) in priority order, and verify the conclusion.

---

## Six Scenarios at a Glance

| # | Scenario | Trigger Words | Top Tool |
|---|---------|--------------|---------|
| 1 | Direction/Decision | Startup/Strategy/Pivot | First Principles |
| 2 | Learning/Internalizing | Can't learn/Exam prep | Feynman |
| 3 | Express/Persuade | Write/Present/Sell | SCQA |
| 4 | Efficiency/Prioritization | Too busy/Unclear | Quadrant |
| 5 | Crisis/Firefighting | Urgent/Emergency | Inversion |
| 6 | Creative/Exploration | New ideas/Brainstorm | Feynman + First Principles |

---

## Three-Step Protocol

1. **Scene Routing**: Identify scenario from 6 options
2. **Tool Selection**: Apply 2-3 tools in priority order
3. **Verification**: Explainable? Example-able? No gaps?

---

## File Structure

```
scenario-first-thinking/
├── SKILL.md                     ← Main entry (English, AI reads this)
├── README.md                    ← This file (English)
├── README.zh-CN.md             ← Chinese version
├── _meta.json                  ← Publishing metadata
└── references/
    ├── six-scenario-routing.md ← Scene deep-dive
    ├── tool-handbook.md         ← 8 tools with cases
    └── scqa-template.md         ← SCQA writing template
```

---

## Design Principles

- **Lightweight**: Minimal logic in SKILL.md
- **Closed-Loop**: Scene → Tools → Verification, three steps complete
- **High Fault Tolerance**: Unclear defaults to Scene 4, tool failure degrades gracefully

---

## Changelog

- **1.0.2** (2026-03-25) — SKILL.md fully English, install command added
- **1.0.1** (2026-03-25) — Added README.en / README.zh-CN dual language
- **1.0.0** (2026-03-25) — Initial release: 6 scenes + 8 tools
