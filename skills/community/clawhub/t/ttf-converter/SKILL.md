---
name: vertical-font-conversion
description: Local-only skill for converting horizontal Chinese fonts into high-quality vertical-reading TTF fonts with a preview-first workflow, grouped glyph rules, and local audit/test artifacts. Use when the user asks to make a 竖版字体 / 竖排 TTF, fix vertical punctuation, quotes, ellipsis, Latin, or digits, generate test images, or explicitly asks for Vertical Font Conversion.
---

# Vertical Font Conversion

Use this skill when the task is about turning a horizontal font into a vertical-reading TTF font, or adjusting an existing vertical font result.

This skill is intentionally **local-only**. It focuses on source checking, grouped conversion, preview generation, local audit, and local test artifacts. It does **not** include remote conversion services, cloud uploads, or device-transfer steps.

## Chinese display name

**竖版字体转换**

## What this skill covers

- Source font precheck before vertical conversion
- Local vertical TTF production workflow
- Stable glyph-group handling rules
- Horizontal and vertical browser preview generation before delivery
- Reader test TXT generation
- Local audit for representative glyph placement
- Grouped conversion aimed at high-satisfaction vertical TTF output

## Trigger conditions

Activate this skill when the user asks for any of the following:

- “制作竖版字体”
- “做竖排 ttf”
- “制作竖版 TTF”
- “改竖排标点 / 引号 / 省略号 / 西文 / 数字”
- “启动 Vertical Font Conversion”
- “按竖版字体转换流程来”

## Default execution meaning

Unless the user explicitly asks to skip steps, “use Vertical Font Conversion” means:

- check the source font first
- make a horizontal preview first
- wait for user confirmation before building the vertical TTF
- make a vertical preview before delivering the font
- generate a reader test TXT
- stay fully local: horizontal preview, vertical TTF, vertical preview, reader test TXT, and audit output when needed

## Mandatory workflow

Follow this order unless the user explicitly asks to skip steps:

1. Read the source horizontal TTF and check that the font opens normally and is not obviously broken.
2. Generate a browser test image from the **original horizontal font** first.
3. The preview must include:
   - Chinese body text
   - Latin letters
   - Arabic digits
   - single-point punctuation
   - book-title marks / quotes / brackets
   - dash / ellipsis
   - one mixed-script sentence
4. Ask the user to judge whether the source font itself is worth continuing.
5. If confirmed, make the vertical TTF by glyph groups.
6. Do **not** send the TTF immediately. Generate and show a browser test image for the vertical result first.
7. Also generate a TXT test file for reader-side validation.
8. Only after user confirmation, send the TTF and related local test artifacts.

If the original horizontal font already has obvious missing punctuation / Latin / digits / rendering defects, stop and tell the user it is not a good source candidate.

## Read next

Before operating, read these references:

- [references/workflow.md](references/workflow.md) — full operating sequence
- [references/rules.md](references/rules.md) — glyph-group rules and latest default parameters
- [references/implementation-notes.md](references/implementation-notes.md) — practical logic, tuning philosophy, and failure-mode awareness for high-satisfaction output
- [references/default-config.json](references/default-config.json) — baseline tunable parameters
- [references/examples.md](references/examples.md) — concrete command examples
- [references/case-template.md](references/case-template.md) — template for recording successful real cases
- [references/cases-zihun-songkekaiti.md](references/cases-zihun-songkekaiti.md) — confirmed real case and lessons from 字魂宋刻楷体

## Script entry points

Prefer these bundled scripts before inventing fresh one-off code:

- `scripts/render_original_preview.py` — generate original horizontal preview image
- `scripts/make_vertical_font.py` — build glyf-based vertical TTF with the bundled grouped-conversion logic
- `scripts/make_vertical_font_cff.py` — build CFF-based vertical font with preserved CharString metadata
- `scripts/render_vertical_preview.py` — generate vertical result preview image
- `scripts/generate_reader_test_txt.py` — generate reader-side TXT sample
- `scripts/audit_font_rules.py` — inspect representative glyph bbox / center data after conversion
- `scripts/run_full_pipeline.py` — one-shot local pipeline for preview → build → preview → TXT

Use the bundled builders as the default baseline. If future tuning is needed, preserve the stable script paths and update the rule implementations behind them.

## Scope boundary

This skill stops at local vertical-TTF deliverables.

Out of scope for this skill:

- epdfont conversion
- upload to `/fonts`
- remote processing services
- cloud transfer / device transfer steps

If a later workflow needs those actions, handle them in a separate skill or a separate explicitly user-directed procedure.

## Operational rules

- Preserve the user-confirmed workflow; do not skip preview steps by default.
- Apply rules to the **full font character set**, not only the demo sentence.
- Process by glyph group; do not use one parameter set for all glyphs.
- For special symbols, prefer preprocessing in horizontal coordinates first, then produce the vertical result.
- Do not rely on only `vert/vrt2` substitutions as the whole solution.
- Do not rotate first and then blindly patch positions.
- If the user provides a reference image, prefer matching the reference while keeping the same grouping logic.
- When a parameter tweak is needed, adjust the minimum necessary group rather than rewriting the whole rule set.
- Before sending a user-facing test image, do your own basic inspection first; do not throw raw debug output at the user as a substitute for checking.
- When the result still feels off, inspect representative glyph bbox / center data with the audit script instead of blind re-guessing.
- For one-shot execution, prefer the bundled full-pipeline script so the output order stays consistent.
- In the current WeChat direct channel, local file delivery should prefer the channel’s real file-send path with an absolute path rather than relying on `MEDIA:` lines alone.

## Output expectations

Typical outputs include:

- horizontal preview image
- vertical preview image
- vertical `.ttf`
- test `.txt`
- optional audit JSON / terminal report
