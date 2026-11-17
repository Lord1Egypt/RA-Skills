---
name: wedding-toast-architect
description: "Use when asked to write, revise, time, or safety-check a wedding speech or toast (best man, maid of honor, parents, friends) — builds a role-tuned 5-part outline with per-section word budgets, estimates speaking time at 3 paces, and red-flag scans drafts for the classics that bomb (ex mentions, drunk stories, divorce jokes, inside jokes, backhanded 'finally settled' compliments) with CUT/SOFTEN/CHECK verdicts."
version: 1.0.1
author: Denis Voronin
license: MIT
tags: [wedding, speech, toast, public-speaking, writing]
---

# Wedding Toast Architect

## Overview
Every year ~2 million US couples marry; nearly every wedding hands a friend or
parent a microphone and 3 minutes they are unprepared for. The result is
predictable: rambled inside jokes, accidental ex mentions, drunk-story
confessions, "ball and chain" humor in front of both grandmothers — and a
regretful speaker replaying it for years.

This skill treats the toast as a buildable artifact with a spec:

1. **build** — questionnaire → 5-part outline with word budgets per section,
   tuned by role (best man / maid of honor / parent / friend / sibling).
2. **scan** — draft → red-flag report: 16 pattern classes with CUT / SOFTEN /
   CHECK verdicts, protected-name enforcement, length vs target, Flesch
   readability for the ear, and long-sentence detection.
3. **time** — words → minutes at 110/135/150 wpm.

Pure Python stdlib. Works offline. No draft text ever leaves the machine.

## When to Use
- "I'm best man in 3 weeks and haven't written anything" (any speech-role panic)
- "Is this speech okay? Be honest." — paste draft, run scan
- "How long will 500 words take to deliver?"
- Parent-of-the-bride/groom, maid of honor, sibling, close-friend toasts
- Rehearsal-dinner speeches, engagement-party toasts (same structure, shorter)

**Don't use for:** vows (intimate, couple-authored — different genre), ceremony
readings (pre-existing texts), professional MC scripts, eulogies (see note:
structure overlaps but tone rules differ — this tool would over-flag).

## How It Works — Numbered Steps
1. Interview the speaker briefly: role, couple names, partner name, years known,
   1-2 story candidates, 1-2 qualities those stories prove, target minutes
   (default 3).
2. Build the skeleton:
   ```
   python3 scripts/toast_architect.py build --role best-man \
       --couple "Alex & Sam" --partner Sam --years-known 9 \
       --stories "rafting capsize; chili cook-off disaster" \
       --qualities "loyal, calm in chaos" --minutes 3
   ```
   Output: 6 sections (hook / who / story1 / story2 / partner / toast) with
   per-section word budgets and second-durations at 135 wpm.
3. Draft against the budgets — one story told well beats three told fast.
4. Scan the draft:
   ```
   python3 scripts/toast_architect.py scan --draft draft.txt \
       --protected "Jordan,Riley" --minutes 3
   ```
   Fix every CUT finding. Decide on SOFTENs. Read CHECKs aloud.
5. Time the final cut: `python3 scripts/toast_architect.py time --words 410`.
6. Rehearse 3× out loud, standing, holding a full glass. Print 18pt+,
   one section per index card, cards numbered.

## What the Scanner Catches (16 pattern classes)
| Class | Severity | Why |
|---|---|---|
| ex-partner references | CUT | exes never belong in toasts |
| drunk/intoxication stories | CUT | all-ages room |
| strip club / vegas | CUT | bachelor content bombs |
| divorce / "ball and chain" jokes | CUT | reads as doubt about the marriage |
| "finally settled" backhanded frames | CUT | insults both partners |
| pregnancy mentions | CUT | not your news to announce |
| profanity | SOFTEN | shrinks the room |
| money / prenup jokes | SOFTEN | divides the room |
| looks-only compliments | SOFTEN | compliment choices instead |
| dating-app jokes | CHECK | only if couple approves the story |
| inside-joke markers `( ... )` | CHECK | translate or cut |
| religion assumptions | CHECK | match the couple's faith |
| "However" early digs | CHECK | usually introduces a slight |
| cliché openers | SOFTEN | "Good evening, for those who don't know me..." |
| filler words on paper | SOFTEN | filler out loud too |
| protected names | CUT | exes, estranged, deceased, private people |

Scoring: 100 − 18·CUT − 7·SOFTEN − 3·CHECK, floored at 0. Ship at ≥85.

## Common Pitfalls
1. **Treating it as a comedy set.** Funny is fine, funny-only flops. The room
   wants warmth + one laugh, not ten laughs and no heart.
2. **Three stories in three minutes.** Budget says ~120 words for story1 —
   that's ONE story with a scene, complication, payoff.
3. **Ignoring the partner section.** Maid-of-honor speeches about the bride
   with 10 seconds for the groom read as a rejection of the marriage. Budget
   14-24% of words for the partner (role-dependent).
4. **Reading from a phone.** Lock screen, glare, notifications. Index cards.
5. **Not timing it.** 500 words = 3.7 min normal, 4.5 min with adrenaline
   pauses. The couple scheduled you for 3.
6. **Trusting the scanner as the only pass.** It catches patterns, not tone.
   The final gate is the question printed at the end: *would you say this to
   the couple's face with both grandmothers listening?*
7. **Writing the night before.** The outline takes 20 minutes; the stories
   need a week of "which detail do I keep" walks.

## Example
```
Speaker: best man, 9 years of friendship, worried about an ex mention.
$ toast_architect.py build --role best-man --couple "Alex & Sam" --partner Sam \
    --years-known 9 --stories "rafting capsize; chili cook-off disaster" \
    --qualities "loyal, calm in chaos" --minutes 3
→ 405-word budget: hook 48 / who 40 / story1 121 / story2 89 / partner 56 / toast 48

$ toast_architect.py scan --draft draft.txt --protected "Jordan" --minutes 3
→ 5 CUT / 2 SOFTEN / 1 CHECK, safety score 0/100:
  CUT  ex-partner reference (1x)
  CUT  drunk/intoxication story (1x)
  CUT  divorce/pessimism joke (1x)
  CUT  'finally settled' framing (1x)
  CUT  protected name 'Jordan' (1x)
  SOFTEN money joke, cliché opener   CHECK inside-joke parenthetical

Rewrite fixes all CUTs; rescan: 92/100 — ready for rehearsal.
```

## References
- `references/toast-craft.md` — structure theory, role budget rationale,
  delivery-day protocol (mic, glass, cards), and the repair guide for each
  flag class with before/after rewrites.
- `references/scanner-patterns.md` — the full pattern table with regexes,
  severity weighting, known false-positive notes, and how to extend.
