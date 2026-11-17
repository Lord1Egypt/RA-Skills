# substack-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**19 endpoints across 1 platform group(s).**

## Substack (19)

### `substack_categories`

- **HTTP:** `GET /substack/categories`
- **What:** List Substack categories. Returns every public Substack category, with the category id required by /substack/category. Ids span two spaces: 32 categories use a numeric id and one uses the string id `podcast`. Both are accepted by /substack/category.
- **Params:** _none_

### `substack_category`

- **HTTP:** `GET /substack/category`
- **What:** List the publications ranked in one Substack category. Returns one page of a category's public publication leaderboard. Each row carries the publication's subscriber signals and its full subscription offering (web plans with multi-currency pricing, App Store plans, and per-tier benefits). Subscriber totals are published to roughly three significant figures and are opt-in per writer; paid subscriber figures are only ever buckets. Upstream serves 25 publications per page and accepts pages 0-26, so at most 675 publications are reachable per category and type.
- **Params:** `category_id` (string, **required**) — Category id from /substack/categories. Numeric for 32 categories, or the string podcast.; `page` (integer, optional) — Zero-based page, 0-26; `type` (string, optional) — Ranking to read

### `substack_explore`

- **HTTP:** `GET /substack/explore`
- **What:** Browse the public Substack Explore surface. Returns one page of Substack's Explore surface. Explore is a feed of heterogeneous modules rather than a flat list, so each page returns the modules it contains and every module names its own type. Known module types are `trendingTopicsExplore` (trending topics and suggested searches), `trendingPostsExplore`, `newBestsellersExplore`, `videoSuggestionsExplore`, `categoryLeaderboard`, `comment` (a single Note) and `post` (a single post). Only the collections a module actually carries are populated. Pagination is cursor-based; early pages are curated shelves and later pages are individual Notes and posts.
- **Params:** `cursor` (string, optional) — Opaque cursor from a previous response's next_cursor; `tab` (string, optional) — Explore tab id from the tabs endpoint with surface=explore; `type` (string, optional) — Tab type

### `substack_leaderboard`

- **HTTP:** `GET /substack/leaderboard`
- **What:** List a Substack category's bestseller leaderboard. Returns one page of a category's bestseller leaderboard, pairing each ranked publication with its author. This is a different surface from /substack/category: it exposes the trending ranking (the site's "Rising" tab), validates its ranking values rather than silently defaulting, accepts the extra cross-category id `bestseller`, and returns the author alongside the publication. Use a category_id from /substack/categories whose in_leaderboard is true. Upstream serves 25 rows per page and accepts pages 0-25.
- **Params:** `category_id` (string, **required**) — Category id from /substack/categories with in_leaderboard true. Numeric, or the string ids podcast or bestseller.; `page` (integer, optional) — Zero-based page, 0-25; `type` (string, optional) — Ranking to read

### `substack_note`

- **HTTP:** `GET /substack/note`
- **What:** Get one public Substack Note. Returns one public Note with its author, engagement counts, and the post it links to when it has one. Notes are Substack's short-form social posts. note_id is the numeric id from a Note URL: in `/@handle/note/c-316240438` it is `316240438`.
- **Params:** `note_id` (integer, **required**) — Numeric Note id

### `substack_note_replies`

- **HTTP:** `GET /substack/note/replies`
- **What:** List replies to a Substack Note. Returns one page of public replies to a Note, each in the same shape as /substack/note. Pagination is cursor-based: pass the previous response's next_cursor back as cursor.
- **Params:** `cursor` (string, optional) — Opaque cursor from a previous response's next_cursor; `note_id` (integer, **required**) — Numeric Note id

### `substack_note_restacks`

- **HTTP:** `GET /substack/note/restacks`
- **What:** List the Notes that restacked a Substack Note. Returns one page of the Notes that restacked a given Note, each in the same shape as the single-Note endpoint. A restack may carry its own commentary in `body` or be a bare reshare with an empty body. Pagination is cursor-based.
- **Params:** `cursor` (string, optional) — Opaque cursor from a previous response's next_cursor; `note_id` (integer, **required**) — Numeric Note id

### `substack_notes`

- **HTTP:** `GET /substack/notes`
- **What:** Browse the public Substack Notes feed. Returns one page of the public Notes feed for one tab. tab and type come as a pair from the Notes feed tabs endpoint. Pagination is cursor-based: pass the previous response's next_cursor back as cursor. Post-only rows in the upstream feed are omitted; every returned row is a Note.
- **Params:** `cursor` (string, optional) — Opaque cursor from a previous response's next_cursor; `tab` (string, optional) — Feed tab id from the Notes feed tabs endpoint; `type` (string, optional) — Tab type from the Notes feed tabs endpoint

### `substack_notes_tabs`

- **HTTP:** `GET /substack/notes/tabs`
- **What:** List the Substack feed tabs. Returns every selectable tab for one surface. The two surfaces expose different tab sets: `feed` has 34 tabs (the main feed, the bestseller feed, and one per category) and `explore` has 33. Each row's id and type must be passed together to the matching feed endpoint, which rejects a tab whose type does not match.
- **Params:** `surface` (string, optional) — Which surface's tabs to list

### `substack_post`

- **HTTP:** `GET /substack/post`
- **What:** Get one public Substack post. Returns one public post with the extended metadata the archive listing omits, including word count, every credited byline, and podcast audio details where the post has them. Post bodies are not returned.
- **Params:** `publication` (string, **required**) — Publication subdomain or custom domain; `slug` (string, **required**) — Post slug, the trailing path segment of the post URL

### `substack_publication`

- **HTTP:** `GET /substack/publication`
- **What:** Get a Substack publication and its subscription offering. Returns a publication's public profile and its complete subscription offering: every purchasable web plan with per-currency pricing, the separately priced App Store plans, per-tier benefit copy, and the toggles governing which tiers are sold. Identify the publication by name (a subdomain such as semianalysis, or a custom domain such as www.thefp.com) or by numeric publication_id -- exactly one is required. Prefer publication_id when you have it: it reads a compact document, while resolving by name has to parse the publication's full homepage.
- **Params:** `publication` (string, optional) — Publication subdomain or custom domain. Provide this or publication_id.; `publication_id` (integer, optional) — Numeric publication id. Cheaper than resolving by name. Provide this or publication.

### `substack_publication_contributors`

- **HTTP:** `GET /substack/publication/contributors`
- **What:** List a Substack publication's public contributors. Returns one page of the writers credited on a publication, ranked as Substack ranks them. Rows include each writer's handle, profile URL, and bestseller badge tier, so a publication can be fanned out into individual /substack/user lookups. Large publications return several hundred contributors on the first page.
- **Params:** `page` (integer, optional) — Zero-based page; `publication` (string, **required**) — Publication subdomain or custom domain

### `substack_publication_posts`

- **HTTP:** `GET /substack/publication/posts`
- **What:** List a Substack publication's public post archive. Returns one page of a publication's public post archive with title, subtitle, canonical URL, publish date, engagement counts, and whether each post is paywalled. search filters the publication's own posts full-text; a query with no matches returns an empty list rather than the unfiltered archive.
- **Params:** `limit` (integer, optional) — Rows per page, 1-50; `offset` (integer, optional) — Zero-based row offset; `publication` (string, **required**) — Publication subdomain or custom domain; `search` (string, optional) — Full-text filter over the publication's own posts; `sort` (string, optional) — Archive ordering

### `substack_publication_recommendations`

- **HTTP:** `GET /substack/publication/recommendations`
- **What:** List the publications one Substack publication recommends. Returns the publications a given publication recommends to its own readers, as a publication-to-publication graph. Useful for discovering publications beyond the 675-per-category ceiling on /substack/category. publication_id is the numeric id returned by /substack/publication, /substack/category, or /substack/user.
- **Params:** `publication_id` (integer, **required**) — Numeric publication id

### `substack_search`

- **HTTP:** `GET /substack/search`
- **What:** Search posts and publications across Substack. Searches posts across all of Substack and returns the publications that also matched, unlike /substack/publication/posts which searches within a single publication. Set focus_publication_id to additionally receive that one publication's own matching posts in focused_posts alongside the site-wide results.
- **Params:** `focus_limit` (integer, optional) — Cap on focused_posts, 1-20. Requires focus_publication_id.; `focus_publication_id` (integer, optional) — Numeric publication id whose own matching posts are returned in focused_posts; `page` (integer, optional) — Zero-based page, 20 posts per page; `query` (string, **required**) — Search text

### `substack_user`

- **HTTP:** `GET /substack/user`
- **What:** Get a public Substack writer profile. Returns one public Substack profile: identity, the publications the writer contributes to, their publicly visible subscriptions, and every subscriber signal Substack publishes. total is opt-in per writer and rounded to roughly three significant figures; when a writer hides it, total_hidden is true and total is 0, which must not be read as zero subscribers. paid_rough, paid_rough_int, and paid_tier are buckets - no exact paid subscriber count is published anywhere. follower_count is exact but counts followers, not subscribers.
- **Params:** `handle` (string, **required**) — Substack profile handle

### `substack_user_activity`

- **HTTP:** `GET /substack/user/activity`
- **What:** List a Substack user's public activity. Returns one page of a user's public activity: the notes they wrote, posts they published, and items they liked, replied to, or restacked. types is an optional comma-separated filter accepting `note`, `post`, `like`, `replies` and `restack`; omit it for the default mixed feed. Each item's kind is the upstream's own finer-grained label, so filtering on `restack` returns both `comment_restack` and `post_restack` items. Pagination is cursor-based.
- **Params:** `cursor` (string, optional) — Opaque cursor from a previous response's next_cursor; `types` (string, optional) — Comma-separated activity kinds: note, post, like, replies, restack; `user_id` (integer, **required**) — Numeric user id from the user endpoint

### `substack_user_connections`

- **HTTP:** `GET /substack/user/connections`
- **What:** List a Substack user's followers, following, or subscribers. Returns one of a user's public connection lists. Each entry is a full profile in the same shape as /substack/user, subscriber signals included. user_id is the numeric id returned by /substack/user. The upstream returns a bounded preview of each list rather than the complete membership.
- **Params:** `list` (string, optional) — Which list to read; `user_id` (integer, **required**) — Numeric user id from /substack/user

### `substack_user_search`

- **HTTP:** `GET /substack/user/search`
- **What:** Search public Substack writer profiles. Searches public Substack profiles by name or handle. Each result carries the same subscriber signals as /substack/user, so a search enumerates writers without a second lookup per profile. Returns 20 profiles per page; use has_more rather than assuming a fixed depth, since result counts vary by query.
- **Params:** `page` (integer, optional) — Zero-based page; `query` (string, **required**) — Search text matched against profile names and handles
