# Changelog

All notable changes to this project will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
versioning follows [Semantic Versioning](https://semver.org/).

## [0.6.4] - 2026-05-21

### Changed

- **English SKILL docs**: root, compare, and evaluate `SKILL.md` bodies translated to English for ClawHub and international users.
- **Bilingual triggers**: frontmatter `description` includes English and Chinese trigger phrases.
- **Chinese reference**: added `references/zh-CN.md`; agents load it when the user writes in Chinese.
- **Regional defaults**: document UK-only support with `london` as default city; ClawHub homepage in skill metadata.

## [0.6.3] - 2026-05-21

First public release for ClawHub and Claude Skill distribution.

### Highlights

- **Cross-platform price comparison (compare)**: search multiple second-hand marketplaces by keyword and return results sorted by price. Supports OK.com, Gumtree, eBay, and Amazon.
- **In-depth item evaluation (evaluate)**: fetch listing details from URLs and score items on seller trust, listing authenticity, condition, price competitiveness, and risk signals, with buy recommendations.
- **End-to-end workflow (summarize)**: one command for fetch details → score multiple items → comparative summary.
- **bb-browser adapters**: built-in search and detail adapters per platform; install with `python scripts/cli.py install`.
- **Optional vision model**: configure an OpenAI-compatible vision API (e.g. Qwen-VL) for image-based authenticity and condition analysis via `--vision-model`.

### Regional support

- **United Kingdom only for now**: defaults to UK marketplaces (Gumtree, eBay UK, Amazon UK, etc.); compare and evaluate flows are optimized for UK sites.
- **Coming later**: US, Australia, Canada, and other OK.com regions. Per-country adapters are already in the codebase and will be enabled in future releases.

### Other

- Added MIT `LICENSE`; unified package version to `0.6.3`.

## [0.6.2] - 2026-05-19

### Fixed
- **Amazon adapters** (`search.js`, `search-uk.js`, `detail.js`): add CAPTCHA detection with actionable error hints; add wrong-region/currency detection (JPY/SGD instead of GBP/USD); strengthen request headers to mimic real browser; fix `condition` field bug where `sort` value leaked into condition.
- **OK.com adapter** (`ok/search.js`): distinguish server-side empty results from parse failures for better diagnostics; fix double currency symbol (`$$300` → `$300`).
- **Python compare.py**: defensive double-currency-symbol strip in `_normalize_items`; pass adapter `hint` and `summary` messages through to error output.

### Changed
- **All platforms**: default sort changed from `price` (low-to-high) to `best` (relevance) to avoid surfacing irrelevant low-price accessories.
- **platforms.py**: removed explicit `"sort": "price"` from default args for gumtree, all ebay-*, and all amazon-* platforms.
- **SKILL.md**: added "代码提交规范" section — CHANGELOG must be updated before every push.

## [0.6.1] - 2026-05-09

### Fixed
- **Gumtree detail adapter** (`adapters/gumtree/detail.js`): static `fetch()` HTML often has no gallery `<img>` tags because the carousel is JS-rendered. Images are now collected in order from JSON-LD (`application/ld+json`), Open Graph / Twitter meta tags, image URLs in inline `<script>` blobs, then the original DOM selectors as a fallback. Restores non-zero `images` for evaluate / vision flows.
- **Smoke test** `test_load_vision_config_defaults`: temporarily clears `_CONFIG_SEARCH_PATHS` so the “vision disabled with no config” assertion does not fail when developers have `~/.config/used-price-compare/vision.json`; unblocks the pre-push hook and matches CI behaviour.

## [0.6.0] - 2026-04-29

### Added
- **Evaluate sub-skill** with detail page fetching and item reliability scoring
- Detail page adapters for all 4 platforms: `ok/detail.js`, `ebay/detail.js`, `gumtree/detail.js`, `amazon/detail.js`
- Three new CLI subcommands: `fetch-detail`, `evaluate`, `summarize`
- `evaluator.py` — 5-dimension scoring engine (seller trust, listing authenticity, condition value, price competitiveness, risk flags)
- `fetcher.py` — URL-to-platform routing and bb-browser subprocess management for detail pages
- `models.py` — `ItemDetail`, `SellerInfo`, `EvalScores`, `EvalResult` dataclasses
- `skills/compare/SKILL.md` and `skills/evaluate/SKILL.md` sub-skill definitions
- 10 new smoke tests covering URL routing, evaluator scoring, and CLI parser

### Changed
- Root `SKILL.md` refactored into umbrella router (xiaohongshu-skills pattern), dispatching to compare and evaluate sub-skills
- `compare.py` `format_comparison_table()` now returns raw structured data only (analysis/recommendation removed from code, aligning with 0.5.0 CHANGELOG)
- Version bumped to 0.6.0

### Removed
- `analysis.py` deleted (replaced by `evaluator.py` with richer detail-page-based scoring)
- `_build_recommendation()` removed from `compare.py`
- `analysis` and `recommendation` keys removed from `compare` CLI output

## [0.5.0] - 2026-04-23

### Changed
- Analysis layer removed from CLI — all reliability scoring, verdict, and purchase recommendations now handled by the calling Agent via SKILL.md prompts
- `format_comparison_table` output simplified: raw structured data only (price_ranking, by_platform, lowest_price, ok_best)
- `price_ranking` items now include full title, condition, seller, location (previously truncated to 60 chars)
- New `ok_search_url` field replaces hardcoded recommendation text

### Removed
- `analysis.py` — 325-line rule-based scoring engine (relevance, price sanity, condition, seller trust, value score)
- `_build_recommendation` and `_platform_highlight` functions from compare.py
- `analysis`, `analysis.best_value`, `recommendation` fields from CLI JSON output

## [0.4.0] - 2026-04-22

### Added
- Item reliability analysis module with 5-dimension scoring (relevance, price sanity, condition, seller trust, value score)
- Three-stage output: price comparison -> reliability analysis -> purchase recommendation
- `analysis` field in CLI JSON output with per-item scores, flags, and verdict

### Changed
- Output format restructured into three clear sections for better decision flow

## [0.3.0] - 2026-04-22

### Fixed
- UK cities defaulting to US country routing (only 4 UK cities were mapped)
- Hardcoded `us.ok.com` URL in recommendations now resolves by country
- OK adapter summary always showing GBP regardless of country

### Added
- 9 UK cities: Leeds, Liverpool, Glasgow, Edinburgh, Bristol, Cardiff, Sheffield, Nottingham, Newcastle
- 7 US cities: Boston, Miami, Washington DC, Philadelphia, Atlanta, Dallas, Seattle
- Amazon UK adapter and family-based routing (amazon-us / amazon-uk)
- Currency detection (`currency` field on CompareItem)

### Removed
- Craigslist platform (adapter deleted, all code references cleaned)
- OfferUp references from documentation (never implemented)

## [0.2.0] - 2026-04-22

### Changed
- Project renamed from `bargain-skills` to `used-price-compare`
- Python package renamed from `scripts/bargain/` to `scripts/used_price_compare/`
- CLI prog name changed to `used-price-compare`
- PRD renamed from `PRD-bargain-radar.md` to `PRD-price-watch.md`

## [0.1.0] - 2026-04-22

### Added
- Initial release with multi-platform price comparison via bb-browser
- Supported platforms: OK.com, Craigslist, Gumtree, eBay (US/UK/AU/CA), Amazon
- CLI with `compare`, `platforms`, and `install` subcommands
- Per-country eBay adapter routing based on city-to-country mapping
- Parallel platform querying with ThreadPoolExecutor
- Price ranking, platform comparison, and purchase recommendations
