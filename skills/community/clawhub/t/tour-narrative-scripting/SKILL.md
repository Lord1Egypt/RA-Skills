---
name: tour-narrative-scripting
version: 1.0.0
description: Write narration scripts for product tour videos. Produces dual-audience
  narration (technical + non-technical), timed to screen segments, with hooks and
  CTAs. Used by Sara for product tour content.
metadata:
  openclaw:
    emoji: 🎬
---

# Skill: Tour Narrative Scripting

**Owner:** Sara  
**Version:** 1.0  
**First used:** 2026-03-24 (Reddi Agent Protocol dual-audience tour)

---

## What This Skill Does

Produces dual-use copy from a single tour spec input:

- **Captions** — short labels for slideshow display (≤12 words each)
- **Narration** — 1–2 sentences per step for TTS voiceover

The common failure mode is writing captions optimised for the slide and then discovering the narration needs a full rewrite. This skill avoids that by treating both registers as a single writing unit from the start.

---

## Input

A tour spec (from Phase 1 / Archie) with:
- Step table (ID, title, URL path, audience tag, interaction)
- Narration arc (3–4 sentence story summary)

---

## The Dual-Register Pattern

```
Caption (slideshow):  ≤12 words. Noun phrase or fragment OK. No audience assumptions.
Narration (TTS):      1–2 full sentences. Active voice. Natural spoken rhythm. Builds on caption.
```

Caption and narration serve the same step but speak to different contexts:
- The caption is read in silence on a screen. It must orient the viewer instantly.
- The narration is heard, not read. It must sound like a person talking, not a manual.

Write both at the same time for every step. Do not finish all captions then write all narration — the registers will drift.

---

## Output Format

```markdown
## Step 03 — Agent Marketplace [All]
**Caption:** Browse 11 registered specialists — filter by model, rate, reputation
**Narration:** The agent index lists every registered specialist with their model, per-call rate, and on-chain reputation score. No curation, no approval — registration is permissionless.
```

One block per step. Steps numbered with zero-padding (01, 02 …). Audience tag in brackets at the end of the heading.

---

## Examples

### Good

```
Caption:    "Two paths. One protocol."
Narration:  "Whether you're offering compute or hiring it, the protocol is the same.
             On-chain escrow, blind reputation scoring, and pay-per-call — no monthly
             subscriptions, no gatekeepers."
```

Why it works: Caption is a hook, not a description. Narration expands the idea rather than restating what's visible. Both work independently.

### Bad

```
Caption:    "The landing page shows the product"
Narration:  "This screenshot depicts the landing page of the Reddi Agent Protocol application."
```

Why it fails: Caption is a description of the screenshot rather than a statement about the product. Narration is stiff and reads as a label, not a voice. Neither would pass a spoken-aloud test.

---

## Audience Tagging Rules

| Tag | Who you're writing for | Pronoun use |
|---|---|---|
| `[All]` | Someone who doesn't know which path they're on yet | "you" is fine; avoid "as a specialist" or "as an orchestrator" |
| `[Specialist]` | Someone offering compute / running agents | "you" = specialist — "Your Ollama instance", "Your rate" |
| `[Orchestrator]` | Someone hiring compute / submitting jobs | "you" = orchestrator — "Your brief", "Your escrow" |

Never mix audience assumptions in a single caption. If a step is `[All]`, the caption must make sense to someone on either path.

---

## Timing Checks

Before finalising, read every step aloud:

| Element | Target duration | Action if over |
|---|---|---|
| Caption | ≤3 seconds | Cut words — fragment is fine |
| Narration | 8–15 seconds | Split into two steps rather than speeding TTS |

If narration regularly runs over 15 seconds, the step is trying to carry too much — break it up or move explanation to an earlier step.

---

## Common Mistakes

**Narration describes what's visible.**  
Cut "Here we can see…" and "This shows…" entirely. The viewer can see the screenshot. Narration should describe what it *means*, not what it *is*.

**Over-explaining mechanics in every step.**  
Establish the core protocol concept once (ideally in steps 1–3). After that, reference it briefly ("the same escrow mechanism") rather than re-explaining from scratch. Repetition reads as distrust of the audience.

**Losing the narrative thread.**  
Each step should feel like the next sentence of the same story. Read the narration for all steps consecutively, ignoring the screenshots. Does it flow as a coherent 60–90 second monologue? If it reads as disconnected bullet points, rewrite for continuity.

**Pronoun drift in dual-audience tours.**  
An `[All]` step that accidentally uses "your agent job" (orchestrator framing) alienates specialists. Check every pronoun in `[All]` steps against the audience neutrality rule.

**Saving narration for after captions are done.**  
Captions written purely for the eye often use fragment logic ("Filter by model. Rate. Reputation.") that needs rewriting for the ear ("You can filter by model, rate, or reputation score."). Draft both together; adjust one register, then the other.

---

## Checklist Before Handoff to Kit (Phase 3)

- [ ] Every step has both a caption and a narration line
- [ ] All captions ≤12 words
- [ ] All narration passes the spoken-aloud timing test (8–15s)
- [ ] `[All]` steps contain no audience-specific pronouns
- [ ] Narration arc is traceable across all steps end-to-end
- [ ] Output formatted as step blocks (see Output Format above)

---

## Related

- Playbook: `playbooks/product-tour/PLAYBOOK.md`
- Upstream: Phase 1 spec from Archie
- Downstream: Phase 3 screenshot capture by Kit (captions used as filename hints); Phase 4 video narration by Finn (narration fed directly to TTS)
