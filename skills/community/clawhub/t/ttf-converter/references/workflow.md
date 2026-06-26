# Workflow

## Goal

Turn a horizontal Chinese TTF into a deliverable vertical TTF with preview-first validation and reader-side test artifacts.

This workflow is intentionally local-only.

Core requirements:

- minimize blind trial-and-error
- process characters by glyph group
- never skip key preview gates
- show test images before delivering final files

## Tools expected

Python libraries commonly used:

- `fontTools`
- `Pillow`

Common font operations / helpers:

- `TTFont`
- `TTGlyphPen`
- `TransformPen`
- `rotate_about(cx, cy, 90)`
- `translate(dx, dy)`
- `scale_about(gcx, gcy, sx, sy)`
- `compose(A, B)`

Common script responsibilities:

- original horizontal preview image
- vertical TTF generation
- bbox / center / position audit
- vertical preview image
- reader test TXT generation

## Default path

Use this default interaction path unless the user clearly asks otherwise:

1. Receive a source font file.
2. Open the source horizontal TTF and confirm it is readable.
3. Check whether Chinese, Latin letters, digits, and punctuation exist.
4. Generate a browser preview image from the original horizontal font.
5. Let the user inspect whether the original font is worth continuing.
6. If the user confirms, build the vertical TTF by glyph groups.
7. Generate a browser preview image for the vertical TTF.
8. Generate a reader test TXT file.
9. Do not deliver the TTF before the user confirms the vertical preview.
10. After confirmation, deliver the TTF and related local test artifacts.

## Required preview coverage

Both the horizontal source preview and the vertical result preview should include:

- Chinese body text
- Latin letters
- Arabic digits
- single-point punctuation
- book-title marks / quotes / brackets
- dash / ellipsis
- one mixed-script sentence

Recommended text:

```text
天地玄黄 宇宙洪荒 日月盈昃 辰宿列张
ABC abc 1234567890
，。；：？！,.;:?!
《测试》〈样例〉「引号」『双引号』“弯引号”‘单引号’
() [] {} （）［］｛｝〔〕【】
— —— … ……
春眠不觉晓，ABC123；处处闻啼鸟。
```

## Reader test TXT

Generate a TXT file for reader-side testing. It should include:

- several Chinese body lines
- one mixed Chinese/Latin/digit sentence
- letters and digits
- single-point punctuation
- paired punctuation
- dash and ellipsis

## Stop conditions

Stop early and report clearly if:

- the source font cannot be opened
- the source font has obvious broken tables
- the horizontal preview is visibly broken
- punctuation / Latin / digits are missing in the source font
- the user has not yet confirmed continuing after the horizontal preview
- the vertical preview has not yet been confirmed but the task is already asking for final TTF delivery

## Adjustment order

When the user says a glyph class is misplaced, prefer this order:

1. identify the glyph group
2. reuse the known group rule
3. tweak the group parameter minimally
4. regenerate preview
5. inspect it yourself first
6. ask user to confirm before final delivery

## Full-font requirement

Never limit processing only to the visible test sentence.
Apply the confirmed rule set to all glyphs that belong to each group in the full font.

This is not “fix the few characters visible in the test image”; it is a full-font grouped conversion.
