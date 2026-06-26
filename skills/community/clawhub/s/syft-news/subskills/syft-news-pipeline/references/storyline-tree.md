# Storyline Tree Route

Use this route when the user wants a relationship-first reading view rather than a flat briefing.

## Preferred Inputs

- an aggregated daily news pool
- a finished daily briefing
- `profiles/profile_summary.md`
- `profiles/following_topics.md`
- optional confirmed guidance rules

## Outputs

Create:

- `storylines/storyline_tree_<date>.md`
- `storylines/storyline_tree_<date>.html`
- `storylines/storyline_tree_<date>.json`
- optionally `storylines/storyline_notes_<date>.md`

Visible outputs must be polished deliverables.
Do not leak retrieval notes, query wording, or route jargon into user-facing prose.

## Core Model

Organize information into:

1. facts
2. events
3. branches
4. trunks

Each trunk should express one structural storyline.
Each branch should express one interpretable angle attached to that trunk.

## Build Order

1. Identify 3 to 8 candidate trunks from the cleaned pool.
2. Test whether each candidate really deserves trunk status.
3. Create branches only after trunk identity is coherent.
4. Use topic top or search extension only after the base tree is stable.

## Admission Rules

A trunk usually needs at least two of:

- structural consequence
- multi-event continuity
- a clear causal chain
- strong match to declared macro or identity interests
- capacity to support more than one meaningful branch

Thin but relevant material should stay visible as a branch, watch item, or orphan highlight rather than being silently dropped.

## Hobby and Culture Rules

- Do not merge unrelated IPs or collector logics.
- Keep Fate, EVA, cameras, and Japan travel separate when they are independently meaningful.
- Allow branch logic based on recurring cadence, not only macro-style causality.

## Quality Gate

Before finalizing, verify:

1. trunk and branch titles read like names
2. merged timelines are chronologically sorted
3. visible Chinese reads naturally
4. HTML looks like an editorial card page, not a debug dashboard
5. thin but relevant interests remain visible somewhere
