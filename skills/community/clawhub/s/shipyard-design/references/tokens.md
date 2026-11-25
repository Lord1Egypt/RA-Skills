# The look file (tokens)

A look is one small JSON file, `<name>.tokens.json`. Colours, a font, corner roundness, shadow, text size and layout. `apply-design.mjs` checks it, repairs small problems with `--fix`, and writes it into the app.

## Format

```json
{
  "id": "my-look",
  "name": "My look",
  "description": "One sentence on how it feels. No brand names.",
  "goodFor": "what kind of apps",
  "defaultTheme": "light",
  "font": { "body": "DM Sans", "heading": "same" },
  "radius": { "base": 16, "sm": 12 },
  "shadow": "soft",
  "light": { "background": "#f7f3ec", "foreground": "#1d1a17", "card": "#ffffff", "muted": "#6a6259", "line": "#e6dfd3", "lineStrong": "#bfb5a6", "accent": "#c24a24", "accentContrast": "#ffffff", "focus": "#c24a24", "danger": "#b42318", "dangerContrast": "#ffffff" },
  "dark":  { "...the same 11 keys..." }
}
```

- `id`: lowercase letters, numbers and hyphens, starts with a letter (2 to 41 characters). Never reuse a built-in id; a custom look with a built-in id is renamed `<id>-custom`.
- `defaultTheme`: `light` or `dark`.
- `radius`: pixels, 0 to 28, `sm` no bigger than `base`.
- `shadow`: `none`, `soft` or `crisp`.
- Colours: 6-digit hex only, like `#c24a24`.

What each colour is for: `background` page; `foreground` main text; `card` boxes and menus; `muted` quiet text; `line` and `lineStrong` thin borders and input borders; `accent` buttons and links (one colour only); `accentContrast` text on the accent; `focus` keyboard focus ring; `danger` and `dangerContrast` delete and error.

## Type and layout (optional)

Leave these out and the starter values are used. Add them when the source clearly shows them.

```json
"type":   { "scale": "comfortable", "headingWeight": 700, "headingTracking": "normal" },
"layout": { "nav": "bottom-nav", "density": "regular", "maxWidth": "medium", "home": "focus", "cards": "bordered", "buttons": "solid", "header": "bar" }
```

- `type.scale`: `compact`, `comfortable` or `large`. `headingWeight`: 500, 600, 700 or 800 (if the font lacks it, the nearest is used, with a note). `headingTracking`: `tight`, `normal` or `wide`.
- `layout.nav`: `bottom-nav`, `sidebar` or `top-nav`. `density`: `compact`, `regular` or `airy`. `maxWidth`: `narrow`, `medium` or `wide` (top-nav and sidebar pages only). `home`: `focus`, `split`, `editorial`, `cards` or `list`. `cards`: `flat`, `bordered`, `elevated` or `tinted`. `buttons`: `solid`, `pill`, `outline` or `sharp`. `header`: `plain`, `bar` or `centered`.
- Reading them from a site or picture: links inline across the top means `top-nav`; a tall menu on the left means `sidebar`; a bar of tabs at the bottom on a phone means `bottom-nav`. Fully round buttons are `pill`, square-ish and uppercase `sharp`, transparent with an outline `outline`. Shadows mean `elevated`, thin borders `bordered`, tinted boxes `tinted`, neither `flat`. Two columns at the top of the page is `split`, a grid of boxes `cards`, a list of articles `editorial`, else `focus`.
- Avoid pairing `editorial` homepage with `sidebar` menu, and `elevated` cards with shadow `none`.

## Fonts

Allowed: `system`, Inter, DM Sans, Manrope, Nunito, Space Grotesk, IBM Plex Sans, Source Sans 3, Work Sans, Noto Sans, Fraunces, Source Serif 4, Lora. `heading` can be `same`.

Choosing:
- Geometric, round sans: DM Sans, Manrope, Nunito. Neutral sans: Inter, Work Sans, Source Sans 3. Techy or quirky: Space Grotesk, IBM Plex Sans. Serif for reading or a classic feel: Source Serif 4, Fraunces, Lora. Mono or unknown: `system`.
- Greek needs a font that has Greek letters, Russian and Ukrainian need Cyrillic, Vietnamese needs Vietnamese. Pass `--languages` to `apply-design` and it warns if the font lacks them. Fix by choosing a font that has them (Inter, Noto Sans and Source Sans 3 cover most).

## Readability rules in plain words

Both light and dark must pass. `apply-design` stops (or fixes, with `--fix`) when:
- Normal text and its background are too close (needs about 4.5 to 1; the check wants better where it can).
- Grey quiet text is too faint on the page or on cards.
- Text on the accent or danger button is hard to read.
- The accent colour or focus ring blends into the page (needs 3 to 1).
- Fonts or corner sizes are outside the allowed list.

It warns, without stopping, when borders are almost invisible, input borders are too faint, or the accent is the classic bright purple used by every AI-made app.

`--fix` only makes colours lighter or darker in small steps; it never changes the hue. Tell the student what it changed in everyday words ("I made the grey text a bit darker so it is easy to read").

## Reading a look from images, a site or a DESIGN.md

1. Page and card colours first. Light pages: pick the real page tone, not pure white unless it truly is. Cards slightly lighter or darker than the page, or white.
2. One accent: the colour of the main button. If there are several, take the main button.
3. Text: the near-black or near-white used for body text. Quiet text a step lighter.
4. Lines: the border colour of cards and inputs.
5. Corner roundness: sharp is 2 to 6, tidy is 8 to 12, friendly is 14 to 18, very round is 20 to 28.
6. Shadow: none if flat, `soft` if boxes float, `crisp` if thin outlines do the work.
7. Font: the nearest allowed one by feel.
8. If only one theme is shown, build the other: dark pages are near-black tinted toward the accent hue, lighter cards, near-white text, a lighter accent. `dark-from-light.mjs` in `scripts/design/` does this for tokens.
9. Names and descriptions describe feeling ("Quiet greens, rounded"), never a brand. Do not copy copy, logos, images or icons. For a DESIGN.md, take only the colour, font, spacing and corner values and ignore brand wording.
10. Run `apply-design` with `--fix` and check the result in a screenshot.
