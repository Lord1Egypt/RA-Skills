# Query flow for UI inspiration retrieval

Use this reference when the user wants to search, review, compare, or retrieve archived UI inspiration from the library.

## Goal

Turn the inspiration database into a practical visual search system.

A successful retrieval should help the user:
- find the right references quickly,
- see the actual images again,
- compare a few strong options,
- make a design decision with minimal friction.

## Retrieval modes

### Mode A — Exact lookup
Use when the user refers to a known title, a recent image, or a specific previously seen item.

### Mode B — Structured filter lookup
Use when the query maps cleanly to fields such as platform, page type, style tags, component tags, or use case.

### Mode C — Keyword retrieval
Search free-text fields such as:
- `Summary`
- `Highlights`
- `Source`
- `Name`

### Mode D — Visual-goal retrieval
Use when the user asks for a purpose rather than a strict field match, such as:
- suitable for cover design
- suitable for a hero section
- AI-style key visual
- suitable for a video cover

In this mode, infer a retrieval bundle instead of relying only on exact field matches.

## Query mapping examples

Use these examples as lightweight intent-to-retrieval mappings:

- `find AI-style hero references`
  - prefer `AI-native`, `Tech-forward`, `Premium`
  - prefer landing-page, home, or hero-like references when identifiable
  - prioritize bold first-screen composition and strong headline/CTA patterns

- `find dark dashboard references`
  - prefer `Dashboard`
  - prefer `Dark Theme`
  - boost dense but readable data layouts

- `find onboarding references`
  - prefer `Onboarding`
  - boost `Stepper`, `Progress Indicator`, `Card-based`

- `which ones are suitable for a cover?`
  - treat as visual-goal retrieval, not exact taxonomy lookup
  - boost high-clarity, high-contrast, strong focal-point references
  - prefer images that still read well at a glance

- `find enterprise list-page references`
  - prefer `List`, `Data Table`, `B2B`, `Enterprise`
  - boost filter-heavy and table-oriented layouts

- `find AI product homepage references`
  - prefer `Home`, `AI Tools`, `AI-native`, `Tech-forward`
  - boost hero, CTA, prompt-input, and product-explanation patterns when present

## Ranking rules

When multiple matches exist, rank them by:
1. direct fit to the user’s goal,
2. exact structured-field match over inferred or keyword-only matches,
3. strong page-type and style-tag combinations over single weak signals,
4. real design usefulness,
5. reference value,
6. clarity at a glance,
7. retrievable image availability when relevance is otherwise similar,
8. recency as a weak tie-breaker.

Prefer these ranking biases:
- exact field match > inferred tag match > free-text keyword hit,
- page type + style tag agreement > keyword-only similarity,
- records with usable images > text-only records when overall relevance is close.

Return 1-5 images. Prefer 3 when many exist.

## Result formatting rules

Preferred output per result:
1. the image itself,
2. title,
3. one-line why-it-matches note,
4. optional item link.

If image return fails, fall back to:
- title,
- rationale,
- key tags,
- item link,
- and state clearly that preview delivery failed.

## Record update safety rule

When a user asks to add an image to an existing record, do not overwrite the current image set by default.

Default behavior:
- read the current record,
- preserve existing image files,
- append new files.

Only replace existing images when the user explicitly says:
- replace
- overwrite
