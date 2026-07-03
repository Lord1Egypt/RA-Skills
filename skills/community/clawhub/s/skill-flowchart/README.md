# SkillFlowChart

> Turn any `SKILL.md` into a self-contained decision flowchart HTML.

**English** | [中文](README.cn.md)

SkillFlowChart generates clean, deterministic decision flowcharts from natural-language skill definitions. It splits the work where each side excels: **AI extracts semantics, a script computes geometry** — so every render of the same input is pixel-identical.

## Table of Contents

- [How It Works](#how-it-works)
- [Quick Start](#quick-start)
- [nodes.json Schema](#nodesjson-schema)
- [Themes](#themes)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [Design Principles](#design-principles)
- [Contributing](#contributing)
- [License](#license)

## How It Works

```
SKILL.md  ──AI extracts──▶  nodes.json  ──script renders──▶  HTML
            (semantics)      (structured)     (deterministic)    (SVG)
```

| Stage | Who | Why |
|-------|-----|-----|
| Read SKILL.md → nodes.json | AI (LLM) | Natural language is unstable; AI understands context |
| nodes.json → HTML | Script (Python) | Coordinate math must be deterministic and reproducible |

The AI **never** outputs coordinates or SVG. The script **never** guesses semantics. The only interface between them is the `nodes.json` schema.

## Quick Start

### Prerequisites

- Python 3.8+ (standard library only, zero dependencies)
- Any LLM to extract `nodes.json` from your `SKILL.md`

### Usage

```bash
# 1. Ask your AI to read SKILL.md and generate nodes.json
#    (extraction rules are documented in SKILL.md)

# 2. Run the script
python3 scripts/flowchart.py nodes.json --out flowchart.html

# 3. Open the HTML in any browser
open flowchart.html
```

### Options

```bash
python3 scripts/flowchart.py <nodes.json> [--out <output.html>] [--theme light|dark|transparent] [--json-out <debug.json>]
```

## nodes.json Schema

```json
{
  "title": "My Skill",
  "subtitle": "Optional description",
  "nodes": [
    {"id": "entry",   "type": "entry",    "label": "Start",            "role": "ai"},
    {"id": "check",   "type": "decision", "label": "Valid?",           "role": "decision"},
    {"id": "exit",    "type": "terminal", "label": "Exit",             "role": "terminal"},
    {"id": "process", "type": "process",  "label": "Run",              "role": "script"},
    {"id": "report",  "type": "output",   "label": "Generate Report",  "role": "output"}
  ],
  "edges": [
    {"from": "entry",   "to": "check",   "label": "",    "side": "bottom"},
    {"from": "check",   "to": "exit",    "label": "No",  "side": "left"},
    {"from": "check",   "to": "process", "label": "Yes", "side": "bottom"},
    {"from": "process", "to": "report",  "label": "",    "side": "bottom"}
  ],
  "legend": []
}
```

### Node Types

| type | shape | description |
|------|-------|-------------|
| `entry` | rounded rect | flow start point |
| `decision` | diamond | branch point (yes/no, mode switch) |
| `process` | rounded rect | processing step |
| `output` | rounded rect | report / file output |
| `terminal` | rounded rect | exit / error termination |

### Roles (color mapping)

| role | description |
|------|-------------|
| `ai` | AI inference / LLM call |
| `output` | report / file output |
| `decision` | decision point |
| `script` | script execution |
| `terminal` | termination / error |

> **One node = one role.** If a step involves multiple types of work (e.g. script baseline + AI analysis), split it into separate nodes.

### Edge `side` (critical)

The AI must explicitly label each edge's `side` — the script never guesses direction.

| side | meaning | layout behavior |
|------|---------|-----------------|
| `bottom` | main flow down | target at next level, inherits x from source |
| `left` | decision left branch / fork left | decision → same level horizontal; process → next level fork |
| `right` | decision right branch / fork right | same as left, mirrored |
| `""` | unlabeled (same as `bottom`) | inherits upstream |

**Decision** `left`/`right` → same level, horizontal connector.
**Process** `left`/`right` → next level, orthogonal fork (no diagonal lines).

## Themes

Three built-in themes:

| theme | background | label handling |
|-------|-----------|----------------|
| `light` (default) | white | centered with white halo |
| `dark` | `#0a0a0f` | centered with dark halo |
| `transparent` | none | vertical edge labels offset to one side |

```bash
python3 scripts/flowchart.py nodes.json --theme dark --out dark.html
```

## Examples

### HaluCatch (Hallucination Detection)

A complete real-world example with multi-level decisions, side-branch convergence, and multi-role nodes.

- [Light theme](docs/halucatch-light.html)
- [Dark theme](docs/halucatch-dark.html)
- [Transparent theme](docs/halucatch-transparent.html)

### TRAE Security Review

17 nodes, 18 edges. Contains 4 decision points, 2 side-branch convergences, and 2 termination drops.

- [Light theme](docs/security-review-light.html)
- [Dark theme](docs/security-review-dark.html)

## Project Structure

```
SkillFlowChart/
├── README.md                          # English documentation
├── README.cn.md                       # 中文说明
├── SKILL.md                           # Skill definition (AI entry point + extraction rules)
├── scripts/
│   └── flowchart.py                   # Core: nodes.json → SVG + HTML
├── docs/
│   ├── halucatch-nodes.json           # Example input (HaluCatch)
│   ├── halucatch-light.html           # Example output (light)
│   ├── halucatch-dark.html            # Example output (dark)
│   ├── halucatch-transparent.html     # Example output (transparent)
│   ├── security-review-nodes.json     # Example input (Security Review)
│   ├── security-review-light.html     # Example output (light)
│   └── security-review-dark.html      # Example output (dark)
├── tests/
│   └── simple.json                    # Minimal test case
└── LICENSE
```

## Design Principles

- **Structured relay** — layout logic never depends on the LLM; same input always produces identical output
- **Zero dependencies** — pure Python standard library, no `pip install` needed
- **Self-contained HTML** — single file output, no external CSS/JS references
- **No diagonal lines** — all connectors are horizontal or vertical (orthogonal routing)
- **Platform-agnostic** — works with any LLM (ChatGPT, Claude, Gemini, local models, etc.)

## Contributing

1. Fork the repo
2. Edit `SKILL.md` (extraction rules) or `scripts/flowchart.py` (layout/rendering)
3. Test with `tests/simple.json` and `docs/halucatch-nodes.json`
4. Submit a pull request

## License

MIT
