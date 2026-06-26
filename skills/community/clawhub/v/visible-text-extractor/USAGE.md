# visible-text-extractor usage

## Best use cases

Use this skill when the source contains meaningful visible text but normal copy/paste is incomplete or impossible:

- WeChat / 公众号 articles
- event posters
- long screenshots
- image-heavy landing pages
- local image folders
- GIFs with text overlays

## 1) URL -> markdown

```bash
python3 skills/visible-text-extractor/scripts/extract_visible_text.py \
  --url 'https://example.com/article' \
  --format markdown \
  --output result.md
```

## 2) URL -> JSON

```bash
python3 skills/visible-text-extractor/scripts/extract_visible_text.py \
  --url 'https://example.com/article' \
  --format json \
  --output result.json
```

## 3) WeChat article with special handling

```bash
python3 skills/visible-text-extractor/scripts/extract_visible_text.py \
  --url 'https://mp.weixin.qq.com/s/xxxx' \
  --browser-fallback \
  --page-screenshot-ocr \
  --format markdown \
  --output wechat.md
```

Behavior:
- try WeChat-specific extraction first
- then static HTML extraction
- then browser fallback if needed
- report `blocked: true` explicitly when the page cannot be read cleanly

## 4) OCR discovered page images

```bash
python3 skills/visible-text-extractor/scripts/extract_visible_text.py \
  --url 'https://example.com/article' \
  --ocr-images \
  --format markdown \
  --output result.md
```

## 5) Local text or HTML input

```bash
python3 skills/visible-text-extractor/scripts/extract_visible_text.py \
  --text-file ./article.txt \
  --format markdown \
  --output result.md
```

```bash
python3 skills/visible-text-extractor/scripts/extract_visible_text.py \
  --html-file ./saved-page.html \
  --format markdown \
  --output result.md
```

## 6) Screenshot / long image

```bash
python3 skills/visible-text-extractor/scripts/extract_visible_text.py \
  --image ./screenshot.png \
  --ocr-images \
  --format markdown \
  --output image-result.md
```

## 7) Image directory

```bash
python3 skills/visible-text-extractor/scripts/extract_visible_text.py \
  --image-dir ./images \
  --ocr-images \
  --format json \
  --output images-result.json
```

## 8) Local GIF

```bash
python3 skills/visible-text-extractor/scripts/extract_visible_text.py \
  --image ./demo.gif \
  --ocr-images \
  --gif-mode placeholder \
  --format json \
  --output gif-result.json
```

Notes:
- local GIFs can be frame-extracted when tooling exists
- remote GIFs are treated conservatively
- unsupported situations must be reported explicitly

## 9) OCR cleanup / section reconstruction

```bash
python3 skills/visible-text-extractor/scripts/postprocess_ocr_text.py \
  --input-json ./ocr-result.json \
  --title 'Clean Result' \
  --body-text 'Optional summary or body text' \
  --output-json ./clean.json \
  --output-markdown ./clean.md
```

This step is for noisy OCR. It helps:
- remove obvious garbage lines
- compress broken Chinese spacing
- deduplicate near-duplicate content
- classify image text into likely information types
- regroup image text into readable supplement blocks instead of raw OCR dumps
- preserve high-value facts such as price, time, place, rules, audience, contact, and validity

## 10) One-step Word deliverable

When the user wants a workbench-like experience, use the one-step pipeline:

```bash
python3 skills/visible-text-extractor/scripts/extract_visible_text_deliverable.py \
  --url 'https://mp.weixin.qq.com/s/xxxx' \
  --browser-fallback \
  --page-screenshot-ocr \
  --ocr-images \
  --dedupe \
  --title-override '交付标题（可选）' \
  --output-prefix ./deliverable/result
```

Outputs:
- `result.raw.json`
- `result.clean.json`
- `result.clean.md`
- `result.docx`

This is the closest thing to a zero-threshold workflow:
- one command in
- readable markdown out
- Word deliverable out
- raw audit layer still preserved

## Zero-threshold recommendation

If the user just wants the final answer with minimal friction, prefer the one-step deliverable pipeline over running multiple scripts manually.

Use the low-level scripts only when:
- debugging extraction quality
- investigating OCR failures
- comparing raw vs clean output
- building custom downstream workflows

## Quality expectations

A good final result should:
- be human-readable first
- keep raw OCR available for audit
- preserve major sections
- separate uncertainty from confirmed text
- avoid dumping decorative or broken OCR into the main answer
