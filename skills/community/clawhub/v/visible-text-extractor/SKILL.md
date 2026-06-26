---
name: visible-text-extractor
description: Extract and reconstruct as much visible text as possible from webpage URLs, article pages, screenshots, long images, image directories, and GIFs. Use when the goal is not just raw OCR, but a clean, human-readable result with section grouping, OCR cleanup, deduplication, structured JSON, original reading-order reconstruction, and explicit uncertainty notes. Especially useful for WeChat articles, event posters, long screenshots, mixed text-plus-image pages, and cases where visible information must be preserved without dumping noisy OCR into the final answer.
---

# Visible Text Extractor

Use this skill to turn a webpage article, URL, screenshot set, long image set, or local image collection into complete, readable, reusable text.

## Core workflow

1. Extract visible body text from the main source.
2. Discover ordered images and GIF-like assets.
3. OCR image content when needed.
4. Preserve a raw/audit layer.
5. Run a human-first cleanup pass.
6. Classify image-like content by likely information type.
7. Reconstruct image content into human-readable supplements instead of raw OCR dumps.
8. Output polished markdown first; keep raw OCR as JSON or appendix data.

## What this skill is good at

- General webpage article extraction
- WeChat / 公众号 article extraction with special handling
- News pages, blogs, tutorials, explainers, and image-heavy articles
- Screenshots and long-image OCR
- Image directory OCR in display order
- GIF frame extraction plus OCR when `ffmpeg` is available
- Rebuilding noisy OCR into a cleaner reading version
- Producing either reader-friendly clean output or full transcript-style output

## Main script

- `scripts/extract_visible_text.py`

## Supporting resources

- `scripts/postprocess_ocr_text.py` — clean OCR output, merge broken spacing, remove obvious garbage, and regroup into readable sections
- `scripts/extract_with_browser.js` — browser-rendered fallback for JS-heavy pages
- `scripts/extract_gif_frames.sh` — GIF frame extraction via `ffmpeg`
- `scripts/build_deliverable_docx.js` — convert cleaned markdown into a Word document
- `scripts/build_transcript_docx.js` — convert transcript-style markdown into a Word document
- `scripts/build_authorized_capture_docx.py` — one-step pipeline for already-authorized browser pages, saved HTML, screenshots, and mixed inputs into clean markdown + JSON + Word deliverable
- `scripts/extract_visible_text_deliverable.py` — one-step pipeline from source input to clean markdown + JSON + Word deliverable
- `scripts/extract_visible_text_transcript_deliverable.py` — one-step pipeline for transcript-style full extraction output
- `scripts/extract_visible_text_reading_order_deliverable.py` — one-step pipeline for reading-order transcript output
- `scripts/build_wechat_interleaved_docx.py` — reconstruct WeChat article reading order by interleaving extracted body blocks and image OCR text in original flow order
- `scripts/ocr_high_accuracy.py` — higher-accuracy OCR with preprocessing variants and segmented long-image handling
- `references/output-schema.md` — target output structure and cleanup rules
- `references/deliverable-workflow.md` — one-step deliverable workflow guidance
- `references/troubleshooting.md` — failure patterns, environment limits, and how to respond cleanly
- `references/product-positioning.md` — what mature deliverable quality means for this skill
- `references/generalization-plan.md` — how to evolve the skill across travel deals, rule pages, event posters, and tutorial long images
- `references/universal-article-extractor-spec.md` — generalized capability contract for article, mixed-media, and screenshot-heavy extraction

## Required behavior

When raw OCR is noisy, do not stop at extraction.

- Keep the raw candidate layer for traceability.
- Prefer readability over raw OCR score when two candidates are close.
- Remove decorative fragments, isolated symbols, repeated garbage, and near-duplicate lines from the polished result.
- Keep uncertainty visible instead of pretending confidence.
- Never silently drop a major section when partial reconstruction is possible.
- Never present raw OCR dump as the final answer if a cleaner reconstruction can be produced.
- Preserve article structure when available: title, subtitle, author/source/time, heading levels, paragraphs, lists, captions, table-like rows, and appended notes.
- Treat information-bearing images as first-class content rather than an appendix afterthought.
- For image-heavy pages, support transcript-style and reading-order outputs in addition to clean article outputs.

## WeChat / 公众号 handling

For `mp.weixin.qq.com` URLs:

- Try dedicated article extraction first when available.
- Fall back to static HTML parsing.
- Fall back again to browser rendering if needed.
- When the user cares about article readability, prefer reconstructing the final Word output in original reading order instead of appending all image OCR at the end.
- Use `scripts/build_wechat_interleaved_docx.py` when the task is specifically “keep original article order” for WeChat posts.
- If the page is blocked / validation-gated, report `blocked: true` clearly instead of pretending success.

## Typical commands

Extract URL to markdown:

```bash
python3 {baseDir}/scripts/extract_visible_text.py \
  --url 'https://example.com/post' \
  --format markdown \
  --output result.md
```

Extract URL to JSON:

```bash
python3 {baseDir}/scripts/extract_visible_text.py \
  --url 'https://example.com/post' \
  --format json \
  --output result.json
```

Extract WeChat article with fallbacks:

```bash
python3 {baseDir}/scripts/extract_visible_text.py \
  --url 'https://mp.weixin.qq.com/s/xxxx' \
  --browser-fallback \
  --page-screenshot-ocr \
  --format markdown \
  --output wechat.md
```

Extract local screenshot or long image:

```bash
python3 {baseDir}/scripts/extract_visible_text.py \
  --image ./screenshot.png \
  --ocr-images \
  --format markdown \
  --output image-result.md
```

Run OCR post-processing:

```bash
python3 {baseDir}/scripts/postprocess_ocr_text.py \
  --input-json ./ocr-result.json \
  --title 'Clean Result' \
  --body-text 'Optional summary or body text' \
  --output-json ./clean.json \
  --output-markdown ./clean.md
```

Run the one-step deliverable pipeline:

```bash
python3 {baseDir}/scripts/extract_visible_text_deliverable.py \
  --url 'https://mp.weixin.qq.com/s/xxxx' \
  --browser-fallback \
  --page-screenshot-ocr \
  --ocr-images \
  --dedupe \
  --output-prefix ./deliverable/result
```

This should emit:
- `result.raw.json`
- `result.clean.json`
- `result.clean.md`
- `result.docx`

Run the already-authorized capture pipeline when the page can be opened in a browser or exported/saved first:

```bash
python3 {baseDir}/scripts/build_authorized_capture_docx.py \
  --url 'https://example.com/page' \
  --browser-capture \
  --ocr-images \
  --dedupe \
  --output-prefix ./deliverable/captured
```

Useful cases:
- browser can open the page but direct fetch is incomplete
- user provides a saved HTML page plus screenshots
- user wants one command that turns visible page content into a Word document
- user wants status visibility instead of silent long waits

Operational expectations for this pipeline:
- print stage logs so long OCR jobs do not look stuck
- fail loudly if expected outputs are not created
- detect obvious WeChat validation/interstitial text early
- optionally send the generated docx back to Feishu in one run
- when a source is blocked, stop pretending and switch to authorized-input workflows: saved HTML, screenshots, long images, copied text

Practical optimization rule:
- do not keep hammering a blocked source in the same mode
- if browser/direct fetch returns validation text, pivot immediately to the best authorized artifact path
- prioritize delivery quality: visible content captured by the user is better than repeated blocked fetch attempts

## Key options

- `--url` webpage URL
- `--text-file` local plain text / markdown input
- `--html-file` local saved HTML page
- `--image PATH` add one local image or GIF; repeat as needed
- `--image-dir DIR` OCR all supported images / GIFs in a directory
- `--format markdown|json` output format
- `--output PATH` output file path
- `--ocr-images` OCR discovered or provided images
- `--dedupe` deduplicate repeated merged lines
- `--browser-fallback` use browser-rendered fallback for incomplete pages
- `--page-screenshot-ocr` OCR the browser full-page screenshot as a last resort
- `--gif-mode none|placeholder` conservative GIF handling mode

## Quality standard

Default target: produce something a human can read comfortably and share without cleanup.

Release-quality target for article deliverables:
- preserve the article's original reading order whenever the source structure allows it
- avoid dumping all image OCR at the end when images belong in the middle of the article
- prefer a comfortable reading experience over a mechanically grouped OCR appendix
- keep English-heavy charts, dashboards, and mixed Chinese-English figures readable enough that key labels, axes, legends, and result summaries survive extraction

The skill should increasingly treat extraction as a full article understanding and recovery problem, not only a body scrape plus OCR problem:
- recover visible article structure from normal webpages, WeChat posts, blogs, tutorials, and mixed-media articles
- infer whether an image is mainly a price/product page, rules page, poster/event page, course outline, scenery/introduction card, or table-like detail page
- pull out high-value facts first when the user wants a clean readable result
- preserve near-complete text when the user wants transcript completeness
- avoid raw OCR dumps as the main deliverable unless the user explicitly wants audit output

When the user explicitly wants completeness, the skill must support a fuller extraction mode:
- treat each discovered image as a first-class source
- prefer segmented OCR for tall or dense images
- preserve near-complete per-image text blocks before compressing into summaries
- keep summary and full-text layers separate instead of replacing one with the other
- support reading-order transcript output so text and image-derived content can be followed from start to finish

For clean article outputs, prefer a structure like:

1. Title
2. Metadata (author/source/time) when meaningful
3. Main sections in order
4. Integrated image-derived supplements where needed
5. Uncertainty notes only when necessary

For transcript outputs, prefer a structure like:

1. Title
2. Intro/body chunks in order
3. Image text blocks in order or reading order
4. Tail matter / credits / appended notes

Mature-skill rule:
- default users toward the clean markdown / docx outputs unless they ask for transcript completeness
- keep raw JSON for audit, not as the main deliverable
- degrade honestly when the source is blocked or image quality is poor
- do not optimize only for one article family; keep checking travel-deal posts, rule/scoring posts, event posters, news/blog/tutorial pages, and course-outline long images

Read these references when needed:
- `references/output-schema.md`
- `references/deliverable-workflow.md`
- `references/troubleshooting.md`
- `references/product-positioning.md`
- `references/generalization-plan.md`
- `references/universal-article-extractor-spec.md`

## Environment notes

- OCR depends on the local `ocr-local` skill or compatible Tesseract.js setup.
- Browser fallback depends on real browser availability plus `playwright-core` support.
- GIF frame extraction depends on `ffmpeg`.
- Some pages remain partially inaccessible due to login, anti-bot, or validation flows; mark those limits explicitly.
