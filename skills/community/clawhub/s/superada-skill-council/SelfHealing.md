# Self-Healing for Council

This file adapts the useful parts of the `self-healing` skill for council execution.

## Goal

Make council runs more resilient without turning every debate into a distributed systems thesis.

## Reuse These Pieces

### 1) Fallback model chain
If a persona spawn fails, retry with the next model.

Suggested order:
- `opus`
- `sonnet`
- `gemini`
- `glm5`

Use a shorter chain for cheap/fast councils if desired.

### 2) Checkpoint file
Initialize a checkpoint per council run:
- `/tmp/self-heal-council-<label>.json`

Track:
- topic
- domain
- mode
- personas
- current round
- completed rounds
- models tried
- last error

### 3) Proof of completion
The council is not "done" because a sub-agent said vibes were immaculate.

Require:
- transcript captured for each completed round
- persona outputs actually present
- final synthesis generated

## Recommended Council Flow

### Before Round 1
1. initialize checkpoint
2. write domain + persona pack to checkpoint
3. spawn persona agents with first preferred model

### After Each Round
1. verify all persona outputs arrived
2. append round completion to checkpoint
3. store transcript summary/reference in checkpoint if useful

### On Failure
If a spawn fails:
1. record `last_error`
2. record model attempt
3. retry that persona with next fallback model
4. continue only when the required persona outputs are available

## When to Use Watchdog Cron

Only for:
- long full councils
- expensive deep-research councils
- councils chained into broader workflows

Skip for:
- quick councils
- short product/engineering smell tests

## Example Parent-Agent Pattern

```text
Council label: pricing-v2
Domain: sales
Mode: full
Primary model: sonnet
Fallback chain: sonnet -> gemini -> glm5

If any persona spawn fails, retry with the next model and log it in /tmp/self-heal-council-pricing-v2.json.
Do not mark a round complete until all required persona outputs are present.
```

## Minimal Rule

If you only borrow one thing from self-healing, borrow this:

**Do not lose round state when a persona spawn fails.**

That is the part that actually matters.
