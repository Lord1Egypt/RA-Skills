# Themes and templates

Read when the user has brand colors, wants a theme, or has (or wants) their own template. A theme changes values; a template changes structure. Neither changes what a color means. Values: [style-dna.md](style-dna.md). Classes: [components.md](components.md).

## Where the skill looks

First match by name wins.

| Order | Themes | Templates | For |
|---|---|---|---|
| 1 | `./.sketchy/themes/*.css` | `./.sketchy/templates/*.html` | this project; commit it so the team shares it |
| 2 | `~/.sketchy/themes/*.css` | `~/.sketchy/templates/*.html` | this user, every project (`SKETCHY_HOME` moves it) |
| 3 | the skill's `themes/` | the skill's `templates/` | built-ins |

Before building, list what exists in 1 and 2. If the user has a theme or template, use it and say so. A file in 1 shadows one with the same name in 2 or 3.

## How a theme works

A theme is a CSS file loaded right after `engine/sketchy.css`. It sets `--sk-*` custom properties and nothing else: no selectors other than `:root` and `:root[data-theme="night"]`, no component rules, no `!important`.

```html
<link rel="stylesheet" href="engine/sketchy.css">
<link rel="stylesheet" href="themes/harbor.css">
```

| Group | Tokens | May a theme change it? |
|---|---|---|
| Paper | `paper`, `paper-deep`, `paper-light`, `sheet`, `veil`, `halo`, `shadow` | rarely; keep it a mid-tone paper, not white |
| Graphite | `ink`, `graphite`, `graphite-soft`, `graphite-faint`, `focus` | rarely; keep 4.5:1 on the paper |
| Red pencil | `red` (lines), `red-ink` (writing), `red-frame` (main button), `red-soft` | yes: this is where a brand accent goes |
| Colored pencils | `blue`, `green`, `yellow`, `orange`, `violet`, `rose`, `teal`, `peach` | yes, as pastels, keeping the order's meaning |
| Record | `figure`, `gold` | `figure` must stay dark by day, gold by night |
| Stamps | `stamp`, `stamp-blue`, `stamp-green` | yes; `stamp` usually equals `red-ink` |
| Postal | `cream`, `card`, `tape`, `tape-text`, `cover`, `elastic`, `door`, `door-edge`, `door-ink` | yes; `cover` is the natural home for a dark brand color |
| Paper documents | `label-ink`, `label-ink-soft` (cover label), `slip-red`, `slip-paper`, `slip-text` (registered slip, registration label) | yes; `slip-red` follows the accent only if the accent replaced red |
| Button backings | `btn-hover`, `btn-press`, `btn-accent`, `btn-accent-hover` | yes, as pale tints that keep graphite at 4.5:1 |
| Margin math | `maths-ink` | rarely; keep it near graphite |
| Fonts | `font-hand`, `font-mono`, `font-body` | only to add a script the bundled fonts lack (they cover Latin and, for Caveat, Cyrillic), from a local, openly licensed file |
| Sizes, motion | `size-*`, `ease*`, `dur-*` | no |
| `paper-texture` | set by the engine | never |

A few values stay fixed on purpose: inside paper documents (`.sk-doc`, slips, labels, postcards) the pencils switch to day ink so a light document reads the same on any desk; the cover cloths chosen by `data-cover` set their own color; the door's hard shadow and the gauge hatching are fixed. Check these in the screenshots when a theme moves far from the defaults.

## A brand theme from one color

1. **Keep paper and graphite.** They make it a sketchbook. A brand's white background is not paper.
2. **Decide whether the brand color reads as an accent.** It does if it is saturated, clearly not gray, and not a pastel. Then it becomes the red pencil, and red is gone from this theme.
3. **If it does not read as an accent** (pale, grayish, or very close to the paper), leave red as red and use the brand color for the cover (`--sk-cover`) and, as a pastel, for the first pencil slot.
4. **Derive the three red roles:** `red-frame` is the brand color; `red-ink` is the brand color darkened until it reaches 4.5:1 on the paper (3:1 is the floor for text of 28 px and up); `red` (lines) is a lighter, softer tint that still reads against the paper.
5. **Resolve clashes.** If the brand hue sits next to a pencil (a blue brand next to `--sk-blue`), move that pencil to a clearly different pastel so a data series is never mistaken for the accent.
6. **Write the night values too:** lighter `red-ink`, the brand on `cover`, gold and blue untouched.
7. **Check by looking.** Build, run `lint.mjs` (it measures contrast on the real paper), shoot both themes, look at a slide with a chart, a stamp and an accent button.

For reference, on the day paper `#c3c8d1`: graphite 5.3:1, ink 9.0:1, the default red ink 3.8:1, `graphite-soft` 3.8:1.

```css
/* themes/harbor.css: brand teal #0f766e as the accent */
:root {
  --sk-red: #7fb8b0;          /* lines: soft tint of the brand */
  --sk-red-ink: #0b5d57;      /* writing: 4.6:1 on #c3c8d1 */
  --sk-red-frame: #0f766e;    /* the main button frame: the brand itself */
  --sk-red-soft: #b9d9d4;
  --sk-stamp: #0b5d57;
  --sk-teal: #d8c2ae;         /* the teal pencil would read as the accent: a sand pastel instead */
  --sk-slip-red: #0f766e;     /* registration label block; its text stays at 5.0:1 */
  --sk-btn-accent: #bcd3cf;   /* main button backing: graphite on it 5.6:1 */
  --sk-cover: #24433f;        /* door ink on it stays above 9:1 */
}
:root[data-theme="night"] {
  --sk-red: #5fb3a9;
  --sk-red-ink: #8fd0c8;      /* 9.7:1 on #161c2b */
  --sk-red-frame: #5fb3a9;
  --sk-stamp: #5fb3a9;
  --sk-btn-accent: #1f3a37;   /* chalk on it 9.8:1 */
  --sk-cover: #1d3532;
}
```

A cover with a `data-cover` value sets its own cloth and ignores `--sk-cover`: leave `data-cover` off to show the brand cover.

Never: a brand gradient, a brand sans in place of Caveat, two accents, the logo repeated on every slide (one mark on the cover and the end page is enough).

## The starter file

Copy `themes/_starter.css` (in the skill) to `./.sketchy/themes/<name>.css` or `~/.sketchy/themes/<name>.css` and change only the values you need; delete the lines you keep at their defaults so the theme shows what it changes. Name it after the brand or the occasion (`harbor.css`, `board-2026.css`), lowercase kebab-case. `sketchy theme <name>` runs this whole section.

## Templates

A template is an HTML file built only from engine classes and tokens, with `<!-- slot:name -->` comments where the agent writes content. `templates/deck.html` is the model: it has `slot:title`, `slot:theme` and `slot:slides`, and its example content is a fictional company that is replaced in full.

```html
<!doctype html>
<html lang="en" class="sk" data-theme="day">
<head>
<meta charset="utf-8">
<!-- slot:title -->
<title>Board update</title>
<link rel="stylesheet" href="../engine/sketchy.css">
<link rel="stylesheet" href="../themes/harbor.css">
</head>
<body class="sk">
<!-- board-update: harbor theme. Fixed: cover and closing page. Slots: title, summary, slides. -->
<main class="sk-deck" data-seed="board-update" data-transition="page">
  <section class="sk-slide" data-layout="cover">...brand cover, fixed...</section>
  <!-- slot:summary (one title slide: the answer in one line) -->
  <!-- slot:slides -->
  <section class="sk-slide" data-layout="end">...closing postcard, fixed...</section>
</main>
<script src="../engine/sketchy.js"></script>
<script src="../engine/sketches.js"></script>
<script src="../engine/sketchy-deck.js"></script>
<script>SketchyDeck.mount();</script>
</body>
</html>
```

| Rule | Why |
|---|---|
| Use the same `<link>` and `<script>` paths as the built-in templates | `scripts/new.mjs` copies the engine next to the file and treats yours like a built-in |
| Slot names are lowercase kebab-case nouns; a hint may follow in the comment | the agent fills the right thing in the right place |
| Keep fixed parts (brand cover, legal line, closing page) outside slots | they stay the same in every deck |
| Example content is obviously fictional and fully replaced | half-replaced examples are the most common lie in a deck |
| One comment near the top says what it is for, its theme and its slots | the next agent reads that before anything else |
| Only tokens in `<style>`, no external URLs, no CDN fonts | the built file must open offline |
| A `data-seed` named after the template | the same template draws the same way |

## Sharing

| With | How |
|---|---|
| A team | commit `.sketchy/themes/` and `.sketchy/templates/` in the project repository |
| Yourself, everywhere | keep them in `~/.sketchy/` |
| Someone without the skill | send the built file from `scripts/build.mjs`; it carries engine, theme and fonts |
| A custom font | put the `.woff2` next to the theme, load it with a relative `@font-face`, include its license file; only fonts whose license allows redistribution |

Before sharing a template, fill a copy with real content, run `lint.mjs` and `shoot.mjs` on it in both themes, and look at the contact sheet.
