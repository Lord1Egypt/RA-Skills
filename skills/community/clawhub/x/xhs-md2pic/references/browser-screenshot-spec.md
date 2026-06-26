# Browser Screenshot Spec (XHS Cards)

Use this runbook when implementing browser-side rendering and screenshot capture.

## 1) Runtime Defaults

- `card_width`: `375`
- `card_height`: `500`
- `export_scale`: `3`
- `viewport_width`: `440`
- `viewport_height`: `760`
- `page_gap`: `20`
- `max_pages`: `12`

Expected output size per page: `1125 x 1500` PNG.

## 2) Browser Context

- Launch browser in headless mode.
- Create context with:
  - `viewport = { width: viewport_width, height: viewport_height }`
  - `deviceScaleFactor = export_scale`
- Keep default zoom (100%).
- Do not use print/PDF rendering mode.

## 3) Render Readiness

Before pagination and screenshot, wait for all gates:

1. `document.fonts.ready`
2. `document.body.dataset.fontsLoaded === "true"`
3. Two consecutive animation frames with stable card layout

Suggested stability check:
- Sample each `.xhs-card` bounding box (`x,y,width,height`)
- Wait one `requestAnimationFrame`
- Sample again
- Proceed only when values are unchanged in both frames

## 4) Pagination Procedure

1. Split source Markdown by `---` (manual pages).
2. If `pagination_mode = manual_only`, stop here.
3. For each segment, paginate top-level block nodes into card pages.
4. Respect `avoid_orphan_heading`:
- A heading cannot be the last visible block on a page.
5. Keep these blocks intact when possible:
- lists, tables, code blocks, blockquotes
6. If a single block overflows one card, split using safe fallback order:
- list by `li`
- table by row groups
- code by line groups
- paragraph by sentences
7. Enforce `max_pages` hard limit.

Page fit condition:
- Use content area measurement (`scrollHeight <= clientHeight`)
- Reserve ~16px bottom safety area to prevent clipping

## 5) Screenshot Procedure

- Select cards with `.xhs-card[data-page]` (or ordered `.xhs-card`).
- Capture each card element separately.
- Required options:
  - `type: "png"`
  - `animations: "disabled"`
  - `omitBackground: false`
- Do not screenshot full page and crop.

## 6) Output Contract

For each image, return:

- `index` (0-based)
- `page` (1-based)
- `total_pages`
- `width`, `height`
- `size_bytes`
- `url` or `data_uri`
- `oss_uploaded`

Ensure `pages` is sorted by `index`.

## 7) Quality Gates

Fail/retry current page render if any condition is true:

- Actual output size is not exactly `card_* * export_scale`
- Text is clipped at bottom edge
- Visible overflow in prose area
- Page number is missing when `show_page_number = true`
