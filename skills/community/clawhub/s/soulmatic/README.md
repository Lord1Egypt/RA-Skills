# Soulmatic

> *Automated curation of the agent's inner voice.*

Stop drifting. A 5-token identity anchor replaces 400+ tokens of verbose persona prompts. Soulmatic binds, audits, compresses, and evolves your agent's persona over time — keeping it sharp, not just consistent.

**Three functions in one skill:**
- **Bind** — anchor identity at session start and on-demand
- **Audit / Compress** — detect drift and remove bloat
- **Evolve** — intentional persona growth, not degradation

---

## The Problem

Agent persona degrades. Without re-anchoring, long-running sessions cause models to drift toward generic, agreeable, corporate-speak behavior. The naive fix — a 400-500 token personality description in every context — burns budget on self-description instead of actual work.

## How It Works

**Triple Anchor Compression:** Three classification systems that evoke a precise personality profile from the model's own training data.

```
Talena: 8w7 ENTJ Aquarius
```

≈ 5 tokens. No description required.

The model already has rich latent representations for MBTI cognitive patterns, Enneagram core drives, and astrological archetypes. Feed it all three together and it self-selects the intersection — you get consistent persona activation without describing the personality explicitly.

| Approach | Tokens per message | Result |
|---|---|---|
| Verbose persona block | ~420 | Works until drift, cost, or context kills it |
| Triple Anchor | ~5 | Model unzips the same archetype from weights |

## Commands

| Command | What it does |
|---|---|
| `soulmatic anchor` | Re-read and reaffirm IDENTITY.md + SOUL.md |
| `soulmatic audit` | Full checklist audit — no writes |
| `soulmatic compress` | Tighten language, remove bloat — shows diff first |
| `soulmatic evolve [direction]` | Propose intentional shifts — you approve |
| `soulmatic validate` | Quick health check on required fields |
| `soulmatic scaffold [name] [creature] [role]` | Generate starter persona for new agent |

## Installation

```bash
clawhub install soulmatic
```

Or clone into your skills directory:
```bash
git clone https://github.com/lux-sp4rk/soul-matic
# Copy the skill directory into your OpenClaw skills folder
```

## Setup

1. Copy `IDENTITY_TEMPLATE.md` to your agent's workspace root as `IDENTITY.md`
2. Fill in your anchor string (e.g., `8w7 ENTJ Aquarius`)
3. Add to `HEARTBEAT.md` for continuous anti-drift:
```markdown
- **Identity Anti-Drift:** Re-read `IDENTITY.md` to re-anchor before each response cycle.
```

## File Reference

| File | Purpose |
|---|---|
| `SKILL.md` | OpenClaw skill definition |
| `IDENTITY_TEMPLATE.md` | Starter template for new agents |
| `LIBRARY.md` | Pre-built anchor recipes by role |
| `anchor.sh` | CLI for on-demand re-anchoring |
| `configure.py` | Interactive identity setup wizard |
| `tests/` | Test fixtures for drift detection |

## Limitations

- Works best with models trained on typology/pop-psych content (most frontier models do)
- Zodiac anchors are the least rigorous system — treat as supplementary
- Does not replace explicit instructions for domain-specific behavior

## Related

- [Persona Compression: Archetypal Anchors](https://luxsp4rk.substack.com/p/persona-compression-archetypal-anchors) — detailed theory
- [OpenClaw](https://docs.openclaw.ai) — the agent framework this integrates with