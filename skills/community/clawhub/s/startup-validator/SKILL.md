---
name: startup-validator
description: Startup validation before you build—structured validate, compete, and mvp commands plus a reporting template. Use when the user wants to sanity-check a startup idea, competitive landscape, MVP scope, or early PMF thinking. Keywords: startup validation, founder, competitive analysis, MVP, PMF, indie hacker.
---

# Startup Validator — Structure Your Validation Before You Build

## Overview

Helps founders and indie hackers **structure** early validation: market-fit signals, competitive landscape, and MVP scope. Clearer than a generic “idea check”—it’s framed around **starting up** (problem, market, and first ship).

**Trigger keywords**: startup validation, founder idea check, competitive analysis, MVP scope, PMF, pre-launch

## Prerequisites

```bash
pip install requests
```

*(Optional if you extend the tool to call external APIs; the bundled script uses the Python stdlib.)*

## Capabilities

1. **Multi-dimensional review** — market, competitors, tech stack, business model (see `references/startup_validator_guide.md`).
2. **Persona & need framing** — who pays and what job-to-be-done is.
3. **MVP & roadmap sketch** — a realistic first release slice.

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `validate` | Validation pass for an idea | `python3 scripts/startup_validator_tool.py validate [args]` |
| `compete` | Competitive landscape pass | `python3 scripts/startup_validator_tool.py compete [args]` |
| `mvp` | MVP plan scaffold | `python3 scripts/startup_validator_tool.py mvp [args]` |

## Usage (from repository root)

```bash
python3 scripts/skills/startup-validator/scripts/startup_validator_tool.py validate --idea 'SaaS bookkeeping'
python3 scripts/skills/startup-validator/scripts/startup_validator_tool.py compete --market 'bookkeeping'
python3 scripts/skills/startup-validator/scripts/startup_validator_tool.py mvp --idea 'SaaS bookkeeping'
```

## Output format (for the agent’s report)

```markdown
# Startup validation report

**Generated**: YYYY-MM-DD HH:MM

## Key findings
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

## Data snapshot
| Metric | Value | Trend | Rating |
|--------|-------|-------|--------|
| A | XXX | ↑ | ⭐⭐⭐⭐ |
| B | YYY | → | ⭐⭐⭐ |

## Analysis
[Multi-dimensional analysis grounded in data you actually have]

## Recommendations
| Priority | Action | Expected impact |
|----------|--------|-----------------|
| High | [Action] | [Quantify if possible] |
| Medium | [Action] | … |
| Low | [Action] | … |
```

## References

### Core links
- [YC: The real product/market fit](https://www.ycombinator.com/library/5z-the-real-product-market-fit)
- [Pre-build idea validator use case (OpenClaw)](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/pre-build-idea-validator.md)
- [Market research product factory use case](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/market-research-product-factory.md)

### Community
- [Hacker News discussion](https://news.ycombinator.com/item?id=41986396)
- [Reddit r/startups — related thread](https://www.reddit.com/r/startups/comments/1055d61yyz/idea_validator_ai/)

## Notes

- Prefer **real** data from APIs, search, or user-provided sources; do not invent metrics.
- Mark missing data as **unavailable** instead of guessing.
- Treat AI output as **input to judgment**, not a go/no-go by itself.
- Optional: `pip install requests` if you extend the script with HTTP calls.

## Legacy name

This skill was previously published as **`idea-validator`**. The slug is now **`startup-validator`** (friendlier for “founder / startup” workflows). If an old path is bookmarked, migrate to `scripts/skills/startup-validator/`.
