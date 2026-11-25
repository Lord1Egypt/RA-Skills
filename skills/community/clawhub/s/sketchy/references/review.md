# Review

Read before you report an artifact as done. After writing the code you see what you meant, not what rendered. So the work is checked twice: first by you against a list, then by a fresh agent that sees only the pictures and the brief.

## 1. Self-check (the building agent, before asking for review)

Run these in order. Fix and re-run until each passes.

```bash
node scripts/build.mjs deck.html                 # -> out/deck.html, self-contained
node scripts/lint.mjs out/deck.html              # 0 errors; read every warning
node scripts/shoot.mjs out/deck.html             # -> out/shots/deck/slide-01.png ... contact-sheet.png
```

Then open `contact-sheet.png` and every slide image and check:

| Check | Look for |
|---|---|
| Point | each title states a point; one idea per page; nothing a reader must decode |
| Protagonist | one picture, number or chart per page; nothing competes with it |
| Red | exactly one red thing per page; no red used as decoration |
| Collisions | text crossing lines, labels touching, stamps covering figures, corner overlays hitting content |
| Budget | at most 40 words of body text and 6 bullets per slide |
| Numbers | units on every figure, a benchmark beside every result, a source line, bars from zero, distortions disclosed |
| Honesty | no example figures left from the template, no placeholder, `—` only with a note |
| Type | Caveat for words, Courier Prime for figures; no third face; nothing under 20 px on a slide |
| Line grammar | plan dashed, record solid; at night, gold for computed, blue for benchmark |
| Voice | deadpan, no hype words, no exclamation marks outside red-pen notes |
| Phone | the 390 x 844 shot of slide 1 (or the page) has no sideways scroll and readable text |
| Slop | nothing from the slop list in [style-dna.md](style-dna.md) |

Re-shoot only what changed. When the list passes, ask for the review.

## 2. What the reviewer gets

| Give | Never give |
|---|---|
| absolute paths to `contact-sheet.png` and every `slide-NN.png` (or `page-*.png`) | the HTML, CSS or JS |
| the 390 x 844 shot | your build history or reasoning |
| the brief: audience, the one sentence, the decision, language, output, where each number comes from | your own opinion of the work |
| the prompt below, filled in | earlier review scores |

The reviewer must be a new agent with image reading and an empty context. Ask it for review only: it changes no files and starts no agents of its own. If no such agent is available, run section 3 yourself on the images, and write "not independently reviewed" in your report.

## 3. The prompt to hand the reviewer

```text
You are reviewing a finished artifact made with "sketchy", a skill that draws slides,
lessons and reports as pages of a pencil sketchbook. You did not make it. You get only
screenshots and the brief. Do not edit files. Do not start other agents.

The intended look: cool blue-gray paper (night theme: night-blue paper), graphite lines
that look hand-drawn (doubled strokes, hatching, slight wobble), one red pencil mark per
page for the one thing that matters, pastel colored pencils for data, handwriting for
words, typewriter type for every number, and postal props (stamps, slips, postmarks,
postcards). Dashed lines are plans and estimates, solid lines are what happened.

BRIEF
Audience: <who>
The one sentence they must remember: <sentence>
What they decide or do afterwards: <decision>
Output and language: <live deck | PDF | PPTX | video>, <language>
Numbers and sources: <figures and where each comes from>

SCREENSHOTS (open the contact sheet first, then every page)
<absolute path>/contact-sheet.png
<absolute path>/slide-01.png ... slide-NN.png
<absolute path>/slide-01-390x844.png

Score each axis from 1 to 10 with the anchors given. When torn between two scores, give
the lower one. Then:
1. List concrete fixes ordered by impact, at most 8, each as
   "[p. N] what you see -> what it must look like after the fix".
   If a fix adds something, say what to remove to make room.
2. Name the single most important change.
3. Name one thing to keep because it carries the work.
4. Say what you could not judge from still images (motion, sound, timing).

<paste the axes and anchors table from section 4 here>

Answer in this format:
SCORES  Point n | Hierarchy n | Craft n | Honesty n | Voice n | Restraint n
FIXES   (ordered list)
MOST IMPORTANT  (one sentence)
KEEP  (one sentence)
NOT JUDGED  (one line)
```

## 4. Axes and anchors

| Axis | Asks | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|
| **Point** | Does each page say one thing, and does the title say it? | titles are topics; pages mix two or three ideas | most titles are points; a few pages carry two ideas | every page has one idea and a title that states it | the deck could be retold from its titles alone |
| **Hierarchy** | Does the eye land on the right thing first? | everything the same weight, or the wrong thing biggest | the protagonist is visible but competes with labels or props | one protagonist per page, read in the intended order | the order of reading is obvious at thumbnail size |
| **Craft** | Does it look drawn on paper, aligned, free of collisions? | flat fills, overlaps, clipped text, template look | the pencil look holds, with collisions or uneven alignment on some pages | consistent hand, clean alignment, no collisions | every prop sits on purpose; it could pass as a real sketchbook |
| **Honesty** | Are numbers complete, sourced and fair? | numbers without units or sources, bars not from zero, invented-looking figures | units present; benchmarks or sources missing in places | every result has a unit, a benchmark and a source; distortions disclosed | the reader can audit every figure from the page itself |
| **Voice** | Is the writing deadpan, plain and short? | hype, exclamation marks, filler phrases | plain but wordy or generic | short, concrete, dry where it helps | lines a reader would quote; jokes beside numbers, never in them |
| **Restraint** | Is anything there that does not need to be? | decoration everywhere, two reds, crowded pages | some extra lines, props or words to cut | nothing left to remove without losing meaning | every mark earns its place; empty paper does work |

Fixed rules for the reviewer: a page with overlapping or clipped text caps Craft at 4. A figure without a unit or source caps Honesty at 6. A visible template leftover caps Honesty at 4. Two red marks on one page cap Restraint at 6.

## 5. After the review

1. Fix in the reviewer's order, starting with the most important change. Turn vague notes ("crowded") into concrete edits (cut a bullet, enlarge the chart, move the stamp).
2. Reject a fix only with a one-line reason (it would break a user's brand rule, or a rule in SKILL.md). Note the "keep" item and do not polish it away.
3. Lint, re-shoot only what changed, and run a **second round** with a new reviewer and only the new screenshots. Never pass the first scores along.
4. **Stop after two rounds.** If an axis is still under 8, do not loop: report the scores and the remaining gaps plainly ("Craft 7: the chart labels on p. 6 still crowd the bars at phone width").

The final report states the last scores per axis, the round count, and every gap that remains.
