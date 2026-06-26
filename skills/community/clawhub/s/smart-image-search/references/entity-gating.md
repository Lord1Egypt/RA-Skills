# Multi-entity hard gating

Use hard gating for multi-entity queries when soft penalties are not enough.

## Goal

Prevent partial-entity matches from outranking true matches.

## Rule

When the cleaned core query contains 2 or more strong entity tokens:
- identify how many strong tokens each candidate matches
- in `official` mode, if a candidate matches fewer than 2 strong tokens, do not allow it into the top trust tier
- if no candidate matches 2 strong tokens, fall back gracefully and report that confidence is limited

## Practical behavior

- `2+ strong token matches` => eligible for high-priority official candidates
- `1 strong token match` => partial match, keep only as fallback candidate
- `0 strong token matches` => strongly penalize or reject

## Example

Query: `acme mascot official image`
- candidate with `acme` + `mascot` => full entity match
- candidate with only `acme` => fallback only
- candidate with only `mascot` => fallback only
- candidate with neither => reject or bury
