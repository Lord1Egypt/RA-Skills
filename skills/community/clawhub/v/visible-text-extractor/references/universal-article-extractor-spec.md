# universal-article-extractor-spec

## Mission
Upgrade this skill from a sample-driven article extractor into a generalized full-information webpage/article extractor.

Input:
- any article URL
- browser-rendered page HTML
- saved HTML
- screenshot set
- long image set
- local page assets

Output:
- as complete and accurate as possible visible information
- structured for reading and downstream reuse
- optional Word export
- explicit uncertainty instead of silent omission

## Supported source types

The skill should aim to generalize across:
- WeChat official-account articles
- news articles
- blogs
- technical tutorials
- long-form explainers
- image-heavy landing pages
- infographic-like articles
- screenshot threads
- pages containing tables, captions, quotes, footnotes, side notes, and embedded figure text

## Required capabilities

### 1) Text extraction accuracy
Preserve:
- title
- subtitle
- author / source / time when available
- section headings
- body paragraphs
- lists
- block quotes
- captions
- footer notices that are part of article content

Avoid mixing in:
- nav chrome
- recommendation widgets
- floating toolbar text
- repeated follow/share/like controls
- unrelated footer/site chrome

### 2) Image / screenshot / long-image OCR
Treat images as first-class content when they carry information.

Required behavior:
- download every discovered image in order
- detect dense/tall images automatically
- run high-accuracy OCR with multiple preprocessed variants
- segment tall images into overlapping slices
- choose best variant by text quality score
- preserve per-image full text in source order

### 3) Mixed text + image article fusion
Do not force a page into only one lane.

If the article has both body text and meaningful images:
- keep body text in order
- insert image-transcribed blocks in reading order when possible
- avoid dumping all images at the very end unless the user explicitly asks for appendix style

### 4) Hierarchy reconstruction under complex layout
Try to preserve:
- heading levels
- numbered sections
- bullet lists
- figure caption relationships
- section cards / part labels (`Part1`, `引言`, `结语`, etc.)
- table row groupings when visible structure is recoverable

### 5) Word readability
Word output should be:
- readable without cleanup
- visually simple
- ordered in a way a human can follow from top to bottom
- free from metadata clutter unless requested

Default rule:
- do not inject source URLs, image dimensions, OCR engine notes, or confidence chatter into the main reading document unless the user asks for audit details

### 6) Generalization and robustness
Do not overfit to known benchmark articles.

Maintain stable behavior on unseen pages by using:
- generic text extraction rules
- generic image density detection
- generic OCR quality scoring
- generic content ordering heuristics
- explicit uncertainty handling

## Output modes

### A. Clean article mode
Best for normal readers.

Include:
- title
- metadata if meaningful
-正文主线
- merged image text in reading order
- light structure restoration
- uncertainty only when important

### B. Transcript mode
Best for “do not miss anything”.

Include:
- title
- intro/body chunks in order
- every image text block in order
- minimal formatting
- no extra commentary

### C. Audit mode
Best for debugging.

Include:
- raw extraction json
- image OCR candidates
- chosen variant names
- uncertainty notes

## Quality rules

1. Do not silently drop major information-bearing images.
2. Do not aggressively summarize when the user asked for full extraction.
3. Do not flatten all content into one unreadable wall of text.
4. Do not let noisy OCR dominate the reading document; keep low-confidence debris out when clearly worthless.
5. If exact recovery is impossible, keep the best visible reading version and mark uncertainty.
6. Prefer accurate partial extraction over fake completeness.

## Structural heuristics

### Metadata extraction
Look for:
- `og:title`, HTML title, visible h1
- visible byline blocks
- visible time/date strings
- source/author labels

### Body cleaning
Remove or down-rank:
- “继续滑动看下一个”
- “轻触阅读原文”
- “点赞/在看/分享” chrome
- nav labels and recommendation cards when clearly not body

### Image ordering
Preserve discovered image order from the article container.
When possible, map image blocks between nearby body chunks rather than appending all to the end.

### Table handling
If OCR yields table-like rows:
- keep rows line-by-line
- preserve headers first
- avoid rewriting into prose unless the table is tiny and obvious

### Caption handling
If a short line immediately precedes or follows an image-derived block and looks like a caption, keep it adjacent.

## Implementation direction

The pipeline should increasingly look like:

1. fetch / render page
2. extract visible body text + metadata + ordered images
3. OCR each image with multi-variant, segmented high-accuracy pipeline
4. score and select best OCR result per image
5. classify image type
6. build either:
   - reading-order article
   - transcript article
   - audit package
7. export markdown + docx

## Success criteria

A strong generalized result should show:
- more complete body recovery
- stronger image text recovery
- more readable ordering
- fewer irrelevant UI fragments
- stable behavior on unseen article styles
