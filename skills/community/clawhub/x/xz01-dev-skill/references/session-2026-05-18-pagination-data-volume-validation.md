# Pagination data-volume validation correction (2026-05-18)

## Trigger

During the non-rank list pagination repair, routes such as `/alzos001/`, `/video/`, `/gameimg/`, `/gamepack/`, and `/gamepacks/` rendered an empty `<ul class="pagination"></ul>` after the correct `common_data -> getPcPageData/getMobilePageData -> $page_code -> {$page_code|raw}` chain was restored.

## Correction

Do not treat every empty pagination container as a template defect. The xz01_demo helpers may leave `$page_code` empty when the current route has only one page or insufficient eligible data.

Validation must first establish whether the route has more than one page of eligible data.

- Multi-page eligible data + empty pagination = FAIL; fix the demo data chain, not a custom pager.
- One-page/insufficient eligible data + empty pagination = expected demo behavior; report as data-volume-limited.

## Still forbidden

Do not add fallback links such as `上一页 1 下一页`, do not compute page counts in templates, and do not build request-parameter pagination (`request()->param`, `page_count`, `pager_i`, `ellipsis`, disabled prev/next).

## Verification pattern

For representative non-rank routes, validate both:

1. Static chain: list template includes matching `common_data`, common data calls `getPcPageData/getMobilePageData`, and template outputs `{$page_code|raw}`.
2. Rendered behavior: if data exceeds one page, PC shows numeric links and mobile shows `上一页`/`下一页`; if data is one page or insufficient, an empty page-code output is acceptable.
