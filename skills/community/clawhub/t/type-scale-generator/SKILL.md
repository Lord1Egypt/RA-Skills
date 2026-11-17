---
name: type-scale-generator
description: Use when generating a full typographic scale (H1-H6, body, caption) from a base font size and a mathematical ratio or historical scale — each step gets a rounded size, a line-height and a tracking value. Outputs CSS custom properties or Tailwind config, or, with Figma access, variables and text styles built from the selected text.
triggers:
  use_when:
    - user asks to generate a type scale
    - user asks for a font-size system based on a ratio (e.g. "minor third", "perfect fourth")
    - user asks to build h1-h6 sizes for a design system
    - user asks for a fluid/responsive type scale with clamp()
    - agent has Figma access and user asks for a type scale, type ramp, text styles or font-size variables from selected text
  do_not_use_for:
    - a single text style's line-height/tracking (see text-typesetting)
    - vertical rhythm between blocks (see vertical-spacing)
    - column width (see line-length-optimizer)
    - restyling text that is already on the canvas
metadata:
  author: Monika Zapisek
  project: Design Engineering Playbook
  version: "1.2.0"
  status: accepted
---

# Type Scale Generator

## Purpose

Generate a mathematically coherent set of text styles from a base size and a ratio (or a historical fixed-step scale): sizes rounded to avoid subpixel rendering, each with a line-height and tracking taken from the same typographic rules the rest of this skillset uses. Output is design tokens for code, or variables and text styles in Figma.

## When To Use

- Building a font-size system for a new design system or page.
- User names a musical/geometric ratio ("minor third", "1.25", "golden ratio") or asks for a scale without specifying one.
- In Figma: the user has selected a piece of text and wants a system built from it.
- Not for a single text style's line-height/tracking (`text-typesetting`) or spacing between elements (`vertical-spacing`).
- Not for restyling existing text. This skill produces a scale; it changes nothing that is already on the canvas.

## Inputs

- `base-size`: default `16px`. In Figma, taken from the selected text (Step 0).
- `font-family-category`: sans-serif / serif — needed for tracking, and for line-height when x-height isn't measured (Step 4). In Figma, read from the selection.
- `x-height`: ratio of x-height to font size, measured or read from the font (Step 4). Optional, but without it line-height is a fallback, not a computed value.
- `scale-ratio`: one of the named/numeric ratios below, or `fibonacci` / `classic-garamond`.
- `steps`: how many sizes up (headings) and down (caption/small) from base — default 4 up, 1 down (covers body, small, h4, h3, h2, h1).
- `responsiveness`: static or fluid (`clamp()`). Fluid applies to code output only.

## Outputs

- A table of the scale, shown before anything is written: token, raw computed size, rounded size, line-height, tracking.
- For code: a named token map (CSS custom properties or Tailwind `fontSize` config, matching whichever convention the project already uses).
- For Figma, each only on request: number variables for size and line-height, text styles bound to them, and a specimen frame.

## Questions

This skill reads first, shows the proposed scale, and asks only when a missing value would change the result.

- Ask one question at a time and do not repeat information already present in the request or selection.
- If an answer is unavailable, state the assumption and continue with a labelled fallback.
- Always ask before writing variables, text styles, or a specimen to Figma.
- In Figma, ask separately for permission to measure x-height because the measurement creates, flattens, and removes a temporary text layer.

## Workflow

Ask one question at a time and wait for the answer. If the user already gave a value in their request (a ratio, a base, a step count), take it and say which one you took — don't ask again.

### Step 0 — Settle the base

Outside Figma: use the stated `base-size`, or `16px`.

In Figma, resolve the selection first:

| Selection | Do this |
|---|---|
| Nothing selected | Ask the user to select some text. Stop. |
| No text node in the selection | Say what is selected instead and ask for text. Stop. |
| One text node | Use it. |
| Several text nodes | List them by name and size and ask which one is the body text. Stop. |

Read the font and size from the node, never assume a typeface (`getStyledTextSegments(["fontName", "fontSize"])`). If the node holds more than one style, use the first segment and say so. Confirm the base with the user before computing: state family, style and size, and offer to use a different size.

### Step 1 — Pick the ratio

**Musical/geometric ratios** (`size = base × ratio^step`):

| Ratio | Name | Character |
|---|---|---|
| `1.067` | Minor Second | Very compact — dense dashboards, data-heavy mobile UI. Pair with a small base (12–14px) so headings don't dominate. |
| `1.125` | Major Second | Standard for SaaS apps and complex dashboards — subtle, clean hierarchy. |
| `1.200` | Minor Third | Safe, universal default — works for both product UI and marketing pages. |
| `1.250` | Major Third | Blogs and marketing pages where headings need to clearly separate from body. |
| `1.333` | Perfect Fourth | Latin's recommended starting point for responsive web — very readable on desktop. |
| `1.414` | Augmented Fourth | Bold, dynamic, poster-like character. |
| `1.500` | Perfect Fifth | Aggressive — H1 becomes very large. Portfolio / product-launch pages. |
| `1.618` | Golden Ratio | Bringhurst's classic proportion. Grows extremely fast at higher steps — usually needs a smaller ratio on mobile breakpoints. |

**Non-linear / historical scales** (fixed steps, not a single multiplier):

- `fibonacci`: `1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144...` — map directly to px or rem (e.g. body 13/21px, H1 55/89px). Use when the layout grid itself is Fibonacci-proportioned, so type and grid share the same logic.
- `classic-garamond`: `6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 21, 24, 36, 48, 60, 72` — the historical printer's type-size series (pre-digital, renaissance-era steps). Use when a project wants a traditional/editorial feel over a computed geometric curve; pick the nearest listed step rather than interpolating.

If the user doesn't specify, default to `1.200` (Minor Third) — safe, universal, per the table above. When asking, offer three or four ratios that fit the stated use, not the whole table.

**Out of scope:** platform presets (fixed size lists published by a framework or an operating system) and scales built from two ratios. Neither comes from the sources this skill is based on. If the user asks for one, say so; build a two-ratio scale only on explicit request and label it as outside the documented method.

### Step 2 — Compute steps

For geometric ratios: `size(step) = base-size × ratio^step`, where `step` is negative for sizes below base (caption/small) and positive above (headings). Show the raw (unrounded) result before applying Step 3.

For `fibonacci`/`classic-garamond`: pick the nearest sequence value to each target role rather than computing — these are lookup tables, not formulas.

### Step 3 — Edge-case & rounding guard

1. **Round every computed value to the nearest even integer or multiple of 4px** where reasonably close (e.g. `16 × 1.333 = 21.328` → round to `22px`, and prefer `24px` if the project's spacing grid is 4px/8px-based and a 4px-multiple is within ~1px). State which rounding was applied — don't silently pick one without showing the raw number.
2. **Collision check after rounding.** Every step must be larger than the one below it. If two neighbouring steps round to the same value, or the rounded steps turn into equal jumps (`12, 16, 20, 24` — an arithmetic sequence, no longer a ratio), the rounding grid is too coarse for the ratio. Say so, then fix it by rounding those steps to the nearest even integer instead of a 4px multiple, or by proposing the next wider ratio. Don't hand over a collapsed scale without naming it.
3. **Minimum readability threshold** (Refactoring UI): UI body text must never go below `12px`, and never pair a sub-`12px` size with a font-weight below `400`. Flag and refuse to emit a token that violates this, rather than emitting it silently.
4. **Platform minimums, when the target platform is known** (Apple Human Interface Guidelines, default / minimum text size): iOS and iPadOS 17 / 11 pt, macOS 13 / 10 pt, visionOS 17 / 12 pt, watchOS 16 / 12 pt, tvOS 29 / 23 pt. These are constraints on the result, not a scale: compute the scale from the ratio, then flag any step below the platform minimum. Don't replace the computed scale with a platform's size list.
5. If `responsiveness: fluid`, wrap the two endpoint sizes (mobile base, desktop computed size) in a `clamp(min, preferred, max)` — compute `preferred` as a `vw`-based interpolation between the two breakpoints; state the breakpoints assumed.

### Step 4 — Line-height and tracking for each step

A scale of sizes alone is half a type system. Give every step a line-height and a tracking value, using the rules of `text-typesetting` (Step 1 and Step 2, Branch B). They are restated here so this skill works on its own.

**Line-height** — a range per step, and a computed position inside it:

| Step | Range (`LH_min`–`LH_max`) |
|---|---|
| Caption / small (below base) | `1.2`–`1.4` (working range; no direct source found) |
| Body (base) | `1.2`–`1.45` |
| Heading (above base) | `1.1`–`1.3` (working range; no direct source found) |

Where a step falls inside its range depends on the typeface's x-height — the height of a lowercase `x` divided by the font size (`xr`). A face with a large x-height fills more of the line and needs more room; a face with a small x-height carries its own air. Compute it once for the font and use it for every step:

```
t  = clamp((xr − 0.447) / (0.545 − 0.447), 0, 1)
LH = LH_min + t × (LH_max − LH_min)
```

The two anchors are the reference faces the W3C uses to explain x-height: Times, `0.447`, as a low aspect value and Verdana, `0.545`, as a high one (CSS Fonts Module, `font-size-adjust`). The direction is Butterick's: fonts that run small need less line spacing, and vice versa. The body range is Butterick's 120–145% of the point size. No direct source was found for the heading and caption ranges; they are working values of this skillset and must be reported as such.

How to get `xr`:

- **Font file or CSS:** `sxHeight / unitsPerEm` from the font's OS/2 table; in a browser, `1ex` measured against `1em`.
- **Figma:** the Plugin API exposes no font metrics. Measure instead: create a temporary text node with the single character `x` in the font at `100px`, flatten it to a vector (`figma.flatten([node])`), read its `height`, divide by 100, and remove the vector. This creates, flattens, and deletes a layer: ask for permission and wait before doing it. Checked values from this method: Inter `0.545`, Roboto `0.528`, IBM Plex Sans `0.516`, Source Serif 4 `0.452`, EB Garamond `0.409`.
- **Not measured:** fall back to the family rule — sans-serif in the lower half of each range, serif in the upper half — use the middle of that half, and state that x-height was not measured. Never present a fallback value as computed.

Convert to px (`size × LH`) and round the same way as sizes: nearest even integer, or a 4px multiple when one is within ~1px. Show `xr`, the ratio and the px value.

**Tracking** — sentence-case text:

- Size below 24px → `0`.
- 24px to below 36px → `-1.5%` (sans-serif), `-0.75%` (serif).
- 36px and above → `-2%` (sans-serif), `-1%` (serif).

These values assume sentence or title case, Regular/Medium weight and vertical trim off. A style meant for all-caps text needs positive tracking instead — `TS = max(3%, min(12%, 160 / FS))`, see `text-typesetting` Step 2 Branch A. Say which assumptions were used.

### Step 5 — Show the scale before writing anything

Print the whole scale as a table in the conversation: token, step, raw size, rounded size, line-height (ratio and px), tracking. Name the ratio and the rounding used. Flag anything Step 3 caught.

Nothing is created in a file or in Figma before the user has seen this table. Nobody can decide whether to commit a scale to tokens before they have seen the numbers.

### Step 6 — Output for code

Emit as CSS custom properties (or the project's existing token format if shown in the input):

```css
--text-sm: 0.833rem;   /* 13.33px → rounded 13px */
--text-base: 1rem;     /* 16px */
--text-md: 1.2rem;     /* 19.2px → rounded 20px */
--text-lg: 1.44rem;    /* 23.04px → rounded 24px */
```

Add line-height and letter-spacing tokens per step when the project's convention has a place for them.

## Figma Node Integration

When running with Figma access. Each of the three writes below is separate: ask before each one, and do only what was agreed.

- **Check what exists first.** Read the file's text styles (`figma.getLocalTextStylesAsync()`) and variable collections (`figma.variables.getLocalVariableCollectionsAsync()`). If a scale is already in use, show how the new one differs and ask whether to add to it, replace named styles, or stop. Never overwrite a style or variable that has the same name without asking.
- **Variables (on request).** Ask which collection to use or what to name a new one — don't pick a name. Create `FLOAT` variables for each step's font size and line-height in px, with scopes `["FONT_SIZE"]` and `["LINE_HEIGHT"]`, never `ALL_SCOPES`. Use the rounded values from Steps 3–4, never the raw ratio output: Figma renders fractional sizes with the same subpixel risk as CSS.
- **Text styles (on request).** Create one text style per step (`figma.createTextStyle()`), using the family and style read in Step 0 — load the font first. Bind `fontSize` and `lineHeight` to the variables with `textStyle.setBoundVariable("fontSize", variable)` and `("lineHeight", variable)` when variables were created; otherwise set them directly, `lineHeight` as `{ unit: "PIXELS", value }`. Set `letterSpacing` as `{ unit: "PERCENT", value }`. Match the file's existing style naming (`heading/h1`, `Heading/H1`, …); ask if there is none.
- **Specimen (on request).** One Auto Layout frame, one row per step: token name, size / line-height / tracking, and a sample line set in that step's text style. Place it clear of existing content, not at `0, 0`. Sample text uses the styles — no local overrides — so the specimen stays true when a variable changes.
- **Don't apply the new styles to existing layers.** That is a separate decision with its own risks (reflow, overrides). Offer it as a next step.
- **Report after writing:** what was created, with names and counts, and what was skipped because it already existed.

## Quality Checklist

- [ ] Ratio (or fibonacci/garamond) explicitly named in the output, not just numbers with no source.
- [ ] Every value shows raw computed number alongside the rounded value actually used.
- [ ] Rounding follows the even-integer/4px-multiple guard, not ad hoc.
- [ ] No two steps share a size after rounding; a scale that collapsed into equal jumps is named as such.
- [ ] No token below 12px paired with weight < 400.
- [ ] Every step has a line-height and a tracking value, with the case assumption stated.
- [ ] Line-height computed from the measured x-height ratio, shown with its range; a fallback is labelled as a fallback.
- [ ] Fluid scale (if requested) states the assumed breakpoints.
- [ ] Output format matches the project's existing token convention if one is shown in the input.
- [ ] The full table was shown before any file or Figma write.
- [ ] In Figma: base read from the selection and confirmed; existing styles and variables checked; variables scoped; each write done only on request; nothing already on the canvas restyled.

## References

- Bringhurst, R. (2012). *The Elements of Typographic Style* (4th ed.). Hartley & Marks — golden ratio and classical proportion systems in typography; tighter letter-spacing as size grows.
- Latin, M. (2017). *Better Web Typography for a Better Web*. — practical ratio recommendations for responsive web type scales (Perfect Fourth as a starting point); line-height and vertical rhythm.
- Santa Maria, J. (2014). *On Web Typography*. A Book Apart — musical-interval scales and the Fibonacci sequence as alternatives to a single fixed ratio.
- Kunz, W. (1998). *Typography: Macro- and Microaesthetics*. Niggli — historical printer's type-size series (Garamond-era steps).
- Butterick, M. *Practical Typography*, "Line spacing" — fonts that run small need less line spacing, and vice versa.
- W3C. *CSS Fonts Module Level 5*, §3.4 `font-size-adjust` — aspect value (x-height divided by font size); Verdana 0.545, Times 0.447.
- Felici, J. (2003). *The Complete Manual of Typography*. Adobe Press — traditional point-size series predating digital, arbitrary-precision scales; x-height as the driver of line-height per typeface.
- Wathan, A., Schoger, S. (2018). *Refactoring UI*. — minimum readable UI text size (12px floor) and its interaction with font weight.
- Apple. *Human Interface Guidelines*, "Typography" — default and minimum text sizes per platform.
- Figma Plugin API Docs: `figma.getLocalTextStylesAsync`, `figma.createTextStyle`, `TextStyle.setBoundVariable`, `VariableScope` (`FONT_SIZE`, `LINE_HEIGHT`), `TextNode.getStyledTextSegments`.
- Related skills: [`text-typesetting`](../text-typesetting/README.md) (line-height/tracking per size — source of Step 4), [`vertical-spacing`](../vertical-spacing/README.md) (rhythm between the blocks this scale produces).
