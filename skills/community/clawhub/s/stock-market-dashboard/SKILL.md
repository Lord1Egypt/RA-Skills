---
name: stock-market-dashboard
description: "Build a stock market dashboard as a single self-contained HTML file you can open in a browser. Generates a morning market briefing from live data: a fear-to-greed market mood gauge with its component signals, sentiment breadth, sector heat, the biggest 7-day SentiSense Score shifts, an options radar, a watchlist with sentiment scores and analyst consensus, insider cluster buys, congressional trades, institutional flows, overnight story clusters, and the week's earnings calendar. No backend, no build step, no dependencies, one file. Use for \"build me a stock market dashboard\", \"make a stock dashboard html\", \"morning market briefing\", \"watchlist dashboard\", \"daily market report\". Read-only. No trading, no purchases, no write operations, no wallet access."
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

# Market Dashboard: build a real one as a single HTML file

> Turn live market data into a morning desk note you can open in a browser. One self-contained
> HTML file: no backend, no build step, no dependencies, no deploy. Fear-to-greed market mood and
> its component signals, sentiment breadth, sector tone, the biggest 7-day Score shifts, an options
> radar ranked against each name's own history, your watchlist, insider and congressional and
> institutional position changes, overnight stories ranked by impact, Street rating moves, and the
> week's earnings. Read-only API.

**Base URL:** `https://app.sentisense.ai`
**Website:** https://sentisense.ai
**Full API reference:** https://sentisense.ai/skill.md
**Authentication:** API key via `X-SentiSense-API-Key` header. Get a free key at https://app.sentisense.ai/get-api-key. No key yet? Follow "No key yet" in the `0-sentisense-onboarding` skill: one POST returns a temporary free key the agent can use right away and a link the user opens to keep it.

## Permissions

- Network: HTTPS to app.sentisense.ai only.
- Credentials: SENTISENSE_API_KEY from the environment.
- Shell: none required.
- Files: writes one HTML file the user names.

---

## What this skill is

A recipe, not a template. You fetch real data and **write the HTML yourself**, fresh each time.
Nothing here ships a prebuilt app the user has to clone, configure or maintain, and that is the
point: the file is disposable because regenerating it is cheaper than updating it.

**The output contract, which is the part that matters:**

1. **One file.** Everything inline: CSS in a `<style>` block, any JS in a `<script>` block, no CDN
   links, no external fonts, no image URLs. It must render correctly with no network access.
2. **It opens by double-clicking.** No server, no `npm install`, no build.
3. **Data is baked in at generation time.** The file is a *snapshot*, not a live view. Say so in
   the footer with the generation timestamp, or a reader three days later will think it is current.

If the user asks for something live and interactive that updates on its own, this is the wrong
shape and you should say so rather than quietly producing a stale-by-design file.

---

## The calls

Fetch everything first, then write the file once. Do not interleave writing and fetching, or you
will end up hand-patching a half-written document.

| Section | Endpoint |
|---|---|
| Market mood + signals | `GET /api/v2/market-mood?days=30` |
| Sector tone vs market | `GET /api/v1/sentiment/sectors` |
| Sentiment breadth | `GET /api/v1/sentiment/breadth` |
| Score shifts, 7-day movers | `GET /api/v1/trackers/sentiment-movers` |
| Options radar | `GET /api/v1/options/overview` |
| Insider cluster buys | `GET /api/v1/insider/cluster-buys` |
| Congressional trades | `GET /api/v1/politicians/activity` |
| Institutional net flows | `GET /api/v1/institutional/flows` |
| Overnight stories | `GET /api/v1/documents/stories` |
| Street rating changes | `GET /api/v1/analyst/activity?actionTypes=UPGRADE,DOWNGRADE,INITIATE&lookbackDays=1` (`3` on a Monday) |
| Earnings this week | `GET /api/v1/calendar/earnings?week=this` |
| Latest price (15-minute delayed), per ticker | `GET /api/v1/stocks/{ticker}/quote` |
| **SentiSense Score**, per ticker | `GET /api/v2/metrics/entity/{ticker}/metric/sentisense?startTime={epochMs30dAgo}` |
| Sentiment polarity, per ticker | `GET /api/v2/metrics/entity/{ticker}/metric/sentiment` |
| Analyst consensus, per ticker | `GET /api/v1/analyst/{ticker}/consensus` |

A five-ticker watchlist plus the market-wide sections is 31 calls: 11 market-wide plus 4 per
ticker. On PRO run them concurrently. A free key allows 30 requests a minute, so cap concurrency
or spread the calls over more than a minute, and on a `429 rate_limit_exceeded` wait for the
`Retry-After` seconds before retrying.

**Parameter details that are not optional, each of which silently degrades the page if you drop
it:**

- **`sentisense` and `sentiment` are different metrics on different scales.** `sentisense` is the
  SentiSense Score, which is unbounded and centred on 0; single-day readings on heavily discussed
  names pass plus or minus 40, so scale the diverging bar to the values you fetched rather than to
  a fixed range. `sentiment` is polarity, bounded to [-1, 1]. Every threshold in this skill (the
  diverging bar, the strong-regime band) is on the Score scale. Feed it polarity and every one of
  them is wrong by two orders of magnitude: nothing ever clears them, and the page silently
  renders every name as unremarkable. Fetch both if you render both columns.
- **Metric calls default to a 7-day window.** The 30-day average this page leads with does not
  exist in that response. Pass `startTime` as epoch millis 30 days back, or you are averaging a
  week and calling it a month.
- **`days=30` on market mood, not `days=7`.** Below roughly two weeks of history the API returns
  `weeklyChange: null` and a `null` `change` on every one of the six signals, so the trend arrows
  the layout depends on all disappear.
- **`actionTypes` and `lookbackDays` on analyst activity.** The bare call is mostly reiterations,
  which are not rating changes, so without the `actionTypes` filter the "Street moves" section is
  padding. The window matters as much: `lookbackDays` defaults to 30, it counts back that many
  calendar days from today in US Eastern time with today included, and rows arrive newest first,
  50 to a page. A call without it therefore fills the panel from the last several sessions, which
  is not "today". For the latest session's moves pass `lookbackDays=1` from Tuesday to Saturday,
  `2` on a Sunday and `3` on a Monday, each of which reaches back to the last weekday session.
  Size the panel from `totalCount` rather than a fixed row count: a quiet session leaves only a
  handful of real changes, and that is the data, not a broken call. Label the dates you show.
- **`week=this` on the earnings calendar.** Without a window the calendar returns the whole
  forward window on PRO (about two months, hundreds of events), which a heading of "Earnings this
  week" would misdescribe. `week=this` is the Monday-to-Sunday week containing the current US
  Eastern date on every tier, and `metadata.windowStart` / `metadata.windowEnd` echo the dates, so
  put them in the section heading. Generating on a weekend for the week ahead, ask for
  `week=next` and title the section for that week.
- **Drop rating-change rows whose grades did not move.** `actionType` comes from the research
  provider and is not cross-checked against `fromGrade` and `toGrade`, so a few rows a week arrive
  as an `UPGRADE` with identical grades, or an `INITIATE` that still carries a `fromGrade`. In a
  dense dashboard row that renders as "UPGRADE Buy to Buy", which reads as a bug in your dashboard.
  Filter to rows where `fromGrade != toGrade` before rendering the transition, and keep the
  unfiltered count if you also show a total.

Several v1 endpoints wrap the payload as `{ isPreview, previewReason, data }`; read `data`. The
movers, options, insider, politicians, flows, analyst and earnings calls all do. Market mood,
sectors, breadth, stories, quote and the metrics endpoints return their payload directly.

**On a free key some panels are previews, and a preview is a slice, not the window.** When a
response carries `isPreview: true` and a `totalCount` larger than the rows you received, you have
the top or newest few, not everything: currently 5 rows for insider cluster buys and congressional
trades, 5 per side for institutional flows, and the top 25 for the options radar. Label each such
panel with what it is ("newest 5 of 1,774 congressional trades, free preview") and never write
absence from a slice: no "no cluster buying", "Congress is quiet" or "nothing unusual in options"
while `totalCount` says there is more. A preview whose `totalCount` equals its rows is complete,
as the `week=this` calendar is on every tier. The analyst consensus preview keeps
`consensusLabel`, the target band and `numberOfAnalysts` but serves the five rating counts as `0`
and `recommendationMean` as `null`. Those zeros are withheld, not a survey with no ratings, so on
a preview drop the buy/hold/sell distribution and the "rated" count from the watchlist row rather
than printing "0 rated".

**Identify your client.** Send a `User-Agent` naming your agent runtime and this skill, for
example `OpenClaw/1.4 (stock-market-dashboard)` or `ClaudeCode/2.1 (stock-market-dashboard)`. Substitute your own runtime and
version if neither matches. You can also volunteer what your agent is called by adding an
`agent/<your-agent-name>` token inside the same parentheses, as in
`OpenClaw/1.4 (stock-market-dashboard; agent/research-desk)`. All of it is optional, and it is what tells
us this skill has real integrations behind it, so it gets prioritized and you get notice before it
changes.

```bash
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v2/market-mood?days=30"
```

**Ask for the watchlist if the user did not give one.** Do not invent tickers. If they want a
default, say you are picking one and name the tickers.

---

## Layout

Top to bottom. The order is the argument: market state frames everything below it, the user's own
names come next, and the calendar is context rather than headline.

1. **Masthead.** Name it like a desk note, not a report. The week it covers, the generation
   timestamp, whether it is pre-open or post-close.
2. **Market state**, three columns: the mood hero with its phase, the six component signals as
   thin bars, and all eleven sectors ranked by tone *relative to the market* (`consensusVsMarket`,
   with `consensusLabel` as the wording). Sector tone is market-relative on purpose, because news
   tone skews positive as a genre and an absolute number would read bullish everywhere.
3. **Sentiment breadth** as a single stacked strip: bullish, neutral, bearish share plus net
   breadth against a month ago. Breadth is what confirms or denies the composite, so it sits
   directly beneath it.
4. **The divergence callout, when the signals genuinely disagree.** The most valuable paragraph on
   the page. When Risk Appetite is greedy while Social Momentum is fearful, that gap *is* the read
   and a composite alone hides it. **Skip it entirely when nothing diverges. Do not manufacture
   tension.**
5. **Score shifts**: the biggest 7-day moves, warming and cooling. This tracker ranks by its
   `Score change (7d)` metric: the name's 7-day average SentiSense Score minus its 30-day average,
   so it measures how far the last week has pulled away from the month. It is not a change in
   tone and not a change since seven days ago. Rows carry `category` (`improving` or
   `deteriorating`), the 30-day average Score where one exists (`SentiSense Score`) with its band
   (`Score tone`), and polarity columns (`Sentiment now`, `7d ago`, `Change (7d)`). Label the
   section as Score shifts. If you show the polarity change beside it, name it as a separate measure, because the
   two can disagree in sign: a name can lead the warming list while its tone fell. A leaderboard
   is static and a delta is actionable, so prefer movers over top-N.
6. **Options radar**: names at extremes of *their own* IV rank and put/call history, not absolute
   levels. Absolute IV just re-sorts the same volatile names every day.
7. **Watchlist**: price, score with a diverging bar, today, sentiment, analyst consensus, and a
   "watch for" note carrying each name's top signal. The note is the reason to read the row.
8. **Filings and flows**: insider cluster buys, congressional trades, institutional net flows.
   Position *changes*, never a static holder list, which changes nobody's morning.
9. **Overnight, ranked by impact**: the top story clusters with their impact score and sentiment.
   **The endpoint returns latest-first, not impact-first. Sort by `impactScore` yourself** or the
   heading is a lie and the lead story is merely the most recent one.
   A morning read with no narrative is a spreadsheet.
10. **Street moves**: real rating changes only, reiterations excluded. Disagreement is the signal;
    lead with any same-day upgrade and downgrade on one name.
11. **Earnings week**, compressed to a handful of names per day with per-day counts.
12. **Footer**: how to read the score, per-field freshness, the absent-vs-zero note, and the
    disclaimer. All four required.

**The inclusion bar for any section: would a professional change their behaviour because of it?**
A price the reader can get anywhere fails. A divergence, an anomaly, a position change or an
unusual filing passes.

**Convergence is worth calling out and worth wording carefully.** When independent sources line up
on one name (an insider cluster buy, a congressional purchase, and a positive score), say so as an
*observation* and explicitly not as a signal. That framing is not decoration, it is the line
between research and advice.

---

## Design

One surface, restrained ink, color only where it carries meaning. Note there is no "raised" step:
the page sits directly on the validated chart surface and nothing is boxed on top of it.

```
--bg:#0d1117    --track:#1b2330
--line:rgba(255,255,255,.06)   --line2:rgba(255,255,255,.13)
--ink:#e8edf4   --ink2:#9daaba  --ink3:#66738a
--bull:#2e9d75  --bear:#e05c4a  --flat:#6b7280   --data:#3182ce
--gold:#D4A843  (brand chrome only, never a data series)
```

Hairline borders as translucent white rather than a solid grey step: they recede correctly at any
surface lightness and never read as a box edge.

That bull/bear/data trio is validated for colorblind separation against this dark surface, so
substitute at your own risk. The usual finance red-green pairing is one of the worst possible
choices for deuteranopia; the green here is pushed toward teal specifically to survive it.

**Calm and dense are not opposites, but you have to earn both.** What makes a dense page read calm
is mechanical, not a matter of taste:

- **Delete the boxes.** Cards inside cards are the single biggest source of visual noise. Let the
  page sit on one surface and separate sections with a micro-label, a hairline and generous space
  (about 50px), not with borders.
- **Let type carry hierarchy.** A serif for the masthead, callouts and story headlines against a
  sans with tabular numerals for every figure. Two weights is enough. A large light hero number
  reads calmer than a bold one.
- **Ration the color.** Bull and bear belong on *text and thin fills*, never on filled panels or
  pills. A tinted panel is just another box. Reserve the accent for one or two rules on the page.
- **Whitespace is the instrument.** If it feels crowded, the fix is space, not smaller type.

Rules that keep it readable:

- **Never encode by color alone.** Every colored chip also carries its label as text. A red chip
  says "Decreased", it does not just look red.
- **Tabular numerals** (`font-variant-numeric:tabular-nums`) on every numeric column, or the digits
  jitter between rows and the table looks broken.
- **Give bars a `min-width` of about 4px.** A genuine reading of 0.9 on a 100-point scale renders
  as nothing at all and is indistinguishable from missing data. A visible stub is honest; an empty
  track is not.
- **A diverging bar needs a visible midpoint.** A score centered on zero is drawn from the centre
  outward, with a 1px centre line, not as a left-anchored fill.
- **Recessive grid, thin marks, no gradients on data.** Gradients belong on the mood scale, which
  is a legend, not on anything a reader has to compare.

---

## Honesty rules, all five load-bearing

**1. Label freshness per field, because it varies inside one row.** Prices are 15-minute delayed,
not live: annotate them with `priceAsOf` where the payload carries it. `priceAsOf` is omitted
outside regular hours, so a pre-open brief labels the price by session ("last close") rather
than by the response `timestamp`, which is the time it was served. Scores, sentiment and
signals come from the latest analytical batch and are older still. A 13F quarter that is still
filing shows early filers only, so positions will grow. Earnings dates are curated and unconfirmed
ones shift. Putting a price next to a batch score with no note invites the reader to diff them and
conclude something is broken.

**2. A zero is not a missing value, and it fails in both directions.** The **SentiSense Score**
(`metric/sentisense`, not `metric/sentiment`) is centred on zero, so a same-day `0.0` can be a
genuine neutral or a day on which nothing was measured. Decide from the day's own sample, which
every Score point carries under `metricValue.properties`: `bull`, `bear`, and `directional`
(their sum).

```
no point for the day, or directional == 0   ->  ABSENT, render "no reading"
value == 0.0  AND  bull == bear > 0          ->  REAL, render 0.0
```

Both halves are load-bearing, and each corresponds to a real row:

- A name averaging about 7 over 30 days that reports `today 0.0` with `directional 0` had no
  bullish or bearish analyses that day. Rendering 0.0 prints a neutral nobody measured.
- A name averaging about 10 that reports `today 0.0` with 14 bullish and 14 bearish analyses is a
  **measured neutral**: a balanced day, not a gap. Suppressing it invents a hole.

Do not use the 30-day average as the test. A quiet day and a balanced day for the same name look
identical through it, so any threshold on it either suppresses genuine neutrals or keeps holes.
The last point can be the current day so far, so early in the day `directional 0` means no
reading yet. Rendering an absent value as zero on a zero-centered scale is unfalsifiable by the
reader: they cannot tell a real neutral from a gap. Inventing a gap is equally unfalsifiable.
Decide from the counts, not by eye.

**3. The score is a nowcast, not a forecast.** It reads how bullish or bearish the market currently
is on a stock, weighted by how actively it is discussed. It does not predict price. Never label it
a buy signal, a target, or a prediction, and do not build a "top picks" section out of it.

**4. Do not narrate a partial sample.** The 13F flows endpoint returns `isPending` plus a
`filerCount` / `baselineFilerCount` pair while the quarter is inside the 45-day filing window. At
that point you are looking at a **fraction of filers, and early filers are not a random sample of
late ones.** Report the numbers, state the coverage as a percentage, and stop. Do not write the
sentence explaining what the pattern means.

The tell that you have crossed the line is a clause like "X are net sellers of Y", "the smart money
is rotating out of Z", or any sentence where a partial dataset acquires a motive. **Direction is
reportable from a partial sample. Magnitude and intent are not.** This is the single easiest way to
turn a correct dashboard into a wrong one, because the numbers stay right while the sentence
underneath them goes wrong.

Same discipline applies anywhere coverage is incomplete: a still-filing quarter, a curated calendar
with unconfirmed dates, an options radar built from one session's chains.

**5. Every dashboard carries a disclaimer.** Not optional and not a footnote in 9px grey:

> Not investment advice. Generated from public and licensed market data for research and
> educational purposes only. Not a recommendation to buy or sell any security, and it does not
> account for your circumstances, objectives or risk tolerance.

---

## Reading the numbers

- **SentiSense Score.** Centered on zero. Negative is bearish, positive is bullish, and readings
  beyond about plus or minus 23 are strong. Show the 30-day average and today's value together:
  the gap between them is the story, and "warming" or "cooling" describes that gap.
- **Market Mood.** 0 to 100, fear to greed. Bands: 0-15 Extreme Fear, 16-30 Fear, 31-45 Anxiety,
  46-55 Neutral, 56-70 Optimism, 71-85 Greed, 86-100 Extreme Greed.
- **Risk Appetite is inverse VIX.** A *high* value means a calm, risk-on market. This one reads
  backwards from what people expect, so label it in the tooltip.
- **Social Momentum and Options Flow describe the previous session** (a Monday row describes
  Friday); the other four signals describe the row's own date. Say so when they diverge from them.
- **Analyst counts do not reconcile, and that is correct.** The price-target population and the
  buy/hold/sell survey are different samples. Report "58 analysts" against the target band and
  "61 rated" against the distribution rather than forcing them to match. On a free-key preview
  the distribution is withheld (see the preview note under the calls), so show the label and the
  target band only.

---

## Extending it

Natural additions once the base page works, each one more call and one more section: options
positioning and IV rank, congressional and insider trades on the watchlist names, news stories per
ticker, a sentiment leaderboard of the most bullish and bearish names. Add them as sections in the
same file rather than splitting into multiple pages.

For "show the broader market", hand off to the `market-heatmap` skill when available. Pass the desired scope, metric, and watchlist context. Return a market treemap with coverage and as-of labels. Hand off only when the user changes the question; do not automatically route back. If the sibling is unavailable, answer the supported part here using a connected tool or the inline REST workflow, state any remaining gap, and never require an install.


**Keep it one file.** The moment it needs a bundler it stops being the thing that makes this
useful, which is that anyone can generate one, email it, and have it open on the other end.

## Delivering the file

The file lands on the machine the agent runs on, which is not always the machine the user is
looking at. Before presenting a path as if it were clickable, say where the file lives and how to
open it: on a local desktop surface, the absolute path plus "open it in your browser" is enough;
on a hosted or chat surface (a web chat talking to a remote host), a bare local path is not
retrievable by the user, so offer a real delivery route instead: the host's file/attachment
mechanism if it has one, serving the file briefly over a local port you name explicitly (state
which machine "localhost" refers to), or pasting the HTML for the user to save. If the host
offers a render surface for HTML documents (a canvas or render-only preview panel), presenting
the dashboard there is a good fit, because this file is a self-contained static snapshot by
design; check that the capability is actually connected before promising it. Treat such a
surface as display, not interaction: a panel that renders HTML may not run scripts or accept
input, and this dashboard is built to be read either way.

For example, OpenClaw's canvas node is such a surface: it renders the file well, and on some
surfaces it is render-only, which this snapshot is designed for. Since OpenClaw 2026.8.1 the
same host offers a better route: the `show_widget` tool takes the finished page as
`widget_code` with a short `title`, renders it inline in the chat, and with `pin: true` plus a
stable `name` (use `market-dashboard`) places it on the session dashboard, where it survives
`/new` and `/reset`. A later call with the same `name` replaces it in place, which is how the
next morning's note supersedes today's without another file. Pick a large `size` (`xl` or
`full`) and keep the page under the 262,144-character limit inline clients enforce. Inline
widgets are sandboxed (inline style and script allowed, no external loads, no network), which
this no-network file already satisfies. Do not declare `capabilities.netOrigins` for it: the
agent fetches the data with the key in its own environment and renders a snapshot, so the
widget never needs the API origin or the key, and it works under every session permission
mode. Check that the tool is present before promising it; when it is not, the canvas or the
file route above still applies.
