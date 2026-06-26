# output-schema

## Goal
Produce text that a human can read quickly, not a raw OCR dump.

## Preferred output layers

1. **clean_markdown**
   - Human-first polished markdown
   - Keep headings, bullets, event fields, people, time, place
   - Remove obvious OCR garbage, decorative fragments, isolated symbols, and duplicate lines
2. **structured_blocks**
   - Ordered blocks with `type`, `heading`, `text`, `source`, `confidence_notes`
   - Types: `title`, `intro`, `section`, `event_info`, `speaker`, `cta`, `footer`, `unknown`
3. **raw_ocr_candidates**
   - Preserve best-effort OCR text per image/frame for auditability

## Cleaning rules

- Merge broken Chinese spacing: `我 们` -> `我们`, `中 山 大 学` -> `中山大学` when the line is mostly CJK
- Normalize common OCR punctuation noise: repeated `|`, stray `<`, isolated bullets, repeated brackets
- Collapse repeated blank lines
- Remove decorative-only lines unless they contain meaningful text
- Deduplicate near-identical lines after whitespace/punctuation normalization
- Keep uncertain text only in a separate note or raw section, not mixed into polished prose

## Human-friendly markdown layout

### Recommended order

1. Document title
2. One-screen summary
3. Core content, grouped into logical sections
4. Key facts card
5. Speakers / organizations
6. Registration / CTA
7. OCR uncertainty notes
8. Raw appendix only if requested

### Recommended section names for event-like posters/articles

- 概览
- 活动信息
- 主题讲座
- 案例分享
- 创业空间 / 资源支持
- 相关活动
- 结语
- 附：原始 OCR 片段（可选）

## Reconstruction guidance

When several images clearly belong to one poster/article:
- infer section boundaries from repeated markers like `Part1`, `Part2`, `引言`, `结语`
- merge overlapping text from consecutive images
- prefer semantically complete sentences over highest raw OCR score
- when two candidates disagree, keep the more readable one and mention uncertainty separately if important

## Never do this

- Do not present raw noisy OCR as the main final answer when a cleaner reconstruction is possible
- Do not silently drop major sections just because OCR is imperfect
- Do not invent facts absent from source text
