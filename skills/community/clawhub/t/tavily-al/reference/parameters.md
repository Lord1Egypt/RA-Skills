# Reference: Parameters

All parameters across Tavily endpoints, with type, default, meaning, and guidance on when to change them. `SKILL.md` is authoritative; this elaborates.

> Verification needed: confirm parameter names, types, defaults, and value ranges with https://docs.tavily.com (especially beta crawl/map).

---

## search (`POST /search`)

| Parameter | Type | Default | Meaning | When to change |
|---|---|---|---|---|
| `query` | string | — (required) | The search query. | Always set. Keep it focused, keyword-rich, disambiguated (section 13 of SKILL.md). |
| `search_depth` | `basic` \| `advanced` | `basic` | Retrieval thoroughness. Advanced digs deeper at higher cost. | Use `basic` by default; switch to `advanced` only when basic results are weak or precision matters. |
| `topic` | `general` \| `news` | `general` | Search corpus / mode. | Use `news` for breaking/current events; otherwise `general`. |
| `days` | integer | provider default | News look-back window in days. Applies with `topic: "news"`. | Set for recent-news scoping (e.g. last 3-7 days). |
| `time_range` | `day` \| `week` \| `month` \| `year` | unset | Restrict results to a recent window. | Set when recency matters (prices, releases, "latest"). |
| `max_results` | integer (0-20) | 5 | Number of results returned. | Lower (3-5) for simple facts; raise (up to 10) for surveys. Avoid setting high "just in case". |
| `include_answer` | bool \| `basic` \| `advanced` | `false` | Return a synthesized answer in addition to results. | Use `basic`/`advanced` for a quick summary; keep `false` when you will synthesize and cite yourself. Always cite the underlying result URLs, not the answer blob. |
| `include_raw_content` | bool \| `markdown` \| `text` | `false` | Include full page text per result. | Leave off to save payload/cost; prefer a targeted `extract` when you need full text. |
| `include_images` | bool | `false` | Include image results. | Enable only when images are genuinely needed. |
| `include_domains` | string[] | unset | Restrict results to these domains. | Force authoritative/official sources; scope multi-vendor comparisons. |
| `exclude_domains` | string[] | unset | Drop these domains. | Remove known spam/low-quality sources. |

## extract (`POST /extract`)

| Parameter | Type | Default | Meaning | When to change |
|---|---|---|---|---|
| `urls` | string \| string[] | — (required) | One or more URLs to extract. | Batch multiple URLs in one call to save round-trips. |
| `extract_depth` | `basic` \| `advanced` | `basic` | Extraction thoroughness. | Use `advanced` for complex/heavy pages that return too little under `basic`. |
| `format` | `markdown` \| `text` | `markdown` | Output format of extracted content. | Prefer `markdown` (preserves structure); use `text` for plain content. |

## crawl (beta) (`POST /crawl`)

| Parameter | Type | Default | Meaning | When to change |
|---|---|---|---|---|
| `url` | string | — (required) | Starting URL. | Point at the relevant section root or homepage. |
| `max_depth` | integer | provider default | Link hops to follow from the start. | Keep small (1-2) to control cost/noise; raise only when needed. |
| `limit` | integer | provider default | Max pages to fetch. | Set conservatively to cap cost. |
| `instructions` | string | unset | Natural-language steering of which pages matter. | Use to focus the crawl on relevant content. |
| path include/exclude filters | string[] / patterns | unset | Restrict crawl to/from certain URL paths. | Stay within the relevant docs section; exclude noise. |

> Verification needed: confirm exact crawl parameter names, defaults, and limits with https://docs.tavily.com

## map (beta) (`POST /map`)

| Parameter | Type | Default | Meaning | When to change |
|---|---|---|---|---|
| `url` | string | — (required) | Starting URL. | Point at the site/section root. |
| depth/limit/path filters | as crawl | provider defaults | Bound the traversal. | Keep conservative; map is for inventory, not content. |

> Verification needed: confirm exact map parameter names, defaults, and limits with https://docs.tavily.com

## usage (`GET /usage`)

No request parameters; the API key identifies the account.

---

## Quick defaults the agent should assume

- `search_depth` / `extract_depth`: **basic**.
- `topic`: **general** (switch to **news** for current events).
- `max_results`: **3-5**.
- `include_answer`, `include_raw_content`, `include_images`: **off** unless needed.
- crawl/map `max_depth` and `limit`: **small/conservative**.
