# Memory Template - Real Estate Investing

Create these files inside `~/real-estate-investing/`.

## `memory.md`

```markdown
# Real Estate Investing Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Strategy
- Preferred strategies:
- Target hold period:
- Capital range:
- Financing comfort:
- Minimum return or cash-flow guardrails:
- Management preference:

## Buy Box
- Markets:
- Asset types:
- Price band:
- Bedrooms or unit count:
- Rehab tolerance:
- Hard no-go rules:

## Current Priorities
- What the user is optimizing for right now:
- What must be protected:
- Questions still unresolved:

## Notes
- Durable lessons from prior deals:
- Repeated mistakes to avoid:
```

## `pipeline.md`

```markdown
# Real Estate Investing Pipeline

| deal | market | strategy | stage | headline ask | thesis fit | top risk | next step | updated |
|------|--------|----------|-------|--------------|------------|----------|-----------|---------|
| Example duplex | Cleveland | buy-and-hold | triage | 245000 | medium | roof + taxes | verify rent comps | YYYY-MM-DD |
```

## `markets.md`

```markdown
# Market Notes

| market | asset focus | rent reality | insurance or tax risk | operating notes | updated |
|--------|-------------|--------------|------------------------|-----------------|---------|
| Columbus | duplex | strong demand around hospitals | reassessment risk | local PM depth is good | YYYY-MM-DD |
```

## `decisions.md`

```markdown
# Decisions and Post-Mortems

| date | deal | outcome | why | lesson |
|------|------|---------|-----|--------|
| YYYY-MM-DD | Example duplex | passed | DSCR too thin after real expenses | reject debt-sensitive deals faster |
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context still forming | Keep gathering market and strategy context naturally |
| `complete` | Enough context exists | Work from stored guardrails unless the user updates them |
| `paused` | User does not want more setup right now | Answer deal questions without pushing more discovery |
| `never_ask` | User does not want proactive setup questions | Stop asking for more profile detail unless required |

## Key Principles

- Save durable investing preferences and lessons, not every transient listing detail.
- Update `last` whenever the strategy, buy box, or active pipeline changes materially.
- Keep exact addresses optional; shorthand property references are often enough.
- Post-mortems matter: the value is not only what was bought, but what was wisely rejected.
