---
name: rngneeds-unity
description: Teach agents how to design, implement, explain, and debug gameplay randomness with the RNGNeeds Unity plugin. Use when a request involves RNGNeeds types or concepts such as ProbabilityList, ProbabilityItem, PLCollection, weighted picks, loot tables, gacha, spawn tables, dialogue weighting, AI choice weighting, repeat prevention, depletable lists, card deck extensions, deck order, draw pile, discard pile, hand, graveyard, shuffle plans, influence providers, pick history, seeding, or custom selection methods in Unity/C#.
---

# rngneeds-unity

Use this skill for RNGNeeds-specific work. If the request is only about generic Unity randomness and does not involve RNGNeeds, handle it normally.

## Work sequence

1. Identify the job: choose a pattern, write code, explain behavior, or debug a setup.
2. Read only the reference files needed for that job.
3. Ground the answer in actual RNGNeeds behavior and API names.
4. Recommend the right mechanic first when the user describes a gameplay goal but not an implementation.
5. If a detail is missing, inspect the package source or docs instead of inventing methods.

## Route by request

- **Choose the right RNG pattern**: read `references/decision-guide.md`, then `references/common-patterns.md`, then `references/core-concepts.md` as needed.
- **Write or refactor Unity/C# code**: read `references/api-surface.md` and `references/examples.md`.
- **Answer tutorial, support, or docs-style questions**: read `references/guide-workflows.md` first, then `references/examples.md`.
- **Explain weird probabilities or surprising results**: read `references/pitfalls.md` and `references/core-concepts.md`.
- **Build dynamic odds from game state**: read `references/core-concepts.md`, `references/api-surface.md`, and `references/examples.md`.
- **Model decks, draw piles, discard piles, hands, graveyards, limited rewards, or finite stock**: read `references/decision-guide.md`, `references/common-patterns.md`, `references/pitfalls.md`, and `references/examples.md`.

## Guardrails

- Distinguish **BaseProbability** from the final **Probability** used during selection.
- Distinguish **disabled** items from **removed** items, and **depletable** items from infinite ones.
- Distinguish **weighted selection** from **deck-order operations**. If the user cares about top, bottom, hand, discard, cut, or shuffle order, prefer deck extensions over `PickValue()`.
- Warn that disabled items still occupy probability space, and if selection lands on one that pick is ignored. Disabled or depleted states can reduce result count unless `MaintainPickCountIfDisabled` is enabled.
- Warn that repeat prevention changes behavior: `Spread` is fast but more biased, `Repick` is lower bias, `Shuffle` preserves distribution better but does not guarantee zero repeats between separate picks.
- Warn that influenced lists recalculate before selection, and final displayed outcomes may normalize.
- Warn that `PickValues()` returns a shared internal list reference. Copy it if the caller must keep results after another pick.
- Prefer `TryPickValue(...)` when failure matters, especially for value types where `default(T)` can look like a real result.
- Note that if an item's value implements `IProbabilityInfluenceProvider`, it overrides an external provider assigned to that item.
- Note that deck extensions are order-centric and use simple seeded index/random operations, not the list's weighted selection methods.
- Prefer `KeepSeed` or a custom seed provider for deterministic behavior instead of ad hoc randomness hacks.
- Reach for custom selection methods only when built-in behavior does not satisfy the requirement.

## Output expectations

- Explain *why* a feature fits the gameplay goal, not only *how* to call it.
- Keep code examples short and focused on RNGNeeds.
- Use RNGNeeds terminology consistently so designers and programmers can discuss the same setup.

## Reference map

- `references/core-concepts.md`: terminology and mental model
- `references/decision-guide.md`: choose the right feature for the job
- `references/common-patterns.md`: common gameplay setups
- `references/guide-workflows.md`: tutorial-style workflows distilled from the docs guides
- `references/api-surface.md`: high-value classes, properties, and methods
- `references/pitfalls.md`: gotchas and debugging heuristics
- `references/examples.md`: compact Unity/C# examples
- `references/test-prompts.md`: prompt pack for manual skill testing
