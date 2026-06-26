# Real cases — 字魂宋刻楷体

## Case 1

- Font name: 字魂宋刻楷体
- Source type: glyf TTF
- Date: 2026-04
- Status: confirmed

## Input

- Source font path:
  - `/home/yuvia/.openclaw/media/inbound/字魂宋刻楷体_W2_商用需授权---7a782dce-2f81-48dc-83c3-40197379df59`
- Whether horizontal preview passed:
  - yes
- Visible source issues before conversion:
  - none that blocked the vertical workflow

## Goal

- What the user cared about most:
  - practical readability in a reader, not just theoretical vertical support
  - single-point punctuation must sit in the upper-right area and feel attached to the previous character
  - `「」『』` must stay inside the Han-character box and not be treated as ordinary centered punctuation
  - ellipsis and dash must sit on the correct middle line
- Whether a reference image was provided:
  - yes, later tuning was refined against user feedback and reference-style constraints

## Config used

- Config file path:
  - equivalent to the current bundled default config, with user-validated emphasis on the following points
- Important overrides / final confirmed defaults:
  - single punctuation:
    - rotate after horizontal preprocessing
    - target upper-right area
    - current long-term default scale: `0.80`
    - tuning priority: `tx` -> `ty` -> `scale`
  - corner quotes:
    - `「` / `『` right side
    - `」` / `』` left side
    - keep inside Han-character boundary
    - current long-term default scale: `0.90`
  - dash / ellipsis:
    - horizontal form preserved
    - middle-line alignment
    - current long-term default scale: `0.90`
  - Latin / digits:
    - do not rotate
    - align to Han column center

## Output

- Horizontal preview:
  - produced first and used as go / no-go gate
- Vertical font:
  - produced after grouped conversion
- Vertical preview:
  - produced before final delivery
- Reader TXT:
  - produced

## Result review

- What worked well:
  - grouped processing was the key; one-size-fits-all transforms would have failed
  - horizontal preprocessing before vertical result generation was the right logic for punctuation
  - replacing curly quotes with `「」『』` greatly stabilized the visual result
- What still needed micro-tuning:
  - single punctuation was the most sensitive group
  - question mark / exclamation mark line feel could require small targeted correction
- Which glyph group caused most trouble:
  - single-point punctuation
  - corner quotes
  - ellipsis middle-line placement
- Final user satisfaction estimate:
  - high enough to become the main reusable baseline for this skill

## Lessons

- Reusable parameter lesson:
  - for this font family, single punctuation at `scale=0.80` is a much better default than older smaller trials
  - corner quotes should be treated by left/right boundary logic, not generic centering
- Failure mode to avoid next time:
  - do not keep adjusting numbers in the wrong coordinate-direction assumption
  - do not only fix the visible test sentence; apply grouped rules to the full font
- Whether this case should influence the default config:
  - yes; this case is the strongest basis for the current bundled defaults

## Historical note

Earlier testing history included downstream epdfont and reader-upload workflows, but those are intentionally outside the current skill scope. The current skill should stay focused on producing a high-quality vertical TTF plus local preview and test artifacts.
