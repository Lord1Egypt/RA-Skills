# Rules

This file holds the reusable glyph-group rules and current default parameter logic.

## Core principles

- Process glyphs by **group**, not one-off by test sentence.
- Apply confirmed rules to the **full font**, not only commonly seen characters.
- For special symbols, preprocess in horizontal coordinates first, then produce the vertical result.
- Do not treat `vert/vrt2` substitutions as the whole solution.
- Do not rotate first and then blindly patch positions.

## Group A: Chinese body text

- Default: rotate Chinese body glyphs clockwise 90°.
- Default rotation center:

```python
cx = upem / 2
cy = upem / 2 - font['hhea'].descent
```

- Default: no extra per-glyph translation.

## Group B: single-point punctuation

Applies to:

- Chinese: `，。、、？！：；`
- Western: `, . ! ? : ;`

Target:

- upper-right area of the vertical cell
- visually near the right side
- visually attached to the previous character
- must not cross the Chinese character boundary

Processing order:

1. preprocess translation in horizontal coordinates
2. scale as needed
3. rotate clockwise 90° into the vertical result

Template:

```python
M = compose(
    rotate_about(cx, cy, 90),
    compose(
        translate(tx, ty),
        scale_about(gcx, gcy, sc, sc)
    )
)
```

Current default parameters:

```python
tx = 620
ty = 40
sc = 0.80
```

Question mark / exclamation mark note:

- if `？` and `！` do not sit well on the same visual line, `tx` may be tuned separately
- still keep them inside the single-point punctuation logic
- still do not cross the Chinese character boundary

Tuning priority:

1. `tx`
2. `ty`
3. `sc`

Experience rule:

- if the result looks visually farther left while the numeric adjustment seemed to push right, first suspect the horizontal preprocessing direction was misunderstood

## Group C: paired punctuation, book-title marks, brackets, Chinese corner quotes

Applies to:

- `《》〈〉`
- `「」『』`
- `（）[]{}〔〕【】`

Base rule:

- do not rotate
- keep horizontal form
- default scale: `0.90`
- stay within the Chinese character boundary
- align to the vertical cell middle line, except for the special left/right handling of `「」『』`

Default center:

```python
target_center = (500, 700)
```

General default transform:

```python
centered_transform(..., target_center=(500, 700), scale=0.90)
```

## Group D: curly quote replacement

Applies to:

- `“”‘’`

Rule:

- do not keep them as curly quotes
- replace as:
  - `“” -> 「」`
  - `‘’ -> 『』`

After replacement, do **not** use generic centered quote handling.
Use the special `「」『』` rules below.

## Group E: special rules for `「」『』`

- keep horizontal form
- scale: `0.90`
- all results must stay within the Chinese glyph box and not overflow vertically
- `「` and `『` should sit to the right side
- `」` and `』` should sit to the left side

Execution requirements:

- bbox right edge of `「` and `『` should approach the Chinese character right boundary without crossing it
- bbox left edge of `」` and `』` should approach the Chinese character left boundary without crossing it

This is a character-frame-fit rule first, not a blind center rule.

## Group F: dash and ellipsis

### Dash

- keep horizontal form
- keep it on the middle line
- default scale: `0.90`

```python
centered_transform(..., target_center=(500, 700), scale=0.90)
```

### Ellipsis

- keep horizontal ellipsis form
- keep it on the middle line
- do not allow it to sit too low
- default scale: `0.90`

```python
scale = 0.90
dx = 500 - gcx
dy = 700 - gcy
M = compose(translate(dx, dy), scale_about(gcx, gcy, scale, scale))
```

## Group G: Latin letters and Arabic digits

Applies to:

- `0-9`
- `A-Z`
- `a-z`

Rule:

- do not rotate
- align with the Han-character column center

Parameters:

```python
dx = 500 - gcx
dy = 700 - gcy
M = compose(
    translate(dx, dy),
    scale_about(gcx, gcy, 0.92, 0.92)
)
```

## CFF fonts

For CFF-based fonts:

- do not rely on glyf-table editing logic
- rewrite CFF CharStrings with `fontTools` `T2CharStringPen` + `TransformPen`
- preserve original CharString `private` and `globalSubrs`
- otherwise saving may fail with width-related errors such as `nominalWidthX`

## Final configuration summary

A finished deliverable should satisfy all of the following by default unless the user explicitly asks for a different target:

1. Chinese body text rotates clockwise 90°.
2. Latin letters and digits do not rotate and align to the Han column center.
3. Single-point punctuation is preprocessed in horizontal coordinates, then rotated clockwise 90°, and ends in the upper-right area with scale `0.80`.
4. Paired punctuation / book-title marks / brackets keep horizontal form, use scale `0.90`, and stay within the Chinese character boundary.
5. `“”‘’` must be replaced with `「」『』`.
6. `「` and `『` sit right; `」` and `』` sit left; all remain inside the character boundary; scale `0.90`.
7. `— / ―` keep horizontal form on the middle line with scale `0.90`.
8. `… / ……` keep horizontal form on the middle line with scale `0.90`.

## Forbidden mistakes

- only editing `vert/vrt2`
- rotating first and then blindly patching positions
- processing all characters with one parameter set
- delivering before generating preview images
- asking the user to do the basic debug reading that should have been checked before sending a test image
