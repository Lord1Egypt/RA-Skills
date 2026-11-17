# Repair or Replace

> Don't guess. Score it.

A [Hermes Agent](https://hermes-agent.nousresearch.com/docs) / OpenClaw skill
that helps you decide whether to **fix, replace, or recycle** a broken item
using a weighted decision matrix across cost, lifespan, condition, sentiment,
and environmental impact.

## Why

When something breaks, the repair-vs-replace decision is usually made on gut
feel — or worse, on whatever the repair shop quotes before you've thought it
through. This skill structures the decision: it takes the numbers you have
(repair cost, replacement cost, age), combines them with factors you might not
have considered (remaining lifespan, environmental cost, sentimental value),
and produces a clear, score-backed recommendation with reasoning.

## What's Included

- **`SKILL.md`** — core skill: decision matrix, quick-reference, when-to-use.
- **`references/`**
  - `decision-matrix.md` — full scoring algorithm, weights, and rationale.
  - `item-lifespans.md` — expected lifespan data for 40+ common items.
  - `environmental-impact.md` — e-waste, embodied carbon, and sustainability.
- **`scripts/repair_or_replace.py`** — the main decision engine (stdlib only).
- **`scripts/sample_run.sh`** — example invocations for different item types.

## Quick Start

```bash
# Basic decision
python3 scripts/repair_or_replace.py \
  --item "washing machine" \
  --age 8 \
  --repair-cost 250 \
  --replacement-cost 800 \
  --expected-lifespan 12

# With symptoms and condition
python3 scripts/repair_or_replace.py \
  --item "refrigerator" \
  --age 10 \
  --repair-cost 200 \
  --replacement-cost 900 \
  --expected-lifespan 14 \
  --symptoms "not cooling properly" \
  --condition 4

# Factor in strong sentimental value (grandfather's watch)
python3 scripts/repair_or_replace.py \
  --item "vintage watch" \
  --age 20 \
  --repair-cost 150 \
  --replacement-cost 500 \
  --expected-lifespan 40 \
  --sentimental 9

# JSON output
python3 scripts/repair_or_replace.py --item "laptop" --age 5 \
  --repair-cost 300 --replacement-cost 1000 --format json

# Interactive mode (prompts for each value)
python3 scripts/repair_or_replace.py --interactive
```

Example output:

```
Repair or Replace — Decision Report
====================================
Item                : washing machine
Age                 : 8 years
Expected lifespan   : 12 years

Repair cost         : $250
Replacement cost    : $800
Cost ratio          : 31% (repair is 31% of replacement)

Decision Matrix (weighted):
  Cost Ratio        : 25.0/30  → Repair favored (cost ratio < 50%)
  Remaining Life    : 12.5/25  → Only 33% lifespan remaining
  Condition         : 10.5/15  → Decent overall condition
  Sentimental       :  2.0/10  → Low sentimental value
  Environmental     : 16.0/20  → Repair avoids e-waste

Total Score         : 66.0/100

Recommendation      : REPAIR
Confidence          : Moderate (66%)

Reasoning:
  • Repair cost is well below the 50% threshold (31%)
  • Item still has some remaining lifespan
  • Repair avoids generating e-waste
  ⚠ Only 33% of expected lifespan remains — consider future repair costs
```

## Decision Matrix

| Factor            | Weight | What It Measures                              |
| ----------------- | ------ | --------------------------------------------- |
| Cost Ratio        | 30%    | Repair cost as % of replacement cost          |
| Remaining Life    | 25%    | How much of expected lifespan is left         |
| Condition         | 15%    | Overall state beyond the current fault        |
| Sentimental       | 10%    | Emotional/irreplaceable value                 |
| Environmental     | 20%    | E-waste avoidance + energy efficiency gains   |

See `references/decision-matrix.md` for the full algorithm.

## Installation (Hermes Agent)

Copy or symlink this directory into your skills folder:

```bash
cp -r repair-or-replace ~/.hermes/skills/
```

Hermes auto-discovers skills with a valid `SKILL.md`. See the
[skills docs](https://hermes-agent.nousresearch.com/docs) for details.

## Requirements

- Python 3.8+ (stdlib only — no pip install needed)

## License

MIT © Denis Voronin
