---
name: unusual-options-activity
description: "Unusual options activity radar for US stocks and ETFs: end-of-day IV rank, implied volatility, options sentiment, put/call percentile, 25-delta skew, open-interest walls, and max pain, each ranked against the ticker's own trailing history. Use for unusual options activity, options flow scanner, IV rank, implied volatility, options sentiment, put/call ratio, max pain, open-interest walls, spotting where options positioning is stretched for a ticker. Read-only. No trading, no purchases, no write operations, no wallet access."
homepage: https://sentisense.ai
primaryEnv: SENTISENSE_API_KEY
metadata:
  openclaw:
    primaryEnv: SENTISENSE_API_KEY
    envVars:
      - name: SENTISENSE_API_KEY
        required: false
        description: "SentiSense API key, optional to install. Get one free at https://app.sentisense.ai/get-api-key, or with no key follow the No key yet steps in the 0-sentisense-onboarding skill for a temporary free one with no signup. Used only to authenticate read-only data calls; no write or trading scope."
---
# Options Radar (SentiSense)

Read the options market for US stocks without pulling and cleaning a full option chain yourself. This skill turns each session's chain into a small set of end-of-day analytics through the read-only SentiSense API, and it ranks every reading against that stock's own trailing history rather than against other stocks. You get a market-wide radar of the most interesting names, and a per-stock dossier covering IV rank, put/call percentile, 25-delta skew, open-interest walls, max pain, and the session's unusually active contracts.

Read-only educational data interface. Output is informational context about how a chain looks today versus its own past, never a personalized buy or sell recommendation, and never a forecast.

## When to Use

Reach for this skill when the question is about options positioning or activity on a stock:

- "Any unusual options activity in $NVDA today?" (unusually active contracts, ranked by premium)
- "Where is implied volatility for this name relative to its own range?" (IV rank)
- "Is the options market leaning puts or calls here?" (put/call ratio and its percentile)
- "What is the downside skew on $TSLA?" (25-delta put-minus-call skew and its percentile)
- "Where are the open-interest walls and max pain?" (strike structure for the dossier expiry)
- "Which stocks have the most stretched options readings right now?" (the market-wide radar board)
- "How did call and put volume build through today's session on $NVDA?" (the intraday history, one point per 15-minute cycle: PRO, or a free key on a sample company)

This skill pairs naturally with `stock-sentiment`, `politicians-stock-tracker`, and `institutional-13f-tracker`: the strongest reads come from convergence. Rich call activity that lines up with climbing sentiment, a congressional buy, and institutional accumulation on the same ticker is a story; any one signal alone is noise.

Do not use it for order entry, portfolio management, greeks-based hedging, or personalized advice. It has no write, trading, or wallet surface; every endpoint is a GET.

## What this data actually is (read before interpreting)

Options data is easy to over-read. Four things to hold onto:

- **It is end-of-day, not real-time.** Each reading describes the latest published snapshot, and `asOf` names its session: quote it. The snapshot refreshes each weekday evening after the close (the run starts about 21:15 ET), so after successful publication `asOf` is that day's session, and between the close and that refresh it is still the previous session. Follow-ups compare the next session's open interest and remain pending until that chain is observed. On weekends and holidays `asOf` is the latest completed session. This is not an intraday tape, so it does not classify sweeps or blocks and it does not stream live prints; the intraday readings are a 15-minute delayed count and percentile (see "Intraday session fields" below) plus, on PRO, the per-session `intraday-history` series of volumes and `atmIv`; each carries its own timestamp and can describe a later session than `asOf` in the same response. "Unusually active contracts" means the session's volume ran far above standing open interest, which is a fresh-positioning signal, not a live order-flow feed.
- **Percentiles are the point, not the raw levels.** A put/call ratio of 0.9 or an IV of 45% means little on its own. Every reading is served next to its rank within the ticker's own trailing window (a percentile for put/call and skew, a min-max range position for IV rank), so "put/call volume at the 92nd percentile of its 1y range" is the actual signal: unusual *for this specific name*. Lead with the ranked context, not the raw number. Units: IV and the expected moves are fractions (`atmIv` 0.3124 is 31.24%), `skew25d` is an IV difference in the same fraction units (0.0293 is 2.93 percentage points), and ranks and percentiles run 0 to 100.
- **Coverage is two bounded universes.** Stocks: more than 1,100 of the most actively optioned US names (the number moves as the universe is rebuilt), reported in the overview's `coverageCount`, which is the number to quote rather than any figure written here. The `rows` of `/options/overview` are the authoritative list. ETFs: covered funds are served on the same `/stocks/{ticker}/options/...` paths, and on the radar they are a SEPARATE board, `etfRows`, never mixed into `rows`. The full overview's `etfRows` is the authoritative fund list: `GET /api/v1/etfs` lists every fund SentiSense tracks, a wider set, and a tracked fund without an options snapshot returns `data: null` from `/summary`. A free key receives only the top 25 ETF rows, so absence from that slice does not establish noncoverage. `coverageCount` counts stocks only. Rank the two boards independently: every reading is a percentile of that ticker's own history, so an ETF's `interestScore` compares to other ETFs, not to a single stock. A ticker in neither universe returns `200` with `data: null` (summary) or an empty `series` (history). Treat a null as "not covered", not as an error.
- **Building baseline is not zero.** A covered ticker with too little history (`observations1y` under 60 sessions) returns its raw readings with the percentiles and `interestScore` omitted while its baseline accrues. A ticker with a full history can still be unscored when its latest session fell below the liquidity floor ($100,000 of estimated premium activity, `notionalVol`). Report a missing percentile or score as unavailable, never as a low reading, and call it a building baseline only when `observations1y` is low.

## Prerequisites

- A free `SENTISENSE_API_KEY`. Get one at https://app.sentisense.ai/get-api-key. The key is required on every call; anonymous requests return `401 api_key_required`. No key yet? Follow "No key yet" in the `0-sentisense-onboarding` skill: one POST returns a temporary free key the agent can use right away and a link the user opens to keep it.
- Any HTTP client. Plain `curl` works, or Python 3.8+ using only the standard library (`urllib`, `json`); no third-party packages required. On macOS python.org installs can raise `CERTIFICATE_VERIFY_FAILED` (missing CA certs): run the bundled `Install Certificates.command`, use the system `/usr/bin/python3`, or use `curl`.
- Network access to `https://app.sentisense.ai`.
- Read-only scope. Every endpoint here is a GET. Nothing this skill does can place a trade, move money, or modify account state.

## Permissions

- Network: HTTPS to app.sentisense.ai only.
- Credentials: SENTISENSE_API_KEY from the environment.
- Shell: none required.
- Files: none.

| Tier | Request quota | Rate | Options data |
|------|---------------|------|--------------|
| Free | 1,000 requests/month | 30 requests/min | Radar: top 25 rows plus every market-pulse aggregate. Per-stock dossier: full detail for the first 10 calls each calendar month, then a headline-only preview. History: `1y` window. Intraday history: not available (preview with `data: null`). Sample companies: full dossier, any history window and the intraday history. |
| PRO ($15/mo) | Unlimited | 300 requests/min | Full radar board, unlimited full dossiers, and history windows up to `5y` (2+ years available, from July 2024, growing daily), and the per-session intraday history. |

The free tier exercises every workflow below on real data, with one limit: the walls and the unusual-contract list (Workflow 3) come only with a full dossier, so on a free key they last as long as the month's ten full dossiers do. Full data on a set of sample companies is free: their `/summary`, history and intraday history come back in full on a free key, marked `sampleCompany: true`, and a sample company's dossier never spends one of the ten. Read the list from `upgrade.sampleTickers` on an options preview, or see https://sentisense.ai/docs/api/#full-sample-responses-with-a-free-key. Every other covered `/summary` call spends one of the ten full dossiers, repeat calls for the same ticker included, and calls made earlier in the month on the same account count too, so branch on `isPreview` rather than counting calls yourself. On a free key every covered summary also returns `dossierAllowance` `{ limit, remaining, resetsAt }` beside `data`: `remaining` is the full dossiers left after that call and `resetsAt` is the reset moment in epoch seconds, so you can tell your user "7 full dossiers left this month" or when the preview lifts. Another request on the same account can spend the count before your next call, so `isPreview` stays the branch. Uncovered tickers that return `data: null` never spend the monthly dossier meter. The dossier allowance and the monthly request quota reset at the start of the first day of each calendar month, Eastern time (America/New_York).

## How to Run

Issue HTTP GET requests to `https://app.sentisense.ai` and synthesize the JSON into a concise, sourced answer. Authenticate every request with the `X-SentiSense-API-Key` header; keep the key in the shell environment and never place it in a query string or in user-facing output.

The options endpoints return the wrapped envelope `{ isPreview, previewReason, data }`; `GET /api/v1/etfs` and the name resolver below return bare arrays. When `isPreview` is `true` (`previewReason: "PRO_REQUIRED"`), say so ("showing the free preview slice"). Inside `data`, unavailable nested metric fields are omitted rather than sent as `null`, but envelope fields can be an explicit `null` (`previewReason` on a full response, `data` for an uncovered ticker), and so can the resolver's `ticker`: handle absent and `null` alike. Two distinct `429` responses exist: a per-minute `rate_limit_exceeded` includes a `Retry-After: 60` header, so wait that long before retrying; a monthly `quota_exceeded` carries no `Retry-After` header and does not clear until the next calendar month, so stop calling rather than retrying.

```python
import os, json, urllib.parse, urllib.request

API_ORIGIN = "https://app.sentisense.ai"

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def sentisense_api_url(path):
    url = urllib.parse.urljoin(API_ORIGIN + "/", path)
    parsed = urllib.parse.urlparse(url)
    if (parsed.scheme != "https" or parsed.hostname != "app.sentisense.ai"
            or parsed.netloc != "app.sentisense.ai"
            or parsed.username is not None or parsed.password is not None
            or parsed.port is not None):
        raise ValueError("API URL must use https://app.sentisense.ai with no credentials or port")
    return url

def get(path):
    url = sentisense_api_url(path)
    req = urllib.request.Request(
        url,
        headers={"X-SentiSense-API-Key": os.environ["SENTISENSE_API_KEY"]},
    )
    with urllib.request.build_opener(NoRedirect).open(req) as r:
        return json.load(r)

board = get("/api/v1/options/overview")
data = board.get("data")  # None before the first nightly build
rows = (data or {}).get("rows", [])
```

The REST recipe in this file is the primary path. A maintained command-line client is available as the separate `sentisense-cli` skill for hosts that prefer one.

**Company and fund names are not tickers.** When the user names the company or the fund ("unusual activity in tesla", "skew on the S&P 500 ETF") instead of typing a symbol, resolve it first: `GET /api/v1/kb/entities/search?q={name}&type=company&limit=5`, or `type=etf` for a fund (`SPY` resolves only under `etf`, never under `company`). The response is a bare array of `{name, urlSlug, type, ticker}`, best match first; take the first match with a non-null `ticker` (a tracked subsidiary can outrank its listed parent: "google" returns Google LLC with `ticker: null` before Alphabet `GOOGL`), ask a one-line clarification when several plausible matches carry tickers, and say so when the array is empty. Never uppercase the name into a symbol: `/stocks/TESLA/options/summary` answers `200` with `data: null`, which reads like an uncovered name when the real failure was the identifier. An exact ticker the user typed skips this step.

## Endpoints

- **`GET /api/v1/options/overview`** : the market-wide radar, one row per covered stock in `rows` plus the ETF board in `etfRows` (same row shape, omitted when a build has none), plus a few market-pulse aggregates (`asOf`, `medianIvRank`, `marketPcVol`, `extremeCount`, `coverageCount`). Rows arrive ranked by `interestScore` descending, so the top of the list is the most interesting names; unscored rows sort last. Free keys receive the top 25 rows plus `totalCount`; PRO keys receive every row. Every row carries `ticker`, `name`, `sector`, `asOf`, `notionalVol`, `observations1y` and `unusualCount`; nearly every row also carries `atmIv` and `skew25d` (a handful without a valid at-the-money reading omit both) and, when `atmIv` is valid, the expected-move set: `expectedMove1d`/`expectedMove5d`/`expectedMove20d`, a calibrated 90% range, and `expectedMove1s1d`/`expectedMove1s5d`/`expectedMove1s20d`, the one-sigma convention (`atmIv * sqrt(h / 252)`), all fractions of price over 1, 5 and 20 trading sessions. A row's own `asOf` can be a session behind the board's `asOf`; quote the row's `asOf` and say so when the two differ. **The rest are sparse, and the sparse ones are exactly the fields worth sorting on**, because a row only carries them when that reading exists for the ticker: on a full board of 1,028 rows measured 2026-09-05, `ivMove20` appeared on 1,020, `pcVol` on 950, `ivRank1y` and `skewPctl1y` on 943, `interestScore` on 870, `sentiment` and `pcVolPctl1y` on 865, `maxVolOiRatio` and `maxUnusualPremium` on **189**, and `wallSide` / `wallStrike` / `wallShare` on **31**. Since unavailable row fields are omitted from the JSON entirely, a re-sort of the board by premium or by wall is ranking the 18% and the 3% of rows that have one, not the board. Treat an absent field as "no reading for this ticker", never as a zero or a low value: say how many rows carried it when you rank on one, and do not describe a wall board of 31 names as the market's heaviest walls. The same response carries `highlights` (stocks) and `etfHighlights` (ETFs): each ticker's highest-premium qualifying contract of the latest completed session with an expiry at least one day out (same-day expiries are not eligible; a contract more than 20% in the money, measured as the gap between strike and underlying price as a share of the underlying price, is passed over whenever the ticker has another eligible one, so a deep in-the-money highlight means nothing else qualified), one per ticker, up to 10, ranked by `premiumPctl1y` (that premium against the ticker's own previous 252 sessions; omitted while the baseline builds). Free keys receive the top 3 of each. Each list carries its own stamp, `highlightPolicy` for `highlights` and `etfHighlightPolicy` for `etfHighlights`: read a list under that rule only when its own stamp is `ex0dte-v1`, since an absent stamp means that list was built under the older rule, which allowed same-day expiries.
- **`GET /api/v1/stocks/{ticker}/options/summary`** : the latest dossier for one stock. `data` is `null` for uncovered or unknown tickers (which never spend the dossier meter), otherwise `{ asOf, sentiment, latest, context, oiWalls, unusual }`. Free keys receive this full dossier for the first 10 calls each calendar month; after that, `data` is a headline-only preview of `{ asOf, sentiment, ivRank1y, atmIv, expectedMove1d, pcVol, pcVolPctl1y, maxPain }`, plus the intraday session fields below when present, with `isPreview: true` until the monthly reset. Free-key summaries for covered, listed tickers, full or preview, carry `dossierAllowance` `{ limit, remaining, resetsAt }` on the envelope beside `data` (`limit` is 10; `remaining` is 0 on the last full dossier and on every preview; `resetsAt` is Unix epoch seconds, rounded down to the second); PRO keys, delisted tickers and null summaries omit it. `latest` is the aggregate for the returned `asOf` session (volumes, open interest, `pcVol`/`pcOi`, `vwIv`, `atmIv` plus the `atmIv60`/`atmIv90` term structure, `iv25c`/`iv25p`, `skew25d`, `netDelta`, `notionalVol`, `contracts`). `context` holds `ivRank1y` (a min-max range position, 0-100) plus the percentile readings (`pcVolPctl1y`, `pcVolPctl5y`, `pcOiPctl1y`, `skewPctl1y`) and `observations1y`. `oiWalls` holds `expiry`, `maxPain`, and up to three `callWalls` / `putWalls` `{ strike, oi }` levels. `unusual` is the top 5 contracts by premium, each `{ contract, type, strike, expiry, dte, volume, oi, volOiRatio, premium, oiPrior, oiNext, oiChange, oiConfirmation, oiObservedAt, oiVintage }`; the oi-prefixed fields are the open-interest follow-up described below.
- **`GET /api/v1/stocks/{ticker}/options/history`** : the daily aggregate time series, ascending by date, `{ ticker, window, series }`. Each `series` element has the same shape as `latest`. `window` is `1y` (default), `2y`, or `5y`; `5y` returns the available history within that window (2+ years, from July 2024, growing daily), not a guaranteed five years. Free keys receive `1y` regardless of the requested value, except on a sample company, which gets the window requested; the response's `window` field reports what was actually served.
- **`GET /api/v1/stocks/{ticker}/options/intraday-history?session=YYYY-MM-DD`** (PRO, or a free key on a sample company; free keys on any other ticker get the preview with `data: null`): one session's intraday series for a stock or ETF, `{ ticker, session, live, delayMinutes, cycles, missingCycles, series }`, one `series` point per 15-minute board cycle that carried the ticker, oldest first, each `{ cycle, asOf, asOfEt, callVol, putVol, pcVol, unusualCount, maxPremiumPctl1y, atmIv }`. A full session is 27 cycles, about 09:45 to 16:15 ET (`asOfEt` is the build stamp and can read 10:14 or 16:14), from 15-minute delayed chains; `asOf` is epoch seconds, `callVol` and `putVol` are running contract counts for the session so far (not dollars), and `pcVol` is `putVol / callVol`. Without `session` it serves the most recent session the board ran; a malformed or future `session` returns `400 invalid_session`. The history is forward-only: the first stored session is 2026-10-15, and an earlier session returns an empty `series` with `cycles: 0`, so never describe that as a quiet day. `series` can be shorter than `cycles` when the ticker was off the board for some cycles (the gaps show in `cycle`), and an empty `series` with `cycles` above 0 means the ticker was never on that session's board or is not covered: it says nothing about volume, so never call it a quiet day. `unusualCount` is capped at 5, so a flat 5 means at least 5. `missingCycles` (omitted when there are none) lists cycles with no stored history at all, whose numbers are unknown, not zero, so say so when a chart crosses one. `maxPremiumPctl1y` is omitted until the ticker's intraday baseline holds 60 sessions, so expect it absent on most tickers for the first months. The series carries no contract, strike, premium, open interest or print size. Its `atmIv` uses a stricter rule than the end-of-day `atmIv`, so treat the two as related series, not interchangeable values. The overview's `intradayAsOf` / `intradayAsOfEt` date the board behind `intradayActiveCount` and `intradayRanking` and are omitted with them, the normal state outside the session. `live` is `true` only for today's session between 09:40 and 16:20 ET; `capabilities.intradayBoard.apiData: false` refers to the contract-level board rows, not to this series.

**Intraday session fields.** On a trading day the app runs an intraday options board, rebuilt every 15 minutes from 15-minute delayed chains, and publishes the session's large prints after the close. On the API the intraday session is a count and a percentile on `/summary` and `/overview`, and a volume series on `/intraday-history`; the contract-level board is in the app. `/summary` adds `intradayFlow` (`unusualCount`, contracts on the ticker's row passing the unusual rule so far, up to 5; `firstSeenEt` and `firstSeenAt`, the earliest cycle that flagged one; `flowPctl1y`, the ticker's intraday highlight against its own history, omitted while that baseline holds fewer than 60 sessions; `asOfEt`, `asOf` in epoch seconds, `live`, `delayMinutes`), plus `largePrintCount` (the ticker's large prints in the latest published post-close session, up to 25) and `largestPrintPctl` (the highest percentile among them). `/overview` adds `intradayActiveCount` (stocks with at least one unusual contract so far) and `intradayRanking` (up to 25 of them as an array of ticker symbols, ordered by each ticker's own-year percentile where one exists and otherwise by the size of its largest flagged contract; it carries no per-ticker score, so take numbers from each ticker's `/summary`). Both carry `capabilities.intradayBoard`, which describes the board, not data: `apiData: false` means its rows are app-only, `access` is `signed_in_pro` or `power_user` (an early-access group), and `url` opens it. The fields are the same on every tier, previews included, carry no contract, strike, price or premium amount, and are omitted before the day's first board.

## Workflows

**1. Scan the radar for stretched names**

**Identify your client.** Send a `User-Agent` naming your agent runtime and this skill, for
example `OpenClaw/1.4 (unusual-options-activity)` or `ClaudeCode/2.1 (unusual-options-activity)`. Substitute your own runtime and
version if neither matches. You can also volunteer what your agent is called by adding an
`agent/<your-agent-name>` token inside the same parentheses, as in
`OpenClaw/1.4 (unusual-options-activity; agent/research-desk)`. All of it is optional, and it is what tells
us this skill has real integrations behind it, so it gets prioritized and you get notice before it
changes.

```bash
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/options/overview"
```
Rows are pre-ranked by `interestScore`. Lead with the top few by that score, and show each one's `notionalVol` beside it: a scored row traded at least $100,000 of premium that session, so a stretched reading near that floor is still thin activity and should be labeled as such. Then re-sort client-side for a specific lens: `notionalVol` for "most active by premium", `abs(ivMove20)` for "biggest IV moves", or `pcVolPctl1y` for the most put-heavy names. Always report the percentile alongside the raw reading, and skip rows where `interestScore` is omitted (unscored: a building baseline or a session below the liquidity floor).

To filter the whole universe by IV rank, unusual premium or expected move rather than read the radar board, use the `stock-screener` skill and its curated "High IV Rank" and "Unusual Premium + Bullish" screens.

**2. Read one stock's options dossier**

```bash
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/stocks/TSLA/options/summary"
```
Summarize in percentile terms: where `atmIv` sits in its 1y range (`ivRank1y`), whether `pcVol` is high or low for this name (`pcVolPctl1y`), and which way `skew25d` leans (positive means puts bid richer than calls, a downside-demand tilt). Note `maxPain` and the nearest walls as context for the dossier expiry, not as targets. If `context` percentiles are missing, report them as unavailable, and as a building baseline only when `observations1y` is low. If `isPreview` is `true` instead, the free monthly dossier meter is spent: only the headline fields are present, so summarize those and say the full dossier needs PRO or the next monthly reset (give the date from `dossierAllowance.resetsAt` when it is present), rather than reading the missing sections as a data gap. On a full free dossier, mention `dossierAllowance.remaining` once so the user knows how many full reads are left this month; when `sampleCompany` is `true`, say instead that the read was free because the ticker is a sample company and spent none of them.

**3. Spot unusually active contracts**

```bash
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/stocks/TSLA/options/summary" | python3 -c "
import sys, json
j = json.load(sys.stdin)
d = j.get('data')
if j.get('isPreview'):
    print('PREVIEW: the unusual list is withheld on the free headline preview (needs PRO or the monthly reset)')
elif d is None:
    print('NOT COVERED: data is null for this ticker')
else:
    print(json.dumps(d.get('unusual', []), indent=2))
"
```
On an `isPreview: true` response the `unusual` key is absent because the section is withheld, not because the session had no unusual contracts: never report "no unusual activity" from a preview. Say the list needs a full dossier, and use the preview's `largePrintCount` only for what it is, a count of large prints in the latest published post-close session, capped at 25. The `unusual` list is contracts whose session volume ran far above open interest (`volOiRatio`), ranked by dollar `premium`. A high ratio on a short-dated contract is often event-driven, so quote the `dte` and let the reader weigh it. This is end-of-day activity, so describe it as "unusually active in the last session", not as a live sweep. Each contract also carries an open-interest follow-up once the next session's open interest has been read: `oiConfirmation` is `opened` (open interest rose by at least half the session's volume), `closed` (it fell by at least a quarter of it), `mixed`, `pending`, or `unmatched` (not in the next chain). `pending` supports no conclusion about the next session's open interest yet. A contract that expired on the flagged session is never in the next chain, so it resolves `unmatched` and cannot show a position carried overnight. To follow up after the dossier rolls forward, keep the `contract` id and the session's `asOf`: the resolved follow-up lands on that date's `/options/history` row as `unusualOi`, one entry per contract. Report the numbers: "open interest rose by 3,100 (62% of that session's volume)", "fell by 900", or "changed little (+40)". These net changes do not establish trade composition; buyer or seller not identified. `oiObservedAt` is UTC epoch seconds and `oiVintage` is `prior_settle`, `settled`, or `next_session`.

**4. Chart how a reading has trended**

```bash
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/stocks/TSLA/options/history?window=1y"
```
Pull `atmIv`, `pcVol`, or `skew25d` out of `series` to show the trend behind today's percentile. A free key gets `1y` on every ticker except a sample company; the `window` field confirms what was served.

**5. Follow the convergence.** When rich call activity or a low put/call percentile lines up with climbing sentiment (`stock-sentiment`), a congressional buy (`politicians-stock-tracker`), or institutional accumulation (`institutional-13f-tracker`) on the same ticker in the same window, that agreement is the read worth surfacing. Say so explicitly, cite each source, and note when the dots disagree (for example, bullish flow against a put-heavy skew) rather than forcing a clean story.

## Answering well

- **Lead with the percentile.** "IV rank 74 (elevated for this name)" carries the signal; the bare 53% IV does not. Do the same for put/call and skew.
- **Say end-of-day.** Frame every reading as the session its `asOf` names, except the intraday session fields: quote those with their clock and the delay ("3 unusual contracts on NVDA as of 14:30 ET, 15-minute delayed"). Never imply real-time flow, live sweeps, or intraday order tape, and never name the contracts behind a count the API does not list.
- **Do not overstate structure.** Max pain and open-interest walls are descriptive magnets and context, not predictions of where the stock will close. `netDelta` is the chain's aggregate net delta exposure (open-interest-weighted), not an inference about dealer books and not a gamma or hedging figure.
- **Respect the baseline.** If percentiles or `interestScore` are omitted, report them as unavailable rather than reading them as a zero or a bearish signal, and say history is still accruing only when `observations1y` is low.
- **Report only what the API returns.** Do not infer greeks, dealer gamma, or intentions the data does not contain, and do not frame any of it as advice. Options carry a high level of risk; this is derived analytics for education.

## Going further

Free covers every workflow above except `intraday-history`, which is PRO only outside the sample companies: the top of the radar, ten full dossiers a month, and a year of history. **PRO ($15/mo)** lifts the monthly request cap (no monthly limit, just a 300/min rate), returns the full radar board and unlimited full dossiers, and deepens history, plus sentiment, smart-money flows, insider detail, and AI insights across the rest of the SentiSense API. Apply coupon `AGENTS` at checkout for a builder launch discount: https://app.sentisense.ai/pricing?coupon=AGENTS. A preview response's `upgrade` object may carry a different current code in its `url`; either code works, and when that object is present, relay its `price` and `url`.

**ClawHub Skill:** [clawhub.ai/TheSentiTrader/unusual-options-activity](https://clawhub.ai/TheSentiTrader/unusual-options-activity)

---

*SentiSense is a read-only financial intelligence API. Options analytics here are derived, end-of-day, and for informational and educational purposes only, not investment advice. Options carry a high level of risk.*
