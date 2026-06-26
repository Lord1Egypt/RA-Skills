# Unicode Characters and Font Encoding

Reference for diagnosing and fixing build failures caused by non-ASCII
characters and monospace/code text that renders in the wrong font.  **The
correct fix depends on the TeX engine** — pdfLaTeX (8-bit) and XeLaTeX/LuaLaTeX
(Unicode) behave oppositely here, so identify the engine *before* applying any
fix below.

These bite hardest in literate programs, where source bytes — test fixtures,
Unicode normalization tables, ASCII-art diagrams — are woven *verbatim* into
the `.tex` and must then be typeset by the engine.  See the
`literate-programming` skill for the weaving angle.

Search patterns: `DeclareUnicodeCharacter`, `fontenc`, `pdffonts`,
`Unicode character`, `not set up`, `iftex`, `newunicodechar`, `beramono`, `T1`.

---

## Know your engine first

Run this before anything else — the same source needs different fixes per
engine, and a build system can switch engines without you noticing:

```bash
grep -m1 'This is' doc/ltxobj/forcing.log
#   "This is pdfTeX …"  → 8-bit engine  (Symptom 1 / Symptom 2 below apply)
#   "This is XeTeX …" / "This is LuaHBTeX …" → Unicode engine (see that section)
```

| | pdfLaTeX (8-bit) | XeLaTeX / LuaLaTeX (Unicode) |
|---|---|---|
| Unmapped non-ASCII byte | **fatal** `Unicode character … not set up` | non-fatal `Missing character` warning (renders if the font has the glyph) |
| `\DeclareUnicodeCharacter` | available (see below) | **undefined** — using it is an `Undefined control sequence` error |
| `\usepackage[utf8]{inputenc}` | relevant (provides the declaration mechanism) | silently **ignored** (`inputenc package ignored with utf8 based engines`) |
| Remap a code point | `\DeclareUnicodeCharacter{XXXX}{...}` | `\newunicodechar{<char>}{...}` (newunicodechar package) |
| Glyph selection | OT1/T1 font encodings + `fontenc` | `fontspec` / `\setmonofont` etc. |

**The build system decides the engine.** `latexmk -pdf` → pdfLaTeX;
`latexmk -xelatex` / `-lualatex` → the Unicode engines.  In Makefile-driven
literate projects the rule itself may be *tangled* from a `.nw` (e.g.
`tex.mk`), so a submodule/`make` update can flip the engine — re-check the
`.log` banner, never assume from a prior build.

Make engine-specific preamble code robust with `iftex` (verified to build
cleanly under both engines):

```latex
\usepackage{iftex}
\ifpdftex
  \usepackage[T1]{fontenc}     % so T1-only mono fonts (Bera Mono) select
  \usepackage[utf8]{inputenc}  % provides \DeclareUnicodeCharacter portably
  \DeclareUnicodeCharacter{2500}{-}\DeclareUnicodeCharacter{2502}{|}
  % … more mappings …
\else
  % XeTeX/LuaTeX read UTF-8 natively, so these never error -- but if the active
  % font lacks a glyph you get a blank plus a "Missing character" warning.  The
  % default mono font (Latin Modern Mono) has no box-drawing or exotic
  % punctuation, so map the SAME code points here for parity with pdfLaTeX:
  \usepackage{newunicodechar}
  \newunicodechar{─}{-}\newunicodechar{│}{|}
  % … same set, keyed by the literal character, not the hex code point …
\fi
```

`\newunicodechar` is keyed by the literal UTF-8 character (`\newunicodechar{─}{-}`),
whereas `\DeclareUnicodeCharacter` is keyed by the hex code point
(`\DeclareUnicodeCharacter{2500}{-}`).  Map both branches to the same fallback
so the two engines render code fixtures identically.

---

## Symptom 1 (pdfLaTeX only): "Unicode character … not set up for use with LaTeX"

```
! LaTeX Error: Unicode character ┌ (U+250C) not set up for use with LaTeX.
! LaTeX Error: Unicode character ‛ (U+201B) not set up for use with LaTeX.
```

This is an **8-bit-engine** error; under XeLaTeX/LuaLaTeX it does not occur
(see the Unicode-engine section).

**Cause.** pdfLaTeX only typesets code points that have a
`\DeclareUnicodeCharacter` mapping.  Common Latin accents, en/em dashes, and
curly quotes are predefined; exotic punctuation (reversed-9 quotes
`U+201B`/`U+201F`, hyphen and dash variants `U+2010`–`U+2015`, `≈ U+2248`) and
box-drawing glyphs (`U+2500`–`U+257F`) are not.  The error fires the first time
such a byte reaches the typesetter — in a literate program, that is wherever
the woven code chunk lands (the log shows the source line, e.g. `l.933`).

### Fix A — declare a printable mapping (preferred, minimal)

Add to the document preamble.  The replacement is normal LaTeX, so map each
code point to a sensible ASCII or math rendering:

```latex
\usepackage[utf8]{inputenc}   % see note below — load it before the mappings
\DeclareUnicodeCharacter{2010}{-}      % hyphen
\DeclareUnicodeCharacter{2012}{-{}-}   % figure dash (-{}- avoids a ligature)
\DeclareUnicodeCharacter{2015}{-{}-{}-}% horizontal bar
\DeclareUnicodeCharacter{201B}{'}      % single high-reversed-9 quote
\DeclareUnicodeCharacter{201F}{"}      % double high-reversed-9 quote
\DeclareUnicodeCharacter{2248}{\ensuremath{\approx}}  % almost equal to
\DeclareUnicodeCharacter{2500}{-}\DeclareUnicodeCharacter{2502}{|}  % box drawing
\DeclareUnicodeCharacter{250C}{+}\DeclareUnicodeCharacter{2510}{+}  % box corners
\DeclareUnicodeCharacter{2514}{+}\DeclareUnicodeCharacter{2518}{+}
```

**Load `\usepackage[utf8]{inputenc}` first.** `\DeclareUnicodeCharacter`
originates in `inputenc`'s `utf8` support; the LaTeX kernel (≥ 2018) also
exposes it, but relying on that breaks on older installations and in setups
where it is not active — the failure is `! Undefined control sequence.
\DeclareUnicodeCharacter`.  Loading `inputenc` makes it available portably and
is harmless on modern pdfLaTeX.  (Do **not** add it for a Unicode engine, where
`inputenc` is ignored and the command stays undefined — guard with `iftex`.)

ASCII fallbacks also keep box-drawing art inside the monospace code font
instead of shelling out to a special glyph font.

### Fix B — a purpose-built package

`\usepackage{pmboxdraw}` declares the whole `U+2500` box-drawing range and
draws each glyph from rules.  **Caveat:** it pulls in its own Unicode-dispatch
machinery; if the document already has subtle font issues, prefer the explicit
`\DeclareUnicodeCharacter` mappings above, which touch nothing else.

### Fix C — switch engine

XeLaTeX/LuaLaTeX read UTF-8 natively and need no declarations — but the *font*
must still contain the glyph, and switching engines is a project-wide change
(fonts, fontspec, build rules).  Reserve this for documents that genuinely
need broad Unicode, not for a handful of stray code points.

### Do NOT "fix" it by editing the source

When the offending byte lives in a code chunk, resist deleting or escaping it
in the `.nw`/`.tex` source.  The tangled program often *needs* the real byte at
runtime — a test that asserts an ASCII-art figure is filtered, a normalization
table that maps real typographic punctuation.  Fix the *presentation* in the
preamble; leave the *bytes* alone.

---

## Symptom 2 (pdfLaTeX): code/monospace renders in a proportional roman font

This is an OT1/T1 font-encoding problem specific to the 8-bit engine.  Under
XeLaTeX/LuaLaTeX, fonts are chosen with `fontspec`/`\setmonofont`, not
`fontenc`.

The giveaway in extracted text (`pdftotext`): an underscore comes out as `˙`
and straight quotes become curly — e.g. `COMMENT_MARKER = "X"` extracts as
`COMMENT˙MARKER = ”X”`.  That is **OT1 roman**, not typewriter: in the OT1
encoding, slot 95 (`_`) is the dotaccent glyph `˙`, and text fonts apply quote
ligatures.  cmtt (or any real monospace) would show a true underscore.

**Cause.** A monospace font that exists only in **T1** (and TS1) encoding —
notably **Bera Mono** (`beramono`, family `fvm`) — cannot be selected while the
document is still in **OT1**, because `\usepackage[T1]{fontenc}` was never
loaded.  `\ttfamily` then has no usable shape and silently falls back to the
roman family.  `\ttdefault` *looks* correct (`fvm`); the encoding is what is
missing.

### Fix — load T1 fontenc

```latex
\usepackage[T1]{fontenc}  % required so T1-only fonts (Bera Mono, …) select
```

Watch for this when a **local** preamble has the line commented out while the
project's **shared** preamble enables it — a standalone document that inputs
its own preamble can quietly miss it.  Loading `fontenc` is orthogonal to the
Unicode mappings in Symptom 1; a document with woven code typically needs both.

---

## Under XeLaTeX / LuaLaTeX (Unicode engines)

Neither symptom above applies, and the pdfLaTeX fixes actively break:

- **No `\DeclareUnicodeCharacter`.** It is undefined on Unicode engines —
  using it gives `! Undefined control sequence. \DeclareUnicodeCharacter`.
  `\usepackage[utf8]{inputenc}` does **not** rescue it (the package is ignored,
  emitting `inputenc package ignored with utf8 based engines`).  Guard any
  `\DeclareUnicodeCharacter` block with `\ifpdftex … \fi` (see "Know your
  engine first").
- **No "not set up" error.** XeTeX/LuaTeX read UTF-8 natively, so a stray code
  point is not fatal.  If the active font lacks the glyph you get a non-fatal
  `Missing character: There is no <char> in font …` warning and a blank; if it
  has the glyph, it just renders.  For a woven box-drawing test fixture, those
  warnings are cosmetic and the build still succeeds.
- **To remap a character**, use `\newunicodechar` (newunicodechar package),
  the Unicode-engine analogue of `\DeclareUnicodeCharacter`:
  ```latex
  \usepackage{newunicodechar}
  \newunicodechar{≈}{\ensuremath{\approx}}
  ```
- **To make a missing glyph appear** (rather than remap it), select a font
  that contains it for that span, e.g. `\setmonofont` to a fuller mono face,
  or wrap the span in a font that has box-drawing glyphs.

---

## Diagnostics (run these before guessing)

```bash
# FIRST: which engine? pdfTeX vs XeTeX/LuaTeX — decides which fixes apply.
grep -m1 'This is' doc/ltxobj/forcing.log        # "This is pdfTeX" / "XeTeX" …

# Count each failure class (don't grep only one — they mask each other).
grep -c 'Unicode character'          doc/ltxobj/forcing.log  # pdfLaTeX not-set-up
grep -c 'Undefined control sequence' doc/ltxobj/forcing.log  # e.g. DeclareUnicodeChar on XeTeX
grep -c 'Missing character'          doc/ltxobj/forcing.log  # Unicode-engine, non-fatal

# Per-page font list: is the expected monospace font actually embedded?
pdffonts -f 6 -l 6 doc/forcing.pdf               # look for BeraSansMono / fvm
pdffonts doc/forcing.pdf | grep -i 'bera\|mono'  # …anywhere in the document

# Glyph→Unicode probe: extract a code line and inspect the underscore/quotes.
pdftotext -f 6 -l 6 doc/forcing.pdf - | grep MARKER
#   real "_" and straight quotes  → monospace OK
#   "˙" and curly quotes          → OT1 roman fallback (load T1 fontenc)

# Render a page to eyeball the font directly.
pdftoppm -png -r 150 -f 6 -l 6 doc/forcing.pdf /tmp/page
```

Authoritative test: `pdffonts` shows *which* fonts a page embeds, and
`pdftotext`'s glyph mapping reveals *which encoding* — together they distinguish
"wrong font selected" from "right font, missing glyph" without guesswork.

---

## Quick decision guide

| Build symptom | Engine | Likely cause | Fix |
|---|---|---|---|
| `Unicode character … not set up` | pdfLaTeX | undeclared code point | `\DeclareUnicodeCharacter` (Fix A), `inputenc` loaded |
| many box-drawing errors at once | pdfLaTeX | `U+2500` range in source | declare them, or `pmboxdraw` |
| `Undefined control sequence \DeclareUnicodeCharacter` | XeTeX/LuaTeX | pdfLaTeX-only macro on a Unicode engine | guard with `\ifpdftex`; use `\newunicodechar` if remapping |
| `Missing character: … in font` | XeTeX/LuaTeX | font lacks the glyph | non-fatal; switch font for that span, or ignore |
| code looks serif; `_`→`˙` in extract | pdfLaTeX | T1-only mono font, no T1 fontenc | `\usepackage[T1]{fontenc}` |
| right font but a glyph is `□`/missing | any | glyph absent from font | different font, or map the char |
