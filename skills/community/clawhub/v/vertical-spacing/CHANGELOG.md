# Changelog — vertical-spacing

All notable changes to this skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and semantic versioning.

## v1.2.0 — 2026-10-08

- **Removed — unsupported optical-gap number:** the claim that `gap: 16px` reads as about `11px` was removed. The exact difference depends on font metrics, line-height and adjacent glyphs and must be measured.
- **Changed — Figma alert:** rewritten in English and no longer invents an estimated optical gap.
- **Changed — README:** documents the inside-out grouping check and the Questions/write-permission contract.

## v1.1.0 — 2026-10-08

### Figma Plugin API names corrected

Checked against the Figma Plugin API docs and by reading text layers in a live Figma file
(`Foundations — Symphonia Score (Free)`, Typography page, read-only).

- **Fixed — `textLeadingTrim` → `leadingTrim`** (values `"CAP_HEIGHT"` / `"NONE"`), in the skill
  and the README.
- **Fixed — Step 6:** removed the reference to per-item gap overrides and `itemReverseZIndex`.
  Auto Layout has one `itemSpacing` per frame; the heading gets its space from a wrapping frame.
- **Added — `listSpacing`:** the gap between items of a native list inside one text node.
- **Added — bound values:** spacing bound to a variable is reported with the nearest on-grid
  variable, not replaced by a raw number.
- **Changed — README:** repository link corrected.
- **Added — "Questions" section:** read first, report, then ask; a question only when the value can't
  be read and changes the result; always before a write. Lists the questions this skill may need.
- **Added — Step 2a, grouping check:** "internal ≤ external" for title–description, label–field,
  list items and similar pairs; reversed and ambiguous groupings are reported. Description now
  names the Gestalt principle of proximity. Sources: Wertheimer, NN/g (Harley 2020), Butterick.
  The sources give no ratio; the existing "2–3×" is labelled as the skill's working value.

## v1.0.0 — 2026-07-08

Initial release.
