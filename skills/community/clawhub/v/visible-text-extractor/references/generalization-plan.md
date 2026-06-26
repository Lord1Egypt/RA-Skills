# generalization-plan

## Goal
Turn this skill from a page-level extractor into a generalized visible-information extractor for diverse WeChat articles and image-heavy posts.

## Target source families

1. Deal / travel / product posts
   - fares
   - coupons
   - hotel packages
   - transfer rules
   - screenshots from booking apps

2. Rules / standards / rubric posts
   - scoring tables
   - process charts
   - policy screenshots
   - dense long images with many bullet rules

3. Event / poster / forum / campus activity posts
   - posters
   - agenda cards
   - speaker blocks
   - registration QR posters
   - mixed title/time/location/eligibility/CTA graphics

4. Tutorial / course-outline / slide-collage posts
   - long image outlines
   - concept cards
   - lecture screenshots
   - formula / code screenshot hybrids

## Current failure pattern
The current pipeline is good at:
- getting some page body text
- doing shallow OCR on discovered images
- extracting a few high-value lines

It is weak at:
- treating each image as a first-class document
- segmenting long images into smaller OCR units
- preserving near-complete text instead of only key facts
- separating poster-like image reconstruction from rule/table-like text extraction
- handling formula/code regions differently from prose regions

## Required capability upgrades

### 1) Image-first mode
For image-heavy pages, do not reduce image OCR to a side note.

Behavior:
- download every discovered image
- score likely information density
- for dense images, run segmented OCR automatically
- produce per-image full text blocks before summary blocks

### 2) Segmented OCR for long and dense images
Use tiled crops with overlap for tall images.

Minimum behavior:
- detect tall images by aspect ratio or height threshold
- crop into overlapping windows
- OCR each window
- merge while removing duplicated overlap lines

### 3) Multi-style reconstruction
Choose reconstruction strategy by detected image type.

- pricing/product pages -> preserve product, price, room, route, validity, restrictions
- rules/rubric pages -> preserve headings and scoring/bullet structure as faithfully as possible
- posters/activity pages -> preserve title, organizer, time, location, audience, signup, speakers, CTA
- outline/slide-collage pages -> preserve section order and major bullets, not just 5 highlights
- code/formula regions -> keep as low-confidence verbatim appendix if readable; do not mix noisy code into polished prose

### 4) Deliver both full-text and clean summary layers
The user may want either:
- complete per-image extracted text
- cleaner reconstructed summary

So deliverables should include both layers.

Recommended structure:
- article body
- per-image full extracted text
- per-image cleaned reconstruction
- uncertainty notes

### 5) Honest confidence handling
When a region is decorative, tiny, blurred, or effectively unreadable:
- say it contains little/no readable text
- do not fabricate completeness

## Benchmarks to keep testing
Use these article families repeatedly:
- travel / booking deal article
- rule / scoring article
- event / poster article

A good iteration should improve at least one of these without badly regressing the others.
