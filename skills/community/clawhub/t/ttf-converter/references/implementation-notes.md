# Implementation notes

This file exists so another AI can quickly understand not just the visible rules, but the practical logic that makes the skill produce a high-success vertical font result.

## Target standard

The goal is not merely “a font was converted”.
The goal is: after following this skill, another AI should be able to produce a vertical font that reaches roughly 95%+ user satisfaction in the common workflow with minimal blind trial-and-error.

That means the skill must capture:

- grouped glyph logic
- stable default parameters
- delivery order
- stop conditions
- tuning order
- known failure modes
- practical tool entry points

## Why the workflow starts with a horizontal preview

Because many failures are not vertical-layout failures at all.
Sometimes the source font itself is missing:

- punctuation
- Latin letters
- digits
- quote variants

Or the source font is simply a poor candidate.
If the original font is already broken, vertical conversion just wastes time.

## Why grouped processing matters

A high-satisfaction result does not come from one global transform.
Different glyph classes want different behaviors:

- Chinese body glyphs want rotation
- Latin / digits want center alignment without rotation
- single-point punctuation wants right-upper placement and smaller scale
- paired punctuation wants horizontal preservation and middle-line alignment
- `「」『』` wants left/right edge behavior, not generic centering
- dash / ellipsis wants horizontal preservation and middle-line return

If an agent forgets this and uses one transform for everything, output quality collapses immediately.

## Why single-point punctuation is its own trap

Single-point punctuation often fails because the agent changes the right concept in the wrong coordinate system.
The working rule is:

1. preprocess in horizontal coordinates
2. scale
3. rotate 90° clockwise into the vertical result

If the output keeps drifting visually left when the agent thinks it is moving right, first suspect the preprocessing direction was misunderstood.
Do not keep increasing numbers blindly.

## Why `“”‘’` are replaced

Keeping curly quotes often produces unstable and visually awkward vertical results.
The proven rule is to replace them with `「」『』`, then apply the dedicated side-placement logic.

This raises consistency and reduces repeated special-case debugging.

## Why `「」『』` must not be simply centered

A centered result often looks wrong even if mathematically neat.
The user-validated target is:

- `「` / `『` close to the right boundary
- `」` / `』` close to the left boundary
- all staying inside the Han-character frame

The visual constraint beats blind centering.

## What “95% satisfaction” means in practice

In practice, this skill should get most of the way there if it succeeds on these visible checks:

- Chinese body text reads naturally in vertical flow
- Latin / digits no longer drift outside the text column
- single-point punctuation is compact and near the upper-right area
- quotes / brackets / book-title marks do not break the character frame
- dash / ellipsis sit on the correct middle line
- the user sees a coherent preview before final delivery

The last 5% often comes from source-font-specific micro-adjustment, not from rewriting the whole method.

## Tuning philosophy

When the user says something is off:

- do not restart from zero
- do not rewrite all groups
- find the affected group
- tweak only that group
- preserve all already-correct groups

This is the difference between controlled iteration and random regression.

## Practical minimum toolchain

The skill is most effective when these are available:

- `fontTools`
- `Pillow`

The script layer in `scripts/` gives a practical execution path so the agent does not need to reinvent these pieces every time.

## Parameterization matters

A high-satisfaction default is good, but real fonts vary.
So the skill should not force every future adjustment into source-code edits.

That is why the bundled builders now accept a JSON config override.
This gives another AI a safer way to tune:

- single punctuation placement
- corner-quote left/right bounds
- dash / ellipsis scale
- Latin / digit scale
- overall target center

The ideal behavior is:

- keep the default config for most fonts
- only override the smallest relevant group when a specific font deviates
- record successful overrides as real cases so later agents learn faster

The bundled real-case notes are important because they convert abstract rules into proven operational memory. When a new font resembles a known successful case, start from that case’s defaults before inventing a new path.

## Current executable scope

The skill now includes two bundled executable paths:

- **glyf-based TTF** builder
- **CFF-based font** builder

The CFF path preserves original CharString `private` and `globalSubrs` metadata so save-time failures like `nominalWidthX` are less likely.

This means another AI can now follow one skill and still choose the correct executable path based on font kind, instead of treating CFF as a purely theoretical appendix.

## Do not lose these ideas when evolving the skill

If the skill gets refactored later, preserve these invariants:

1. preview first
2. grouped processing
3. full-font handling, not test-sentence hacks
4. curly-quote replacement
5. side-based handling for `「」『』`
6. user confirmation before final TTF delivery
7. glyf and CFF should both have executable paths, not just documented theory
8. one-shot automation must still preserve the preview-first artifact order
