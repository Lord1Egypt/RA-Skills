# Failure modes

Both endpoints echo `error_code` (mirroring the HTTP status), `error_msg`, and `search_id` in the body. Log `search_id` on every call - it is the reference Querit support traces.

## 400 - malformed request

The body reached the server and was rejected. `error_msg` names the field, e.g. `Invalid time range option` for a `timeRange.date` that does not match the accepted forms. Fix the payload; retrying is pointless.

## 401 - the header or the key

Confirm the `Bearer ` prefix and that the env var actually reached the process. A key exported in one shell is not visible to a service started in another, and a `.env` that is loaded by the dev server may not be loaded by a worker or a cron job.

## 403 - entitlement, not a bad credential

Usually per-endpoint subscription. Search and contents are subscribed separately, so a working search key can return `No active contents subscription. Please subscribe to the contents plan to use this API.` on `/v1/contents`. Read `error_msg` before sending the user to check their key. When designing a search-then-contents pipeline, confirm the key covers both endpoints first.

## 429 - QPS

Plan-dependent and lower than most people expect. Batch work needs a client-side limiter, not just retries - retries alone convert a rate problem into a slower rate problem with more failed calls. Retry 429 and 5xx with exponential backoff and jitter; never retry other 4xx.

## Timeouts

On `/v1/contents`, a slow page is a `crawlTimeout` matter reported in `statuses[]`, not a transport failure. A client-side timeout below `crawlTimeout` aborts requests the server would have completed, which shows up as an intermittent, URL-dependent failure.

## 200 with nothing useful

Check the shape before blaming relevance:

- Empty `results.result` is a real no-hit. Narrow `filters` are the usual cause - especially a `timeRange` window with no coverage, or a `sites.include` list the query does not match. Re-run without `filters` to separate the two.
- A missing `sentence` on some results is expected: `needContent` returns text only where it was available. Missing from every result in the response points at the account lacking the page-text option.
- An empty `content` on `/v1/contents` means the crawl failed, not that the page was blank - cross-check the entry's `statuses[]` status, and treat a requested URL that appears in neither array as a failure too. Recording either as an empty document turns a fetch failure into a silent quality problem. `contents-api.md` has the join.

## Isolating the layer

Run `scripts/querit_smoke.py` with the same key and a trivial query before debugging through the application stack. If the smoke test succeeds and the app fails, the credential and the endpoint are fine and the problem is in the app's request construction, environment, or network path.
