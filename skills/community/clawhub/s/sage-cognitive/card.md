# Cognitive Card — Generation Guide

Supplementary to `SKILL.md`. Defines how to generate shareable cognitive cards
after the user completes Phase 0 (KNOW) or requests one explicitly.

---

## Trigger Conditions

Generate a card when:
- User completes the quickstart profile (Phase 0 wrap-up)
- User says: "show my card" / "我的认知卡片" / "generate card"
- Weekly Digest completes and user has ≥7 days of data

Do NOT generate a card proactively mid-conversation.

---

## Data Sources (read from memory)

Pull from these memory tiers in order:

| Card Field     | Memory Tier | What to Extract                                     |
|----------------|-------------|-----------------------------------------------------|
| Name / Role    | core        | Identity: name, role                                |
| Decisions      | core        | Personality: decision style (e.g. "gut-first")      |
| Peak Energy    | core        | Personality: energy patterns (e.g. "10am–12pm")     |
| Superpower     | archive     | Coach insights: most-repeated strength observation  |
| Blind Spot     | archive     | Coach insights: most-repeated friction pattern      |
| Growth Edge    | working     | Most active growth area or current challenge        |

If a field has no data yet, use `"..."` as placeholder — never fabricate.

---

## Card Formats

### 1. Minimal (default — use this first)

```
┌─────────────────────────────────┐
│  🧠 Cognitive Card               │
│                                 │
│  {Name} · {Role}                │
│                                 │
│  ⚡ Decisions : {decision_style} │
│  🔋 Peak      : {peak_energy}   │
│  💪 Strength  : {superpower}    │
│  🫣 Blind spot: {blind_spot}    │
│  🌱 Growing   : {growth_edge}   │
│                                 │
│  sage-cognitive v0.1.0          │
└─────────────────────────────────┘
```

Rules:
- Fixed width: 35 chars inside border
- Values: ≤20 chars, trim with "…" if longer
- No company name, no email — privacy-safe by default

### 2. Narrative (叙事版)

3–4 sentences written as a perceptive friend describing the user.
Tone: warm, specific, grounded in observed behavior — not flattery.

Template:
> {Name} is a {role} who leads with {decision_style} and hits their stride
> around {peak_energy}. Their real edge is {superpower} — people feel it before
> they name it. The thing they're still learning to work with: {blind_spot}.
> Right now they're pushing on {growth_edge}.

### 3. Comparison (对比版 — requires ≥2 card snapshots in archive)

```
┌──────────────────────────────────────┐
│  🧠 Growth Snapshot · {date_range}    │
│                                      │
│  Decisions : {v1} → {v2}            │
│  Energy    : {v1} → {v2}            │
│  Strength  : {v1} → {v2}            │
│                                      │
│  New this period: {new_observation}  │
│                                      │
│  sage-cognitive v0.1.0               │
└──────────────────────────────────────┘
```

Use "→" to show change. If unchanged, show only current value (no arrow).

---

## Update Rules

- First card: generate immediately after Phase 0 completes
- Subsequent updates: only after ≥7 days of new data since last card
- On update: prepend "Changed: ..." or "New: ..." to highlight deltas
- Archive each snapshot with timestamp before overwriting

---

## Generation Prompt (for AI)

When generating a card, run this internal sequence:

1. Load core memory → extract Name, Role, decision_style, peak_energy
2. Scan archive memory → find the observation with highest repetition count
   for strength; find the observation tagged as friction or blind spot
3. Load working memory → find the most recently active growth item
4. Fill the Minimal template; if any field is missing, use "..."
5. Output the card in a code block so it renders as monospace (easy screenshot)
6. Ask: "Want the narrative version too?" — one follow-up, no pressure

---

## Privacy Rules

- Never include: email, company name, manager names, project code names
- Never include: specific financial or personnel data
- Safe to include: first name, generic role title, behavioral observations

---

## Brand Footer

Always end with: `sage-cognitive v0.1.0`
This is the growth flywheel anchor — visible in every shared screenshot.
