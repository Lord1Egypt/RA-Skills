# Vertical Spacing

**Compute vertical margin/padding/Auto Layout gap against a grid base — correctly, including vertical-trim.**

Snaps spacing values to a grid base (8px, or 4px for denser UI), applies the proximity rule (elements above a heading get more room than elements below it), and accounts for vertical-trim's effect on optical spacing without assuming a universal pixel correction.

## What it does

- Snaps every margin/padding/gap value to a clean multiple of the grid base; flags off-grid values found in existing input.
- Applies the Gestalt proximity rule asymmetrically around headings (top spacing ≫ bottom spacing).
- Checks groups from the inside out: an internal gap must not exceed the gap around its group; reversed and ambiguous groupings are reported by meaning, not just by number.
- **Vertical-trim correction**: checks `leadingTrim` on any text layers inside the spacing context before giving a final value — if trim is off, the optical gap is smaller than the set value; recommends either compensating or turning trim on.
- With Figma access: reads the selected Auto Layout frame's `layoutMode`, `itemSpacing`, and padding directly, plus child text nodes' `leadingTrim`, and can write corrected values back on explicit request.
- Reads first and asks only when a missing value changes the result; every write requires permission.

## When to use

- Reviewing or defining spacing for a card, section, article, or form.
- Fixing an Auto Layout frame in Figma where gap/padding look inconsistent or off-grid.

## When NOT to use

- Spacing within a single text style (line-height/letter-spacing) — see `text-typesetting`.
- Column width — see `line-length-optimizer`.

## What's inside

```
vertical-spacing/
├── README.md    ← this file
├── SKILL.md     ← full workflow, Figma integration, quality checklist
└── LICENSE      ← MIT
```

## Related skills

Part of a small typography/layout family in this playbook: this skill depends on vertical-trim state set by [`text-typesetting`](../text-typesetting/README.md). [`line-length-optimizer`](../line-length-optimizer/README.md) sets column width (the other axis), [`microtypography`](../microtypography/README.md) applies character-level fixes last.

## License

MIT — see `LICENSE`. Author: **[Monika Zapisek](https://monikazapisek.com)**. Project: **Design Engineering Playbook**.

---

*Part of the [Design Engineering Playbook](https://github.com/monikazapisek/design-engineering-playbook) — AI-assisted workflow artefacts for product designers working in agile and lean environments.*
