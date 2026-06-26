# Session note: full-page visual QA is mandatory for xz01 visual acceptance

## Trigger

During a live xz01 search/header visual repair, the initial validation used first-viewport screenshots and passed the result. The user corrected the workflow:

> 你下次截图,进行整页截图,不要进行局部截图. 你没看到布局,以及很多细节方面的问题吗?

## Durable lesson

For xz01 homepage/page visual QA, first-viewport screenshots are not sufficient evidence. They can miss lower-page layout issues such as mobile navigation overflow, footer/back-to-top placement, lower-module spacing, card clipping, text truncation, and end-of-page artifacts.

## Required workflow

1. Capture PC full-page screenshot with a desktop viewport.
2. Capture mobile full-page screenshot using real mobile UA + mobile emulation widths such as 390px and, when needed, 360/430px.
3. If the page is long, split the full-page screenshot into segments and/or create a contact sheet.
4. Submit the full-page screenshot or contact sheet to AI visual review.
5. Explicitly inspect lower modules and footer, not only header/search/first viewport.
6. Treat AI findings as actionable repair items; do not mark PASS until full-page review passes.

## What this session found only after full-page review

- Mobile top navigation last item was clipped.
- Footer had an abnormal grey area and centered `顶` button after it.
- Search magnifier right-side safe spacing was tight.
- Some module spacing and gradient-card text readability needed refinement.

## Repair pattern used

- Mobile navigation: use an internal horizontal scroller (`overflow-x:auto`, `flex:0 0 auto`, adequate end padding) while keeping page-level `scrollWidth == clientWidth`.
- Back-to-top: avoid a document-flow centered button after footer; use a small non-obstructive right-bottom control or otherwise avoid large footer-after whitespace.
- Search icon: keep compact magnifier visual-only entry with sufficient right safe margin.
- Long-page visual review: regenerate full-page screenshots and contact sheets after repair.
