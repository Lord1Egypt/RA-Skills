---
name: sync-clearance-memo
description: >
  Use this skill when a music supervisor, sync licensing director, music publisher, or
  artist manager needs to evaluate and document the clearance path for a song placement
  in film, TV, advertising, video games, or branded content. Covers composition rights
  mapping, master rights identification, one-stop assessment, sample chain verification,
  territory and term analysis, and indicative fee estimation. Produces a DRAFT sync
  clearance memo for licensing-team review before any deal is negotiated or confirmed.
---

# Sync Clearance Memo

Evaluate the clearance path for a composition and master recording, then produce a licensing-ready DRAFT clearance memo documenting all rights holders, clearance complexity, and a recommended deal structure.

## Flow

1. **Song intake** — Ask for: song title, ISRC (if known), ISWC (if known), artist and recording name, and intended use description (media type, scene description or ad brief, territory, term, exclusivity level: Non-exclusive / Exclusive / First-negotiation, and placement tier: Background Instrumental / Background Vocal / Feature / Title). Confirm one item at a time if the user is unsure.

2. **Composition rights mapping** — Identify all songwriters and their share percentages. For each writer, identify the publisher or PRO-registered administrator, PRO affiliation (ASCAP / BMI / SESAC / SOCAN / PRS / APRA / GEMA / etc.), and best clearance contact. Flag any unknown or unregistered writer shares as Open Items.

3. **Master rights mapping** — Identify the master rights holder (major label, independent label, distributor-administered, or artist-owned). Confirm the documentation source used (label copy, distributor statement, artist agreement reference, or discogs/PRO database lookup). Flag any work-for-hire uncertainty, label co-ownership, or reversion-clause risk.

4. **One-stop assessment** — Determine whether a single entity controls both master and all publishing shares. Classify as one of:
   - **One-Stop** — single entity clears both master and composition; lowest friction.
   - **Near One-Stop** — one sub-publisher or co-writer share requires a separate approval.
   - **Multi-Party** — separate master and composition negotiations required.
   Assign a Clearance Complexity rating: **Low** (one-stop, clean rights) / **Medium** (near one-stop or known restrictions) / **High** (multi-party, unknown shares, or sample chain).

5. **Sample chain verification** — Ask whether the recording contains any sampled audio or interpolated melody. If yes: identify the sampled composition and master, their current rights holders, and whether an existing sample clearance is already in place. If the sample is uncleared, flag it as a **Blocking Issue** — placement must not proceed until the sample is cleared.

6. **Territory and term analysis** — Map the requested territory and term against known rights restrictions. Flag any reversion rights, option periods, geographic carve-outs (e.g., print rights excluded, streaming-only), or public domain status by territory. List all Known Restrictions.

7. **Indicative fee estimation** — Provide a fee range table based on use type (Background Instrumental / Background Vocal / Feature / Title), media type (Theatrical Film / Broadcast TV Series / Streaming Series / National Ad / Regional/Digital Ad / Social / Trailer), and term (Single Use / One Year / Three Years / In Perpetuity). Reference current market benchmarks from ASCAP, BMI, Music Publishers Association, and industry-standard sync rate guides. Label all estimates **INDICATIVE ONLY — subject to negotiation and rights-holder approval**.

8. **DRAFT memo assembly** — Compile all sections into the structured output below. Mark the document **DRAFT — NOT A LICENSE**. Include an Open Items list for any unresolved questions and an unsigned Licensing Team Review block.

## Key Rules

- Never represent the memo as a confirmed license, authorization to use, or legal opinion.
- Always flag incomplete rights information rather than assuming clearance is available.
- Mark every fee figure as INDICATIVE; never present ranges as final or binding quotes.
- If a sample is uncleared, always flag it as a Blocking Issue before any further placement steps.
- Do not log or disclose confidential deal terms shared by the user in the output document.
- Ask one clarifying question at a time during intake; do not front-load all questions in a single message.
- If ISRC or ISWC are unknown, proceed with available information and note the gap in Open Items.

## Output Format

```
SYNC CLEARANCE MEMO — DRAFT
Date: [YYYY-MM-DD]
Song: [Title] / ISRC: [code or "Unknown"]
Intended Use: [media type | placement tier | territory | term | exclusivity]
Prepared by role: [role only — no personal identifying data]

────────────────────────────────────────
1. COMPOSITION RIGHTS MAP
────────────────────────────────────────
Writer | Share % | Publisher / Administrator | PRO | Clearance Contact
[row per writer]
Flags: [unknown shares, unregistered writers, or "None"]

────────────────────────────────────────
2. MASTER RIGHTS MAP
────────────────────────────────────────
Rights Holder | Contact | Documentation Source | Notes / Flags

────────────────────────────────────────
3. ONE-STOP ASSESSMENT
────────────────────────────────────────
Classification: [One-Stop / Near One-Stop / Multi-Party]
Clearance Complexity: [Low / Medium / High]
Rationale: [1–2 sentences]

────────────────────────────────────────
4. SAMPLE CHAIN
────────────────────────────────────────
Sampled Work | Original Artist | Composition Rights Holder | Master Rights Holder | Clearance Status | Flag
[row per sample, or "No samples identified"]

────────────────────────────────────────
5. TERRITORY AND TERM FLAGS
────────────────────────────────────────
[Known restrictions, reversion dates, geographic carve-outs — or "None identified"]

────────────────────────────────────────
6. INDICATIVE FEE RANGE (NEGOTIATION REFERENCE ONLY — NOT BINDING)
────────────────────────────────────────
Use Type | Media | Term | Master Range (USD) | Sync (Pub) Range (USD) | Total Est. Range | Basis
[row per combination requested]

────────────────────────────────────────
7. OPEN ITEMS AND QUESTIONS
────────────────────────────────────────
1. [item]
2. [item]

────────────────────────────────────────
8. LICENSING TEAM REVIEW
────────────────────────────────────────
Reviewed by: _________________________ Date: __________
[ ] Cleared to Begin Negotiation
[ ] On Hold — See Open Items Above
[ ] Blocked — Uncleared Sample or Rights Issue
```

## Feedback

If the user expresses an unmet need, limitation, or dissatisfaction with this skill, surface the contribution link only at that moment:
https://github.com/archlab-space/Open-Skill-Hub/issues
