# Type Scale Generator

**Generate a mathematically coherent type scale from a base size and a ratio — sizes, line-heights and tracking.**

Computes H1–H6, body, and caption sizes from a chosen ratio (musical/geometric, Fibonacci, or the historical Garamond printer's series), rounds to avoid subpixel rendering, and refuses to emit anything below the UI-legibility floor.

## What it does

- 8 named geometric ratios (Minor Second `1.067` through Golden Ratio `1.618`), each with a plain-language description of its character and best use case.
- Two non-linear historical scales: `fibonacci` (sequence-based, ties directly to a Fibonacci-proportioned layout grid) and `classic-garamond` (the renaissance-era printer's fixed type-size steps).
- Rounding guard: every computed value snaps to the nearest even integer or 4px multiple, with the raw and rounded numbers both shown.
- Readability floor: refuses to emit a token below 12px, or below 12px paired with a font-weight under 400.
- Optional fluid scale via `clamp()` for responsive sizing.
- Line-height and tracking for every step — the same rules as `text-typesetting`. Line-height is computed from the typeface's x-height inside a range per role, not picked from a table.
- The body line-height range (`1.2`–`1.45`) is source-backed; heading (`1.1`–`1.3`) and caption (`1.2`–`1.4`) ranges are explicitly labelled as working values because no direct source was found.
- Shows the whole scale as a table before anything is written.
- With Figma access: takes the base from the selected text, checks existing text styles and variables, then creates number variables, text styles bound to them, and a specimen frame — each only on request. Existing text is never restyled.
- Reads first and asks only for missing values that change the result. Measuring x-height and every Figma write require permission.
- Not included: platform presets and two-ratio scales. They don't come from the sources this skill is based on.

## When to use

- Building a font-size system for a new design system or page.
- User names a ratio ("minor third", "1.25", "golden ratio") or asks for a scale with no preference stated.

## When NOT to use

- A single text style's line-height/tracking — see `text-typesetting`.
- Spacing between blocks — see `vertical-spacing`.

## What's inside

```
type-scale-generator/
├── README.md    ← this file
├── SKILL.md     ← full ratio table, rounding guard, quality checklist
└── LICENSE      ← MIT
```

## Related skills

Part of a small typography/layout family in this playbook: this skill's output sizes feed [`text-typesetting`](../text-typesetting/README.md) (line-height/tracking per size) and [`vertical-spacing`](../vertical-spacing/README.md) (rhythm between the blocks it produces).

## License

MIT — see `LICENSE`. Author: **[Monika Zapisek](https://monikazapisek.com)**. Project: **Design Engineering Playbook**.

---

*Part of the [Design Engineering Playbook](https://github.com/monikazapisek/design-engineering-playbook) — AI-assisted workflow artefacts for product designers working in agile and lean environments.*
