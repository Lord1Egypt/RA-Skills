# 2026-05-16 — demo_xz01 systematic validation correction

User correction: xz01 work must learn from `/root/.openclaw/workspace/demo_xz01` systematically, not only patch one page at a time. Ambiguous rules may be listed for user confirmation, but obvious xz01 defects must be handled directly.

## Learned demo_xz01 conventions

- Treat `demo_xz01` as a read-only pattern corpus. Do not edit it and do not copy it blindly.
- Required dual-end template coverage must be systematic: PC `cms/*` and mobile `mobile/*` counterparts for homepage, list pages, search/page/404/500, and software/game/news/collection detail pages.
- Software/game list pages and detail pages must exist and render with real data through the existing ThinkPHP/template data functions; they must not be omitted, referenced only, or filled with static placeholders.
- List pages that paginate should follow the demo data-rendering pattern using `getPcPageData` / `getMobilePageData` and output `$page_code|raw` or equivalent pagination variables. A page failing because pagination variables are missing must be fixed in the template/header/footer include chain, not hidden.
- Every add/modify/delete development change must clear `/www/wwwroot/www.900az.com/runtime/` before validation.
- Before packaging, scan both PC and mobile front-end URLs for 500/ThinkPHP errors. Packaging is forbidden if any checked existing DB route returns a 500-style page.
- Validate all relevant dual-end pages by static template scan, curl/browser HTTP access, screenshots, and AI visual review.

## Resource loading rules confirmed by user

- Do not use the old common jQuery path: `<script type="text/javascript" src="/themes/default/common_cms/common/jquery.min.js"></script>`.
- Use theme-side PC/mobile asset jQuery loading consistent with demo_xz01, such as `/themes/default/common_cms/pc/assets/js/jquery.min.js` or `/themes/default/common_cms/mobile/assets/js/jquery.min.js` where an absolute path is needed, or the corresponding local `assets/js/jquery.min.js` form in copied common assets.
- If UIkit is needed, use: `<link rel="stylesheet" href="/themes/default/common_cms/pc/assets/css/uikit.css"><script src="/themes/default/common_cms/pc/assets/js/uikit.js"></script>` (or the minified demo-equivalent only when matching actual assets requires it).
- If Swiper/carousel is needed, include both: `<script src="/themes/default/common_cms/pc/assets/js/swiper-bundle.min.js"></script>` and `<link rel="stylesheet" href="/themes/default/common_cms/pc/assets/css/swiper-bundle.min.css">` adapted per PC/mobile asset location.

## Validation scripts now part of the skill

Skill support scripts are stored under `scripts/` and should be copied or invoked from there:

- `xz01-runtime-clear.sh` — clear ThinkPHP runtime cache before validation after every dev change.
- `xz01-backend-baseline-check.sh` — ensure backend/PHP scope has not been modified accidentally.
- `xz01-theme-diff-check.sh` — inspect theme-only diff boundaries.
- `xz01-quick-http-gate.py` — quick URL HTTP gate for key URLs.
- `xz01-template-static-scan.py` — static template scan for dual-end completeness, bad resource paths, pagination-pattern gaps, mobile target_blank, malformed links, and forbidden filler assets.
- `xz01-full-url-scan.py` — crawl same-host PC/mobile pages and fail on 5xx, ThinkPHP errors, malformed internal links, mobile blank-targets, many empty placeholders, and zero-count software/game list pages.
- `xz01-screenshot-core.sh` — capture deterministic Chromium headless screenshots for core PC/mobile pages before AI visual review.

## Packaging gate

Before creating any zip package under `/root/.hermes/workspace/xz01/`:

1. Clear runtime cache.
2. Run static template scan.
3. Run HTTP/crawl scan on PC and mobile.
4. Ensure list and detail pages for software/game render with data.
5. Capture PC and mobile screenshots for all relevant existing DB routes/pages.
6. Submit screenshots to AI visual review and incorporate findings.
7. Only package if all gates pass.
