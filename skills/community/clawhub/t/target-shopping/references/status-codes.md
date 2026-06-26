# HTTP status codes from the public-facing API

The shared client (`scripts/_common.py`) raises a `RuntimeError` (and the
script `c.fail()`s with structured JSON) on anything other than 200/206.

| Code | Meaning here | What to do |
| --- | --- | --- |
| 200 | OK | — |
| 206 | Partial Content. Returned as a normal success by `plp_search_v2` and friends, often with a non-fatal `errors` block in the JSON body (e.g. sponsored-search backend failed). | Treat as success. Inspect `errors[]` in the body if some fields are missing. |
| 400 | Bad request. Almost always: missing required param (`visitor_id`, `key`), unknown operation name, or wrong types. | Re-check `references/endpoints.md`. The error body usually names the field. |
| 403 | Blocked. IP throttled, behind a WAF, or missing Origin/Referer. | Slow down (`TARGET_MIN_INTERVAL=2`), set a real User-Agent, or back off entirely. |
| 404 | Not found. Bad TCIN or wrong operation path. | Verify the TCIN exists at `https://www.target.com/p/-/A-<tcin>`. |
| 410 | Gone. The operation was removed. Notably `pdp_fulfillment_v1`. | Use the replacement op (`fiats_v1` for fulfillment). |
| 429 | Rate limited. | Increase `TARGET_MIN_INTERVAL` (default `1.0` second). The client retries 5xx but **does not** retry 429 — back off and try again later. |
| 5xx | Upstream internal error. | The client retries up to 2 times with exponential backoff. If it persists, the API is having a bad day; try again in a few minutes. |

## Embedded GraphQL errors

A 200/206 response can still contain a partial-failure `errors` array at the
top level alongside `data`. Example: sponsored-search occasionally 400s
upstream, but the rest of the search response is fine. The skill's `trim()`
functions tolerate missing fields, so this usually surfaces as `null`s in
the trimmed output rather than a hard failure. Use `--raw` to inspect.
