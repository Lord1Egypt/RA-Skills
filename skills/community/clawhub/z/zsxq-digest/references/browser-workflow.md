# Browser workflow (OpenClaw recovery path)

Use this only when token mode is unavailable, expired, blocked, or needs verification.

## Goal

Turn a logged-in browser view into a lightweight JSON snapshot that can be normalized by `scripts/collect_from_browser.py`.

## Recommended manual workflow

1. Attach a logged-in Knowledge Planet tab through OpenClaw browser tooling.
2. Open the aggregated update feed or the specific planet page you want to inspect.
3. Use `browser.snapshot` to confirm the page is logged in and that visible cards are present.
4. Use `browser.act` with `request.kind="evaluate"` and the starter function in `scripts/browser_capture_starter.js`.
5. Save the returned JSON locally as `browser-capture.json`.
6. Feed that JSON file into:
   - `scripts/collect_from_browser.py`
   - then `scripts/dedupe_and_state.py`
   - then `scripts/digest_updates.py`

## Recommended snapshot fields

Each visible card should be reduced to the smallest useful shape:

```json
{
  "circle_name": "AI投研圈",
  "author": "作者名",
  "published_at": "2026-03-08T09:00:00+08:00",
  "title_or_hook": "标题或首句",
  "content_preview": "页面上可见的预览文本",
  "url": "https://wx.zsxq.com/topic/123"
}
```

Optional fields:
- `likes`
- `comments`
- `content_type`
- `item_id`

## Why keep browser capture minimal

- lowers maintenance cost when page structure changes
- avoids brittle deep scraping logic in the public MVP
- keeps browser mode focused on recovery and verification
- lets token mode remain the primary deployment path

## Expected limitations

- long posts may remain collapsed
- some timestamps may be relative or missing
- some cards may not expose stable ids in the visible UI
- very active feeds may push older important posts below the fold

When this happens, prefer:
- `PARTIAL_CAPTURE`
- preserving the original URL
- honest incompleteness notes in the final digest

## Starter extraction function

Use the function stored in `scripts/browser_capture_starter.js` as the initial `browser.act` evaluate payload.

What it does:
- looks for visible `a[href*="/topic/"]` links
- walks up the DOM to find a reasonable text container
- emits a compact JSON payload with an `items` array

What it does **not** guarantee:
- exact circle names
- full author extraction
- expanded long-post content
- resilience to future DOM changes

Treat it as a recovery starter, not a forever parser.

## Suggested future automation split

Keep the layers separate:

1. **browser tool layer**
   - navigates and snapshots the page
2. **capture-to-json layer**
   - extracts visible cards into a small JSON file
3. **normalization layer**
   - `scripts/collect_from_browser.py`
4. **digest pipeline layer**
   - `scripts/run_digest_pipeline.py`

This separation keeps the repo publishable even if browser orchestration evolves later.
