# skill-net

[中文版](./README_zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-3.1.0-blue)

> Diagnose, map, and score your OpenClaw skill ecosystem — find orphans, trace dependencies, measure health.

## What Problem This Solves

When managing 100+ skills, you need to answer questions like:
- "What actually depends on `/review`?"
- "If I delete `skill-factory`, what breaks?"
- "Which skills have no trigger phrases?"
- "How healthy is my ecosystem overall?"

`skill-net` scans every SKILL.md, builds a dependency graph, and produces actionable diagnostic reports.

**When to trigger:** "analyze ecosystem", "full scan", "ecosystem health", "skill health", "what depends on X", "if I delete Y what breaks", "find orphans", "技能生态"

## Features

- **Ecosystem Health Score** — weighted 0–100 score across 4 dimensions (trigger coverage, metadata completeness, cross-referencing, cohesion)
- **Dependency Graph** — maps all skill references (both `skill-*` mentions and protocol commands like `/review`, `/qa`)
- **Orphan Detection** — finds skills with SKILL.md but no trigger phrase
- **Impact Analysis** — for any skill, shows exactly what breaks if it's deleted, grouped by category
- **Bilingual Reports** — output in English, Chinese, or both via `--lang` flag
- **Structured Output** — saves `ecosystem.json` + `report.md` for further processing

## Quick Start

```bash
# Full bilingual scan (default: ZH then EN)
python3 scripts/analyze_deps.py

# Chinese report only
python3 scripts/analyze_deps.py --lang=ZH

# English report only
python3 scripts/analyze_deps.py --lang=EN

# JSON output (for automation)
python3 scripts/analyze_deps.py --json

# Impact analysis for a specific skill
python3 scripts/analyze_deps.py --impact=review
```

## Output Sections

| Section | Description |
|---------|-------------|
| 🌡️ Health Score | 0–100 ecosystem score |
| 📊 Composition | Core Hubs / Bridges / Leaves / Isolated / Orphans |
| 🗑️ Delete Impact | What breaks if you remove skill X |
| 📋 Ecosystem Map | ASCII tree of skill relationships |

## Ecosystem Health Formula

```
Health Score = (
  trigger_coverage  × 30%  +
  metadata_complete × 20%  +
  cross_reference    × 20%  +
  ecosystem_cohesion × 30%
)
```

## Key Findings (Real Data)

**The most-connected nodes are protocol commands, not `skill-*` named skills:**

| Skill | Type | Referenced By |
|-------|------|---------------|
| `/review` | protocol | 59 skills |
| `/qa` | protocol | 10 skills |
| `/summarize` | CLI | 3 skills |
| `/weather` | protocol | 3 skills |

Traditional dependency detection (looking only for `skill-X` mentions) **severely underestimates** real ecosystem relationships.

## Directory Structure

```
skill-net/
├── SKILL.md              # Entry point + skill definition
├── LICENSE               # MIT License
├── README.md             # This file
├── README_zh.md          # Chinese version
├── CONTRIBUTING.md       # Contribution guide
├── .gitignore
├── scripts/
│   ├── analyze_deps.py   # Main analyzer (self-contained)
│   └── requirements.txt   # (empty — no external deps)
└── data/
    ├── ecosystem.json    # Structured data (generated)
    └── report.md         # Markdown report (generated)
```

## Skill Classification

| Type | Definition |
|------|-----------|
| 🔵 Core Hub | Referenced by 3+ skills (high blast radius) |
| 🟡 Bridge | Both references others and is referenced |
| 🟢 Leaf | References others, nothing references it |
| ⚪ Isolated | Self-contained, no dependencies |
| ⚠️ Orphan | Has SKILL.md, no trigger phrase detected |

## Caveats

- **Orphan ≠ Broken** — many skills use `/protocol` activation instead of `use when` phrases. Orphans are flagged for awareness, not as errors.
- **Impact is directional** — `A mentions B` doesn't mean `B depends on A`. Delete impact shows what *could* break, not what *will*.
- **Does not modify skills** — this is a read-only diagnostic tool.

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.