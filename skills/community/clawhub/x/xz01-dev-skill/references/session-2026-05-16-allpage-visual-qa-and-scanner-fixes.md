# 2026-05-16 — All-page visual QA + scanner false-positive fixes

## Context

During xz01 validation the user required PC+mobile all-page scanning before packaging, including template code scan, curl/browser access, screenshots, and AI recheck. Core page screenshots were not enough when the crawl discovered many existing DB routes.

## Durable workflow lesson

When the user asks for “双端所有页面 / 全部页面截图 + AI复检”:

1. Run static template scan first.
2. Run URL crawl for PC+mobile existing DB routes and save the JSON result.
3. Capture screenshots for every URL in the crawl result, not only the homepage/list pages.
4. Also keep a small core screenshot set for direct inspection: PC/mobile homepage, software list, game list, news/list, and at least one detail page per content type.
5. Build contact sheets from the full screenshot set and submit every contact sheet to AI visual review. This is the scalable way to AI-review dozens of pages without losing coverage.
6. Keep the screenshot manifest with URL → file path mapping so any contact-sheet issue can be traced back to the exact page.
7. If a screenshot command times out for a detail page, retry with Chromium flags such as `--disable-dev-shm-usage`, `--disable-extensions`, and `--virtual-time-budget`; do not mark the page as visually checked until a screenshot exists.

## Scanner implementation pitfall

Avoid naive zero-count detection:

```python
re.search(r'0\s*款', body)
```

This falsely matches strings such as `10款`. Use a digit-boundary-aware pattern instead:

```python
re.search(r'(?<!\d)0\s*款', body)
```

## AI visual triage rule

AI may flag a page-label mismatch if a game route displays a database category label like “手游下载”. Treat this as a possible wording observation, not an automatic fail, when:

- the DB route is valid,
- the page renders game/software/news data correctly,
- there is no 500, no empty list, no broken pagination, and no layout defect.

If the user requires label normalization, handle it in the template display layer only; do not create routes or modify database categories by default.
