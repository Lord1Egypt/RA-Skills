# Scripts — Bidi, CJK, Encoding, Fonts

Three failure families live here and get confused with each other constantly: **bytes** (mojibake), **rendering** (missing glyphs, wrong shaping), and **direction** (bidi). Diagnose which one before touching anything — the fixes have nothing in common.

**Contents:** [Telling the Three Apart](#telling-the-three-apart) · [Mojibake Decoder](#mojibake-decoder) · [Encoding Rules](#encoding-rules) · [Normalization and Length](#normalization-and-length) · [Bidirectional Text](#bidirectional-text) · [Mirroring a Layout](#mirroring-a-layout) · [Arabic and Hebrew Specifics](#arabic-and-hebrew-specifics) · [CJK Typography](#cjk-typography) · [Indic and Southeast Asian Scripts](#indic-and-southeast-asian-scripts) · [Fonts](#fonts) · [What To Write Down](#what-to-write-down)

**Before debugging a rendering problem you have seen before**, read `## Environment` and `## Pain Points` in `~/Clawic/data/translate/memory.md` — a font that lacks a script and a pipeline hop that re-encodes are environment facts, and both were found the hard way once.

## Telling the Three Apart

| What you see | Family | Test |
|---|---|---|
| Latin letters where other letters should be (`Ã©`, `â€™`) | Bytes | The text is intact; only the decoding is wrong. Same string in a hex viewer shows valid UTF-8 |
| Question marks or underscores replacing characters | Bytes, and **lossy** | The information is gone; no display fix exists, re-export from the source |
| Empty rectangles, or one word in a visibly different typeface | Rendering | Copy the text out — it pastes correctly elsewhere |
| Correct characters, wrong order or punctuation at the wrong end | Direction | Only affects mixed-direction text; pure Arabic looks fine |
| Correct characters, wrong *shapes* (disconnected Arabic letters) | Rendering | The font lacks shaping tables, or the text was letter-spaced |

## Mojibake Decoder

| Seen | What happened | Example |
|---|---|---|
| `Ã©`, `Ã±`, `Ã¼` | UTF-8 bytes decoded as Latin-1 / CP1252 | `café` → `cafÃ©` |
| `â€™`, `â€œ`, `â€"` | UTF-8 smart punctuation decoded as CP1252 | `it's` → `itâ€™s` |
| `æ¼¢`, `ä¸­` | UTF-8 CJK (three bytes) decoded as Latin-1 | Each character becomes three symbols |
| `ï»¿` at the start of a file | A UTF-8 BOM being shown as text | Common in CSV read by a parser that does not strip it |
| `ÃƒÂ©` | **Double** encoding — the mojibake was itself encoded again | Each extra hop adds a layer; fix the hops, not the text |
| `?` or `_` per character | Lossy conversion into a charset that cannot hold the character | Latin-1 database column receiving Chinese |
| `&#233;` or `é` in visible text | Escaped text being displayed instead of decoded | An escaping step ran twice |

Procedure: find the **one hop** that assumes a legacy encoding — file read, HTTP header, database connection charset, CSV import, terminal, template engine — and fix it there. Repairing the characters by hand is a guarantee that the next export is broken the same way, and hand-repair silently loses the characters that mapped to the same replacement.

## Encoding Rules

- **UTF-8 everywhere, declared everywhere**: file, HTTP `Content-Type` charset, HTML `<meta charset>`, database, database *connection*, and the build tool. The connection is the one people forget, and it is the one that corrupts on write.
- **MySQL's `utf8` is not UTF-8**: it is a three-byte subset that cannot store emoji or several CJK extension characters. `utf8mb4` with `utf8mb4_0900_ai_ci` or a locale-appropriate collation is the correct choice.
- **CSV for spreadsheets is a special case**: Excel on Windows guesses the encoding unless the file has a UTF-8 BOM, so a translated CSV without one opens as mojibake for a whole team.
- **BOM: yes for CSV consumed by spreadsheet apps, no for source code, JSON, and web assets** where it breaks parsers and shifts byte offsets.
- Emoji, flags and skin-tone modifiers are multi-code-point sequences. Truncating by code point splits them into rubble.

## Normalization and Length

- `é` exists as one code point (U+00E9, NFC) and as two (`e` + combining acute, NFD). They look identical, compare unequal, and have different lengths. **Store and compare NFC**; normalize on input.
- macOS filesystems hand back decomposed (NFD) filenames, which is why a filename search fails on a Mac and works on Linux with the same code.
- **Three ways to count "length", and they disagree**: bytes (UTF-8: 1-4 per character), code points, and grapheme clusters (what a reader calls a character). A length limit for a translator means grapheme clusters; a database column limit means bytes. State which one a limit is (`software-strings.md`).
- Case conversion is locale-sensitive (`locales.md`, Turkish) and not reversible: German `ß` uppercases to `SS`, and `SS` lowercases to `ss`.

## Bidirectional Text

Text is **stored in logical order** — the order it is spoken — and the Unicode Bidirectional Algorithm decides display order at render time. This is correct behavior and cannot be improved by reversing strings.

The trouble is **neutral characters**: punctuation, spaces, digits and most symbols have no direction of their own and take it from their surroundings. An Arabic sentence ending in a period that follows a Latin product name puts the period on the wrong side, because the period sat between an LTR run and the paragraph edge.

Fixes, in order of preference:

1. **Isolate embedded runs.** In markup, wrap user-supplied or opposite-direction text in `<bdi>`, or set `dir="auto"` on the element. In plain text, use the isolate characters FSI (U+2068) … PDI (U+2069). Isolation is what makes the neutral characters around the run resolve from the paragraph, not the run.
2. **Set the paragraph direction explicitly** (`dir="rtl"` on the container, `direction: rtl` in CSS). Never rely on the first strong character.
3. **A single mark as a last resort**: LRM (U+200E) or RLM (U+200F) next to the stubborn neutral character. The old embedding controls LRE/RLE/PDF are superseded by isolates — they leak direction across boundaries.

- **Numbers always run left to right** inside RTL text, including phone numbers, versions and prices. Only the digit *shapes* vary by locale.
- **Never concatenate to build a bidi string.** `name + ": " + value` places two neutrals between two runs of unknown direction; the result is unpredictable per value.
- Test with real Arabic or Hebrew and with a mixed string containing a Latin brand name, a number and a trailing period — that one string exposes almost every bidi bug.

## Mirroring a Layout

RTL is not a translation, it is a layout mode. Mirror the interface, not the content.

| Mirror | Do not mirror |
|---|---|
| Reading and navigation order, sidebars, breadcrumbs | Logos and brand marks |
| Progress bars, sliders, carousels, back and forward arrows | Media playback controls (play still points right by convention) |
| Alignment and indentation, list bullets, checkbox and label order | Clock faces, and anything showing real-world objects with a fixed handedness |
| Directional icons (undo, reply, indent) | Charts with a time axis (keep the data's own direction, and state it) |

- Build with **logical CSS properties** — `margin-inline-start`, `padding-inline-end`, `inset-inline`, `text-align: start` — so the same stylesheet serves both directions. Physical `left`/`right` is the reason RTL support becomes a second codebase.
- Ellipsis truncation, focus order, drag directions and swipe gestures all flip too.
- Mixed-direction input fields (an email address in an Arabic form) need `dir="auto"` per field, not per page.

## Arabic and Hebrew Specifics

- **Arabic letters are contextual**: each has initial, medial, final and isolated forms, joined by the font's shaping tables. Letter-spacing an Arabic string breaks the joins and produces text that looks like a ransom note; so does rendering character by character in an animation.
- No uppercase exists in either script — do not apply `text-transform: uppercase`, and do not use case to create emphasis. Bold is acceptable; emphasis in Arabic is more often achieved by a different typeface weight or by wording.
- Arabic-Indic digits (٠١٢٣) versus ASCII digits is a **regional** choice: Egypt and the Gulf commonly use Arabic-Indic, the Maghreb uses ASCII. Follow the locale, and never mix within one screen.
- Hebrew has grammatical gender on verbs addressed to the reader, so "you saved" differs by the reader's gender; either phrase impersonally or provide a `select` (`software-strings.md`).
- Arabic expands roughly 20-25% over English in character count but often needs *more* line height than that suggests, because of ascenders, descenders and diacritics.

## CJK Typography

- **No spaces between words**, so line breaking happens between characters and follows kinsoku rules: a line may not begin with 。、」）or end with 「（. Renderers that break naively produce text that reads as broken to a native.
- **Insert a space between Han characters and adjacent Latin text** in high-quality typography (`Acme のアカウント`); many CJK fonts and layout engines do it automatically, and doing it manually in the string fights the engine.
- **Italics do not exist as a native convention.** Slanting a CJK face is a synthetic distortion; use a heavier weight, a different face, or Japanese emphasis dots (圏点).
- **Han unification**: the same code point renders with different, culturally wrong shapes depending on the font's language. Set `lang="ja"` / `lang="zh-Hans"` / `lang="ko"` on the element so the right face is chosen — the characters are identical, the glyphs are not.
- Full-width and half-width forms of the same character exist (`Ａ` vs `A`, `１` vs `1`). Normalize on input for search; keep the author's choice in display text.
- Vertical writing (`writing-mode: vertical-rl`) is real for Japanese print and some web content; Latin runs inside it need `text-combine-upright` to stay readable.
- CJK contracts by roughly a third in character count against English, so the risk is not overflow but text that looks lost in a box sized for English.

## Indic and Southeast Asian Scripts

- Devanagari, Bengali, Tamil and their relatives form **conjuncts and reordered vowel signs**: the visual order of a syllable is not the logical order of its code points. Cursor movement, selection and truncation must operate on grapheme clusters or they split a syllable.
- Thai, Lao and Khmer have **no spaces between words**; correct line breaking needs a dictionary, so a naive renderer wraps mid-word. Do not insert spaces to fix it — that changes the text.
- Thai stacks tone marks and vowels above and below the base character, so line height must grow; text that fits in Latin clips in Thai.
- These scripts have the thinnest font coverage in default stacks — the tofu risk is highest here, especially in PDFs and canvas rendering.

## Fonts

- **Coverage is per script, not per language.** Before promising a locale, confirm the delivery surface (app, web, PDF, video, email) has a font covering its script in every weight used. A missing weight silently synthesizes a fake bold that looks wrong in Arabic and CJK.
- PDF and print pipelines must **embed** the font; a document that renders on the designer's machine and shows tofu on the client's is an unembedded font, every time (`documents.md`).
- CJK fonts are large (megabytes). Web delivery needs subsetting or a system-font stack; loading a full CJK face blocks first paint.
- When a fallback face kicks in mid-sentence, the reader sees mixed shapes and weights. That is a font-stack bug, not a translation one, and it is worth reporting as such.

## What To Write Down

- A pipeline hop that re-encodes, a font that lacks a script, a renderer that ignores kinsoku, a CMS that mangles entities: **`## Environment` in `~/Clawic/data/translate/memory.md`**. These facts change every future decision for that surface, so they do not belong in an incident note.
- A rendering defect that reached a reader goes in **`## Pain Points`** with its cause, in one line.
- If the fix took more than a couple of minutes to find and will recur, it becomes **`artifacts/<surface>-rendering.md`** with the chain of checks and the fix, plus its `## Boxes` line naming the symptom, in the same turn (`memory-template.md`).
