# Browser recovery path

Use browser mode as the **secondary** path when token mode fails, expires, or is blocked.

## Purpose

Browser mode is mainly for:
- recovering from `TOKEN_EXPIRED`
- verifying whether the account can still access the target planets
- capturing visible feed previews when direct token requests are blocked

It is not the default path for remote-host deployment.

## MVP contract

The current lightweight browser script does **not** control the browser directly.
Instead, it normalizes a locally captured JSON feed snapshot into the same digest-ready item schema used by token mode.

Input shape accepted by `scripts/collect_from_browser.py`:

```json
[
  {
    "circle_name": "AI投研圈",
    "author": "作者名",
    "published_at": "2026-03-08T09:00:00+08:00",
    "title_or_hook": "标题或首句",
    "content_preview": "可见预览",
    "url": "https://wx.zsxq.com/topic/123"
  }
]
```

It also accepts an object with an `items` array.

## Why this MVP shape

- keeps the public skill lightweight
- avoids pretending a generic Python script can own OpenClaw browser-tool orchestration
- lets browser capture and normalization evolve independently
- preserves a clear recovery path without making browser mode a hard runtime dependency

## Error expectations

- `BROWSER_UNAVAILABLE`: no capture file or browser path available
- `EMPTY_RESULT`: capture exists but has no usable items
- `PARTIAL_CAPTURE`: visible preview only; long content not expanded
- `QUERY_FAILED`: malformed input or unexpected capture shape

## Suggested future upgrade

Later, a richer browser workflow can:
1. open aggregated feed via OpenClaw browser tooling
2. capture visible cards into JSON
3. feed that JSON into `collect_from_browser.py`
4. continue with dedupe and digest normally
