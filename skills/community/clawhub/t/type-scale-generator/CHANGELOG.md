# Changelog — type-scale-generator

All notable changes to this skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and semantic versioning.

## v1.2.0 — 2026-10-08

- **Added — Questions contract:** read first, ask one question at a time, and ask before every Figma write.
- **Changed — x-height measurement:** now requires explicit permission before the temporary text layer is created, flattened and removed.
- **Clarified — line-height sources:** body `1.2`–`1.45` remains source-backed by Butterick; heading `1.1`–`1.3` and caption `1.2`–`1.4` are labelled as working values because no direct source was found.

## v1.1.0 — 2026-10-08

### A full type scale, and a Figma workflow

API names checked against the Figma Plugin API docs (`TextStyle.setBoundVariable`, `VariableScope`).
Nothing was written to a Figma file for this release — the Figma workflow is untested in the Figma agent.

- **Added — Step 0:** in Figma the base size and font are read from the selected text and confirmed
  with the user; four selection cases handled.
- **Added — Step 3, collision check:** steps that round to the same value, or collapse into equal
  jumps, are named and fixed instead of handed over.
- **Added — Step 4:** every step gets a line-height and a tracking value, using the rules of
  `text-typesetting`. Line-height is a range per role and size; the position inside it is computed
  from the typeface's x-height ratio, with a labelled fallback when x-height isn't measured.
  Body range is Butterick's 120–145%. Anchors and sources as in `text-typesetting` Step 1a; the Figma measuring method was run in a
  scratch file.
- **Added — Step 5:** the whole scale is shown as a table before any file or Figma write.
- **Added — Figma Node Integration:** `FLOAT` variables scoped to `FONT_SIZE` / `LINE_HEIGHT`, text
  styles bound to them, a specimen frame. Each write only on request; existing styles and variables
  are checked first and never overwritten silently; existing text is never restyled.
- **Added — out of scope, stated:** platform presets and two-ratio scales, because they don't come
  from the sources the skill is based on.
- **Changed — workflow:** one question at a time; values already given in the request are not asked
  for again. Old Step 4 (code output) is now Step 6.
- **Changed — README:** repository link corrected; feature list updated.
- **Added — Step 3, platform minimums:** Apple HIG default and minimum sizes as a constraint on the
  computed scale, flagged, never substituted for it.

## v1.0.0 — 2026-07-08

Initial release.
