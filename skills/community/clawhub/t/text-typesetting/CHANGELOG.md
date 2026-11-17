# Changelog — text-typesetting

All notable changes to this skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and semantic versioning.

## v1.2.0 — 2026-10-08

- **Clarified — line-height sources:** body `1.2`–`1.45` is source-backed; heading `1.1`–`1.3` and label/caption `1.2`–`1.4` are labelled as working values because no direct source was found for their exact endpoints.
- **Changed — README:** documents the Questions contract and the permission gate for x-height measurement and writes.
- **Verified — live Figma probes:** `PRETTY` persists as a `textWrapStyle`; native hanging punctuation overhangs `"`, `“`, `„`, `«`, and `(` in Inter but not `—`; no explicit `KERN` key appeared in 1,913 reference text nodes, so an absent key is now reported as "not explicitly overridden," not as proof that kerning is on.

## v1.1.0 — 2026-10-08

### Figma Plugin API names corrected; one all-caps tracking formula

Checked against the Figma Plugin API docs and by reading text layers in a live Figma file
(`Foundations — Symphonia Score (Free)`, Typography page, read-only).

- **Changed — all-caps tracking (Step 2, Branch A):** the three size bands (`+10%` / `+6%` / `+2%`)
  are replaced by one formula, `TS = max(3%, min(12%, 160 / FS))`, shared with `glyph-fidelity`
  Rule 1. The two skills used to return different values for the same size (14px: `+6%` vs
  `+11.4%`). **Values change:** 14px is now `+11.4%`, 20px is `+8%`, 40px is `+4%`.
- **Fixed — `textLeadingTrim` → `leadingTrim`.** The skill stated the reverse. `textLeadingTrim`
  does not exist on a text node and reading it throws.
- **Fixed — `textCase` values:** `"UPPER"` (not `UPPERCASE`); `"SMALL_CAPS_FORCED"` added to
  Branch A; `letterCase` → `textCase`.
- **Fixed — kerning guard (Step 5):** `fontKerning` does not exist. Kerning is an OpenType feature;
  the skill now reads `openTypeFeatures`, flags `KERN: false`, and reports that a script cannot
  switch it back on.
- **Fixed — figure styles and `case` (Steps 4, 6):** `fontFeatures` does not exist and
  `openTypeFeatures` is read-only. These are now reported as a step for the user, never as applied.
- **Changed — hanging punctuation (Step 7):** uses the native `hangingPunctuation` property instead
  of a negative `paragraphIndent` (`-0.45 × fontSize`).
- **Fixed — variable fonts:** axis values are read from `fontName.variationSettings` via
  `getStyledTextSegments`; `fontVariations` does not exist.
- **Added — Figma Node Integration:** `figma.mixed` handling; values owned by a text style or a
  variable are reported, not overridden on the node; `lineHeight` / `letterSpacing` written as
  `{ unit, value }`.
- **Fixed — dash sources:** the incomplete "Hunt, R." reference is replaced. Spaced en dashes to set
  off phrases is Bringhurst §5.2.1; the unspaced em dash is the Chicago Manual of Style convention,
  not Bringhurst's.
- **Added — Step 1a, line-height from x-height:** the position inside a role's range is computed from
  the x-height ratio (`t = clamp((xr − 0.45) / 0.10, 0, 1)`), with a labelled fallback to the
  serif / sans-serif rule. Anchors: Times `0.447` and Verdana `0.545`, the W3C's reference faces
  for low and high x-height (CSS Fonts Module Level 5, §3.4). Direction: Butterick, "Line
  spacing". Heading and caption ranges are unchanged. The Figma measuring method (flatten a
  temporary `x`, read its height) was run in a scratch file: Inter `0.545`, Roboto `0.528`,
  EB Garamond `0.409`, no nodes left behind.
- **Changed — body line-height range (Step 1):** `1.4`–`1.65` → `1.2`–`1.45`, Butterick's 120–145% of
  the point size. **Values change:** body text now gets a tighter line-height than before.
- **Fixed — Step 1b example:** it said line-height grows from `1.5` to `1.7` at 85 characters, but
  the formula above it gives `+0.02`. The example now follows the formula (`1.35` → `1.37`).
- **Added — "Questions" section:** read first, report, then ask; a question only when the value can't
  be read and changes the result; always before a write. Lists the questions this skill may need.
- **Not directly toggle-tested:** the `KERN` key in `openTypeFeatures`; the reference file exposed no explicit `KERN` key.
- **Added — Step 2c, light weights:** weights below 400 on small text are flagged (Apple HIG).

## v1.0.0 — 2026-07-08

Initial release.
