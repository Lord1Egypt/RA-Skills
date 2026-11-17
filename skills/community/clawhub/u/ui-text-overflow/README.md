# UI Text Overflow

**Check whether text in a user interface fits its container — and still fits when it changes.**

Compares how much text sibling UI components carry, turns that into a character budget, finds text that is cut off with no way to read the rest, and checks whether the layout holds with longer copy, a translation or larger text.

## What it does

- Compares sibling components (cards in a grid, rows in a list) by the number of lines each text takes, and names the outliers.
- Gives a character budget per text role, as a range a writer can aim for.
- Lists truncated text and marks each one: full text reachable, or not.
- Flags fixed-height text boxes and clipped text.
- Runs a resilience check: longer copy, translation, user text spacing (WCAG 1.4.12), larger text.
- With Figma access: reads the selected components directly; writes only on request.

## What it doesn't do

- It doesn't rewrite, shorten or pad copy. It reports the budget and leaves the wording to a content pass.
- It doesn't call uneven card text a rule violation. No typographic source prescribes equal lengths; the requirements are that content stays available and containers adapt.

## When to use

- Cards or list rows look uneven because their texts differ in length.
- You need to tell a writer how long a title or description can be.
- Reviewing ellipsis, max lines or fixed-height text before handoff or localisation.

## When NOT to use

- Reading width of a text column — see `line-length-optimizer`.
- Spacing between blocks — see `vertical-spacing`.

## What's inside

```
ui-text-overflow/
├── README.md     ← this file
├── SKILL.md      ← rules, Figma integration, quality checklist
├── CHANGELOG.md
└── LICENSE       ← MIT
```

## Status

Draft. The Figma line-count estimate and the resilience check have not been run in the Figma agent yet.

## License

MIT — see `LICENSE`. Author: **[Monika Zapisek](https://monikazapisek.com)**. Project: **Design Engineering Playbook**.

---

*Part of the [Design Engineering Playbook](https://github.com/monikazapisek/design-engineering-playbook) — AI-assisted workflow artefacts for product designers working in agile and lean environments.*
