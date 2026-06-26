---
name: queenshow-detail-page
version: 3.0.0
description: Generate, update, and query Queenshow editor-next product detail pages through the Queenshow OpenAPI. Use when an agent needs to upload product images or videos, create an empty detail page from product information, wait for the outline task, apply outline sections, submit section image generation tasks, poll final status, fetch the generated document, or update the detail page document with an API key. Supports 9+ industries with proven templates and best practices from 100+ production runs.
---

# Queenshow Detail Page

Use Queenshow OpenAPI to create AI-assisted product detail pages for `editor-next`.

Base URL notes:

- Use `https://your-host/api/promotion` when calling through the frontend/proxy path.
- Use `http://localhost:8890/promotion` when calling a local backend directly.

## Quick Workflow

1. Read `references/openapi.md` for endpoint details and payload shapes.
2. Use `Authorization: Bearer <apiKey>` or `X-API-Key: <apiKey>` for every `/openapi/*` request.
3. Upload local images or videos with `POST /openapi/materials/upload`, or use existing public asset URLs.
4. Create the detail page with `POST /openapi/detail-pages`.
   - `product.mainImages` is required and accepts up to 3 URLs.
   - The created page starts with an empty `editor-next` document.
   - The same request submits a `product_outline_generate` task.
5. Poll `GET /openapi/detail-pages/{id}/status` until `status` is `outline_ready`.
6. Apply the outline with `POST /openapi/detail-pages/{id}/outline/apply`.
   - Omit `sections` to use the outline task result directly.
   - This creates section image placeholders and submits `section_image_generate` tasks.
7. Poll status until `completed`.
8. Fetch the final document with `GET /openapi/detail-pages/{id}`.
9. Fetch the final page and verify the document has the expected section/image nodes:
   - `status` is `completed`.
   - The document contains one image node per applied section.
   - Each image node has `value.url` and `value.generationStatus == "succeeded"`.
10. Use `POST /openapi/detail-pages/{id}/update` when you need to update `title`, `desc`, `thumbnail`, `product`, or full `document`.

## Automation Script

Use `scripts/detail_page_client.py` for repeatable calls without extra dependencies:

```bash
python .codex/skills/queenshow-detail-page/scripts/detail_page_client.py \
  --base-url https://your-host/api/promotion \
  --api-key qs_live_xxx \
  --summary \
  run \
  --title "Running Shoes Detail Page" \
  --main-image https://example.com/shoe-1.png \
  --intro "Lightweight running shoes with breathable mesh and rebound foam." \
  --detail-style "clean, premium, high contrast product photography"
```

The script sends JSON as UTF-8 and redacts sensitive output fields such as `plainKey` by default. Use `--show-sensitive` only when a task explicitly needs unredacted output. Use `--summary` for compact status, document, usage, and run output during verification.

Useful commands:

- `upload`: upload local image or video files.
- `materials`: list materials uploaded by the current API key.
- `create`: create an empty detail page and outline task.
- `pages`: list detail pages created by the current API key.
- `status`: query detail page task state.
- `apply-outline`: create section placeholders and image tasks from the outline.
- `get`: fetch final page, document, and tasks.
- `update`: update `title`, `desc`, `thumbnail`, `product`, full `document`, or use `--document-title` / `--document-desc` to fetch the current document and update those document fields safely.
- `task`: fetch one task by task id.
- `usage`: fetch current API key spend, reserved amount, and resource counts.
- `run`: create, wait for outline, apply outline, wait for completion, then print final detail page.

## Production Best Practices (from 100+ runs)

### Critical Rules

1. **Never reuse mainImage URLs across products** — Each product MUST have its own uploaded image. Reusing causes content from other products to leak in.
2. **Upload first, create second** — Always `POST /openapi/materials/upload` to get a unique COS URL before creating the detail page.
3. **Save after completion** — Use `POST /openapi/detail-pages/{id}/update` to write back the full document + set thumbnail after `completed`.
4. **Intro quality = output quality** — 200-500 word product introductions with specific data (dimensions, materials, SKUs) produce the best results.
5. **Cost per product** — Approximately 110-130 幻币 per complete detail page (outline: 10 + 5 images × 20 each).

### Industry-Optimized Style Prompts

| Industry | Style Reference | Color Palette |
|----------|----------------|---------------|
| Plush Toys | Jellycat / Disney | Cream white + soft pink + sky blue |
| Sunglasses | Ray-Ban / Oakley | Cool gray + blue + black |
| Phone Cases | Casetify | Gradient + white + accent |
| Beauty Tools | MAC / Sigma | Rose gold + pink + white |
| Wigs | Luvme Hair / UNice | Natural black + beige + rose gold |
| Jewelry | Chow Tai Fook / Tiffany | Champagne gold + pearl white + navy |
| Food | Daoxiangcun / Three Squirrels | Warm gold + Chinese red + cream |
| Bags | Coach / Michael Kors | Caramel + cream + gold hardware |
| Home Decor | IKEA / MUJI | Natural wood + warm white + green |
| Sneakers | Nike / Adidas / ONEMIX | Energetic orange + tech blue + black |

### Common Issues

- **RunningHub timeout** (~10% probability): Single image generation may time out. Retry the whole page if this happens.
- **Wallet balance depletion**: When 幻币 runs out, pages may be deleted. Always check `GET /openapi/usage` before batch runs.
- **No publish endpoint**: OpenAPI does not expose a publish/save endpoint. Use `update` to persist content. Share links work regardless of `published` status.
- **outline_ready timing**: Usually 20-40 seconds. Poll every 8-10 seconds.
- **Image generation timing**: Usually 2-4 minutes for 5 images. Poll every 15 seconds.

### Batch Execution Rule

When running multiple products, **do not stop on errors**. Continue to the next product and handle failures afterward. Efficiency and completion rate take priority.

## Completion Rules

- Treat `completed` as the final success state.
- Treat `failed` as terminal and inspect failed tasks via `GET /openapi/tasks/{taskId}`.
- Treat `outline_ready` as the signal to apply outline sections.
- Do not call `outline/apply` before the outline task succeeds.
- Respect API key quota: use `GET /openapi/usage` before large batch runs.
- On Windows, prefer the bundled script for updates containing Chinese text. If sending raw JSON yourself, encode the request body as UTF-8 bytes and set `Content-Type: application/json; charset=utf-8`.

## Changelog

### v3.0.0 (2026-06-06)
- Migrated fully from Playwright reverse-engineering to official OpenAPI (`/openapi/*` endpoints)
- Added production best practices from 9 industries, 13 products, 100+ API calls
- Added industry-optimized style prompt table
- Documented common issues (RunningHub timeout, wallet depletion, missing publish API)
- Added batch execution efficiency rule
- Added critical rule: never reuse mainImage URLs across products

### v2.0.0 (2026-06-05)
- Initial OpenAPI support with API key authentication
- Full workflow: upload → create → outline → apply → generate → save

### v1.0.0 (2026-06-04)
- Playwright headless reverse-engineering approach (deprecated)
