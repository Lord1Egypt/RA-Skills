# Critique

Load when: inspecting, reviewing, auditing, or giving design feedback.

Critique starts with observation, not taste language. Name what is visible, explain the user impact, then give the better direction.

If you cannot see the rendered output, say that the critique is inferred from code.

Input priority:

1. Screenshot or rendered browser view.
2. Live URL or running app.
3. Component/page file plus inferred render.
4. Description only, with assumptions stated.

## Output Shape

Use this structure unless the user asks for a shorter review:

```md
## Context
[What this is, who it is for, task/emotional context, register, likely facets.]

## First Look
[Direct reaction grounded in visible facts.]

## What Earns Its Place
[2-3 specific strengths that serve the user or the intended impression.]

## What Does Not Earn Its Place
[Unearned elements, redundancy, visual noise, generic AI tells.]

## Reflex Check
[Category defaults or second-order aesthetic defaults the work is falling into.]

## Craft Faults
[Hierarchy, spacing, alignment, typography, color, container strategy, icons, motion, states.]

## Human Touch
[Where the work feels cared for, or where it feels sterile, indifferent, or incomplete.]

## Top Moves
1. [Highest-impact structural or IA change.]
2. [Highest-impact behavioral/state change.]
3. [Highest-impact visual/craft change.]
```

For the better direction in each move, pull from proven moves in `patterns.md` rather than inventing generic advice — name the specific pattern (phases over a flat list, scoreboard over sibling metric cards, expanded target area, layered reveal) that fixes what you observed.

## Lenses

### Structure

- Is the current job obvious?
- Is there one primary action or subject?
- Is complexity staged?
- Does the architecture match the user's mental model?
- Can any whole section, column, card, label, or action leave?

### Visual Craft

- Does visual weight match importance?
- Are type roles clear and restrained?
- Is spacing rhythmic rather than default?
- Are edges optically aligned?
- Does color have assigned work?
- Do strokes, shadows, and containers clarify grouping or add noise?
- Are icons consistent in family, stroke, size, and meaning?

### Register Fit

- Brand: does it have a point of view without filler?
- Product: does it feel trustworthy, familiar, and efficient?
- Mobile/native: does it respect platform expectations?
- Dashboard/tool: can users scan, compare, and act repeatedly?
- Does the result come from this product's scene and character, or from the category's default aesthetic?

### States And Care

- Empty, loading, error, disabled, success, focus, hover, active.
- Long text, small text, many items, no items.
- First-time use, recovery, permission, and edge cases.
- Copy that respects the user's emotional state.

## Severity

Order issues by user impact:

1. Structural: wrong model, wrong flow, wrong hierarchy.
2. Behavioral: unclear feedback, missing state, broken interaction.
3. Visual: type, color, spacing, alignment, motion polish.

Do not spend a critique on color if the architecture is wrong.
