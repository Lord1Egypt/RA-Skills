---
name: Typography Foundations
slug: typography
version: 1.0.0
homepage: https://clawic.com/skills/typography
description: Set type for screen and print: measure, leading, tracking, optical sizes, weight axes, and the difference between display and text cuts.
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## Measure, leading, and the reading engine

- Measure = characters per line, the single biggest readability lever. English body: 45-75 chars, sweet spot ~66. CJK: 20-40 chars (each glyph carries more meaning). Mobile effective measure after padding: 30-40 chars is fine, narrower than print tolerates.
- Print tolerates a wider measure than screen: screen reading runs ~20-25% slower than print at equal measure, so screen body sits in the lower half (45-60), print can push to 75-90 in two-column work.
- Leading and measure are inversely coupled: a longer line needs more leading because the eye must track further back to the next line's start. A 75-char line at 1.3 reads cramped; bump to 1.45-1.5.
- Leading and x-height are inversely coupled: tall x-height faces (Inter, Söhne) need more leading than low x-height faces (Georgia, Caslon) at the same size. Two faces at 16px can need 1.4 vs 1.6 to read the same.
- Leading bands: display 0.9-1.1; headings 1.1-1.2; body 1.2-1.5 (screen leans 1.4-1.6, print 1.2-1.3); long-measure body +0.1.
- A line-height in px is a bug: it does not scale with font-size, so nested smaller text inherits the parent's gap. Use unitless (1.5) or em (1.5em), never 24px.
- Body below 14px on screen is a legibility tax: hinting and subpixel rendering degrade below 16px on non-HiDPI. 16px is the screen body floor for content you read, not glance.
- Inheriting 1.5 into a 48px heading gives 72px line spacing and blows the rhythm: set line-height unitless on the body and reset per heading element.

## Tracking and optical sizes

- Tracking direction flips by case: lowercase display wants negative (-10 to -30 / 1000 em), caps want positive (+50 to +100). Tightening caps closes the optical gaps uppercase creates; tightening lowercase display removes air that looks elegant at 12pt and anemic at 120pt.
- Tracking is scale-dependent: the same -20 / 1000 em reads as tight at 120pt and invisible at 12pt. That is why optical-size axes exist: they interpolate tracking, x-height, and contrast together. Hand-tuning tracking across a size range without opsz is manual work the axis does for free.
- CSS `letter-spacing` in px does not scale with font-size: -0.5px is huge at 12px and nothing at 120px. Use em (`-0.02em`) so it tracks the size.
- Small body (sub-14pt) often needs +5 to +15 tracking to open counters that subpixel rendering clogs. Negative tracking on small body closes counters and drops legibility; the `tracking-tight` class on body is a frequent culprit.
- Body tracking at 0 to -5 / 1000 em is the flat zone; past -10 at body sizes you fight the type designer's spacing. Trust the built-in spacing for body, override only at display sizes.
- `word-spacing` is the lever nobody pulls: +5 to +10 / 1000 em loosens long-measure ragged text without touching letter spacing; justified text reads denser when word-spacing tightens.

## Display cuts vs text cuts

- The cut is not about size, it is about optical compensation. Display cuts have higher stroke contrast, tighter letterspacing, lower x-height, refined terminals. Text cuts have larger counters, more open apertures, taller x-height, sturdier joins. Same family, different job.
- A text cut at display size looks anemic: counters enlarged to survive 10pt look gaping at 96pt, strokes read thin. A display cut at body looks chunky and clogs: high contrast strokes turn to mush below 14pt, tight spacing fills counters.
- The crossover is ~28-32pt: above it, reach for the display cut (or opsz at the display end); below it, the text cut. Faces with no opsz axis have a native size band where they were designed to sit.
- Optical compensation is invisible until you see the wrong cut next to the right one: the wrong one reads as "off" with no named cause. The signal is counter fullness and stroke contrast relative to size.
- Geometric sans (Futura, Avenir) at body size on screen: low x-height and even strokes read as elegant but clog below 16px. Humanist sans (Inter, Söhne, Source Sans) are designed for the small screen and survive 14px. Pick by where the face will actually sit.
- Superfamilies with serif + sans + optical sizes (Source, IBM Plex, Roboto variable) carry a whole product without pairing risk; the cost is a thinner identity than a bespoke pairing.

## Weight, variable fonts, and faux bold

- Weight reads one step heavier on screen than print: subpixel and grayscale AA fatten stems. A 400 body on screen looks like a 500 on paper. Print body sits at 400; UI body often sits at 500 because 400 reads thin at small screen sizes.
- Faux bold (synthesized when the bold weight file is missing) shows as uneven stem thickening and clogged counters. The signal: bold looks heavier in some glyphs than others, counters shrink unevenly. Fix: load the actual weight file, set `font-synthesis: none`.
- Variable fonts expose `wght` as a continuous 1-1000 range. The win is not more weights, it is the exact optical weight a size needs: a 550 at 14px, a 500 at 16px, a 480 at 24px. Static fonts force 400 or 700 with nothing between.
- Variable font cost: one file is smaller than four static weights above ~3 weights, but every axis you load (opsz, wght, slnt, wdth) adds parse time. Load only the axes you use; `font-variation-settings` on an axis the file lacks is a silent no-op.
- UI weight ladder: body 400-500, sub-label 500-600, heading 600-700. Print ladder: body 400, subhead 500-600 italic, heading 700. Past 700 most UI faces read toyish; reserve 800+ for display faces built to carry it.
- Italic is a separate design, not slanted roman. A real italic has different letterforms (a, e, f change shape). Synthesized oblique (slant transform) reads as cheap and breaks at joins; load the italic file.

## Type selection and pairing

- Pair by contrast in one axis, harmony in the rest: contrast in classification (serif + sans), harmony in x-height and era. Two contrasts (geometric sans + humanist serif + different x-heights) read as clash.
- The uncanny valley of pairing: two faces that are similar but not identical read worse than two clearly different faces. Two humanist sans with slightly different x-heights is the common failure; you cannot name why it looks off.
- Match x-heights optically, not metrically, when pairing: set both faces side by side, size the sans down until the x-heights align, then read the ratio. A 16px serif paired with a 14px sans can look balanced if their x-heights match.
- One superfamily with serif + sans (Source, IBM Plex, Roboto) is the safe product default; the designer already matched x-heights and weights. Bespoke pairing wins on identity, loses on maintenance.
- Avoid pairing two distinctive display faces: two faces with strong character (two slabs, two geometric display faces) compete. One neutral + one distinctive is the stable config.
- Catalog of classifications by what they signal: geometric sans (Futura) = modern, formal; humanist sans (Inter, Frutiger) = neutral, readable, the UI default; grotesque (Helvetica) = corporate, flat; transitional serif (Times, Georgia) = readable, traditional; old-style (Caslon, Garamond) = warm, literary; slab (Rockwell) = industrial, assertive; mono = code, data, technical.
- Mono for data tables and code only: tabular figures and fixed advance widths align columns. Mono for body is a legibility tax; the even rhythm that helps code hurts prose.

## Scale, rhythm, and the grid

- Modular scale beats arbitrary px: pick a ratio (1.2 minor third, 1.25 major third, 1.333 perfect fourth, 1.5 perfect fifth, 1.618 golden) and a base (16px), derive sizes as base x ratio^n. The result has internal rhythm, not a pile of typed numbers.
- Ratio choice signals density: 1.2 is dense (documentation, dashboards), 1.333 is balanced (marketing sites), 1.5-1.618 is expressive (hero pages, editorial). The wider the ratio, the more the heading dominates.
- Baseline grid only works if line-height is a multiple of the grid: a 4px grid with 16px body at 1.5 (24px line) snaps; at 1.4 (22.4px) it does not. Pick line-height first, derive the grid, not the reverse.
- Type scale snaps to the spacing scale: if spacing is 4/8/12/16/24/32, type sizes should land on or near those multiples so the rhythm holds across the layout. A 17px heading in a 4px grid is a drift that compounds.
- Two sizes + three weights + three grays generate more hierarchy than five sizes. Add a size only when weight and color cannot carry the distinction; the competent adds a size, the elite changes weight or color first.
- `tabular-nums` on any number that aligns in a column or changes (price, timer, count): `font-variant-numeric: tabular-nums` is the CSS, `font-feature-settings: "tnum"` the fallback. Proportional figures are the default and misalign.

## Screen rendering and fallbacks

- System font stack renders instantly, web font renders identity. The tradeoff is the FOIT/FOUT flash: `font-display: swap` shows fallback then swaps (FOUT, shift risk), `block` hides text up to 3s then shows fallback (FOIT, no shift but invisible), `optional` loads if cached else stays fallback (no shift, no flash, first visit sees the fallback).
- Layout shift on swap is the descender jump: fallback and web font have different x-heights and metrics, so lines reflow when the swap fires. Match the fallback's x-height and advance width to the web font, or use `size-adjust` on the fallback, to kill the shift.
- Subpixel rendering is dead on macOS (Retina forces grayscale AA) and fading on Windows (HiDPI). Hinting matters below 16px on non-HiDPI: a hinted font (Verdana, Tahoma, Inter) stays crisp at 12px; an unhinted face turns to fuzz. Pick hinted faces for dense UI.
- Variable font as the only file: one woff2 with the axes you need replaces 4-6 static weights. Below ~3 weights the static set is smaller; above it, variable wins on bytes and on the optical range.
- `font-feature-settings` is the power tool: `tnum` (tabular figures) for any number that aligns in a column or changes, `lnum` vs `onum` (lining vs old-style figures) for data vs prose, `ss01`-`ss20` for stylistic sets the designer built in. Set on body, not per element, to avoid cascade cost.

## Print: where the rules invert

- Leading is physical in print: the space between baselines in points, not a multiplier. 10pt type on 13pt leading = 3pt of space. The ratio is the same concept, the unit is absolute.
- Print body sits at 9-11pt with 11-13pt leading (120-130%); screen body sits at 16-18px. Same ratio, different absolute sizes, because print is read at ~30cm and screen at ~50cm.
- Justify works in print, breaks on screen. Print has a hyphenation engine (InDesign, TeX) that breaks words to keep word spacing even; CSS `hyphens: auto` is spotty and the engine is weak, so justified web text gets rivers (word spaces stacking vertically) and loose lines. Ragged right is the web default for a reason.
- Tracking and kerning survive print exactly as set; what you see in the proof is what prints. Screen rendering rounds stem edges, so tracking reads ~5-10% tighter on screen than it will in print. Proof in the target medium, not on screen.
- Widows (last line of a paragraph alone at the top of the next column) and orphans (first line alone at the bottom) are print sins; CSS `widows` and `orphans` properties control them but support is uneven. Manual fix: tighten or loosen the paragraph by a word.
- Rivers form in justified text when word spaces stack vertically; the fix is hyphenation, looser tracking, or a narrower measure. A river is visible as a white diagonal stripe through a block of text.
- Print measure is wider: two-column work tolerates 50-60 chars per column, single-column can go to 75-90. Screen single-column stays at 45-60 because the eye tires faster on self-illuminated text.

## Situations, play

| Situation | Play |
|---|---|
| Body feels cramped on mobile | Bump leading to 1.5-1.6, not font-size. Check measure is 30-40 chars. |
| Heading looks loose and airy | line-height 1.0-1.15, tracking -10 to -20 / 1000 em. Reset inherited line-height. |
| Display face looks anemic at large size | Wrong cut. Switch to display opsz, or tighten tracking -20 to -30. |
| Text face clogs at small size | Wrong cut. Switch to text opsz, or open tracking +10 to +15. |
| Pairing reads "off" but you cannot name why | x-height mismatch. Set both faces side by side, size the sans down until x-heights align. |
| Justified web text has rivers | Enable `hyphens: auto` + lang attribute, or switch to ragged. Reduce measure to 45-60. |
| Web font swap causes layout shift | Match fallback x-height and advance width. Use `font-display: swap` + `size-adjust` on the fallback. |
| Heading inherits body line-height | Set `line-height` unitless on body, reset per heading. Never px line-height. |
| Bold looks uneven, counters clog | Faux bold. Load the real bold weight file, set `font-synthesis: none`. |
| Caps look too tight | Add +50 to +100 / 1000 em tracking. Caps need positive, lowercase display needs negative. |
| Numbers misalign in a table | `font-variant-numeric: tabular-nums` (or `font-feature-settings: "tnum"`). Proportional figures are the default. |

## Where camps disagree

- **Serif vs sans for body**: serif wins in print (serifs guide the eye along the line, long-form reading-speed studies favor serif). Sans wins on low-DPI screen (serifs fuzz below 16px without hinting). On HiDPI screen the gap closes; pick by identity, not legibility. The competent picks sans for screen by reflex, the elite checks the DPI and the measure first.
- **Justified vs ragged**: justify for formal, print, multi-column work where hyphenation is available; ragged for screen, narrow measure, and any context without a hyphenation engine. Justify without hyphenation is worse than ragged in every case.
- **System fonts vs web fonts**: system wins on perf and zero flash; web font wins on identity and the optical range a system stack cannot give. Variable fonts narrow the gap (one file, full optical range) but cannot beat zero-cost. The frontier is first-visit perceived performance vs brand consistency; `font-display: optional` is the compromise for content below the fold.
- **Modular scale vs pragmatic sizing**: scale gives rhythm and a defensible type system; pragmatic sizing (pick the size that fits the content) gives flexibility and handles edge cases a scale cannot predict. Scale for systems and design tokens; pragmatic for editorial one-offs.
- **Hyphenation on web**: `hyphens: auto` with a `lang` attribute works in modern engines but break quality varies by language and browser. The elite hyphenates long-measure justified text in print, leaves web ragged unless the CMS has a server-side hyphenation engine.

## Related Skills

Install with `clawhub install <slug>` if the user confirms:
- `figma` - where type specs become components, variables, and Dev Mode handoff
- `design-tokens` - pipe the type scale and font features into platform code via Style Dictionary
- `design-system` - the type scale, weights, and feature settings this skill feeds
- `css`, `tailwindcss` - the `font-variation-settings`, `font-feature-settings`, and `line-height` units this skill reasons about
- `accessibility` - contrast, resize, and the legibility floor this skill sets
