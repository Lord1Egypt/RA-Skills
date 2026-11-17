# Text Typesetting

**Compute line-height and letter-spacing for a text style — correctly, including vertical-trim.**

Sets a coherent `line-height` and `letter-spacing` (tracking) for a given font size and text role (body, heading, UI label, caption), and — critically — accounts for vertical-trim / leading-trim state, which changes what "line-height" visually means.

## What it does

- Base `line-height` by role and font family (serif needs more breathing room than sans at the same size).
- Source status is explicit: body `1.2`–`1.45` is backed by Butterick; heading `1.1`–`1.3` and label/caption `1.2`–`1.4` are working ranges because no direct source was found for the exact endpoints.
- Inverse tracking rule: large text (headings) → negative `letter-spacing`; small text (captions, all-caps labels) → positive.
- **Vertical-trim guard**: checks CSS `leading-trim`/`text-box-trim` or Figma `TextNode.leadingTrim` before finalizing line-height — trimmed text reads visually tighter at the same numeric value, so the assumption is always stated explicitly, never silently picked.
- OpenType feature recommendations (tabular numbers for aligned figures, small caps) only when content implies them.
- With Figma access: reads the selected text node's properties directly and can write values back on explicit request.
- Reads first and asks only when a missing value changes the result; x-height measurement and every write require permission.

## When to use

- Setting up or reviewing a text style/token (body, heading, label, caption).
- Inspecting a selected Figma text layer and proposing corrected spacing values.

## When NOT to use

- Generating an entire type scale across multiple sizes at once.
- Spacing *between* elements — that's vertical rhythm, not a single text style.
- Column width — see `line-length-optimizer`.

## What's inside

```
text-typesetting/
├── README.md    ← this file
├── SKILL.md     ← full workflow, Figma integration, quality checklist
└── LICENSE      ← MIT
```

## Related skills

Part of a small typography/layout family in this playbook: this skill's vertical-trim state feeds directly into [`vertical-spacing`](../vertical-spacing/README.md)'s optical-gap correction. [`line-length-optimizer`](../line-length-optimizer/README.md) sets column width, [`microtypography`](../microtypography/README.md) applies character-level fixes last.

## License

MIT — see `LICENSE`. Author: **[Monika Zapisek](https://monikazapisek.com)**. Project: **Design Engineering Playbook**.

---

*Part of the [Design Engineering Playbook](https://github.com/monikazapisek/design-engineering-playbook) — AI-assisted workflow artefacts for product designers working in agile and lean environments.*
