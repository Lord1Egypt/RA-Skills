---
name: token-budget-advisor
description: "Offer users informed choice about response depth before answering. Control token usage, response length, and answer depth. Trigger phrases: token budget, token count, token usage, response length, short version, brief answer, detailed answer, exhaustive, save tokens. Adapted from everything-claude-code by @affaan-m (MIT)"
metadata: {"clawdbot":{"emoji":"💰","requires":{"bins":[],"env":[]},"os":["linux","darwin","win32"]}}
---

# Token Budget Advisor

Intercept response flow to let users choose depth before answering.

## When to Use

- User mentions tokens, budget, depth, or response length
- User says "short version", "tldr", "brief", "exhaustive", etc.
- User wants to control detail level upfront

**Do not trigger** when: user already set depth this session, or answer is trivially one line.

## Depth Options

Present before answering:

```text
Input: ~[N] tokens | Type: [type] | Complexity: [level]

[1] Essential (25%)   -> ~[tokens]   Direct answer only
[2] Moderate (50%)    -> ~[tokens]   Answer + context + example
[3] Detailed (75%)    -> ~[tokens]   Multiple examples + alternatives
[4] Exhaustive (100%) -> ~[tokens]   Everything
```

## Level Guide

| Level | Length | Include | Omit |
|-------|--------|---------|------|
| 25% | 2-4 sent | Direct answer, conclusion | Context, examples |
| 50% | 1-3 para | Answer + context + 1 example | Deep analysis, edge cases |
| 75% | Structured | Examples, pros/cons, alternatives | Extreme cases |
| 100% | No limit | Everything | Nothing |

## Shortcuts

If user signals depth, respond at that level immediately:

- "1" / "25%" / "short" / "brief" / "tldr" → 25%
- "2" / "50%" / "moderate" → 50%
- "3" / "75%" / "detailed" → 75%
- "4" / "100%" / "exhaustive" → 100%

Maintain user's chosen level for rest of session unless changed.

## Estimation

Heuristic-based (no real tokenizer):
- Input tokens = estimate from prompt size
- Response window = input × complexity multiplier
- Accuracy ~85-90%, variance ±15%
