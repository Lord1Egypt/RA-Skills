# self-improving-tech-ppt

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

An AI Agent Skill implementing the **Prompt → Leverage → Memory → Self-Check Loop（提示 → 利用 → 记忆 → 自检循环）** for building and iteratively refining high-density, executive-grade technical architecture & planning PPT slides.

Instead of generating fragile text-heavy slides filled with AI buzzwords, hollow boxes, or broken layouts, this skill gives coding/AI agents:

- **Model-Agnostic Hard Gates (`v1.1.0`)**: Prevents stronger conversational models (like ChatGPT/GPT) from drifting back into sparse "Gamma/Keynote blog slides" or teal+orange AI-slop palettes by enforcing strict palette locks, amber callout width/area caps, anti-oversized-title rules, and 4-quadrant minimum density checks in Python.
- **Native Editable `.pptx` Compiler**: Generates clean 16:9 (`960 × 540 pt`) PowerPoint slides via `python-pptx` with East Asian font binding, OpenXML gradients, refined micro-chip modules, and petite database cylinders.
- **Switchable Theme System (Not Hardcoded)**: Strictly defaults to calm corporate blue (`executive-blue`), with explicit opt-in switching to `slate-minimal`, `steel-teal`, `academic-indigo`, or custom brand color overrides via `build_theme(...)`.
- **Persistent Critique Memory**: Turns every round of human feedback into permanent rules and programmatic blockers so the agent never repeats a mistake or regresses an already-approved element.
- **Dual Self-Check Gate**:
  1. **Automated Static Gate (`run_self_check`)**: Blocks diagonal lines, circular logic (`forbid_terms`), AI buzzwords / colloquialisms (`DEFAULT_BANNED_WORDS`), parentheses, unexpected wraps, and text overflows.
  2. **Visual QA Gate (`render_quicklook_and_crop`)**: Renders the actual `.pptx` via macOS QuickLook (`qlmanage`) with zoomed-in detail crops for mandatory visual inspection before delivery.

---

## Directory Structure

```text
self-improving-tech-ppt/
├── SKILL.md                              # Main agent workflow (4-step self-improving loop)
├── LICENSE                               # MIT License
├── README.md                             # Project overview & quick start
├── references/
│   ├── design-and-anti-ai-rules.md       # Logic, anti-AI blacklist, themes & layout rules
│   └── memory-template.md                # Per-session critique & locked-asset memory ledger
├── scripts/
│   └── ppt_engine.py                     # Native PPTX/SVG/Icon/Self-Check/QuickLook engine
└── examples/
    └── demo_tech_slide.py                # Minimal runnable example across all built-in themes
```

---

## Quick Start

### Install as an Agent Skill

- **ClawHub / OpenClaw**:
  ```bash
  npx clawhub install self-improving-tech-ppt
  ```
- **Antigravity (Global Discovery)**:
  ```bash
  git clone https://github.com/theosunny/self-improving-tech-ppt.git \
    ~/.gemini/config/skills/self-improving-tech-ppt
  ```
- **Workspace / Repo-Scoped**:
  Copy the folder into `.agents/skills/self-improving-tech-ppt/`.

### Run the Demo Script

```bash
python3 -m venv .ppt_venv
.ppt_venv/bin/pip install python-pptx pillow

# Default theme: executive-blue
.ppt_venv/bin/python examples/demo_tech_slide.py

# Switch built-in themes: slate-minimal | deep-teal | academic-indigo
.ppt_venv/bin/python examples/demo_tech_slide.py slate-minimal
```

---

## Built-In Switchable Themes

| Theme Name | Visual Tone | Primary / Deep Anchor / Panel Background |
| --- | --- | --- |
| `executive-blue` *(default)* | Calm Corporate Blue | `#005EA8` / `#08306B` / `#F5F9FE` |
| `slate-minimal` | Consulting Minimalist Slate | `#334155` / `#0F172A` / `#F8FAFC` |
| `deep-teal` | Tech / Cloud Deep Teal | `#0E6E7D` / `#083D47` / `#F4FAFA` |
| `academic-indigo` | Research / Keynote Indigo | `#3451B2` / `#19285E` / `#F6F8FE` |

Custom brand overrides:

```python
from ppt_engine import Scene, build_theme

brand = build_theme("executive-blue", {"blue_main": "#1D4ED8", "navy_deep": "#1E3A8A"})
scene = Scene("my-architecture-slide", theme=brand)
```

---

## License

MIT © 2026
