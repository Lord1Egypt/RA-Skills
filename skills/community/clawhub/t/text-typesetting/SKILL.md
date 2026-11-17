---
name: text-typesetting
description: Use when setting or reviewing line-height, letter-spacing (tracking), and vertical-trim/leading-trim for a text style — computing the geometric relationship between font size and these values for body text, headings, UI labels, or captions.
triggers:
  use_when:
    - user asks to configure a text style or type token
    - user asks "what line-height should this be"
    - user asks to compute tracking / letter-spacing
    - user is setting up h1-h6 / body / label / caption text styles
    - agent has Figma access and user asks to fix/inspect a selected text layer's spacing
  do_not_use_for:
    - generating a full type scale across sizes (see type-scale-generator)
    - vertical rhythm between blocks/components (see vertical-spacing)
    - column width / measure (see line-length-optimizer)
metadata:
  author: Monika Zapisek
  project: Design Engineering Playbook
  version: "1.2.0"
  status: accepted
---

# Text Typesetting

## Purpose

Compute a coherent `line-height` and `letter-spacing` for a given `font-size` and text role, and correctly account for vertical-trim (CSS `leading-trim` / Figma `leadingTrim`) when it changes what "line-height" visually means.

## When To Use

- Setting up a new text style/token (body, heading, label, caption).
- Reviewing an existing style where line-height or tracking look off.
- Inspecting a selected Figma text layer and proposing corrected values.
- Not for generating an entire scale of sizes at once, and not for spacing *between* elements (that's vertical rhythm, a different skill).

## Inputs

- `font-size` (px or rem).
- `font-family-category`: sans-serif / serif / display / monospace (serifs generally need more line-height breathing room than sans at the same size).
- `text-role`: body / heading / UI label / caption.
- `text-case`: original (sentence/title case) or uppercase/small-caps — this is the primary driver of letter-spacing direction, see Workflow step 2.
- `x-height`: the ratio of x-height to font size (`xr`; Times is 0.447, Verdana 0.545), measured or read from the font — it sets where line-height falls inside its range (Workflow step 1a). For tracking, high / low is enough (step 2b). Optional: without it the skill falls back to the family rule and says so.
- `font-weight`: numeric (100–900) if known — scales the tracking magnitude from step 2/2b, see Workflow step 2c.
- `variable-font-axes`: if the font is variable, the actual `wght` value and whether an `opsz` (optical size) axis exists and is bound to size — see Workflow step 2d.
- If available: `leadingTrim` / vertical-trim state (see Figma Node Integration) — this changes the recommended line-height, not just its visual effect.

## Outputs

- `line-height` value (unitless ratio preferred for body text, so it scales with font-size).
- `letter-spacing` value (in `em`, since tracking should scale with font-size, not be a fixed px).
- CSS/token snippet, plus a one-line rationale per value.

## Questions

This skill is an audit, not an interview. Work in this order: read what the file or the input already says, report, then ask.

- Ask only when a value can't be read and the answer would change the result. One question at a time.
- Don't ask for anything the request already states or the file shows — say what you took and where it came from.
- If the question can't be answered, state the assumption and carry on. Never stall the report on it.
- Always ask before writing to a file or a Figma node.

Questions this skill may need:

- The text role (body / heading / label / caption), when the style name and the size don't make it clear.
- In Figma, permission to measure x-height — it creates and removes a temporary layer (Workflow step 1a). Without it, use the labelled fallback.

## Workflow

1. **Line-height range by role and size:**
   - Body text: `1.2`–`1.45` (Butterick: 120–145% of the point size).
   - Headings: tighter, `1.1`–`1.3` — a working range of this skillset; no direct source was found for these exact endpoints.
   - UI labels / captions: `1.2`–`1.4` — a working range of this skillset; no direct source was found for these exact endpoints.

1a. **Position inside the range comes from the typeface's x-height, computed, not picked.** The x-height ratio is the height of a lowercase `x` divided by the font size (`xr`). A face with a large x-height fills more of the line, so its lines look closer together and need more room; a face with a small x-height carries its own air.

   ```
   t  = clamp((xr − 0.447) / (0.545 − 0.447), 0, 1)
   LH = LH_min + t × (LH_max − LH_min)
   ```

   `xr = 0.447` or lower lands on the bottom of the range, `0.545` or higher on the top. The two anchors are the reference faces the W3C uses to explain x-height: Times, `0.447`, as a low aspect value and Verdana, `0.545`, as a high one (CSS Fonts Module, `font-size-adjust`). The direction is Butterick's: fonts that run small need less line spacing, and vice versa. Round `LH` to two decimals. Show `xr`, the range and the result.

   How to get `xr`:
   - **Font file or CSS:** `sxHeight / unitsPerEm` from the font's OS/2 table; in a browser, `1ex` measured against `1em`.
   - **Figma:** the Plugin API exposes no font metrics. Measure instead: create a temporary text node with the single character `x` in the font at `100px`, flatten it to a vector (`figma.flatten([node])`), read its `height`, divide by 100, and remove the vector. This creates and deletes a layer, so ask before doing it. Checked values from this method: Inter `0.545`, Roboto `0.528`, IBM Plex Sans `0.516`, Source Serif 4 `0.452`, EB Garamond `0.409`.
   - **Not measured:** fall back to the family rule — sans-serif in the lower half of the range, serif in the upper half — use the middle of that half, and state that x-height was not measured. Never present a fallback value as computed.

1b. **Measure compensation ("Typography Triangle") — only when the column is wider than ideal:** if `line-length-optimizer` reports (or the input states) a measure wider than the ~65-character ideal — the eye has more trouble tracking back to the start of the next line the wider the column gets — compensate by *increasing* line-height beyond the step-1 base:

   ```
   LH_new = LH_base + ((characters_per_line − 65) / 100) × 0.1
   ```

   E.g. at 85 characters per line, line-height grows from `1.35` to `1.37`. Only apply this when measure is confirmed wider than ~65–75 characters (i.e. already outside `line-length-optimizer`'s comfortable range) — don't apply a correction for a column that's merely at the high end of normal. This is a compensation for a business constraint that's forcing an over-wide container, not a substitute for fixing the width via `line-length-optimizer` when that's actually available.

2. **Letter-spacing (tracking) — driven first by case, then by size.** `text-case` is the primary branch — check it before applying any size-based rule:

   **Branch A — uppercase or small-caps** (Figma `textCase: "UPPER"` / `"SMALL_CAPS"` / `"SMALL_CAPS_FORCED"`, or CSS `text-transform: uppercase`): default font spacing is tuned for mixed-case letterforms, which lose their shape variety when flattened to all-caps — the eye can't recognize word-shapes anymore, only a dense block of equal-height letters. Always add positive tracking, scaled inversely with size (small caps text needs proportionally more room than large). One formula, one result per size (`FS` = font-size in px):

   ```
   TS = max(3%, min(12%, 160 / FS))
   ```

   - Reference values: `10px → +12%`, `14px → +11.4%`, `16px → +10%`, `20px → +8%`, `32px → +5%`, `40px → +4%`, `54px` and above `→ +3%`.
   - This is the same formula as `glyph-fidelity` Rule 1. There are no separate size bands: both skills return the same number for the same size.
   - Write the result as `letter-spacing: 0.08em` in CSS, or `letterSpacing = { unit: "PERCENT", value: 8 }` in Figma.

   **Branch B — sentence/title case** (`textCase: ORIGINAL`): lowercase letters carry their own internal/external counters that already aid legibility — no tracking adjustment needed at body/reading sizes. Only tighten at larger sizes, where letter-spacing optically opens up and headings start to look "broken apart":
   - `font-size < 24px` → `letter-spacing: 0` (`normal`) — don't touch it.
   - `24px ≤ font-size < 36px`, sans-serif → `letter-spacing: -1.5%` (`-0.015em`).
   - `font-size ≥ 36px`, sans-serif → `letter-spacing: -2%` (`-0.02em`).
   - Serif/display faces: apply roughly half the sans-serif tightening — serifs already have less open counters, so the same negative value over-tightens.

2b. **x-height refinement (optional, only if the specific typeface's x-height is known):**
   - **High x-height** (e.g. Inter, Roboto, San Francisco — most UI-oriented sans faces): open, wide counters at small sizes aid legibility, but the letters occupy more vertical space and tolerate — sometimes need — very slightly looser tracking at small sizes to avoid letters visually merging. Bias toward the upper end of the Branch A/B ranges above.
   - **Low x-height** (classic serif and elegant display faces, e.g. Georgia-style proportions): small letters are compact relative to cap-height, leaving more natural vertical air already. Keep tracking closer to zero — loosening it further makes low-x-height letters visually drift apart and the word loses cohesion. Bias toward the lower end of the ranges above, or don't adjust at all if already near zero.
   - If x-height is unknown, skip this refinement — the Branch A/B base values are safe defaults without it.

2c. **Font-weight modifier (apply after Branch A/B + x-height, as a final scaling pass on whatever tracking value step 2/2b produced):**
   - Heavier weights (Bold/700, Black/900) carry thicker strokes, which already reduce the white space inside and between letters — the same *numeric* tracking value reads as looser on a Black weight than on a Regular weight, because there's less counter-space for the extra room to sit in. Reduce the computed tracking magnitude (keep the sign from Branch A/B, scale the number down):
     - Weight ≥ 700 (Bold/Black/Heavy): multiply the Branch A/B result by roughly `×0.7`.
     - Weight ≤ 300 (Light/Thin): multiply by roughly `×1.15` — thin strokes leave more open counters already, and default spacing can look slightly cramped without a small boost.
     - Weight 400–500 (Regular/Medium): no modifier, use the Branch A/B value as-is.
   - This applies in both branches: an uppercase Black-weight label still gets positive tracking (Branch A), just proportionally less than the same label in Regular weight.
   - If weight is unknown, skip this modifier — Branch A/B values already assume Regular/Medium as the default case.

   - **Light weights at small sizes (platform constraint):** Apple's Human Interface Guidelines advise against Ultralight, Thin and Light weights, which are hard to see especially when text is small. Flag any weight below 400 on body, label or caption text. This is a legibility flag from the platform layer; it doesn't change the tracking computed above.

2d. **Variable fonts — read the actual axis value, don't assume a named instance:**
   - A variable font's weight is a continuous value (e.g. `wght: 550`), not a fixed Regular/Bold step. Apply the font-weight modifier (step 2c) by interpolating between the anchor points (400→×1, 700→×0.7, 300→×1.15) rather than snapping to the nearest named instance — a `wght: 550` gets a modifier roughly halfway between ×1 and ×0.7.
   - If the font exposes an **optical size axis** (`opsz`), check it before manually adjusting tracking at all: `opsz` is specifically designed to auto-adjust spacing, stroke contrast, and x-height proportions for the rendering size, which is much of what steps 2/2b/2c are compensating for manually. When `opsz` is bound to `font-size` (CSS `font-optical-sizing: auto` — the default in modern browsers — or the Figma equivalent), treat the manual tracking correction as a smaller supplementary nudge, not the full computed value, and say so in the output rather than silently stacking both corrections.
   - If no variation axis data is available (static font, or Figma reports only a named instance), fall back to the discrete Regular/Bold treatment in steps 2c and don't guess at intermediate values.

3. **Vertical-trim / leading-trim guard (critical — check before finalizing line-height):**
   - Default behavior (trim off): the font's built-in leading (space above cap-height and below baseline) is included in the line box. The `line-height` values above assume this default.
   - If vertical-trim / `leading-trim` is **on** (CSS `leading-trim: both` / `text-box-trim`, or Figma `leadingTrim: "CAP_HEIGHT"`): the line box is cropped to cap-height/baseline, removing the font's built-in air. In this state, the same numeric `line-height` reads as visually tighter — recompute upward (roughly +10–15%) if trim is on and the target visual density should stay the same as the untrimmed baseline. State explicitly whether the recommended value assumes trim on or off — never hand over a bare number without saying which.
   - If unknown (plain CSS with no Figma/plugin context, no way to check), state the assumption ("assuming default leading, trim off") rather than silently picking one.
   - **Property name:** in the Figma Plugin API this is `textNode.leadingTrim`, with the values `"CAP_HEIGHT"` and `"NONE"`. A property called `textLeadingTrim` does not exist on a text node, and reading it throws. CSS calls the same thing `text-box-trim` (`leading-trim` in earlier drafts).

4. **OpenType number styles — pick by content role, not by default.** Digits aren't one glyph set; the font exposes up to four figure styles along two independent axes (form × spacing), and picking wrong is a common, avoidable error:

   | Content role | Figure form | Spacing | CSS | Figma OpenType feature |
   |---|---|---|---|---|
   | Running prose (articles, body copy) | Oldstyle (varying heights, ascenders/descenders — blends into lowercase text instead of forming bright "spikes") | Proportional | `font-variant-numeric: oldstyle-nums proportional-nums;` | `ONUM` |
   | Headings / display / UI counters (prices, single stats, non-tabular labels) | Lining (uniform cap-height) | Proportional (natural rhythm — a `1` shouldn't occupy the same width as an `8`) | `font-variant-numeric: lining-nums proportional-nums;` | `LNUM` |
   | Tables, financial statements, any column of stacked numbers | Lining | Tabular (fixed-width per digit, so units/tens/hundreds columns align vertically) | `font-variant-numeric: lining-nums tabular-nums;` | `LNUM` + `TNUM` |

   - **In Figma these features can be read by a script but not set by one.** `textNode.openTypeFeatures` is read-only and lists only the features changed from the font's default (e.g. `{ TNUM: true }`). There is no `fontFeatures` property and no setter. Read the current state, report which figure style the role needs, and ask the user to switch it in the Type settings panel (Details tab), or apply a text style that already carries it. Never report a figure style as applied.
   - Default to the prose row for body text and the heading row for display/UI unless the user specifies otherwise — don't leave figures at the font's raw default, which is often lining+proportional regardless of role and will look wrong in a paragraph of running text.
   - **Kerning interacts differently per spacing mode** (ties into step 5): proportional figures (prose and heading rows) need the font's kerning left on — pairs like `11` or `74` produce visible gaps without it. Tabular figures have kerning intentionally suppressed by the font itself to preserve fixed-width column alignment — **do not** try to "fix" the spacing of a tabular-figure node by changing kerning; that's the font working as designed, not a bug.
   - **Residual pair collisions in display headings:** even with kerning on, a font with a sparse OpenType kerning table can still leave specific proportional-figure pairs too tight (`11` — the two vertical strokes nearly touch) or too loose (`74` — the diagonal and the crossbar leave a visible gap) at large display sizes, where the flaw becomes visible. If a display heading contains one of these known-risky pairs, apply a local `setRangeLetterSpacing` on just that pair, `±2%`, rather than adjusting the whole node's tracking. Don't apply this pre-emptively — only when the specific pair is present and the size is large enough to make it visible (roughly ≥32px).
   - **Currency and fractional amounts** (e.g. `99.90 zł`, `$4.99`): the cents/grosze portion is a common candidate for the OpenType `Numerator`/superscript feature (`sups` or a fraction feature `frac`) to visually subordinate it to the whole-number part, matching classic price-tag typesetting. Only apply when the content is genuinely a price/currency amount, not a generic decimal (`3.14`, a percentage) — those stay as plain lining figures. Also check the decimal separator (`.`/`,`) isn't visually colliding with a preceding `0` — a rare kerning gap in some fonts — and apply the same local range-tracking fix as above if it is.
   - Small caps (`font-variant: small-caps` / Figma `textCase: "SMALL_CAPS"`) only when explicitly requested — it's a stylistic choice, not a default correction.

5. **Kerning/tracking integrity guard (hard rule, not a recommendation):**
   - **Kerning** (per-pair optical correction baked into the font's OpenType tables, e.g. `AV`, `Ta`, `We`) and **tracking**/`letter-spacing` (a uniform global offset applied to every letter) are complementary, not substitutes. Adjusting tracking in steps 2/2b/2c/2d must never disable or bypass the font's native kerning table.
   - CSS: leave `font-kerning: normal` (the default) — never set `font-kerning: none` as a side effect of a tracking change.
    - Figma: kerning is an OpenType feature that is on by default, and a text node has no `fontKerning` property. A tracking change writes `letterSpacing` only, so it cannot switch kerning off. Read `textNode.openTypeFeatures`; if it explicitly reports `KERN: false`, flag it as likely unintentional. If the key is absent, report the state as "not explicitly overridden" rather than claiming that kerning was verified on: a live 1,913-node reference file exposed no `KERN` key. A plugin script cannot switch kerning back on (`openTypeFeatures` is read-only), so tell the user where to re-enable it instead of reporting it as fixed.
   - The larger the tracking value or font-size, the more visible a missing kerning table becomes (mismatched pairs stand out more at heading sizes) — so this guard matters most exactly where steps 2/2c apply the largest adjustments, not just as a blanket rule.
   - Report the kerning state in the output whenever letter-spacing is changed, so a disabled kerning table isn't silently inherited from the node's prior state.

6. **Dash rendering in Figma (which character/spacing to use is `microtypography` Rule 1c — this step is only the rendering layer on top of that decision):**
   - Whenever a text node contains `-`, `–`, or `—`, kerning must be on (per step 5) so the font's OpenType pair tables can prevent collisions with adjacent outward-leaning letterforms (`V—`, `—A`, `1–9`) — this is the same guard as step 5, just called out explicitly because dash collisions are the most visible failure case.
   - **Display-size / all-caps em dash:** at large sizes or inside an all-caps run (Branch A from step 2), an unspaced em dash can visually crowd its neighbors even with correct kerning. Prefer a small *local* tracking nudge over inserting an actual space — a real space would reopen the "should this have spaces" question Rule 1c already answered, and would break word-count/line-wrap assumptions elsewhere. Apply `+3%` `setRangeLetterSpacing` across the em dash **and the single character immediately on each side of it**, not the dash alone — tracking just the dash glyph itself doesn't change its distance to its neighbors (letter-spacing is applied between characters, not as padding on one glyph), so the range must include at least one adjacent character per side to actually open the gap.
   - **Numeric ranges with en dash in display headings** (e.g. a large "1995–2026"): verify the digits aren't visually touching the dash's arms. If they are (common in cheaper fonts lacking digit-to-dash kerning pairs), apply the same local range-tracking nudge rather than falling back to a spaced dash, since a numeric range must stay unspaced per `microtypography` Rule 1c.
   - **Hyphen height in all-caps (`case`-sensitive forms):** a default hyphen is vertically centered for lowercase text; in an all-caps run it can visually hang too low relative to the capital letters. Check whether the font's OpenType `case` feature (case-sensitive forms — raises hyphens, dashes, parentheses, and similar punctuation to align with cap-height) is available and enable it (CSS `font-feature-settings: "case"`; in Figma, the `CASE` feature in the Type settings panel — a plugin script can read it through `openTypeFeatures` but cannot set it) for all-caps/small-caps nodes rather than leaving the punctuation optically low. Skip if the font doesn't expose the feature — don't fake it with manual vertical offsets.

7. **Hanging punctuation in Figma (the same switch `microtypography` Rule 4 uses, reached from the type-style side):**
    - Trigger: a display heading (≥24px) whose first character is an opening quote (`"`, `“`, `„`, `«`) or parenthesis, where leaving it inside the block makes the following letter's left edge look indented relative to body copy below it.
    - Figma has a native switch: `textNode.hangingPunctuation = true`. A live Inter probe confirmed left overhang for `"`, `“`, `„`, `«`, and `(`, but not for an em dash (`—`). Use the switch for the confirmed marks. Don't simulate the effect with a negative `paragraphIndent`.
    - Verify visually that the letter after the mark now aligns with the column edge. For an unsupported mark such as the tested em dash, say so and leave it. Splitting the mark into its own text node positioned to overhang the block is the only fallback, and it is worth the setup only for a hero heading.
   - Applies to display headings only — don't scan body copy for this.

## Figma Node Integration

When running with Figma access:

- **Read:** `textNode.fontSize`, `lineHeight`, `letterSpacing`, `fontName`, `leadingTrim`, `textCase`, `fontWeight` (read-only), `openTypeFeatures` (read-only), `hangingPunctuation`. Any of them returns `figma.mixed` when the node holds more than one style — read per range with `textNode.getStyledTextSegments([...])` instead of taking the first value.
- **Variable fonts:** `getStyledTextSegments(["fontName"])` returns the axis values in `fontName.variationSettings` (e.g. `{ wght: 500 }`). Use that number for Workflow step 2c/2d instead of trusting the named style string — an instance named "Regular" can carry a custom `wght` like 435. Check the same object for an `opsz` axis before stacking a manual tracking correction on top of it. If `variationSettings` is absent, the font is static: use `fontWeight`.
- **`textCase` check is the mandatory first branch for letter-spacing** (Workflow step 2): `"UPPER"`, `"SMALL_CAPS"`, `"SMALL_CAPS_FORCED"` → Branch A; `"ORIGINAL"`, `"LOWER"`, `"TITLE"` → Branch B. Read this before computing any tracking value — the two branches produce opposite-sign results, so skipping this check risks recommending negative tracking on all-caps text (actively harmful, not just suboptimal).
- **Vertical-trim check is mandatory first step for line-height:** always read `leadingTrim` before recommending a `line-height` value — see Workflow step 3. If it's `"NONE"` and the layer sits inside an Auto Layout frame with a tight `itemSpacing`, flag the interaction with `vertical-spacing` (optical gap will read smaller than the set gap value).
- **Kerning guard (hard rule, see Workflow step 5):** whenever `letterSpacing` is written, read `openTypeFeatures` first. If it reports `KERN: false`, flag it as likely unintentional and point the user to the Type settings panel — it can't be changed from a script.
- **Styles and variables come first:** if the node has a `textStyleId`, or `boundVariables` lists `lineHeight` / `letterSpacing`, the value belongs to that text style or variable. Report the corrected value as a change to the style or variable; don't override it on the single node unless the user asks for a local override.
- **Action back to Figma:** if asked to apply the fix directly, load the node's fonts, then set `lineHeight` and `letterSpacing` as `{ unit, value }` objects (e.g. `{ unit: "PERCENT", value: 150 }`), and `textCase` or `hangingPunctuation` where the step calls for it. OpenType features (figure styles, `CASE`, kerning) can't be written from a script — list them as steps for the user. Report the values first; only write to the node when the user asks for a direct application, not as a silent default.
- **Hanging punctuation:** set `hangingPunctuation = true` only on an eligible display heading — see Workflow step 7 — and only on explicit request, same as every other direct Figma write in this skill.

## Quality Checklist

- [ ] Line-height stated with its role range and the x-height ratio that placed it there; a fallback (x-height not measured) is labelled as a fallback.
- [ ] `text-case` checked first; Branch A (uppercase/small-caps) always positive, Branch B (sentence/title case) only negative above 24px — never the reverse sign.
- [ ] Font-weight modifier applied after the base tracking value, not before (sign comes from Branch A/B, magnitude scaled by weight) — heavier weight scales tracking down, lighter weight scales it up.
- [ ] Variable font `wght` read as a continuous value and interpolated, not snapped to the nearest named instance; `opsz` axis checked before stacking a full manual correction on top of it.
- [ ] x-height refinement applied only when the specific typeface's x-height is actually known, not guessed.
- [ ] Vertical-trim state is explicitly checked (Figma) or explicitly assumed (plain CSS) — never silently ignored.
- [ ] Kerning never switched off as a side effect of a tracking change; `KERN: false` found on a node is flagged, not silently kept.
- [ ] Number-figure style (oldstyle/lining × proportional/tabular) matches content role per the Step 4 table — not left at font default.
- [ ] In Figma, OpenType features (figure styles, `CASE`, kerning) reported as a step for the user — never reported as applied by script.
- [ ] Kerning never treated as a bug on tabular-figure nodes — suppressed kerning there is correct.
- [ ] Dash rendering (step 6) only adjusts local range-tracking or `case` feature — never overrides the character/spacing choice already made by `microtypography` Rule 1c.
- [ ] Hanging punctuation set with the native `hangingPunctuation` switch, on eligible display headings only, and verified visually.
- [ ] `case` OpenType feature checked (not assumed) before claiming a font can raise punctuation to cap-height; skipped cleanly if unsupported.
- [ ] If a Figma node was modified, changes were applied only on explicit request, not silently.
- [ ] Cross-reference to `vertical-spacing` noted when trim state affects Auto Layout gap perception.

## References

- Bringhurst, R. (2012). *The Elements of Typographic Style* (4th ed.). Hartley & Marks — inverse relationship between type size and tracking (larger size → tighter letter-spacing) for sentence-case text.
- Felici, J. (2003). *The Complete Manual of Typography*. Adobe Press — how x-height and glyph width should drive line-height and tracking selection per typeface.
- Butterick, M. *Practical Typography*, "Line spacing" — optimal line spacing is 120–145% of the point size; fonts that run small need less line spacing, and vice versa.
- Apple. *Human Interface Guidelines*, "Typography" — avoid light font weights, especially in small text.
- W3C. *CSS Fonts Module Level 5*, §3.4 `font-size-adjust` — aspect value (x-height divided by font size); Verdana 0.545 as a high value, Times 0.447 as a low one.
- Butterick, M. *Practical Typography*. — all-caps text needs added letter-spacing (5–12%) because default font spacing is tuned for mixed-case letterforms; heavier weights carry proportionally less need for it since strokes already fill more of the counter.
- Wathan, A., Schoger, S. (2018). *Refactoring UI*. — practical uppercase/small-caps tracking values by size band, and UI text minimum-size floor.
- Bringhurst, R. (2012). *The Elements of Typographic Style* (4th ed.), §5.2.1 — spaced en dashes, rather than em dashes, to set off phrases.
- *The Chicago Manual of Style* (17th ed., 2017). University of Chicago Press — the unspaced em dash as the US publishing convention for a parenthetical break.
- OpenType `case` feature (case-sensitive forms) — raises punctuation (hyphens, dashes, parentheses) to align with cap-height in all-caps/small-caps text.
- Felici, J. (2003). *The Complete Manual of Typography*. Adobe Press — oldstyle vs. lining figures, and their correct role split between running prose and tabular/display contexts.
- Latin, M. (2017). *Better Web Typography for a Better Web*. — tabular vs. proportional number spacing for UI/data contexts.
- OpenType number-style registered features: `onum` (oldstyle), `lnum` (lining), `pnum` (proportional), `tnum` (tabular).
- Bringhurst, R. (2012). *The Elements of Typographic Style* (4th ed.). Hartley & Marks — hanging punctuation as optical margin alignment.
- Related skill: [`microtypography`](../microtypography/README.md) Rule 1c — decides which dash character and spacing to use in prose; this skill only handles Figma-rendering-layer kerning/tracking on top of that choice.
- OpenType Font Variations spec (`wght`, `opsz` registered axes) — variable fonts expose weight as a continuous value and, when present, an optical-size axis designed to auto-adjust spacing/contrast per rendering size.
- OpenType `kern` feature / GPOS pair-positioning tables — per-pair optical correction (e.g. `AV`, `Ta`, `We`) baked into the font by its designer, complementary to (not replaced by) a uniform tracking value.
- CSS Working Group Draft: `leading-trim` / `text-box-trim` — crops the line box to cap-height/baseline, removing font-internal leading.
- Figma Plugin API Docs: `TextNode.leadingTrim`, `TextNode.letterSpacing`, `TextNode.openTypeFeatures` (read-only), `TextNode.textCase`, `TextNode.hangingPunctuation`, `TextNode.getStyledTextSegments`.
- Related skills: [`line-length-optimizer`](../line-length-optimizer/SKILL.md) (column width), [`microtypography`](../microtypography/SKILL.md) (character-level fixes) — apply after typesetting values are set, since column width and rag risk depend on the chosen font-size/line-height.
