# 🧠 Multi-Angle Thinking Engine
### محرك التفكير الاستخباراتي + المحاكاة الواقعية

> *"التحليل يصف. المحاكاة تكتشف."*
> *"Analysis describes. Simulation discovers."*

---

## What It Does

A skill for Claude and OpenClaw agents that transforms any question, decision, or idea into a **three-layer deep analysis**:

| Layer | What happens |
|-------|-------------|
| 🔍 **Intelligence** | Gathers real global data via web search before any analysis |
| ⚡ **11 Lenses** | Runs the topic through philosophical, ethical, practical, historical, psychological, systems, financial, technological, adversarial, societal, and counterfactual angles |
| 🌍 **Simulation** | Builds a realistic virtual world with real characters, runs it to completion, and reports back with narrative + findings + surprises |

**Not a list of opinions. A map of the full problem space — lived from the inside.**

---

## Quick Install

**Via ClawHub:**
```bash
clawhub install multi-angle-thinking
```

**Manual:**
```bash
git clone https://github.com/YOUR_USERNAME/multi-angle-thinking.git ~/.openclaw/skills/multi-angle-thinking
```

---

## Trigger Phrases

**English:**
> "Analyze this from all angles" · "Simulate what would happen if..." · "Challenge my thinking on..." · "What am I missing about..." · "Think deeply with me about..."

**Arabic / عربي:**
> "فكر معي في..." · "حلل هذا القرار بعمق" · "ما الزوايا التي لم أفكر فيها؟" · "ما النتائج غير المتوقعة لـ..." · "ماذا سيحدث لو..."

---

## Output Structure

```
🎯  Frame the Reality       — What is really being asked?
🔍  Intelligence Gathering  — Real data from the web (max 6 searches)
⚡  11 Lenses Analysis      — Deep multi-angle breakdown
🌍  Build the World         — Virtual scenario with real characters
👁️  Live Narrative          — Story + findings + surprises
🔮  Final Synthesis         — Convergences, tensions, open questions
```

---

## Guardrails

- Max 6 web searches per analysis
- Simulations of real people are clearly labeled as fictional inference
- Sensitive topics handled with appropriate caution
- Only invoked on explicit user request — never self-triggers
- No collection of private or personal data

---

## Files

```
multi-angle-thinking/
├── SKILL.md                          # Core skill instructions
├── README.md                         # This file
├── assets/
│   └── example-output.md             # Sample analysis output
├── scripts/
│   └── activator.sh                  # Optional session reminder hook
├── references/
│   ├── lenses-guide.md               # Deep guide to all 11 lenses
│   └── simulation-guide.md           # How to build effective simulations
└── hooks/
    └── openclaw/
        ├── HOOK.md                   # Hook documentation
        └── handler.js                # OpenClaw hook handler
```

---

## Example Output

See [`assets/example-output.md`](assets/example-output.md) for a full sample analysis.

---

## Author

Built and designed in **Baghdad, Iraq 🇮🇶** · March 2026
License: **MIT-0** — free to use, modify, redistribute. No attribution required.

If you find it valuable, the best acknowledgment is sharing where you found it.
