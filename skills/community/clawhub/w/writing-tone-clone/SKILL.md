---
name: writing-tone-clone
description: Clone someone's writing tone from sample text and produce a ready-to-use voice skill. Provide writing samples (diary, blog posts, emails, social posts) and get a documented voice profile plus a deployable SKILL.md that replicates that person's exact writing style. Triggers on "write like me", "clone my writing style", "replicate my voice", "capture my tone".
author: Chris Couriard
version: 1.0.1
---

# Writing Tone Clone — Personal Writing Style Replication

Clone someone's writing tone from sample text and produce a deployable voice skill.

## What This Skill Does

Given one or more samples of someone's real writing, this skill:

1. Analyses the text across 8 linguistic dimensions
2. Produces a documented voice profile
3. Writes a deployable `[name]-voice` SKILL.md the person can use immediately

The output is precise and specific — not generic labels like "conversational tone." Every finding is evidenced from the actual text.

---

## Step 1 — Collect Samples

Ask for writing samples if not already provided. The more the better. Ideal sources:

- **Diaries or journals** — most authentic; unguarded, natural voice
- **Personal emails or messages** — informal register
- **Blog posts or social captions** — may be more polished but still useful
- **Voice note transcripts** — captures spoken cadence

Minimum viable input: ~500 words of unedited personal writing.

If multiple sample types are available, use all of them and note which patterns appear across all types (most reliable) vs. only in one context.

---

## Step 2 — Run the Analysis

Analyse the samples across these 8 dimensions. For each dimension, **quote directly from the text** as evidence.

### Dimension 1 — Sentence Structure & Length

- What is the typical sentence length? (Short/punchy vs. long/flowing)
- Do sentences vary in length or stay consistent?
- Are sentences mostly simple, compound, complex, or mixed?
- Does the writer use fragments or run-ons intentionally?

### Dimension 2 — Voice & Register

- Formal or casual? Where on the spectrum?
- Does the writer address the reader directly ("you")? How often?
- First person throughout, or does it shift?
- Is there self-awareness / self-commentary in the writing?

### Dimension 3 — Humour & Tone Markers

- Is there humour? What kind — dry, slapstick, self-deprecating, absurdist?
- Are there ironic asides or understatements?
- Where does the writer make jokes and how are they constructed?
- Is the humour visible in punctuation choices (brackets, dashes, ellipsis)?

### Dimension 4 — Rhythm & Pacing

- Does the writing accelerate into action scenes and slow for reflection?
- Are there deliberate one-line beats for emphasis?
- How are lists used — and do they feel clinical or casual?
- Does punctuation drive rhythm (em dashes, semicolons, commas)?

### Dimension 5 — Vocabulary & Word Choice

- What is the reading level? (Grade school / conversational / formal?)
- Does the writer avoid jargon, or use it naturally?
- Are there recurring words or phrases?
- Are there conspicuous word choices that feel very "them"?
- What words would they never use?

### Dimension 6 — Emotional Register

- How openly does the writer express emotion?
- Are feelings stated directly or implied through action/observation?
- How does the writer handle vulnerability — lean into it or downplay it?
- Is positivity, negativity, or neutrality dominant?

### Dimension 7 — Structural Habits

- How does the writer open paragraphs and entries?
- How do they close or trail off?
- Are transitions used? What kind?
- Do they use bullet points, or resist structure?
- How much scene-setting vs. getting-to-the-point?

### Dimension 8 — What They Don't Do

This is often the most useful dimension. Note:

- Topics, words, or phrases they avoid entirely
- Rhetorical devices they never use (metaphors? hyperbole? statistics?)
- Sentence types they don't write
- Emotional registers they don't express
- Things a generic AI would write that this person never would

---

## Step 3 — Produce the Voice Profile

Compile the 8 dimensions into a single Voice Profile document. Format:

```
# [Name] Voice Profile

## Overview
[2-3 sentence summary of the voice — something that would let a stranger immediately recognise it]

## The 8 Dimensions
[Each dimension as a headed section with findings + quoted evidence]

## Quick Reference Rules
[10-15 bullet points: the most important things to get right when writing in this voice]

## What To Avoid
[Explicit list of things that would break the voice]

## Sample Phrases
[5-10 phrases or sentence types that are distinctly this person]
```

---

## Step 4 — Write the Voice Skill

Using the Voice Profile, write a deployable SKILL.md for this person's voice. The skill should:

- Have a clear description triggering on "write in [name]'s voice", "sound like [name]", etc.
- Load the voice profile as a reference document
- Instruct the agent to follow the Quick Reference Rules strictly
- Include 2-3 worked examples showing the voice applied to different content types
- Include the "What To Avoid" section prominently

Save to: `skills/[name]-voice/SKILL.md`
Save the voice profile to: `skills/[name]-voice/references/voice-profile.md`

---

## Notes on Quality

- **Evidence over assertion.** Never say "conversational tone" without quoting the text that shows it.
- **Specific over general.** "Uses em dashes to insert dry asides" beats "informal punctuation."
- **Negative space matters.** What someone doesn't write is as defining as what they do.
- **Context-dependent.** Note if a pattern only appears in certain contexts (e.g. humour only in personal writing, not professional).
- **Iterate if possible.** If the person can provide feedback on a first attempt, use it to refine the profile.
