# Multi-shot Visual Continuity Check

![Multi-shot Visual Continuity Check promo](assets/promo-1600x900.png)

Find character, prop, lighting, and spatial breaks in an existing shot list before production, then receive the smallest story-preserving corrections.

Provide a written shot list plus character and scene references. The result is a severity-ranked issue list with evidence shot IDs and actionable minimal edits. If required material is missing, the Skill lists the gaps instead of inventing visual facts.

Severity is deterministic: high covers character identity/appearance, prop state, and location conflicts; medium covers hand side, prop position, and light direction or color temperature; low covers lighter differences such as brightness.

## Install

```bash
npx skills add xxjrq/video-visual-continuity-check-cn
```

## Scope

Use it for one chapter, scene, or short-form plan at a time (up to 100 rows). It reviews an existing multi-shot plan; it does not create a new story, storyboard, or model compiler output.

## Runnable examples

- [Successful input](fixtures/success-input.json) and [delivery](fixtures/success-output.json)
- [Missing-material input](fixtures/failure-input.json) and [delivery](fixtures/failure-output.json)

Run the standalone verification:

```bash
python3 scripts/self_test.py
```

The checker reads `description`, `visual`, and categorized picture fields. Clothes and held props are compared only when the actor identity is established; `character_id` and per-person reference dictionaries help resolve ambiguity. Explicit transitions explain only their category and named item; dropping a paper bag cannot explain a phone-position change, and a negated wardrobe change cannot explain changed clothes.

Run `python3 scripts/check_continuity.py fixtures/success-input.json` directly. This conservative Chinese-text checker does not analyze images or video. Ambiguous identity or wording remains a manual confirmation item, not proof of consistency. Verification includes independent positive and negative regressions for identity, named prop holders, descriptive fields, category-specific transitions, and negated actions.

The documentation and examples are original. The repository only consulted the business purpose of [seaartpublic/skills](https://github.com/seaartpublic/skills), and imports no text or code from it. Licensed under [MIT-0](LICENSE).
