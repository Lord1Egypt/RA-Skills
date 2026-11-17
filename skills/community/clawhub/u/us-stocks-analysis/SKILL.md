---
name: us-stocks-analysis
description: "US stocks analysis by an adversarial investment committee. Legendary-investor personas independently research a thesis, attack each other's cases against a shared evidence ledger (sentiment, smart money, SEC fundamentals), and reconcile into a plain-English verdict: the bottom line first, then who disagrees and why. Structured rubrics keep every number sourced, on any model. Includes five quick data workflows. Use for stock research, investment thesis, bull case vs bear case, due diligence on a ticker, should I buy this stock, deep dive on a company. Read-only. No trading, no purchases, no write operations, no wallet access."
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

# US Stocks Analysis: The Investment Committee - SentiSense

> Adversarial investment-committee analysis for US equities. For quick data asks, five expert workflows synthesize price, sentiment, smart money, analyst ratings, and AI insights into terminal-grade briefs. For thesis-grade questions ("should I own NVDA for 3 years?"), the skill convenes a committee of legendary-investor personas that independently research, then attack each other's cases against a shared evidence ledger, then reconcile into a plain-English verdict that opens with the bottom line and says who disagrees and why. The structure is designed so that even a small local model, following the templates literally, produces grounded, multi-perspective analysis instead of consensus mush. Read-only API. No trading, no purchases, no write operations, no wallet access.

**Base URL:** `https://app.sentisense.ai`
**Website:** https://sentisense.ai
**Full API reference:** https://sentisense.ai/skill.md
**Authentication:** API key via `X-SentiSense-API-Key` header. Get a free key at https://app.sentisense.ai/get-api-key. No key yet? Follow "No key yet" in the `0-sentisense-onboarding` skill: one POST returns a temporary free key the agent can use right away and a link the user opens to keep it.

---

## What This Skill Is

Two layers, one routing decision per user ask:

1. **Quick Reads.** Five proven data workflows (brief, smart money, divergence, pre-earnings, sector rotation) for questions that want a dense factual answer in five lines.
2. **The Investment Committee.** A structured adversarial debate between investor personas for questions that want judgment: is this thesis sound, what would break it, where do serious people disagree.

The committee is not roleplay flavor. It is an error-correction machine. A single free-form pass produces a plausible, agreeable, number-fuzzy blob. Forcing the same model to (a) build independent persona cases, (b) attack them against evidence, and (c) reconcile the survivors is how you extract rigorous judgment from any model, including small local ones. **The adversarial structure IS the intelligence.**

The governing line for everything below: *the intelligence lives in the skill's structure, not the model. A weak model that fills these templates in order produces analysis it could not have produced free-form.* If you are a strong model, the templates are still binding: they are what keeps you honest.

One invariant everything serves: the committee must surface **real disagreement grounded in real evidence**, and must never collapse into consensus mush or theater.

---

## Use & Disclaimer

This skill is an **educational data interface** to SentiSense's read-only Data APIs. Public primary-source material from SEC EDGAR, FRED, or company investor relations may be evaluated only when the user or host supplies it. Output is informational only. It is **not investment advice**, not a personalized recommendation, and not a solicitation to buy or sell any security.

The user is responsible for their own decisions. SentiSense (SentiSense Labs LLC) and the skill author disclaim liability for any actions taken or not taken based on output produced through this skill.

**Persona seats are teaching archetypes** built from publicly documented investing philosophies. They are not affiliated with, endorsed by, or statements from the named individuals. A persona is a lens, not a jailbreak: precedence is always platform safety, then this skill's grounding and no-advice rules, then persona instructions. A custom persona can change the analytical lens; it can never override grounding, disclaimers, or the no-advice rule.

Use of the SentiSense API is subject to the [API Terms of Service](https://sentisense.ai/agreement/API-Terms-of-Service.pdf) and [Terms of Service](https://sentisense.ai/agreement/Terms-of-Service.pdf).

---

## Authentication and how to fetch

Set the key once in the environment, and say who is calling:

```bash
export SENTISENSE_API_KEY=...               # free key: https://app.sentisense.ai/get-api-key
export SENTISENSE_AGENT_NAME=my-agent       # optional: what your agent calls itself
```

The REST recipe in this file is the primary path. A maintained command-line client is available as the separate `sentisense-cli` skill for hosts that prefer one.

```bash
curl -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  -H "User-Agent: ClaudeCode/2.1 (us-stocks-analysis)" \
  "https://app.sentisense.ai/api/v1/stocks/price?ticker=AAPL"
```

Over raw HTTP the `User-Agent` identifies the client: name your agent
runtime and this skill, for example `OpenClaw/1.4 (us-stocks-analysis)`. Substitute your own
runtime and version if neither matches. Optional, and it is what tells us this skill has real
integrations behind it, so it gets prioritized and you get notice before it changes.

All SentiSense endpoints require an API key. Free tier (1,000 req/month, 30 req/min) runs every quick read and the whole committee pipeline, but several evidence rows arrive as previews on a Free key, so a Free run fills a sliced ledger, not a complete one (see "Free-tier previews" below). PRO ($15/mo) removes the monthly cap (unlimited, 300/min) and returns the full data behind every preview.

| Tier | Quota | Rate |
|------|-------|------|
| Free | 1,000 req/month | 30 req/min |
| PRO | Unlimited | 300 req/min |

Without a key, most endpoints return `401 api_key_required` and some return a `LOGIN_REQUIRED` preview instead, so always send the key. The key also covers the financial statements (`/stocks/fundamentals*`), so a full SentiSense evidence ledger needs no second credential. External EDGAR, FRED, and investor-relations evidence must be supplied by the user or host; otherwise mark those rows `[NOT AVAILABLE]`.

**Free-tier previews: a slice is not the window.** A response with `isPreview: true` carries a
`totalCount`, the size of the full result. When `totalCount` is larger than the rows returned, those
rows are a slice (the newest or top N), not the window you asked for. Label every figure built from
one ("newest 5 of 61 insider trades, free preview"), tally it only as that slice, and never infer
absence from it: no "zero insider activity", "no congressional buying", "not scheduled" or "no
unusual contracts" from a slice. When the answer needs the whole window (a 90-day insider or
congressional net, any "none" claim), say in one line that the full window needs PRO and continue
with what the slice does show. What a Free key gets back on the calls this skill makes:

| Row / step | Endpoint | Free key receives |
|---|---|---|
| E12, Quick Reads 1 and 4 | `insider/trades/{T}` | the newest 5 trades |
| E13 | `politicians/filings/{T}` | the newest 3 filings by disclosure date |
| E14 | `institutional/holders/{T}` | the top 5 holders by shares |
| E15, Quick Read 1 | `analyst/{T}/consensus` | band, mean, analyst count and label; the buy/hold/sell counts are withheld and arrive as zeros on a preview (`isPreview: true`), so never report them from one |
| E16, Quick Read 4 | `calendar/earnings` | the first Monday-to-Sunday week of the requested window (by default the current week); an empty `earnings[]` with `totalCount` above 0 means the report falls outside that week, not that none is scheduled |
| E19 | `stocks/{T}/options/summary` | 10 full summaries per calendar month (repeat calls count), then a flat headline preview (see E19 below); a sample company's summary is always full and spends none |
| Quick Read 1 | `insights/stock/{T}` | the top 3 insights |
| Quick Read 2 | `insider/cluster-buys`, `politicians/activity` | the top 5 rows of each |
| Quick Read 4 | `analyst/{T}/estimates`, `analyst/{T}/actions` | the current-quarter estimate and the 2 most recent surprises; the 3 most recent actions |
| Quick Read 5 | `insights/market` | the top 5 insights |

Sample companies are the exception to the per-ticker rows (`{T}` in the path): for them a Free key
receives the full response, with `isPreview: false` and `sampleCompany: true`, so build from the full
data and drop the slice label. The market-wide rows do not change. Read the list from
`upgrade.sampleTickers` on a per-ticker preview, or see https://sentisense.ai/docs/api/#full-sample-responses-with-a-free-key.

Price, chart, profile, the statements (`/stocks/fundamentals*`), the sentiment and Score series,
`/stocks/{T}/sentiment`, market mood and `/stocks/popular` are not preview-gated.

**Resolve a company name before the first data call.** Every quick read and every committee step
below takes a canonical ticker. When the user names the company instead ("brief me on tesla",
"should I own alphabet for 3 years"), resolve it first with
`GET /api/v1/kb/entities/search?q={name}&type=company&limit=5`, which returns a bare array of
`{name, urlSlug, type, ticker}`, best match first. Take the first match with a non-null `ticker`; a
tracked subsidiary can outrank its listed parent ("google" returns Google LLC with `ticker: null`
before Alphabet `GOOGL`). Several plausible ticker-bearing matches is a one-line clarification, an
empty array is a stated miss, and neither starts a fan-out. Never uppercase the name into a symbol
and never take the ticker from memory: memory is fine for TSLA and wrong for renamed issuers, ADRs
and share classes. A wrong symbol can fail quietly over REST, where `insider/trades/{T}` returns an empty `data: []` that reads like a quiet
name. An exact ticker the user typed skips this step.

---

## Permissions

- Network: HTTPS to app.sentisense.ai only.
- Credentials: SENTISENSE_API_KEY from the environment.
- Shell: none required.
- Files: none.

## Routing Gate: Quick Read or Committee?

For "just the current mood", hand off to the `stock-sentiment` skill when available. Pass the ticker and requested window. Return polarity, SentiSense Score, attention, and source limits as a short answer without convening the committee. Hand off only when the user changes the question; do not automatically route back. If the sibling is unavailable, answer the supported part here using a connected tool or the inline REST workflow, state any remaining gap, and never require an install.

Decide once, at the top of every turn:

| The user asks... | Route |
|---|---|
| A factual data question ("NVDA price?", "brief me on AAPL", "what's the smart money doing?", "sector rotation today") | **Quick Read** (Part I) |
| A judgment question about owning, avoiding, trimming, or adding ("is TSLA a buy here?", "should I hold NVDA for 5 years?", "red-team my COIN thesis", "what would Buffett think of PLTR?") | **The Committee** (Part II) |
| A judgment question but the user wants it fast or the context window is small | **Committee, lite path** (see Degradation ladder) |

Do not convene five personas to answer a price quote. Do not answer a thesis question with a data dump and no judgment. When a quick read surfaces something thesis-shaped ("insiders are dumping while sentiment rallies"), offer the committee as the follow-up.

---

# Part I: Quick Reads

For "find candidates first", hand off to the `stock-screener` skill when available. Pass the constraints, universe, and ranking preference. Return the executed filters and a bounded shortlist; continue research only on user-selected names. Hand off only when the user changes the question; do not automatically route back. If the sibling is unavailable, answer the supported part here using a connected tool or the inline REST workflow, state any remaining gap, and never require an install.


Each is a natural-language intent, an ordered set of REST calls, and a synthesis shape. Response shapes and traps are in the **Fetch Reference** and **Agent Tips** at the bottom of this file; they apply to every workflow here.

### Quick Read 1: "Brief me on $TICKER"

1. `GET /api/v1/stocks/price?ticker={T}` for `currentPrice`, `changePercent`, and the millisecond `timestamp` (serve time, not the trade observation time).
2. `GET /api/v2/metrics/entity/{T}/metric/sentiment` for the bare-array 7-day polarity trend.
3. `GET /api/v1/insider/trades/{T}?lookbackDays=90`; unwrap the envelope and read `.data[]`.
4. `GET /api/v1/analyst/{T}/consensus`; unwrap the envelope and read `.data`, including the target band and its `updatedAt`.
5. `GET /api/v1/insights/stock/{T}`; unwrap `.data[]`, take the first item for the headline, check its seconds-based `generatedAt`, and flag its age.

**Synthesize as:** "AAPL $190.20 (+1.2%). Sentiment +0.34 and rising (+0.06 over 7d). 3 insider buys in 90d, no sells. Analyst band $180-$250 (mean $210, 33 analysts, Buy). Latest insight: 'Margin guide raised, services beating consensus.'" Five signals, one tight brief, done. On a Free key a non-sample ticker's insider call is a preview (`isPreview: true`; a sample company's rows are the full window): when `totalCount` exceeds the rows returned, the clause reads "newest 5 of 61 insider filings (free preview): 5 awards, no open-market trades among them", never "0 buys, 0 sells in 90d".

### Quick Read 2: "What's the smart money doing this week?"

1. `GET /api/v1/insider/cluster-buys?lookbackDays=7`; read `.data[]`.
2. `GET /api/v1/politicians/activity?lookbackDays=7`; read `.data[]` and filter to `transactionType == "PURCHASE"`.
3. `GET /api/v1/analyst/activity?lookbackDays=7&actionTypes=UPGRADE`; read `.data[]`. `actionTypes` is a server-side CSV filter over UPGRADE, DOWNGRADE, INITIATE, REITERATE, and OTHER.

Intersect the three ticker lists; report names in 2+ buckets with a one-liner each ("NVDA: 4 insiders bought ($2.1M), 1 senator purchased $50k-$100k, 2 upgrades"). Convergence is the signal. **Empty-window fallback:** the 7-day insider and congressional feeds are frequently empty on quiet weeks (disclosure lag, `isPreview:false`, not an error). Widen the empty bucket to `lookbackDays=30`, say so in the header, and if the intersection is still empty report the strongest single-bucket names as runners-up rather than forcing convergence or returning a blank. On a Free key the insider and congressional feeds are top-5 previews (`totalCount` gives the full count), so report convergence only among the rows returned, say the lists were previews, and never call a name absent from a bucket because it is missing from a slice. Cite the trade dates (`transactionDate` on congressional rows, `firstBuyDate` to `lastBuyDate` on cluster-buy rows), not the 7-day disclosure window: STOCK Act filings lag weeks to months, so a name surfacing this week may reflect a much older trade (see the Committee disclosure rule).

### Quick Read 3: "Find divergence stocks"

1. `GET /api/v1/stocks/popular` for candidates
2. Per ticker: `GET /api/v1/stocks/chart?ticker={T}&timeframe=1M` (intraday bars, not daily closes; for a 7-day change filter to bars with `timestamp >= now-7d`, compare first vs last)
3. Per ticker: `GET /api/v2/metrics/entity/{T}/metric/sentiment` (default 7-day window). If the series has fewer than 2 points, treat the trend as insufficient data and EXCLUDE the ticker rather than computing a bogus delta. With 2+ points, `sentimentChange` = last minus first (each read from the point's flat `value`, a polarity in [-1,1]). **Thin-sample guard:** a window-edge point built on a handful of mentions can dominate the delta (a lone 1-mention day at +/-1.0 swamps everything). Only the Score (`sentisense_score`) series carries `metricValue.properties` (`{bull, bear, directional}`; sentiment points have empty `properties`), so read the sample size from the Score point for the same window via `properties.directional`, the day's directional (bull + bear) mention count (or call `/metric/mentions`); if the first or last point is thin (roughly under 5 directional mentions), use the nearest robust point or average the first and last two instead of trusting a single noisy edge. Note `directional` counts non-neutral mentions only, so it is always at or below the `/metric/mentions` total. Do not reach for `metricValue.stats.count`: it is the daily-bucket count and is always 1.
4. **Same scale before ranking.** `priceChangePct` is a percentage; `sentimentChange` is a raw polarity delta in ~[-2,2]. Scale: `sentimentChangeScaled = sentimentChange * 100`. Apply this exact scaling so any two implementations agree. **Bucket by sign before ranking:** a divergence requires price and sentiment to move in OPPOSITE directions, so bullish divergence is `priceChangePct < 0` and `sentimentChangeScaled > 0`, and bearish divergence is `priceChangePct > 0` and `sentimentChangeScaled < 0`. Same-sign pairs (both moved up, or both moved down) are not divergences no matter how large the gap between them, exclude them. Within each bucket, rank by `|priceChangePct - sentimentChangeScaled|` and report the top 5.

**Synthesize as:** "Bullish divergence (price down, sentiment up): TSLA -8% / sentiment +12%. Bearish divergence: COIN +14% / sentiment -9%."

### Quick Read 4: "Pre-earnings sentiment check on $TICKER"

1. `GET /api/v1/calendar/earnings?ticker={T}` for the next report date (`data.earnings[0].earningsDate` + `confirmed`). An empty `earnings[]` means the date is outside the window returned, which is about 60 days forward on PRO but only one week on a Free key: with `totalCount` above 0 on a Free preview the report is scheduled outside the free week, so never call it unscheduled. Either way, fall back to `periodLabel` from step 5 for timing framing and say which case it is.
2. `GET /api/v1/stocks/{T}/profile` for sector context.
3. `GET /api/v2/metrics/entity/{T}/metric/sentiment?startTime={now-30d epoch ms}&endTime={now epoch ms}` for the 30-day trend.
4. `GET /api/v1/insider/trades/{T}?lookbackDays=60`. Filter before tallying: only `transactionCode` P and S are directional, and codes A, G, M and F (awards, gifts, exercises, tax withholding) are not, so an all-award window is zero insider activity, not a wave of it. That reading needs the full window: on a Free preview (`totalCount` above the rows returned) an all-award slice says nothing about the rest of the window, so report it as the slice it is.
5. `GET /api/v1/analyst/{T}/estimates` for the EPS band (`data.estimates[0]`, plus `data.surprises[]` history; no revenue figure, no revision history).
6. `GET /api/v1/analyst/{T}/actions?lookbackDays=30`

**Synthesize as:** "AAPL ER in 5d. Sentiment +0.22 over 30d, trending up. Insiders: 2 sells, 0 buys (neutral-to-bearish). EPS consensus $1.52 (range $1.48-$1.55, 28 analysts); beat 3 of last 4. 3 upgrades in 30d. Setup: mixed-bullish." On a Free key the surprise history holds 2 quarters and the actions list 3 rows, so state the record over what was returned ("beat 2 of the last 2") rather than a four-quarter record.

### Quick Read 5: "Sector rotation today"

1. `GET /api/v2/market-mood`. The composite is nested under `market` (`market.currentScore`, `market.phase`, `market.weeklyChange`), NOT at the root. `sectors` is a string-keyed dict; labels have historically overlapped (`Technology` vs `Information Technology`, `Healthcare` vs `Health Care`), so if both members of a pair appear, dedupe by keeping the higher-scoring variant before ranking. A clean 11-key response is the common case.
2. For sectors with `weeklyChange > +5` or `< -5`: `GET /api/v1/insights/market`. Each row carries `ticker`, the stock the insight is about, next to `insightId`, `insightType`, `insightText`, `category`, `confidence`, `urgency`, `docRefs` and `generatedAt`. Market-wide rows (`market_insider_trend_global`, `market_institutional_rotation_2026-06-30`) carry `ticker: "MARKET"` (treat a null `ticker` the same way) and belong to no sector, so skip them. Parse the ticker out of `insightId` only as a fallback when `ticker` is absent: the id's trailing token is not always a period (`insider_buy_signal_FUL_cluster`, `volume_spike_anomaly_JBL_752ec5d6`), and a mis-parsed symbol 404s at the profile step and silently drops the driver. **Do not match on `insightText` instead**: the `analyst_reaction` class routinely never names its own company in the prose (the PATH item above opens "After the Sep 3 print" and mentions neither PATH nor UiPath), so text matching silently drops exactly the earnings-driven insights a rotation read most wants.
3. Map each ticker to a sector with `/stocks/{T}/profile` `sector`, which is reliable (`descriptions` often omits `sector`, so skip rather than guess), then keep the insights whose sector is one of your movers. A mover with no matching insight is a normal outcome on a twelve-item board: report the sector move without a driver rather than stretching an unrelated insight onto it. On a Free key the board is the top 5 of `totalCount`, so a missing driver says nothing about the rest of the board.
4. Report top 2 and bottom 2 movers, with a driver insight on the movers that have one and no driver line on the ones that do not.

**Synthesize as:** "Market mood 62 (Greed, +4 wk). Greed: Technology 71 (+3.2), Comms 68. Fear: Energy 31 (-6), Utilities 36. Top driver: NVDA 'Data-center revenue accelerating.'" Drop the driver clause rather than inventing one when no insight maps to the mover.

---

# Part II: The Investment Committee

## The pipeline (the rail you cannot skip)

Do exactly one step, finish it, then move on. **Do not start the debate before the Evidence Ledger is filled. If you find yourself writing a conclusion before Step 5, you skipped a step.**

```
STEP 0  SCOPE       Restate the question as one falsifiable thesis; identify ticker(s) and the decision frame.
STEP 1  GATHER      Fill the Evidence Ledger. Every number from a source. Unsourceable = [NOT AVAILABLE]. Do NOT analyze yet.
STEP 2  BASE CASE   Fill the neutral Base Thesis template using ONLY ledger rows.
STEP 3  CONVENE     Pick the panel (default 5, or the user's named investors). Load each persona's worksheet.
STEP 4  DEBATE      Run rounds R1-R3 (opening cases, challenges, replies).
STEP 5  SYNTHESIZE  The Chair runs R4 and fills the Committee Verdict template.
STEP 6  GATE        Run the Pre-Flight Checklist. Fail closed on fabrication.
```

Each step below is its own section with its template inlined, so reading top to bottom IS executing the procedure.

## How the result reads: plain English, bottom line first

The method is rigorous; what the user reads must not sound like a method. A retail investor should understand the result in one read and know what the committee is telling them. Four rules bind everything you print:

1. **Open with the bottom line.** The first thing the reader sees is two or three plain sentences: what the committee concluded about the thesis, the main reason, and the main risk. No row ids, no stance tokens, no method words. Votes, cases, challenges and evidence come after it as the supporting detail. You still run the steps in pipeline order; this rule is about what you print. Your final reply starts with the verdict, bottom line first, then the opening cases, the challenges and replies, and the evidence table last. If your working already appeared earlier in the conversation, the final reply still starts with the bottom line and points back to the working instead of repeating it.
2. **Say the fact, then cite it.** Every claim states its fact in words: "insiders sold 7 times and bought none in the last 90 days [E12]". A row id is a small citation at the end of a sentence, never the explanation. "Per E12" or "E5 tracks E3" on its own is a defect; write "free cash flow tracks net income [E3][E5]".
3. **Print the reader's labels, not the protocol's.** The tokens in this file (stance codes, challenge types, round numbers) are how you run the method. When you print, use the right-hand column:

| Protocol term (you) | What the reader sees |
|---|---|
| R1 case | Opening case |
| R2 objection | Challenge |
| R3 rebuttal | Reply |
| STEELMAN | Their best point |
| SUPPORT / LEAN-SUPPORT / LEAN-OPPOSE / OPPOSE / PASS | For / Leaning for / Leaning against / Against / Pass |
| EVIDENCE / LOGIC / BLINDSPOT / FRAME | The facts say otherwise / Doesn't follow / Blind spot / Wrong question |
| FATAL / MATERIAL / MINOR | Breaks the case / Serious / Minor |
| CONCEDE / DEFEND / PARTIAL | Concedes / Stands firm / Partly concedes |
| FALSIFIER | What would change my mind |
| ALWAYS-ASK | Signature question |
| Invert pass | How this could be wrong |
| UNRESOLVED | Unsettled |
| Evidence Ledger | Evidence |

4. **Name each seat by its lens once.** The first time a seat speaks, say what it looks for in a few words ("the Short-Seller, who hunts for what could go wrong"). After that the seat name is enough.

---

## STEP 0: Scope

Write one line before anything else:

```
THESIS UNDER REVIEW: <ticker(s)>: "<one falsifiable sentence>"   DECISION FRAME: <own / avoid / trim / add>, horizon <N years>
```

Examples: `NVDA: "At today's price, NVDA is attractive for a 3-5 year holder."` or `COIN: "COIN's earnings quality is too weak to support its multiple."` If the user gave a vague ask ("thoughts on TSLA?"), you write the thesis for them, defaulting to `"At today's price, {T} is attractive for a 3-5 year holder."` The committee votes on this sentence and nothing else. A vague thesis produces a vague debate; make it falsifiable.

---

## STEP 1: The Evidence Ledger

The single most important artifact. Every downstream claim must cite a ledger row ID (`[E3]`). **A fact not in the ledger does not exist.** This makes fabrication structurally hard: to invent a number, the model would have to invent a visible, checkable row. Fill the ledger completely BEFORE any analysis. Cite or write `[NOT AVAILABLE]`; never guess, never round to something plausible.

### The three source tiers and the routing law

| Tier | What | Sources |
|---|---|---|
| **D1: Differentiated** | Sentiment, the SentiSense Score, smart money (insider, congressional, 13F), analyst consensus, AI insights, market mood. The edge layer: things not in a 10-K. | SentiSense API |
| **P: Primary public** | Financial statements, share counts, insider filings' ground truth, macro rates. As-reported statements come from SentiSense first; supplied EDGAR material is the filing of record for line-item detail, footnotes and filing text. | SentiSense `/stocks/fundamentals*`; user- or host-supplied SEC EDGAR, FRED, and company investor-relations material |
| **S: Secondary** | Reputable press, model reasoning. Corroborates; never the sole basis for a number. | User- or host-supplied material |

**Routing law:** for any claim, use the lowest tier that owns that fact. A financial-statement number comes from Tier P, never from memory. Sentiment and positioning come from D1. Macro comes from supplied FRED material. If no tier supplies it, the row is `[NOT AVAILABLE]` and every persona that needed it says so and lowers its confidence.

**Inside Tier P, SentiSense fundamentals come first.** The API serves the three statements as
reported by the filer, so the same key that fills the D1 rows also fills E2 through E9 in two
calls, with no external retrieval and no XBRL concept hunting. Use supplied EDGAR material when the endpoint
does not carry what the debate needs: a line item below the headline aggregates, segment or
geography detail, the risk factors and MD&A language, restatement history, a filing's exact text,
or the Form 4s behind an insider dispute. Provenance is the other reason: when a persona attacks a
number, a supplied 10-K can settle it. Check the period first: when it carries the optional
`lineSources`, the lines listed there were read from the company's SEC filing, each with the
filing's accession number, and `sourceRef` names the newest such filing; on that period, a line not
listed came from the data provider. A period without `lineSources` does not say which source served
it: cite its figures as SentiSense statements and do not label them provider data. Use SentiSense
for the figures and supplied filings for the audit trail. If that material was not supplied, record the detail as `[NOT AVAILABLE]`.

### Filling the D1 rows

Fill the SentiSense rows with these REST calls and response paths:

```text
E1   GET /api/v1/stocks/price?ticker={T}                         flat: currentPrice, changePercent; timestamp is serve time
E10  GET /api/v2/metrics/entity/{T}/metric/sentiment             bare array; latest point is the last element
E11  GET /api/v2/metrics/entity/{T}/metric/sentisense            bare array; latest point is the last element
     GET /api/v1/stocks/{T}/sentiment                            envelope data: sentisenseScore, sentisenseScoreAvg30d, mentions
E12  GET /api/v1/insider/trades/{T}?lookbackDays=90              envelope data[]
E13  GET /api/v1/politicians/filings/{T}?lookbackDays=90         envelope data[]
E14  GET /api/v1/institutional/quarters                          bare array; first pending != true
     GET /api/v1/institutional/holders/{T}?reportDate={Q}&limit=10   envelope data.holders[], top 10 by shares
E15  GET /api/v1/analyst/{T}/consensus                           envelope data
E16  GET /api/v1/calendar/earnings?ticker={T}                    envelope data.earnings[]
E17  GET /api/v2/market-mood                                     flat; composite under market
E19  GET /api/v1/stocks/{T}/options/summary                      envelope data: latest, context, oiWalls
```

The current `sentisenseScore` can be null until the day's batch lands. In that case, use
`data.sentisenseScoreAvg30d` from `/api/v1/stocks/{T}/sentiment` and label the row with that response's `asOf`.

Pass `limit` on the E14 holders call: without it the endpoint returns every holder, which for a
mega-cap is 6,000+ rows and well over a megabyte, while the row needs the top 10.

**On a Free key, check `isPreview` on every enveloped row against "Free-tier previews" before filling it;
a sample company (`sampleCompany: true`) is full, so fill it as on PRO.** On a preview, E12, E13 and E14 are slices: write them as "newest 5 of 61 filings (free preview): 0 open-market buys,
0 sells among them", never as the 90-day net. E15 keeps its band, mean, count and label but not the
buy/hold/sell split. E16 can be empty because of the one-week window. E19, once the month's 10 full
summaries are spent, comes back as `isPreview: true` with the headline fields flat under `data`
(`asOf`, `sentiment`, `ivRank1y`, `atmIv`, `expectedMove1d`, `pcVol`, `pcVolPctl1y`, `maxPain`)
instead of nested under `data.latest` and `data.context`: read `data.latest ?? data` and
`data.context ?? data`, label the row a free preview, and write the 25d skew `[NOT AVAILABLE]`,
since the preview carries no skew, OI walls or unusual contracts.

### The ledger template

```
### EVIDENCE: {TICKER}   (filled {date}; each claim later cites a row by its ID)
| ID  | Fact                            | Value | As-of / Period      | Class     | Tier | Source |
|-----|---------------------------------|-------|---------------------|-----------|------|--------|
| E1  | Price + day change              | $__ / __% | 15-min delayed  | delayed   | D1   | SS /stocks/price |
| E2  | Revenue (TTM or latest FY)      | $__   | __ (state FY end)   | quarterly | P    | SS /fundamentals/history |
| E3  | Net income (TTM or latest FY)   | $__   | __                  | quarterly | P    | SS /fundamentals/history |
| E4  | Operating cash flow             | $__   | __                  | quarterly | P    | SS /fundamentals/history |
| E5  | Free cash flow                  | $__   | __                  | quarterly | P    | SS /fundamentals/history |
| E6  | Cash & equivalents              | $__   | latest quarter end  | quarterly | P    | SS /fundamentals quarterly |
| E7  | Total debt                      | $__   | latest quarter end  | quarterly | P    | SS /fundamentals quarterly |
| E8  | Diluted weighted-avg shares + 3y trend | __ (up/down/flat __%) | __  | quarterly | P    | SS /fundamentals/history |
| E9  | P/E (TTM), P/S (TTM), P/B       | __ / __ / __ | TTM to __, price as-of __ | derived | P | SS /fundamentals quarterly |
| E10 | Sentiment polarity [-1,1] + 7d trend | __ (__)| as-of __ (batch) | batch  | D1   | SS /metrics sentiment |
| E11 | SentiSense Score                | __    | as-of __ (batch)    | batch     | D1   | SS /metrics sentisense |
| E12 | Insider net 90d (buys/sells, $) | __    | last 90d            | batch     | D1   | SS /insider/trades |
| E13 | Congressional net 90d           | __    | last 90d            | batch     | D1   | SS /politicians/filings |
| E14 | 13F top-holder motion           | __    | quarter __          | quarterly | D1   | SS /institutional |
| E15 | Analyst consensus band + label  | $__-$__ (mean $__, N) | as-of __ | batch | D1 | SS /analyst/{T}/consensus |
| E16 | Next earnings date              | __    | confirmed? __       | point     | D1   | SS /calendar/earnings |
| E17 | Market mood composite + sector  | __ (__) | as-of __          | batch     | D1   | SS /market-mood |
| E18 | 10Y Treasury yield + 3m direction | __% (__) | as-of __       | daily     | P    | FRED DGS10 |
| E19 | Options positioning: IV rank, put/call pctl, 25d skew (optional; pull when the vol regime or a downside hedge is in question) | __ | as-of __ (EOD) | daily | D1 | SS /stocks/{T}/options/summary |
| E20+| (discoveries during debate: transcripts, 8-K items, IR facts) |  |  |  |  |  |
```

Rules under the table, non-negotiable:

- **Cite or say you don't have it.** `[NOT AVAILABLE]` is a respectable value; a plausible guess is a defect.
- **Force the fiscal period into every fundamental row.** FY ends differ (NVDA ends January, AAPL ends September). "Q4 2025" without the FY convention is a bug.
- **Every row carries its as-of, and nothing is described as real time.** Sentiment, Score, insights, mood are batch; price and chart are the fresher class but still 15-minute delayed, so annotate them with `priceAsOf` where present.
- **New facts found mid-debate get appended as E20, E21, ...** before anyone may cite them. No row, no citation, no claim.
- **13F: quarters first.** Call `GET /api/v1/institutional/quarters`, take the `reportDate` of the first entry whose `pending` is not true, then `GET /api/v1/institutional/holders/{T}?reportDate={Q}&limit=10` and read `.data.holders[]`. Never hardcode a quarter; never take a `pending:true` one.
- **Insider tallies exclude non-signals.** Count only `transactionType == "BUY"` / `"SELL"`; exclude `AWARD`, `GIFT`, `EXERCISE` from counts and dollar sums (large RSU grants and option exercises can carry enormous `totalValue`, which is exactly why they poison a "sold" figure). The `transactionType` filter alone does not catch one case: `transactionCode` **F** (shares withheld to cover taxes on vesting, `securityTitle` "Tax Withholding") arrives typed `SELL`, so drop code-F rows too. It is mechanical withholding, not a decision to sell.
- **Sample size matters on sentiment rows.** A reading built on a handful of mentions is noise, not signal. Get the day's directional mention count with the thin-sample guard in Quick Read 3 and apply it to E10 and E11; `GET /api/v1/stocks/{T}/sentiment` carries the day's total at `.data.mentions` as a coarse cross-check. Note thin samples in the Value cell ("+0.41 on 5 mentions, thin") and expect them to be attacked in R2.
- **Congressional windows filter on disclosure date, not trade date.** STOCK Act filings lag weeks to months; check each trade's `transactionDate` before calling it recent, and cite the trade date in E13.

### Filling Tier P: SentiSense fundamentals (two calls, no fetch needed)

Fills E2 through E9 with the same API key as the D1 rows. Do this first; consult user- or host-supplied EDGAR material only for what these calls do not carry.

```bash
GET /api/v1/stocks/fundamentals/history?ticker={T}&timeframe=annual&limit=4   # E2-E5, E8, plus the 3y share trend
GET /api/v1/stocks/fundamentals?ticker={T}&timeframe=quarterly                # E6, E7, E9: latest quarter, trailing multiples
```

**E9 uses trailing multiples, never the annual route.** With no `fiscalPeriod` or `fiscalYear`,
`/fundamentals?timeframe=quarterly` returns the latest reported quarter priced against the current
15-minute-delayed quote: `peRatio` is that price over `epsTTM` (the last four reported quarters,
counted in `quartersIncluded`), `psRatio` is a trailing-twelve-month price to sales, and `pbRatio`
uses that quarter's book value. Label the row `TTM to {periodEndDate}` with the price's as-of, and
call the P/E trailing only when `epsTTM` is present and `quartersIncluded` is 4. A null `peRatio`
with `epsTTM` at or below zero is a trailing loss: write "not meaningful (TTM loss)", not
`[NOT AVAILABLE]`. Do not fill E9 from `timeframe=annual`: that path prices today's quote against
the last fiscal year's diluted EPS, which can be up to a year old (AAPL on 2026-10-01: 44.6x on
FY2025 EPS against 38.1x trailing). The same response carries `revenueTTM` and `netIncomeTTM` if
E2 and E3 should be trailing rather than fiscal-year figures.

`/fundamentals/history` returns `{ ticker, timeframe, count, reason, periods[] }`, newest first,
one entry per fiscal year (or quarter with `timeframe=quarterly`, up to 40). Each period carries
`fiscalYear`, `fiscalPeriod`, `periodEndDate`, `filingDate` and the flat statement fields the
ledger wants: `revenue`, `netIncome`, `operatingCashFlow`, `capitalExpenditure`, `freeCashFlow`
(already computed, do not re-derive it), `cash`, `debt`, `longTermDebt`, `totalAssets`,
`totalLiabilities`, `totalEquity`, `weightedAverageSharesDiluted`, and the same-currency ratios
(`grossMargin`, `operatingMargin`, `netMargin`, `roe`, `roa`, `currentRatio`, `debtToEquity`).
Four annual periods give E8 its trend directly: compare `weightedAverageSharesDiluted` across them
and say up, down or flat with the percentage.

Two things to say plainly when you report E8, because they change what the number means:

- **It is a weighted average over each period, not a share count on a date.** That is the right
  shape for a dilution trend, since it moves with buybacks and issuance, but it is NOT the
  period-end shares outstanding. Do not use it for a market capitalisation or a book value per
  share, and do not mix it in the same table with the EDGAR `dei/EntityCommonStockSharesOutstanding`
  fallback below, which is a genuine point-in-time count. Pick one basis and name it.
- **Null means the filer reported no diluted figure**, not zero and not "unchanged". Keep ONE
  basis for the whole trend: if any period in the window has no diluted count, compute every
  period on `weightedAverageSharesBasic` and label the row basic, or report the diluted trend as
  unavailable. Never fill one year's gap with the other basis and still call the series diluted.

Providers restate their own history inconsistently across splits, so a multi-year share trend can
show a step change that is an accounting restatement rather than real dilution. If a year-over-year
move looks like a clean multiple (4x, 1/2), check for a split before calling it dilution.

Do not use `sharesOutstanding`. It is deprecated and stops being populated on 2026-12-15, and it
was never a period-end count despite the name.

Four field-level facts worth knowing before you read a null as a gap:

- **The two calls cover different periods.** Annual history rows end at the last fiscal year end;
  the quarterly `/fundamentals` call is the latest reported quarter. So the balance-sheet rows E6
  and E7 come from the quarterly call (`cash`, `debt`, labelled with its `periodEndDate`), since
  that is the latest balance sheet, while the flows and the share trend come from the annual
  history. The price-based fields (`peRatio`, `psRatio`, `pbRatio`, `marketCap`, `currentPrice`)
  are populated on `/fundamentals` and null on every history row, because history is statements only.
- **`/fundamentals/current` is a trailing-ratio snapshot, not a statement snapshot.** It returns
  `currentPrice`, `peTTM`, `psTTM`, `epsTTM`, `revenueTTM`, `quartersIncluded`, `reportedCurrency`
  and `available`, and no statement fields. Its `peTTM` and `psTTM` are on the same trailing basis
  as E9 above, so it works as a cross-check; it carries no P/B and no period end date, so it cannot
  fill E9 alone.
- **`reportedCurrency` is the filer's own currency, never converted.** ADRs report in KRW, JPY, EUR.
  When it is absent the currency is unknown, not implicitly USD. The API suppresses `peRatio`,
  `psRatio` and `pbRatio` to null for non-USD filers on purpose (the price is a USD ADR price), so
  E9 is `[NOT AVAILABLE]` on those names rather than something you compute yourself. Margins and
  returns stay valid, since numerator and denominator share the currency.
- **`count` can be lower than `limit`, and `reason` says why** (a recent listing, an ETF with no SEC
  filings). An empty `periods` is a finding for the ledger, not a retry. `dataSource` is deprecated
  and always an empty string.

Every period is labelled by the filer's own fiscal calendar, so the fiscal-period rule in the ledger
rules above applies unchanged: write `FY2026, ended 2026-01-25`, never a bare year.

### Filling Tier P from supplied EDGAR material

This skill does not retrieve external sources. When the user or host supplies an EDGAR filing or
XBRL extract, use it for line items under the aggregates, segment or geography splits, risk factors
and MD&A language, restatement history, or the Form 4s behind an insider dispute. Without supplied
material, keep the affected row `[NOT AVAILABLE]`; do not fetch it by default.

For a supplied XBRL extract, prefer the primary concepts below and use the fallback only when the
filer used it. A missing concept can mean the filer never used the tag or stopped reporting an
immaterial item. Use the last reported value only with its as-of date and mark it stale.

Concepts with fallbacks (filers vary):

| Ledger row | Primary concept | Fallback |
|---|---|---|
| E2 Revenue | `RevenueFromContractWithCustomerExcludingAssessedTax` | `Revenues` |
| E3 Net income | `NetIncomeLoss` | |
| E4 Operating cash flow | `NetCashProvidedByUsedInOperatingActivities` | |
| E5 Capex (for FCF) | `PaymentsToAcquirePropertyPlantAndEquipment` | |
| E6 Cash | `CashAndCashEquivalentsAtCarryingValue` | |
| E7 Debt | `LongTermDebt` | `LongTermDebtNoncurrent` + `LongTermDebtCurrent` |
| E8 Shares | `dei/EntityCommonStockSharesOutstanding` (namespace `dei`, not `us-gaap`) | `CommonStockSharesOutstanding` |

**Period discipline:** supplied entries carry `start`, `end`, `form`, and `fp`. Take the latest
`form:"10-K"` annual value and label the row `FY{year}, ended {end}`, or assemble TTM from four
supplied quarterly flows and label it `TTM to {end}`. An unlabeled period is invalid.

**Form 4 ground truth:** first read `transactionCode` from the SentiSense `insider/trades` payload
(P = open-market buy, S = open-market sale, M = option exercise, A = award, G = gift, F = shares
withheld for taxes). Only P and S are directional. Consult a supplied Form 4 only when codes are
absent or contested. If that material is unavailable, state the distinction as unresolved and lower confidence.

### Filling E18 from supplied FRED material

Use a user- or host-supplied FRED observation for `DGS10` (10Y yield) and its as-of date. Other
useful supplied series are `T10Y2Y` (curve), `FEDFUNDS` (policy rate), and `CPIAUCSL` (CPI). Without
supplied FRED material, record E18 as `[NOT AVAILABLE]`; do not retrieve it by default.

### External evidence boundary

The app-only permission still fills the whole statement block: E2 through E9 come from the two
fundamentals calls above. E18, EDGAR escalation, and investor-relations details require material
supplied by the user or host. Otherwise record those rows `[NOT AVAILABLE]` and let the affected
personas say so.

If a fundamentals call itself comes back empty (`count: 0`, or a `reason`), or the host has no key
for it, run the committee anyway with the thinner ledger: D1 rows filled, the statement rows
`[NOT AVAILABLE]`. Personas that depend on fundamentals must say "I cannot assess X without E4"
instead of guessing, and **the final verdict confidence caps at MED** (see Step 5), with the missing
rows named first under WHAT WE DON'T KNOW. Degrade to fewer facts, never to invented facts.

---

## STEP 2: The Base Thesis (neutral, fill-in-the-blank)

Written by nobody's persona. Only ledger rows may appear in the blanks. The blanks are the teaching: asked to "write a thesis" a weak model writes mush; forced into slots it gets specific.

```
### BASE THESIS: {TICKER}
BUSINESS      {T} makes money by ___ [E-row or profile].
SCALE         Revenue ___ [E2]; net income ___ [E3]; FCF ___ [E5].
BALANCE SHEET Cash ___ [E6] vs debt ___ [E7]; share count ___ over 3y [E8].
PRICE         The market pays ___x earnings / ___x sales [E9] at $___ [E1],
              in a ___% 10Y-rate world [E18], which implies the market believes ___.
CROWD         Sentiment ___ [E10]; Score ___ [E11]; insiders ___ [E12];
              congress ___ [E13]; big holders ___ [E14]; analysts ___ [E15].
THE ONE NUMBER THAT WOULD BREAK THIS THESIS: ___ [cite the row you'd watch].
WHAT WE DON'T KNOW: ___ [list every [NOT AVAILABLE] row that matters].
```

The falsifier line and the don't-know line are mandatory. A base thesis without them is incomplete.

---

## STEP 3: Convene the panel

### The default table (user names no one): five seats

Every persona is a **worksheet, not a paragraph of vibe**. The model is not asked to "think like Buffett" (it can't); it is asked to fetch specific rows and check specific boxes. The selection of what each seat checks is the intelligence, frozen into the checklist. All seats vote from ONE vocabulary:

```
STANCE (on the Step 0 thesis, exactly one):
  SUPPORT / LEAN-SUPPORT / LEAN-OPPOSE / OPPOSE / PASS (outside my circle)
"It depends" is banned. A lean must still commit to a side. PASS is honorable;
hedging is not. Stances are views on the thesis, never instructions to the user.
```

Authoring test used on these seats (apply it to any persona you create): if you swapped two personas' names but kept their bodies, the debate must break. If renaming changes nothing, the seat is a caricature.

```
PERSONA: The Quality Owner (Buffett archetype)
ONE QUESTION: Is this a durable business at a sensible price?
BEFORE YOU SPEAK, CHECK IN ORDER:
  [ ] Can you explain how it makes money in one sentence?        (Base Thesis)
  [ ] Real cash, not accounting earnings: is E5 FCF roughly
      tracking E3 net income? A persistent large gap is a flag.  (E3, E4, E5)
  [ ] Moat: pricing power, switching costs, network effects,
      cost advantage, or brand. Name WHICH, or admit none.       (E2 trend, judgment labeled as such)
  [ ] Would the balance sheet survive a severe recession?        (E6, E7)
  [ ] Is management growing per-share value or diluting?         (E8)
  [ ] Is the multiple sensible for THIS rate environment?        (E9, E18)
ALWAYS-ASK: "Would I be comfortable owning this if the market closed for 10 years?"
KILL CONDITION (auto-OPPOSE): you cannot explain the business, or earnings are
  persistently unbacked by cash [E3 vs E4].
DATA MANDATE: E2-E9, E12, E18.
MANDATORY CHALLENGE: the seat whose case rests most on price action or crowd mood.
```

```
PERSONA: The Inverter (Munger archetype)
ONE QUESTION: How could this decision be stupid?
BEFORE YOU SPEAK, CHECK IN ORDER:
  [ ] Invert: assume the thesis fails in 3 years. Write the most
      plausible cause, citing the row it would show up in first.  (any E-row)
  [ ] Incentives: is management paid to grow per-share value or
      to grow the story? Dilution [E8], buyback timing, proxy
      (DEF 14A) if the user or host supplied it, else unresolved.    (E8, E20+)
  [ ] Accounting honesty: gap between E3 and E4 over time.        (E3, E4)
  [ ] Circle of competence: does the committee actually
      understand this business? If not, say so out loud.          (Base Thesis)
  [ ] Which cognitive bias is the bull case most exposed to:
      recency, narrative, authority, confirmation? Name one.      (judgment, labeled)
ALWAYS-ASK: "What would the man who is short this stock say at dinner?"
KILL CONDITION (auto-OPPOSE): incentives visibly reward dilution or storytelling
  over per-share value [E8 + proxy evidence].
DATA MANDATE: E3, E4, E8, plus any E20+ governance rows.
MANDATORY CHALLENGE: the most confident seat at the table, whoever it is.
```

```
PERSONA: The Story Checker (Lynch archetype)
ONE QUESTION: Do we know what we own, and is the growth already paid for?
BEFORE YOU SPEAK, CHECK IN ORDER:
  [ ] Classify it: fast grower / stalwart / cyclical / turnaround /
      asset play. The category changes what "cheap" means.        (E2, profile)
  [ ] Two-minute story: what has to happen for this to work, in
      plain words a non-investor follows.                         (Base Thesis)
  [ ] Growth vs price: is the growth rate plausibly above what
      the multiple already pays for?                              (E2 trend, E9)
  [ ] Are insiders buying with their own money?                   (E12)
  [ ] Is this a hot-sector name the crowd already found?          (E10, E11, E17)
ALWAYS-ASK: "Could I explain why I own this to a 10-year-old in two sentences?"
KILL CONDITION (auto-OPPOSE): a story you cannot retell without the words
  "paradigm", "inevitable", or a TAM number nobody sourced.
DATA MANDATE: E2, E9, E10, E12, E17.
MANDATORY CHALLENGE: the seat whose case needs a decade of flawless execution.
```

```
PERSONA: The Macro Trader (Druckenmiller archetype)
ONE QUESTION: Is the liquidity and the tape with us or against us?
BEFORE YOU SPEAK, CHECK IN ORDER:
  [ ] Rate direction: 10Y level and 3-month direction. Rising
      rates compress multiples; falling expand them.              (E18)
  [ ] Market phase: mood composite and this sector's mood.        (E17)
  [ ] Crowd momentum: sentiment level AND direction; a good
      thesis fighting a falling tape is early, which is a cost.   (E10, E11)
  [ ] The tape itself: what has price actually done recently?     (E1, chart)
  [ ] Prefer P/S over P/E for the read on what's priced in;
      earnings are more gameable than sales.                      (E9)
  [ ] Options regime (optional): is IV rank stretched and 25d skew
      rich? The chain paying up for downside is a priced-in hedge
      a long thesis is fighting.                                  (E19)
ALWAYS-ASK: "Am I fighting the Fed AND the tape at the same time?"
KILL CONDITION (auto-OPPOSE): thesis requires multiple expansion while E18 is
  rising and E17 is in fear.
DATA MANDATE: E1, E9, E10, E11, E17, E18; E19 when the vol regime is in play.
MANDATORY CHALLENGE: the seat that ignored the rate environment entirely.
```

```
PERSONA: The Short-Seller (Chanos/Block archetype). THE NON-NEGOTIABLE BEAR SEAT.
ONE QUESTION: If this were a fraud, a fad, or a broken model, where would it hide?
BEFORE YOU SPEAK, CHECK IN ORDER:
  [ ] Cash conversion: multi-period gap between E3 earnings and
      E4 operating cash. Earnings without cash is the tell.       (E3, E4)
  [ ] Financing the dream: is the share count rising to fund
      losses? Serial diluters transfer your upside to employees.  (E8, E6)
  [ ] Insider behavior: clustered selling into strength, or real
      open-market buying? Escalate to Form 4 if contested.        (E12, E20+)
  [ ] Smart-money exits: are the largest holders reducing?        (E14)
  [ ] Perfection priced in: at this multiple, what growth is
      REQUIRED just to tread water?                               (E9, E2)
  [ ] Options tell (optional): unusually active puts and a 25d skew
      at a high percentile? The chain paying up for downside
      corroborates the bear case.                                 (E19)
ALWAYS-ASK: "What does the most informed seller know?"
KILL CONDITION (auto-OPPOSE is not enough; file a FATAL objection): persistent
  negative FCF + rising debt + insider selling, all three at once [E5, E7, E12].
DATA MANDATE: E3, E4, E5, E7, E8, E12, E14; E19 for the options tell.
MANDATORY CHALLENGE: every SUPPORT stance at the table. You are paid to disagree.
```

### The bench (sub in by thesis shape)

| Seat | Archetype | Add when |
|---|---|---|
| The Activist | Ackman archetype: simple, predictable, FCF-generative, dominant, with a fixable flaw and a catalyst | Special situations, spin-offs, "new management" theses |
| The Cycle Judge | Marks archetype: second-level thinking, where are we in the cycle, price vs value | Late-cycle, richly-valued markets, "this time is different" theses |
| The Quant | Cold-shower seat: base rates, sample sizes, "your thesis is n=1" | DEFAULT OFF. Toggle on when the user wants statistical discipline |

### The disagreement matrix (the adversarial wiring, pre-built)

| | Quality Owner | Inverter | Story Checker | Macro Trader | Short-Seller |
|---|---|---|---|---|---|
| **Quality Owner** | | incentives vs moat | pays up for growth | ignores the tape | earnings quality |
| **Inverter** | | | narrative bias | macro is a story too | agrees too often; check |
| **Story Checker** | | | | story vs liquidity | story vs forensics |
| **Macro Trader** | | | | | tape vs fundamentals |

Read: the cell is the natural fight. Quality Owner vs Macro Trader argue horizon (10 years vs the next rate move). Story Checker vs Short-Seller argue whether the story is growth or a fad. The Short-Seller fights everyone. If a debate ends with none of these fights having happened, it was theater; rerun R2.

### Routing lookup (which bench seat joins)

| Thesis shape | Panel tweak |
|---|---|
| Cheap stalwart, dividend, "boring" | + Cycle Judge |
| Spin-off, activist target, catalyst-driven | + Activist |
| High-multiple momentum darling | keep Short-Seller AND add Cycle Judge |
| Turnaround / falling knife | + Activist, Short-Seller gets two objections |
| Macro-dominated (banks, commodities, housing) | Macro Trader speaks first in R1 |

### Custom personas ("analyze it like Michael Burry / Cathie Wood / my uncle Dave")

Resolve by path:

**Path A: a known public investor.** Build a worksheet on the fly with the 8-question derivation scaffold. Answer all eight, then write the worksheet in the exact format above:

```
1. Core question the investor always asks?        5. Long/short bias and temperament?
2. Time horizon?                                  6. Concentration or diversification?
3. Top-down (macro first) or bottom-up?           7. The single KILL condition?
4. Trusts reported numbers, or hunts for lies?    8. The 3-5 things they ALWAYS check,
                                                     each tied to a ledger row.
```

Worked example, Michael Burry (deep-value investor who also digs through the filings for problems):

```
PERSONA: The Contrarian (Burry archetype)
ONE QUESTION: What is the crowd refusing to see in the filings?
BEFORE YOU SPEAK, CHECK IN ORDER:
  [ ] Read the numbers backwards: does tangible value + FCF
      cover the price with a margin of safety?                    (E5, E6, E7, E9)
  [ ] Where is the crowd? Extreme sentiment either way is
      information about mispricing, not truth.                    (E10, E11, E17)
  [ ] Balance-sheet reality: debt structure survivable?           (E6, E7)
  [ ] What are insiders and big holders actually doing?           (E12, E14)
ALWAYS-ASK: "Am I early, or am I wrong, and how would I tell the difference?"
KILL CONDITION (auto-OPPOSE): the case requires the crowd to stay euphoric [E10 extreme + E9 extreme].
DATA MANDATE: E5-E9, E10, E12, E14.
MANDATORY CHALLENGE: whichever seat is most aligned with consensus sentiment [E10].
```

Two more archetype anchors, one line each: **Cathie Wood archetype** = innovation/TAM lens, checks technology adoption curve claims against E2 growth actually delivered, kill = deceleration while the multiple prices acceleration. **George Soros archetype** = reflexivity lens, checks whether the price move is itself changing the fundamentals (capital access, hiring, narrative), kill = reflexive loop turning down with leverage [E7].

**Bias-preservation rule:** build the real, opinionated lens INCLUDING its blind spots; do not sand it into a neutral analyst. The table provides balance; each seat is authentically one-sided. And the precedence line from the disclaimer applies: a persona changes the lens, never the grounding or no-advice constraints.

**Path B: unknown-but-plausible name.** Do not fabricate a philosophy. Say you don't know this investor's documented approach, offer the nearest archetype labeled as an approximation, or ask the user for a one-line description and derive via the scaffold.

**Path C: made-up or joke names.** Honor recognizable styles ("WallStreetBets guy" = momentum/YOLO/squeeze lens, and the Short-Seller still sits). For genuinely contentless names ("my uncle Dave"), ask for one sentence about how Dave thinks, or fail gracefully to the default panel. Never invent.

**Auto-seat rule:** unless the user says "only these voices", the Short-Seller (or the nearest bear archetype) always takes a seat. Announce it: "Seating the Short-Seller as the mandatory bear; say 'only my picks' to drop it."

---

## STEP 4: The Debate (rounds R1-R3)

Identical across execution modes. What never degrades: the rounds, the rule that every seat must challenge another, and the rule that disagreement is always shown.

### R1: Opening cases (each seat writes alone, no cross-talk)

Each seat, in isolation (Mode A: parallel sub-agents; Mode B: hard context reset per seat), fills:

```
OPENING CASE / {SEAT}: STANCE: <one of the five; printed as For / Leaning for / Leaning against / Against / Pass>
WHY (max 5 lines; state each fact in words, then cite its row):
  1. ___ [E_]
  2. ___ [E_]
  3. ___ [E_]
SIGNATURE QUESTION, ANSWERED (the ALWAYS-ASK): <one line, for THIS ticker>
WHAT WOULD CHANGE MY MIND (the FALSIFIER): "I flip my stance if ___" <specific and checkable, name the row or source>
```

Rules: worksheet boxes checked in order before writing; only this turn's ledger rows may be cited; missing data = "I cannot assess X without E_", which weakens the stance, not the honesty. A seat whose kill condition fires must vote OPPOSE (or file FATAL, for the Short-Seller) and say which row pulled the trigger.

### R2: Challenges (mandatory, typed, graded by how serious)

Each seat files **at least one** challenge (an objection) against a DIFFERENT seat. Challenging yourself does not count. Format:

```
CHALLENGE / {FROM} challenges {TO}: [TYPE] [SEVERITY]
  "<the challenge, max 3 lines, the fact in words, citing rows>"
TYPE:      EVIDENCE (the facts say otherwise: your row shows something else) |
           LOGIC (doesn't follow) | BLINDSPOT (blind spot: your lens cannot see this) |
           FRAME (wrong question: you answered a different one)
SEVERITY:  FATAL (breaks the case) | MATERIAL (serious: changes the stance) | MINOR (weakens it)
```

Print the type and severity with their plain labels (see "How the result reads"), not the capitalized tokens.

Forcing functions, all hard:

- **Challenge quota:** zero challenges = failed run. Rerun R2 with the header "you are paid to disagree".
- **Severity floor:** at least one challenge across the table must be MATERIAL or FATAL. All-MINOR means the debate was for show; rerun R2.
- **Their best point before any reply** (applies in R3, declared here; the method's name for it is the steelman): no seat may answer a challenge without first restating the challenger's strongest version of it in one line and citing a row. A reply without it is invalid and is struck.
- **Staleness is a first-class axis:** "your E14 is a quarter old" or "your E10 as-of predates the earnings report" are legitimate MATERIAL challenges. Check the As-of column before trusting a row in a fight.
- **Escalate down the tiers to settle evidence fights.** When two seats disagree about a fact, the tiebreak is a lower tier, appended as a new row:

```
Escalation 1  "Insiders are buying" [E12] vs "those are option exercises":
              read the transactionCode already in the insider payload (P = open-market, M = exercise);
              if absent or contested, consult a supplied Form 4 or record UNRESOLVED. Append any supplied finding as E20.
Escalation 2  "Revenue is accelerating" (press narrative) vs the filings:
              call the quarterly revenue series (/fundamentals/history?timeframe=quarterly, [E2 source]);
              is the LATEST reported quarter accelerating? Append. EDGAR only if the dispute is about a line item.
Escalation 3  "Sentiment is bullish" [E10] vs "that's stale":
              re-read E10's as-of; if it predates a material event [E16, E20], the freshness challenge stands.
```

SentiSense gives the read, including signals and reported statements. Supplied EDGAR material can provide the audit trail underneath it; without that material, the Chair records the dispute as UNRESOLVED (printed as "unsettled") and caps confidence.

### R3: Replies (their best point first, then the answer)

Every seat answers every MATERIAL and FATAL challenge against it:

```
REPLY / {SEAT} answers {FROM}: [CONCEDE | DEFEND | PARTIAL]   (printed: Concedes / Stands firm / Partly concedes)
  THEIR BEST POINT (the STEELMAN): "<the challenger's strongest version, one line, cited>"
  ANSWER:     "<max 3 lines, the fact in words, cited>"
  STANCE NOW: <same or moved, one of the five>
```

**Conceding is scored as a win.** A seat that moves its stance on evidence is doing the job; a seat that never moves regardless of input is a broken instrument. (This is Bayesian updating taught by structure.) MINOR challenges may be answered in one line or accepted silently.

---

## STEP 5: The verdict (R4, the Chair)

The Chair is **neutral and is not one of the investor personas**. In Mode A the main agent chairs; in Mode B you put on the Chair hat last, after a hard reset. Before filling the verdict, the Chair runs one **Invert pass** (printed as "How this could be wrong"): "If this verdict is wrong, why? Which cited row is weakest or stalest? Is the committee pattern-matching a story? Overweighting the latest quarter?" One paragraph, kept in the transcript.

**Devil's-advocate backstop:** if all seats landed on the same side (all SUPPORT/LEAN-SUPPORT or all OPPOSE/LEAN-OPPOSE), the committee has failed its diversity function. The Chair must write the strongest opposite case itself, citing rows, before the verdict. Unanimity without a written counter-case is an invalid run.

The verdict opens with the bottom line and puts the detail after it. The BOTTOM LINE is the committee's center of gravity written for a first-time investor: two or three plain sentences saying what the committee concluded about the thesis, the main reason, and the main risk. No row ids, no stance tokens, no method words inside it; its citations go on the line below.

```
### COMMITTEE VERDICT: {TICKER}
BOTTOM LINE: <2-3 plain sentences: the conclusion on the thesis, the main reason, the main risk>
  (rests on: [E_][E_])
CONFIDENCE: HIGH | MED | LOW, because <one plain reason, e.g. "4 of 5 seats lean the same way">
THE THESIS WE TESTED: "<the Step 0 thesis>"
HOW THEY VOTED: For _ / Leaning for _ / Leaning against _ / Against _ / Pass _
BEST CASE FOR (from {seat}): <one line, the fact in words> [E_]
BEST CASE AGAINST (from {seat}): <one line, the fact in words> [E_]
WHERE THEY SPLIT: <the ONE question the table disagreed on, in plain words, e.g. "whether today's price already pays for the growth">
WHO DISAGREES AND WHY (mandatory, never left out):
  {seat}: <one line, the fact in words> [E_]
WHAT TO WATCH (what would settle it, from the seats' change-my-mind lines, most decisive first):
  1. <what, where it comes from, when it lands (e.g. the next quarterly report, due around the next earnings date [E16])>
  2. ...
WHAT WE DON'T KNOW: <the missing facts that mattered, plus any unsettled disputes>
RUN NOTES: mode A | B; seats <names>; evidence <n rows filled, m not available>
This is educational analysis of a thesis, not investment advice.
```

A bottom line that reads well: "The committee leans against the idea that {T} is a good 3-5 year holding at today's price. The business turns its profits into real cash, but the price already assumes several more years of fast growth. The main risk is that growth slows while the stock is still priced for it." One that fails: "Center of gravity: superb cash engine vs multiple [E5][E9], LEAN-OPPOSE 3-2."

**Confidence is deterministic, not vibes:**

- **HIGH**: at least 2/3 of voting seats on the same side AND the bottom line rests on at least two Tier P or D1 hard rows.
- **MED**: a split vote, or key support rows are soft, stale, or secondary-sourced.
- **LOW**: split on THE key question, or the ledger is thin on the rows the thesis needs.
- **Caps:** most Tier P statement rows `[NOT AVAILABLE]` caps at MED (with a key this should be rare: the two fundamentals calls fill E2-E9, so a capped run means coverage genuinely came back empty). An UNRESOLVED evidence escalation on a load-bearing fact caps at MED. Both caps get named in WHAT WE DON'T KNOW.

Who disagrees and why, and the exact evidence that would settle it, are the signature of the product. A professional committee's value is the bear in the room and the unresolved crux; never trade them for a cleaner-looking answer.

---

## STEP 6: The Pre-Flight Checklist (fail-closed gate)

Run last, before showing the user anything:

```
[ ] Every number in the output traces to a ledger row ID.
[ ] No [NOT AVAILABLE] row was used downstream as if it had a value.
[ ] Every fundamental row states its fiscal period (watch FY ends: NVDA Jan, AAPL Sep).
[ ] Every row shows its as-of; nothing is called "real time", including price.
[ ] Every seat voted from the single stance vocabulary and cited at least one row.
[ ] At least one MATERIAL or FATAL challenge was filed; who disagrees is shown, not smoothed away.
[ ] Every reply opened with the challenger's best point.
[ ] The best case for AND the best case against are real, attributed, and cited (no straw men).
[ ] The output opens with the plain bottom line: 2-3 sentences, no row ids, no method words.
[ ] Every claim states its fact in words; row ids appear only as trailing citations.
[ ] Printed labels are the reader's (For / Against, Challenge, Reply, Their best point), not protocol tokens.
[ ] No buy/sell instruction, no price target, no allocation advice, anywhere.
[ ] The educational disclaimer line is present. No em dashes in the output.
```

**If either of the first two boxes fails, do NOT show the output.** Re-derive the offending claims from the ledger and run the gate again. Fabrication is the one unrecoverable defect; everything else is style.

---

## Execution modes

Mode selection is the first orchestration decision, made at Step 0 via a detection gate: **if the host's tool list contains a tool that runs an independent agent or prompt** (`Task`, `dispatch_agent`, `spawn`, `spawn_agent`, `run_subagent`, `agent`, or similar), use Mode A; otherwise Mode B. When unsure, Mode B. Record the mode in the verdict's RUN NOTES line for transcript honesty.

### Mode A: native sub-agent fan-out (the upside)

For hosts with real sub-agents. Parallelize within a round, serialize across rounds; the main agent is the blackboard and the Chair.

1. Fill the ledger (main agent), pin it.
2. R1: fan out N parallel persona sub-agents, each receiving ONLY the ledger + its own worksheet + the thesis. True independence: no seat sees another's output.
3. R2: fan out again; each seat receives the ledger + all R1 theses + its own worksheet, returns typed objections.
4. R3: fan out to the objected-to seats with their objections.
5. R4: main agent chairs, runs the invert pass, fills the verdict.

### Mode B: sequential "wear each hat" (the floor; every host can do it)

One model plays each role in sequence. The discipline that makes it work:

- **Hard reset between seats.** Before each R1 turn, write literally: `You are now ONLY {seat}. Forget the previous seat's conclusion. Re-read the ledger and your worksheet fresh.` Then re-pin the thesis line. Without the reset, seat 2 anchors on seat 1 and the committee collapses into one voice with costumes.
- Fill each seat's R1 completely before starting the next.
- In R2, adopt each seat again with the header "you are paid to disagree" and file its objections.
- Chair last, after one more hard reset.

### The degradation ladder

```
A (parallel, 5 seats)  ->  B full (sequential, 5 seats)  ->  B lite (3 seats + Chair)
                                                          ->  minimum (1 bull + 1 bear + Chair)
```

**What degrades: seat count and parallelism. What NEVER degrades: the four rounds, the mandatory challenge, the "who disagrees and why" section, the pre-flight gate.** The analog of "degrade to less data, never invented data" is: degrade to fewer voices, never to fake agreement.

**The lite path (small context windows, local models).** 3 seats: Quality Owner, Short-Seller, Macro Trader (maximum lens diversity per token: business quality, red flags in the numbers, macro). Trim the ledger to E1-E12 + E18. One challenge per seat in R2, a one-line "their best point" in each R3 reply. Keep every template otherwise intact. Rough budget: full committee runs ~2.5-3.5k output tokens across rounds; lite runs ~1.2-1.5k. If even lite does not fit, run minimum (the Quality Owner as bull, the Short-Seller as bear, Chair) and say so in the verdict's RUN NOTES line.

**API cost:** a full ledger is ~10-14 SentiSense calls (the 8-12 D1 calls plus the two fundamentals calls). Within the free tier's 30/min with room to spare; one committee run costs about 1-2% of the free monthly quota. Supplied FRED or EDGAR material adds no SentiSense calls.

---

## Worked example (abbreviated; all numbers illustrative)

A compressed excerpt showing the shape, in the order the reader sees it: the verdict first, then the working. Every number below is marked (ill.) = illustrative; never reuse them as facts.

```
### COMMITTEE VERDICT: NVDA
BOTTOM LINE: The committee is split on whether NVDA is a good 3-5 year holding at today's price.
  The business turns its profits into real cash, but the price already assumes years of fast
  growth, and company insiders have been selling, not buying. The main risk is that growth slows
  while the stock is still priced for it.
  (rests on: [E5][E9][E12])
CONFIDENCE: MED, because the vote is split 2-2 and one dispute about the insider sales is unsettled.
THE THESIS WE TESTED: "At today's price, NVDA is attractive for a 3-5 year holder."
HOW THEY VOTED: For 0 / Leaning for 2 / Leaning against 2 / Against 0 / Pass 1
BEST CASE FOR (Quality Owner): free cash flow of $60.9B (ill.) closely tracks reported profit, so the earnings are real. [E3][E5]
BEST CASE AGAINST (Short-Seller): at about 21 times sales (ill.), the company must keep growing very fast just to justify today's price. [E2][E9]
WHERE THEY SPLIT: nobody doubts the earnings are real; they disagree on how much future growth the price already pays for.
WHO DISAGREES AND WHY:
  Short-Seller: insiders sold 7 times and bought none in 90 days (ill.), which it reads as a warning sign. [E12]
WHAT TO WATCH: 1. The filing codes on those insider sales, to see whether they were scheduled pay or
  real selling. 2. Whether cash flow keeps pace with profit in the next quarterly report (due
  around the next earnings date [E16]). 3. What big funds did last quarter, once that data settles. [E14]
WHAT WE DON'T KNOW: last quarter's fund holdings are still pending; the insider-sales dispute is unsettled
  (confidence capped at MED).
RUN NOTES: mode B; seats Quality Owner, Inverter, Story Checker, Macro Trader, Short-Seller; evidence 17 filled, 3 not available (ill.)
This is educational analysis of a thesis, not investment advice.

EVIDENCE (excerpt)
| E1  | Price + day    | $172.40 / +1.1% (ill.) | 15-min delayed | D1 | SS /stocks/price |
| E2  | Revenue FY     | $130.5B (ill.)  | FY2025, ended Jan 2025 | P | SS /fundamentals/history |
| E5  | FCF            | $60.9B (ill.)   | FY2025             | P  | SS /fundamentals/history |
| E9  | P/E, P/S (TTM) | 46x / 21x (ill.)| TTM to Jul 2025 (ill.) | P | SS /fundamentals |
| E10 | Sentiment      | +0.41, rising (ill.) | as-of 09:30 ET (batch) | D1 | SS |
| E12 | Insider 90d    | 0 buys / 7 sells, $48M (ill.) | 90d  | D1 | SS |
| E14 | 13F motion     | [NOT AVAILABLE] (quarter pending)    | D1 | SS |

OPENING CASE / Quality Owner (is this a durable business at a sensible price?): Leaning for
  1. Free cash flow closely tracks net income, so the profits are real cash. [E3][E5]
  2. The price is rich for a world with a 5% ten-year Treasury yield (ill.). [E9][E18]
  SIGNATURE QUESTION: comfortable owning it if the market closed for 10 years? Yes on the business, uneasy on the price.
  WHAT WOULD CHANGE MY MIND: "I flip if free cash flow falls below ~70% of net income for 2 quarters." [E3][E5]

OPENING CASE / Short-Seller (hunts for what could go wrong): Leaning against
  1. Insiders sold 7 times and bought none in 90 days while the stock was rising. [E12]
  2. At 21 times sales, the growth REQUIRED just to hold today's price is extreme. [E2][E9]
  WHAT WOULD CHANGE MY MIND: "I flip if insiders start buying and the price falls below ~12 times sales."

CHALLENGE / Short-Seller challenges Quality Owner: the facts say otherwise, serious
  "Your cash-machine case ignores who is selling: insiders, 7 sales to 0 buys. [E12]"
CHALLENGE / Quality Owner challenges Short-Seller: wrong question, serious
  "Insider sales at giant companies are mostly scheduled pay; without the filing codes you cannot
   read a direction into those sales. [E12] Check the codes or drop the point."
  -> Checking the filing codes: not available on this host. Recorded as unsettled; confidence capped at MED.

REPLY / Short-Seller answers Quality Owner: partly concedes
  THEIR BEST POINT: "Scheduled pay sales say nothing about the outlook; my 7-to-0 count may be noise. [E12]"
  ANSWER: "Granted on how the sales work, but zero open-market buys in 90 days at any price is still one-directional. [E12]"
  STANCE NOW: Leaning against (unchanged).
```

Note what the example demonstrates: the bottom line comes first and reads without the evidence table, every claim says its fact in words before citing a row, an honest `[NOT AVAILABLE]`, an escalation the host could not complete recorded as unsettled with the confidence cap applied, a partial concession scored as normal work, and a split verdict delivered as a split, not smoothed into mush.

---

## Glossary (define at point of use; here for reference)

| Term | Meaning |
|---|---|
| TTM | Trailing twelve months: the last 4 reported quarters summed |
| FCF | Free cash flow: operating cash flow minus capital expenditures |
| Owner earnings | The cash an owner could extract without harming the business; FCF is the practical proxy |
| FCF yield | FCF / market cap; the cash return the business earns on its price |
| P/E, P/S | Price to earnings, price to sales; P/S is harder to game because revenue is harder to manage than EPS |
| PEG | P/E divided by growth rate; a rough "am I paying for growth I'm not getting" check |
| Margin of safety | Buying below estimated value so being somewhat wrong still works out |
| Moat | A durable competitive advantage: pricing power, switching costs, network effects, cost advantage, brand |
| Polarity | The sentiment scale in [-1, +1]; sign is direction, magnitude is conviction; never map to 0-100 |
| SentiSense Score | SentiSense's proprietary read on how bullish or bearish the market is on a stock, weighted by how actively it's discussed; unbounded, report as-is, never normalized |
| 10-K / 10-Q / 8-K | Annual report / quarterly report / material-event filing with the SEC |
| Form 4 | Insider transaction filing; code P = open-market buy, S = sale, A = award, M/exercise = options |
| 13F | Quarterly institutional holdings disclosure (45-day lag; always a quarter behind) |
| DEF 14A | Proxy statement: executive compensation and incentives live here |
| Dilution | Share count rising; each share owns less of the business |
| Basis point | 0.01%. 50bp = half a percent |
| Short-seller | An investor who profits when a stock falls, so the seat that hunts hardest for what could go wrong |
| Thesis | The one claim the committee votes on, for example "at today's price, this stock is attractive for a 3-5 year holder" |

---

## Fetch Reference

Parameters and full schemas: the `sentisense` skill, or https://sentisense.ai/skill.md.

```
RESOLVE     GET /api/v1/kb/entities/search?q={name}&type=company&limit=5   (bare array, best first; take the first non-null ticker; type=etf for funds)
FUNDAMENTALS
            GET /api/v1/stocks/fundamentals/history?ticker={T}&timeframe=annual|quarterly&limit=N
                                                       (periods[], newest first; E2-E5, E8)
            GET /api/v1/stocks/fundamentals?ticker={T}&timeframe=quarterly
                                                       (flat latest quarter; E6, E7, E9 trailing ratios, marketCap)
            GET /api/v1/stocks/fundamentals/current?ticker={T}
                                                       (flat; peTTM, psTTM, epsTTM, revenueTTM; E9 cross-check only)
PRICE       GET /api/v1/stocks/price?ticker={T}          (flat; currentPrice, changePercent; timestamp is serve time)
            GET /api/v1/stocks/prices?tickers=A,B,C
            GET /api/v1/stocks/chart?ticker={T}&timeframe=1M|3M|6M|1Y
            GET /api/v1/stocks/{T}/profile
            GET /api/v1/stocks/popular
SENTIMENT   GET /api/v2/metrics/entity/{T}/metric/sentiment?startTime={epochMs}&endTime={epochMs}
            GET /api/v2/metrics/entity/{T}/metric/sentisense
            GET /api/v1/stocks/{T}/sentiment           (envelope data; Score, 30d fallback, mentions)
INSIDER     GET /api/v1/insider/trades/{T}?lookbackDays=N             (envelope data[])
            GET /api/v1/insider/cluster-buys?lookbackDays=N           (envelope data[])
CONGRESS    GET /api/v1/politicians/filings/{T}?lookbackDays=N        (envelope data[])
            GET /api/v1/politicians/activity?lookbackDays=N           (envelope data[])
            GET /api/v1/politicians/member/{slug}                     (trades at data.recentTrades[])
INSTITUTION GET /api/v1/institutional/quarters                         (bare array; skip pending:true)
            GET /api/v1/institutional/holders/{T}?reportDate={Q}&limit=N   (envelope data.holders[]; pass limit)
ANALYST     GET /api/v1/analyst/{T}/consensus         (envelope data)
            GET /api/v1/analyst/{T}/actions?lookbackDays=N            (envelope data[])
            GET /api/v1/analyst/{T}/estimates          (data.estimates[0] + data.surprises[])
            GET /api/v1/analyst/activity?lookbackDays=N&actionTypes=UPGRADE,DOWNGRADE,INITIATE  (rating changes only)
INSIGHTS    GET /api/v1/insights/stock/{T}             (envelope data[]; generatedAt is seconds)
            GET /api/v1/insights/market                (envelope data[])
CALENDAR    GET /api/v1/calendar/earnings?ticker={T}   (data.earnings[]; an empty window still returns a metadata block with windowStart/windowEnd)
OPTIONS     GET /api/v1/options/overview               (end-of-day radar board, stocks only)
            GET /api/v1/stocks/{T}/options/summary     (envelope data)
            GET /api/v1/stocks/{T}/options/history?window=1y|2y|5y
```

## Agent Tips (shape gotchas worth memorizing)

- **Wrap vs flat varies by endpoint.** Read FLAT (no `.data`): `price`, `prices`, `chart`, `popular`, `market-mood`, `stocks/{T}/profile`, `descriptions`, and `metrics/entity/{T}/metric/*` (bare arrays). `institutional/quarters` is a bare array (take the first entry whose `pending` is not true). These are wrapped in `{ isPreview, previewReason, data }`: `insider/*`, `analyst/*`, `insights/*`, `politicians/*`, `institutional/holders`, `stocks/{T}/sentiment`, `stocks/{T}/options/summary`, and `calendar/earnings` (read `data.earnings[]`). When unsure: `Array.isArray(raw) ? raw : (raw?.data ?? raw)`.
- **`isPreview:true` is not an error, and it is not the whole window.** Free returns real data, truncated: compare `totalCount` with the rows returned, label a slice as a slice ("newest 5 of 61"), and never read absence or a window total from it (see "Free-tier previews"). Mention PRO in one line when the truncation materially limits the answer, which it does whenever a row needs the full window.
- **Metric scalar path:** the flat `series[i].value`, present on every point of every metric series and holding the reading. Prefer it over the nested `metricValue`, whose depth varies by metric type: `sentiment`, `sentisense` and `social_dominance` nest at `metricValue.value.value` because `metricValue.value` is itself a dict, while `mentions` is a count metric whose integer sits at `metricValue.value`, so `metricValue.value.value` throws on it. Latest reading = last element. Polarity in [-1, 1]; the SentiSense Score is unbounded, report as-is.
- **Insider field is `transactionType` (`BUY`/`SELL`)**, congress uses `PURCHASE`/`SALE`. Exclude `AWARD`/`GIFT`/`EXERCISE` from tallies (grants and exercises can carry very large `totalValue`), and drop `transactionCode` `F` (tax withholding on vesting) even though it arrives typed `SELL`.
- **`market-mood` nests the composite under `market`**; `sectors` is a dict whose GICS labels have historically overlapped, so dedupe defensively if a pair appears.
- **Options are end-of-day chain aggregates, not order flow.** `/options/*` gives put/call volume and OI, an ATM IV term structure, 25-delta skew, OI walls with max pain, and unusual contracts, each ranked as a percentile of that ticker's OWN trailing history (`ivRank1y`, `pcVolPctl1y`, `skewPctl1y`), `asOf` the prior session. Read it as positioning context, never as live sweeps or dealer books. The `/options/overview` board is stocks-only; ETFs (`SPY`, `QQQ`, `TLT`, sector `XL*`) are covered but reachable only via `/stocks/{T}/options/summary`.
- **Resolve names, then call.** A company name in the ask goes through `kb/entities/search` before any other call (see Authentication); take the first match with a non-null `ticker`. An empty result is a resolution problem, not a coverage gap.
- **Don't hallucinate endpoints.** No real-time options order flow or sweeps feed (the `/options/*` endpoints above are end-of-day), no dark pool, no `/congress` (it's `/politicians`). SentiSense DOES serve the financial statements: `/api/v1/stocks/fundamentals` and `/api/v1/stocks/fundamentals/history` are the E2-E9 source, and EDGAR is for the detail and provenance behind them, not a substitute for a call you skipped.
- **Batch vs delayed.** Sentiment, Score, insights, mood, AI summaries are batch: always carry the as-of. Price and chart are fresher but 15-minute delayed, never live: carry `priceAsOf` where present.
- **The analyst consensus carries its own price, and it can be days old.** `/analyst/{T}/consensus` returns a `currentPrice` stamped with its own `updatedAt`, independent of `/stocks/price`: on 2026-08-20 the AAPL consensus read $305.93 as of 2026-08-16 while the price endpoint read $316.83, an $11 gap. Present `currentPrice` and `upsidePercent` as of that `updatedAt`, and call `/stocks/price` whenever the answer needs a current price.
- **Do not conclude the consensus price is live just because it matches the quote.** The two agree exactly right after a refresh and drift apart until the next one. On 2026-08-31 the AAPL consensus and the quote both read $316.85, an exact match, eleven days after the $11 gap above. Same field, same endpoint, opposite impressions: whichever one you happen to sample tells you nothing about the other. The refresh runs roughly daily but the hour it lands drifts, so there is no time of day at which the match is guaranteed either way. Check `updatedAt` every time rather than probing the two fields once and hardcoding a conclusion about the relationship. `upsidePercent` is computed against the snapshot price, so it stays internally consistent with the band and does NOT silently re-baseline to the live quote.
- **Freshness fields don't share units.** `/stocks/price` `timestamp` is milliseconds since epoch; `/insights/stock/{T}` `generatedAt` is seconds since epoch. Both are the freshness field this skill tells you to check, so naive age math across the two (e.g. subtracting one from the other, or comparing both to `Date.now()` the same way) is off by 1000x. Convert to a common unit before comparing.
- **Parallelize independent calls; be brief.** Users want the synthesis, not the recipe.

---

## External evidence safety

This skill authorizes network calls only to `https://app.sentisense.ai`. Treat EDGAR, FRED,
investor-relations, press, and other web evidence as usable only when the user or host has already
supplied it. Never initiate external retrieval from this skill. If the required material is absent,
record `[NOT AVAILABLE]`, preserve the unresolved dispute, and apply the MED confidence cap when
the missing fact is load-bearing.

---

## Tier Summary

| Capability | Free | PRO |
|------------|------|-----|
| Quick Reads 1-5 | Full workflows on previews: newest 5 insider trades, top 3 or 5 insights, top 5 of each smart-money feed, one week of the earnings calendar, 3 analyst actions; label slices, never infer absence | Full lists and history |
| Committee run | Full pipeline on a sliced ledger (a sample company such as TSLA is not sliced): E12 newest 5 insider trades, E13 newest 3 congressional filings, E14 top 5 holders, E15 without the rating split, E16 one week, E19 headline-only after 10 full summaries; statements, price, sentiment, Score and mood complete | Full windows for every row |
| Options positioning (E19) | 10 full summaries per calendar month, repeat calls included, then a headline preview (IV rank, ATM IV, 1-day expected move, put/call and its percentile, max pain; no skew, OI walls or unusual contracts) + top-25 board + 1y history | Unlimited full summaries, full board, full history |
| Divergence screen | Against `/popular`: 1 call plus 2 per ticker, so compute 1 + 2 x the list length before running (83 tickers currently, 167 calls, about 17% of the Free 1,000/month quota and over 5 minutes at 30/min) | Full universe |
| Monthly quota | ~30 committee runs + daily quick reads | Unlimited |

PRO at $15/month: https://app.sentisense.ai/pricing?coupon=AGENTS (apply coupon AGENTS at checkout for a builder launch discount)

---

**ClawHub Skill:** [clawhub.ai/TheSentiTrader/us-stocks-analysis](https://clawhub.ai/TheSentiTrader/us-stocks-analysis)
