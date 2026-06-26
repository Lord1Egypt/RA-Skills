# Chat Confirmation Affordances

## Purpose

This file defines a platform-neutral interaction pattern for chat confirmations, quick replies, and button-ready choices.

It solves a practical problem:

- the skill may know that user confirmation is needed
- but the chat still becomes verbose or hard to act on

The solution is to present short, tap-friendly choices that can work as:

- real buttons or chips on platforms that support them
- numbered options in plain chat
- short reply codes in text-only environments

## Core rule

Whenever the skill needs the user to choose, prefer a button-ready confirmation block instead of a long explanatory paragraph.

## Button-ready format

Use a compact structure:

1. one short guidance sentence
2. `2-4` choices only
3. recommended choice first when possible
4. each choice label should be short enough to tap or copy easily
5. also provide a plain-text fallback reply

## Choice design rules

Good labels:

- `只要结论`
- `先做样本`
- `分阶段`
- `一次做完`
- `先给计划`
- `只读分析`
- `继续`
- `展开`

Avoid:

- long sentence labels
- too many options
- labels that overlap heavily in meaning

## Maximum choice count

Default maximum:

- `4` choices for mobile or lightweight chat
- `3` choices is preferred when the decision is simple

If more than 4 choices are needed, split them into a second step instead of showing them all at once.

## Recommended confirmation categories

### Routing confirmation

Use when the user should choose:

- Ask
- Plan
- Craft
- Expert

### Need calibration

Use when the user should choose:

- only judgment
- sample
- staged progress
- full delivery

### Scope confirmation

Use when the user should choose:

- top 3-5 materials
- material list only
- grouped summary
- full report

### Code scope confirmation

Use when the user should choose:

- diagnosis only
- read 1-3 files
- fix one point
- staged refactor

### Test scope confirmation

Use when the user should choose:

- no tests
- minimal validation
- related tests
- full tests

### File safety confirmation

Use when the user should choose:

- read-only
- plan first
- duplicate first
- modify listed files

### Follow-up continuation

Use when the user should choose:

- continue
- expand
- switch mode
- conclusion only

## Fallback reply rule

Every button-ready block should still work as plain text.

Supported fallback forms:

- reply the number only
- reply the short label
- reply the compact code

Examples:

- `2`
- `先做样本`
- `1继续`
- `MPS`

## iMA guidance

In iMA Copilot, button-ready prompts should be especially short:

- one-line guidance
- up to 4 options
- default recommendation included

## Safety note

Button-friendly does not override safety gates.

If the user taps an unsafe option, the skill must still intercept and move to a safer flow.
