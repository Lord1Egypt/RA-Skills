# Slack thread export notes

## Preconditions

- The Slack tab must already be attached via Browser Relay.
- The target tab must be a logged-in Slack workspace tab.
- The export script relies on Slack web client local state (`localConfig_v2`) plus the logged-in browser session.
- This skill assumes the operator is allowed to inspect/export the Slack data they are requesting.

## Why browser-context fetch matters

Direct host-side requests with only the xoxc token can fail with `invalid_auth`.
Calling `fetch('/api/search.messages', ...)` inside the attached Slack page context is more reliable because the browser session supplies the same cookies/session state the Slack web app already uses.

## Common failure modes

- `invalid_auth`: wrong tab, logged-out tab, or trying host-side requests instead of page-context fetch
- `ratelimited`: query too broad or requests too fast; back off and split by channel/date
- browser evaluate timeout: too many pages/channels in one giant evaluate; keep calls short and page-by-page

## Practical thresholds

These are operational heuristics, not guaranteed platform limits:

- Request size: `count=100` rows per page call
- Normal pacing: `0.5s` sleep between page calls
- Ratelimit retry: `3-5s` sleep before retrying the same page
- Good first pass: `1 user × 1-5 channels × <=20 pages`
- Heavy but workable: `1 user × <=10 channels × page-by-page`
- High risk: one evaluate that loops many channels and many pages in one browser call

If you need broad history, use more channels **serially**, not more work inside one evaluate.

## Safe narrowing strategy

1. Start with a channel whitelist.
2. Add `after:YYYY-MM-DD` and `before:YYYY-MM-DD` for large exports.
3. Run `--preflight` first when channel size is unknown.
4. Export raw JSONL first.
5. Apply work-related filtering after collection.
6. If the run fails partway, retry only the channels listed in `--failed-channels-out` or resume with `--resume-from-jsonl`.

## Practical retry pattern

Recommended sequence after a partial run:

1. Inspect `summary.json` for completed vs failed channels.
2. Re-run only the failed channels.
3. Keep the original raw JSONL and pass it via `--resume-from-jsonl` on retry.
4. Write retry failures to a new file so repeated retries stay narrow.

This keeps retries cheap and avoids re-fetching channels that already succeeded.
