# startup-launch-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**22 endpoints across 3 platform group(s).**

## ProductHunt (11)

### `producthunt_about`

- **HTTP:** `GET /producthunt/product/{id}/about`
- **What:** Retrieve Product Hunt product about page. Returns the about-page data for a Product Hunt product, looked up by its slug in `id`. It covers the product's launch details with badges, ranks, comment count and detailed reviews with alternative products, along with the product's ad, forum and media information.
- **Params:** `id` (string, **required**) — Product Hunt slug

### `producthunt_alternatives`

- **HTTP:** `GET /producthunt/product/{id}/alternatives`
- **What:** Retrieve Product Hunt product alternatives. Lists alternatives to a Product Hunt product, looked up by its slug in `id`. `first` sets the page size (default 10), `order` defaults to `most_relevant`, and `tags` takes comma-separated tag slugs. Returns alternative items with ratings, badges and scores, alternative tags with counts, and related discussions. Use `end_cursor` as `cursor` for the next page.
- **Params:** `cursor` (string, optional) — Pagination cursor; `first` (integer, optional) — Page size; `id` (string, **required**) — Product Hunt slug; `order` (string, optional) — Sort order; `tags` (string, optional) — Comma-separated tag slugs

### `producthunt_category`

- **HTTP:** `GET /producthunt/category/{slug}`
- **What:** Retrieve Product Hunt category details. Returns a Product Hunt category by its `slug`, such as `vibe-coding`: name, description, meta title, last update time, parent category and its sub-categories, hero products, questions with top answers, and related discussions.
- **Params:** `slug` (string, **required**) — Product Hunt category slug

### `producthunt_category_products`

- **HTTP:** `GET /producthunt/category/{slug}/products`
- **What:** Retrieve Product Hunt category products. Returns the products in a Product Hunt category (now backed by Product Hunt topics), cursor-paginated. Pass the `cursor` from a previous response's `end_cursor` to page; `page_size` controls the batch size. `page`, `featured_only`, `order` and `tags` are accepted for compatibility but no longer affect the result.
- **Params:** `cursor` (string, optional) — Pagination cursor from a previous response's end_cursor; `featured_only` (boolean, optional) — Accepted for compatibility; no longer affects results; `order` (string, optional) — Accepted for compatibility; no longer affects results; `page` (integer, optional) — Accepted for compatibility; use cursor to paginate; `page_size` (integer, optional) — Page size (number of products); `slug` (string, **required**) — Product Hunt category slug; `tags` (string, optional) — Accepted for compatibility; no longer affects results

### `producthunt_customers`

- **HTTP:** `GET /producthunt/product/{id}/customers`
- **What:** Retrieve Product Hunt product customers. Lists the customer products of a Product Hunt product, looked up by its slug in `id`. `order` is `customers` (default) or `latest_launch`, `page` defaults to 1 and `page_size` to 10. Each item has its name, categories, badges, review and follower counts, and founder shoutouts. An unknown slug returns 404.
- **Params:** `id` (string, **required**) — Product Hunt slug; `order` (string, optional) — Product Hunt customers order; `page` (integer, optional) — Page number; `page_size` (integer, optional) — Results per page

### `producthunt_launches`

- **HTTP:** `GET /producthunt/product/{id}/launches`
- **What:** Retrieve Product Hunt product launches. Lists the launch posts of a Product Hunt product, looked up by its slug in `id`. `order` defaults to `DATE`; pass the returned `end_cursor` as `cursor` for the next page. Each launch has its name, tagline, ranks, scores, comment count, badges and dates. An unknown slug returns 404.
- **Params:** `cursor` (string, optional) — Pagination cursor; `id` (string, **required**) — Product Hunt slug; `order` (string, optional) — Product Hunt launch order

### `producthunt_leaderboard`

- **HTTP:** `GET /producthunt/leaderboard`
- **What:** Retrieve Product Hunt leaderboard. Returns the Product Hunt leaderboard for a `scope` of `daily` (default), `weekly`, `monthly` or `yearly`, positioned with `date` (YYYY-MM-DD) or `year`, `month`, `day` and `week`. Only the first page is served, so a non-empty `cursor` returns an error. `featured` and `order` are accepted but do not change the default view.
- **Params:** `cursor` (string, optional) — Pagination cursor; `date` (string, optional) — Anchor date in YYYY-MM-DD format. Used to derive missing year/month/day/week values.; `day` (integer, optional) — Daily day override; `featured` (boolean, optional) — Featured products only; `month` (integer, optional) — Daily/monthly month override; `order` (string, optional) — Ranking order override. Defaults to scope rank enum.; `scope` (string, optional) — Leaderboard scope: daily, weekly, monthly, yearly; `week` (integer, optional) — Weekly ISO week override; `year` (integer, optional) — Leaderboard year override

### `producthunt_makers`

- **HTTP:** `GET /producthunt/product/{id}/makers`
- **What:** Retrieve Product Hunt product makers. Lists the makers of a Product Hunt product, looked up by its slug in `id`. Each maker has a name, username, headline, avatar, follower count and the posts they made. The response includes `total_count` and claim status, and the returned `end_cursor` can be passed as `cursor` for the next page.
- **Params:** `cursor` (string, optional) — Pagination cursor; `id` (string, **required**) — Product Hunt slug

### `producthunt_product`

- **HTTP:** `GET /producthunt/product/{id}`
- **What:** Retrieve Product Hunt product details. Returns the core Product Hunt product details. The path takes an exact Product Hunt slug; if you only know the product name, look the slug up first with `/producthunt/search` (live) or `/datasets/producthunt-products/search` (indexed). Unknown slugs return 404, and that 404 is cached for 24 hours.
- **Params:** `id` (string, **required**) — Product Hunt slug or numeric ID

### `producthunt_reviews`

- **HTTP:** `GET /producthunt/product/{id}/reviews`
- **What:** Retrieve Product Hunt product detailed reviews. Lists the detailed reviews of a Product Hunt product, looked up by its slug in `id`. Each review has its ratings, such as ease of use and customization, comment count, creation time, the launch it came from and any alternative products named. The response also gives the review counts and an `end_cursor`.
- **Params:** `id` (string, **required**) — Product Hunt slug

### `producthunt_search`

- **HTTP:** `GET /producthunt/search`
- **What:** Search for products, users, or launches on Product Hunt. Searches Product Hunt for the required `query`. `type` is `product` (default), `user` or `launch`, and `page` starts at 1. `featured` and `topics` apply to launch search only. Results come as `edges` with `pageInfo` and `pagesCount`; launch search also returns topic aggregations.
- **Params:** `featured` (boolean, optional) — Launch search only: featured launches only; `page` (integer, optional) — Page number (1-based); `query` (string, **required**) — Search keywords; `topics` (string, optional) — Launch search only: comma-separated topic slugs; `type` (string, optional) — Result type: **product** (default), **user**, or **launch**

## TrustMRR (7)

### `trustmrr_acquire`

- **HTTP:** `GET /trustmrr/acquire`
- **What:** Get TrustMRR acquisition listings. Returns the for-sale startups rendered on the public TrustMRR /acquire marketplace page, with deal metrics (asking price, revenue, multiple, growth). Verified revenue figures come from supported payment providers.
- **Params:** _none_

### `trustmrr_categories`

- **HTTP:** `GET /trustmrr/categories`
- **What:** Get TrustMRR categories. Lists the TrustMRR startup categories, with the total `count`. Each category has its `slug`, `label`, short label, icon name, description, keywords and TrustMRR URL. Pass a category `slug` to `/trustmrr/category/{slug}` to list the startups in it.
- **Params:** _none_

### `trustmrr_category`

- **HTTP:** `GET /trustmrr/category/{slug}`
- **What:** Get TrustMRR category detail. Returns one TrustMRR category by `slug` (lowercase letters, digits and hyphens, for example `saas`) with the startups listed in it. Each startup has its name, slug, URL, description, current MRR, total revenue and last-30-days revenue, all in USD, plus the `on_sale` flag for startups listed for sale. Valid slugs come from `/trustmrr/categories`.
- **Params:** `slug` (string, **required**) — TrustMRR category slug

### `trustmrr_leaderboard`

- **HTTP:** `GET /trustmrr/leaderboard`
- **What:** Get TrustMRR revenue leaderboard. Returns the top 100 startups ranked by the selected metric from the public TrustMRR leaderboard. Revenue and MRR figures are verified through supported payment providers.
- **Params:** `metric` (string, optional) — Leaderboard metric to rank by (default mrr)

### `trustmrr_marketplace`

- **HTTP:** `GET /trustmrr/marketplace`
- **What:** Get TrustMRR marketplace snapshot. Returns the public TrustMRR marketplace snapshot: the 25 most recently listed startups for sale and the current 25 best deals ranked by TrustMRR's recency-aware deal score. Revenue figures are verified through supported payment providers.
- **Params:** _none_

### `trustmrr_startup`

- **HTTP:** `GET /trustmrr/startup/{slug}`
- **What:** Get TrustMRR startup detail. Returns the full verified profile for a single TrustMRR startup by slug: revenue and MRR, growth, asking price and marketplace status, tech stack, marketing channels, and TrustMRR's AI-generated business summary.
- **Params:** `slug` (string, **required**) — TrustMRR startup slug

### `trustmrr_startups`

- **HTTP:** `GET /trustmrr/startups`
- **What:** List all TrustMRR startups. Returns a paginated list of every startup in the TrustMRR directory. Each entry is a slug you can pass to /trustmrr/startup/{slug} for the full verified profile — together these two endpoints let you enumerate the entire directory.
- **Params:** `page` (integer, optional) — 1-based page number (default 1); `page_size` (integer, optional) — Items per page (default 100, max 1000)

## Kickstarter (4)

### `kickstarter_comments`

- **HTTP:** `GET /kickstarter/comments`
- **What:** Get a Kickstarter campaign's comments. Returns the first page of one Kickstarter campaign's comments feed (Kickstarter's own server-rendered initial batch, typically 40-60 comments; total_count reports the feed's real total). Each comment includes the author, whether the author is the creator (a reply), the posted timestamp, and the comment text. creator and slug are the two path segments of the project URL, e.g. lookingglass and musubi for kickstarter.com/projects/lookingglass/musubi.
- **Params:** `creator` (string, **required**) — Creator path segment of the project URL; `slug` (string, **required**) — Project slug path segment of the project URL

### `kickstarter_discover`

- **HTTP:** `GET /kickstarter/discover`
- **What:** Browse or search Kickstarter's Discover surface. Returns one page of Kickstarter's own Discover results -- browse by category id and/or a free-text search term, sorted by magic/popularity/newest/end_date/most_funded, optionally filtered by campaign state and/or restricted to staff picks. Each result includes the campaign's funding snapshot (goal, pledged, percent funded, backers), category, location, creator, and cover photo.
- **Params:** `category_id` (integer, optional) — Kickstarter's own numeric category id (top-level or sub-category), e.g. 16 for Technology; `page` (integer, optional) — 1-based page number; `sort` (string, optional) — Result order; `staff_pick_only` (boolean, optional) — Restrict results to Kickstarter's own \; `state` (array, optional) — Repeatable campaign state filter; `term` (string, optional) — Free-text search query

### `kickstarter_project`

- **HTTP:** `GET /kickstarter/project`
- **What:** Get a Kickstarter campaign's detail. Returns one Kickstarter campaign's detail: funding snapshot (goal, pledged, percent funded, backers, state, dates), category, creator, cover photo, story text, risks & challenges, update/comment/FAQ counts, and reward/pledge tiers. creator and slug are the two path segments of the project URL, e.g. lookingglass and musubi for kickstarter.com/projects/lookingglass/musubi. Reward tiers are best-effort -- see the endpoint's documentation for when they may be omitted.
- **Params:** `creator` (string, **required**) — Creator path segment of the project URL; `slug` (string, **required**) — Project slug path segment of the project URL

### `kickstarter_updates`

- **HTTP:** `GET /kickstarter/updates`
- **What:** Get a Kickstarter campaign's updates feed. Returns one Kickstarter campaign's full updates feed: for each update, its number, title, author, whether the author is the creator, publish date, body text, and comment count. creator and slug are the two path segments of the project URL, e.g. lookingglass and musubi for kickstarter.com/projects/lookingglass/musubi.
- **Params:** `creator` (string, **required**) — Creator path segment of the project URL; `slug` (string, **required**) — Project slug path segment of the project URL
