# Smarty Skills-Infra

An OpenClaw skill that silently learns your preferences, judgment patterns, and working style across sessions — then applies them as soft defaults in every future conversation.

Your AI gets sharper about *you* over time. You never configure anything.

## How it works

Three-layer memory hierarchy, running invisibly alongside your normal work:

| Layer | What it does | When it runs |
|---|---|---|
| **L1 Observer** | Records observations when you correct, state a preference, or retract one | During tasks (only when triggered) |
| **L2 Reflector** | Groups observations into patterns, promotes stable ones to axioms | Session start (when 15+ observations accumulate) |
| **L3 Axiom** | Maintains a lean profile of ≤25 reusable preferences loaded every session | During reflection |

Most tasks produce **zero** observations. The skill only records when you express a real preference signal.

## What gets learned

- Corrections — when you change, rewrite, or redirect output
- Stated preferences — when you explicitly say you prefer, want, or dislike something
- Retractions — when you ask to forget or stop applying a preference

## Example

After a few sessions, your profile might contain:

```
- I prefer short, concise names — abbreviate rather than spell out.
  strength: 5 | domain: code-style | last-confirmed: 2026-03-15

- I want to be challenged, not agreed with. Push back on my first idea.
  strength: 4 | domain: communication | last-confirmed: 2026-03-14

- I prefer TypeScript with strict config for all new projects.
  strength: 3 | domain: tooling | last-confirmed: 2026-03-10
```

These axioms are applied as soft defaults — not rigid rules. The agent adapts when the situation calls for something different.

## Install

Copy the `skills/context-infra/` directory into your OpenClaw skills folder.

```
skills/context-infra/
├── SKILL.md                    # Main skill (70 lines)
└── references/
    └── profile-format.md       # Loaded only during reflection
```

The skill creates two files in your memory directory as it runs:

```
memory/context-infra/
├── observations.log            # Raw preference signals (append-only)
└── context-profile.md          # Your distilled axioms (auto-loaded)
```

## Design

- **Model-agnostic** — works with any LLM, not just Claude
- **Frictionless** — no setup, no prompts, no configuration
- **Minimal context cost** — ~570 tokens for the skill, ~215 tokens for the reference file
- **Self-maintaining** — axioms strengthen, weaken, merge, and go dormant over time
- **User-controlled** — say "forget that preference" and it's retracted immediately

Built through 35 rounds of iterative design optimization ([autoresearch method](https://github.com/karpathy/autoresearch)).

Inspired by [Context Infrastructure](https://yage.ai/context-infrastructure.html) by grapeot.

## License

MIT
