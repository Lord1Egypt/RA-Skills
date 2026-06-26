# Reference: Endpoints

Concise overview of each Tavily endpoint. The agent reaches these either through MCP tools (`tavily_search`, `tavily_extract`, `tavily_crawl`, `tavily_map`) or via HTTP at `https://api.tavily.com/<endpoint>`.

- **Auth (HTTP):** `Authorization: Bearer <TAVILY_API_KEY>`. When using the `tavily-mcp` server, the key is injected by the server — the agent does not send it.
- **Method:** All operational endpoints below are HTTP **POST** with a JSON body, except `/usage` which is a read (GET).
- **Authoritative behavior:** see `SKILL.md`. This file elaborates only.

> Verification needed: confirm HTTP methods, paths, and exact request/response shapes with https://docs.tavily.com

---

## search — `POST /search`

- **Purpose:** Find relevant web results for a query, optionally with a synthesized answer and images. The primary operation for "find / look up / verify".
- **Key params:** `query` (required), `search_depth` (`basic`|`advanced`), `topic` (`general`|`news`), `days` (news look-back), `time_range` (`day`|`week`|`month`|`year`), `max_results` (0-20, default 5), `include_answer` (bool|`basic`|`advanced`), `include_raw_content` (bool|`markdown`|`text`), `include_images`, `include_domains[]`, `exclude_domains[]`.
- **Response shape:** `{ query, answer, images, results: [ { title, url, content, score (0-1), raw_content } ], response_time, request_id }`.
- **Credit cost:** basic ≈ 1 credit; advanced ≈ 2 credits.
  > Verification needed: confirm exact credit cost with https://docs.tavily.com

## extract — `POST /extract`

- **Purpose:** Retrieve clean full content from one or more **known URLs**. Use after you already have/were given URLs.
- **Key params:** `urls` (string or string[]), `extract_depth` (`basic`|`advanced`), `format` (`markdown`|`text`).
- **Response shape:** `{ results: [ { url, title, raw_content } ], failed_results, ... }`.
- **Credit cost:** scales with `extract_depth` and number of URLs; advanced costs more than basic.
  > Verification needed: confirm exact credit cost and per-call URL limits with https://docs.tavily.com

## crawl (beta) — `POST /crawl`

- **Purpose:** Follow links from a starting URL to gather many pages of a site (docs, knowledge bases).
- **Key params:** `url` (start), `max_depth` (hops to follow), `limit` (max pages), `instructions` (natural-language steering), path include/exclude filters.
- **Response shape:** `{ base_url, results: [ { url, raw_content } ], ... }`.
- **Credit cost:** scales with pages fetched and depth.
  > Verification needed: confirm crawl parameters, limits, and credit cost with https://docs.tavily.com

## map (beta) — `POST /map`

- **Purpose:** Discover a site's URL structure (link inventory) **without** fetching full page content. Cheaper than crawl; use it to plan selective extraction.
- **Key params:** `url` (start), depth/limit/path filters analogous to crawl.
- **Response shape:** `{ base_url, results: [ urls ], ... }`.
- **Credit cost:** lower than crawl since content is not downloaded.
  > Verification needed: confirm map parameters, limits, and credit cost with https://docs.tavily.com

## usage — `GET /usage`

- **Purpose:** Check account usage / remaining credits.
- **Key params:** none (auth identifies the account).
- **Response shape:** account usage / credit balance object.
  > Verification needed: confirm the /usage path and response shape with https://docs.tavily.com
- **Use it to:** decide whether to throttle, downgrade to `basic`, or stop when credits are low.

---

## Choosing an endpoint

| Need | Endpoint |
|---|---|
| Find pages for a question | search |
| Read content of URLs you already have | extract |
| Gather many pages across a site | crawl (beta) |
| Inventory a site's URLs cheaply, then fetch selectively | map (beta) → extract/crawl |
| Check remaining credits | usage |

Prefer the **narrowest** operation. On large sites, **map first, then extract** the few pages you need.
