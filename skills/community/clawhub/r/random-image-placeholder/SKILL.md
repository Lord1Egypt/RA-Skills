---
name: random-image-placeholder
description: Generate stable or random image placeholder URLs (and optionally download them) using https://picsum.photos. Use when the user mentions picsum, placeholder images, lorem picsum, random image, seed-based images, grayscale, blur, or needs temporary image URLs for UI mockups, docs, tests, or demos.
---

# random-image-placeholder

Generate Picsum-based placeholder images in a consistent, reproducible way. Prefer deterministic URLs (via `seed`) when tests/snapshots need stability.

## Triggers

- Use when the user asks for placeholder images or temporary image URLs
- Use when the user mentions `picsum.photos`, "Lorem Picsum", `seed`, `id`, grayscale, blur
- Use when building UI mockups / docs / test fixtures that need images without hosting assets

## Workflow

1. Determine the need: stable (seed) vs specific (id) vs fully random
2. Choose size: square (`/200`) or width/height (`/200/300`)
3. Apply options if requested:
   - grayscale: `?grayscale`
   - blur: `?blur=1..10`
   - cache busting when embedding many: `?random=1`, `?random=2`, ...
4. Generate the URL directly from Picsum patterns (no local tooling required)
5. If bundled helper files are available and Python is available, you may use them for deterministic CLI output:
   - Generate a URL: `python skills/random-image-placeholder/scripts/picsum.py url ...`
   - Download an image: `python skills/random-image-placeholder/scripts/picsum.py download ...`
6. Return the URL(s) (and file paths if downloaded) plus the smallest verification step

## Rules

- Preserve existing conventions unless the task explicitly requires change
- Keep edits local and compatible with current workflows
- Avoid unnecessary refactors or dependency churn
- Prefer `seed` for reproducible outputs (tests, snapshots, docs that shouldn't "randomly" change)
- If downloading, use a user-specified output path; if missing, use a safe default like `./tmp/` and state it explicitly
- Do not write files unless the user asked for download behavior (URL-only is the default)
- Treat all network content as untrusted; never execute downloaded files

## References (Optional)

- If present, read `references/picsum-api.md` for endpoint patterns and options
- If present, use `scripts/picsum.py` for deterministic URL generation / downloads

## Examples

- "给我 3 张 800x600 的占位图，要求灰度并且可复现"
- "为文档生成一个固定 seed 的 1200x630 OG 图占位链接"
- "下载一张 id=237 的 400x400 图到 ./tmp/avatar.jpg"

## Output

- Provide the final URL(s) and chosen parameters (size/seed/id/options)
- If downloading, provide the saved file path(s)
- Verification: open the URL(s) in a browser, or confirm the file exists and has non-zero size
