# council

Topic-aware multi-agent debate for real decisions.

This skill adapts the classic “council” pattern into something actually useful for production agents:
- personas change by **topic/domain**
- works across **engineering, sales, support, product, growth, ops, and mixed strategy**
- supports **quick** and **full** council modes
- includes a light **self-healing** layer for failed persona spawns

## What it does
Instead of one model pretending to contain the whole company in its head, `council` creates structured disagreement between specialist lenses.

Examples:
- engineering council for architecture and API decisions
- sales council for pricing and deal strategy
- support council for escalations and workflow design
- product council for PRDs and prioritization
- mixed council for messy strategic tradeoffs

## Modes

### Quick council
Use for reversible or low-stakes questions.
- 1 round
- 3–5 personas
- fast recommendation

### Full council
Use for load-bearing decisions.
- 3 rounds
- 4–6 personas
- visible debate + convergence + unresolved tensions

## Domain packs
Included persona packs:
- engineering
- sales
- support
- product
- growth
- ops
- mixed

## Self-healing features
Borrowed from our self-healing spawn pattern:
- fallback model chain
- checkpoint file per council run
- proof-of-completion requirement

This prevents a failed persona spawn from nuking the whole debate like a dramatic intern pulling the fire alarm.

## Files
- `SKILL.md` — skill behavior and routing
- `Personas.md` — topic-based persona packs
- `RoundStructure.md` — quick/full council flow
- `OutputFormat.md` — transcript and synthesis format
- `Implementation.md` — OpenClaw execution pattern
- `SelfHealing.md` — resilience layer
- `ExecutorPrompt.md` — ready-to-use execution prompt
- `scripts/select-pack.py` — choose domain/persona pack from a topic
- `scripts/init-checkpoint.sh` — create checkpoint file
- `scripts/update-checkpoint.sh` — update round/model progress

## Typical use
```text
/council Should we redesign our API auth layer for multi-tenant B2B integrations?
```

Expected behavior:
1. classify the topic
2. choose the right domain pack
3. pick quick/full mode
4. spawn persona runs
5. synthesize recommendation + tradeoffs + next action

## Why this exists
Because some decisions need friction, not confidence.

Single-agent answers are often fine.
But when the choice affects architecture, pricing, customer experience, or operational risk, a council gives you something better:
- competing incentives
- explicit tradeoffs
- sharper synthesis

## Credits
Built by the [Enterprise Crew](https://github.com/henrino3) for [OpenClaw](https://github.com/openclaw/openclaw).
