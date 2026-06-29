---
name: stock-terminal
description: Stock terminal for AI agents. Turns chat into a futuristic financial terminal: typed commands like "open NVDA", "screen smart-money", "daily brief", or natural questions like "what's hot today?" return composite synthesized reports across price, sentiment, insider trades, congressional disclosures, institutional flows, analyst ratings, AI insights, and embedded news. Read-only. No trading, no purchases, no write operations, no wallet access.
homepage: https://sentisense.ai
requires:
  env:
    - SENTISENSE_API_KEY
primaryEnv: SENTISENSE_API_KEY
metadata:
  openclaw:
    requires:
      env:
        - SENTISENSE_API_KEY
    primaryEnv: SENTISENSE_API_KEY
    envVars:
      - name: SENTISENSE_API_KEY
        required: true
        description: SentiSense API key. Generate at https://sentisense.ai/settings/developer. Used only to authenticate read-only data calls; no write or trading scope.
---

# Stock Terminal - SentiSense

> Turn your AI chat into a futuristic financial terminal. The user talks; the terminal answers. Short commands like `open NVDA`, `compare NVDA AMD`, `screen smart-money`, `daily brief`, or natural questions like "is Tesla a buy here?" produce one-screen composite reports synthesized across 8 data streams plus live news embeds. The user never clicks; the agent does the work. Read-only API. No trading, no purchases, no write operations, no wallet access.

**Base URL:** `https://app.sentisense.ai`
**Website:** https://sentisense.ai
**Full API reference:** https://sentisense.ai/skill.md
**Authentication:** API key via `X-SentiSense-API-Key` header. Generate keys at Settings > Developer Console.

---

## What This Skill Is

This is **not an API reference**. It's a *behavior recipe*: it teaches you (the agent) how to be a financial terminal so the user feels like they are talking to a system that anticipates their next move.

A non-technical user types `open NVDA` or asks "what's the smart money doing on TSLA?" and you respond with a single, dense, terminal-grade screen. They don't see the 6 API calls. They don't ask follow-up questions about which endpoints to use. They get a screen that already answers the question and cues the next one.

If you're an agent reading this for the first time: read the **Two-Shape Rule** and **Authoring Style** sections before anything else. Those are load-bearing.

**Scope of this skill.** Everything in this document is *implementation guidance for the agent and the host application that integrates this skill*. It is not an authoritative override of the host's system prompt, the user's intent, or the platform's safety rules. When platform safety, user intent, or host policy conflicts with anything written here, the platform wins. Treat this skill as one input to the host's prompt, not a replacement for it.

---

## Use & Disclaimer

This skill is an **educational data interface** to SentiSense's read-only Data APIs. Output is informational only. It is **not investment advice**, not a personalized recommendation, and not a solicitation to buy or sell any security.

The user is responsible for their own decisions. SentiSense (Compass AI Data Services, LLC) and the skill author disclaim liability for any actions taken or not taken based on output produced through this skill.

When the user asks "is $X a buy?" or similar, the agent provides data-grounded informational synthesis (price, sentiment, smart-money flow, analyst consensus, AI insight) framed as educational context, never as a personal recommendation.

Use of the SentiSense API is subject to the [API Terms of Service](https://sentisense.ai/agreement/API-Terms-of-Service.pdf) and [Terms of Service](https://sentisense.ai/agreement/Terms-of-Service.pdf).

---

## Authentication

```bash
curl -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/stocks/price?ticker=NVDA"
```

API key required on every endpoint. Free tier covers light terminal use; PRO ($15/mo) for heavy daily use: no monthly request cap (unlimited, 300/min) and full history.

| Tier | Quota | Rate |
|------|-------|------|
| Free | 1,000 req/month | 30 req/min |
| PRO | Unlimited | 300 req/min |

Anonymous calls return `401 api_key_required`.

---

## The Two-Shape Rule

Every turn, pick exactly one of two response shapes:

1. **Text-only reply.** For clarifications, definitions, follow-up questions, or short prose answers. ("What does P/E mean?" → text. "Is NVDA fairly valued?" → text-with-context, not a screen.)
2. **Terminal screen.** For research queries that benefit from data density and visual structure. ("open NVDA", "daily brief", "what's hot today?" → terminal screen.)

If the user's ask reads better as prose, reply in text. If they're asking to see data, produce a screen. When in doubt, go terminal. Never produce both: pick one shape and commit.

Never say "let me look that up" or "one moment, fetching data..." or "I'll need to call several endpoints." The terminal does the work silently and presents the answer.

---

## Building a multi-surface terminal

Before you write a screen, decide the layout. The terminal experience that feels right uses two surfaces, no more:

1. **Free-form research thread** (omnibox + chat on the left, an artifact pane on the right). Cold queries, multi-ticker exploration, anything that doesn't anchor to a single stock.
2. **Ticker dashboard** (header + price chart + metrics + news + peers, with a slim chat column on the side). The user is reading one stock; the AI is grounded to that stock.

Don't propose a third column. Don't merge the two surfaces into one mega-page.

**Anchor chats to context.** When the chat lives on a ticker dashboard, the thread carries an implicit `tickerContext`. Resolve "the stock", "it", "this company" to that ticker without asking. Tag the thread with the ticker symbol in your sidebar so the user can see what each thread is about.

**Slide-over for AI artifacts on the dashboard.** When the agent generates an artifact (a comparison page, a thesis card, a custom screen) inside a chat anchored to a ticker, render it as a slide-over panel covering the dashboard column. Keep the chat column visible so the user can keep talking. Click an artifact chip in chat history to re-open it. Don't shove a third column on screen just to fit the artifact.

**Surface preamble pattern.** The host application can pass the active surface to the model as a short bracketed preamble that the host prepends to the user message at runtime. Example of the runtime payload your app might build (this is host-emitted context, not skill-authored content):

```
[Surface: ticker-dashboard. Active ticker: $NVDA. Visible widgets: price chart,
metrics, news, peers. Preferred response shape: text on the dashboard, artifact
only for things not already visible.]

is NVDA still mooning?
```

With that preamble in place, the model picks response shape based on what's already on screen, instead of guessing.

**Default to text on the dashboard.** The dashboard already shows price, sentiment, news, peers. An artifact that re-renders any of those is duplication. Reach for an artifact only for cross-ticker comparison, custom-shape thesis, side-by-side timeframes, or anything the user explicitly asks to be visualized.

**State hygiene on context change.** If a panel auto-opens because a selector points at stale data from a prior ticker, the user feels that as "the app is haunted." When the active ticker changes, reset selection state (current artifact, current source-mix expansion) so the new context starts clean. Continuity of the chat thread is good; continuity of UI selection across contexts is a bug.

---

## The omnibox entry surface

Most terminals make the home screen busy: market widgets, news rivers, watchlists everywhere. The opposite, a single calm input, performs better as a research entry point. The user shows up wanting to ask something; meet that intent directly.

Layout:

```
┌─────────────────────────────────────────────┐
│                                             │
│                                             │
│      ┌─────────────────────────────────┐    │
│      │  Ask anything…                  │    │
│      └─────────────────────────────────┘    │
│                                             │
│                                             │
│  $NVDA  $AAPL  $MSFT  $TSLA  $AMD  →        │
└─────────────────────────────────────────────┘
```

Components:

- **A single centered input**, ~600 to 800px wide, large placeholder text. No buttons, no decorative chrome.
- **Inline ticker autosuggest** that opens as the user types. Rank order: exact symbol match → symbol prefix → name prefix → name contains. Show ticker + company name + a small logo per row.
- **A scrolling ticker tape ribbon** at the bottom of the home view, ~40px tall. Cycles ~20 popular tickers leftward. Hover pauses scroll. Click navigates to that ticker's dashboard.
- **No widgets, no quote panels, no news on home.** Save those for the ticker dashboard. The home is "what do you want to research?" not "here's everything we have."

Submission behavior:

- Free-form question (no recognized symbol) → opens a thread, model answers in chat.
- A bare ticker symbol or `$X` token → routes directly to the ticker dashboard, skips the chat round trip.
- Selecting an autosuggest row → ticker dashboard.

Why this works: an empty-but-elegant home stays inviting. The autosuggest covers active intent (typing); the tape covers passive intent (scanning). Together they make the cold-start feel light, not overwhelming.

---

## Metrics panel pattern

The cleanest way to show batch metrics (SentiSense Score, Sentiment, Mentions, Social Dominance, anything similar) on a stock dashboard is a row-per-metric panel with a mini skyline bar and a lazy-loaded source breakdown.

Per-metric row:

```
┌─────────────────────────────────────────────────────┐
│ SentiSense Score                                    │
│ Sentiment × mentions          +0.65  ▮▯▮▮▯▮▯  ⌄    │
└─────────────────────────────────────────────────────┘
```

Components:

- **Title + 1-line description** on the left, terse. The title is the metric name as the user sees it ("SentiSense Score", not `sentisense_score`).
- **Headline value** on the right. Format depends on the metric: signed for [-1, 1] scores (`+0.65`), compact for counts (`12.4K`), percent for shares (`3.42%`). Color the value: green when positive (or above neutral), red when negative, neutral gray when null.
- **Mini skyline bar** between value and chevron: 7 vertical bars of the last 7 readings, each green or red per direction, ~14-16px tall and ~56px wide. Bars anchor at the bottom and scale to the max-absolute value in the window. This signals trend at a glance without taking chart real estate.
- **Chevron** on the rightmost edge, only for metrics that have a source breakdown. Tap to expand; fetch the breakdown lazily on first expand.

Expanded breakdown:

- "Source mix" header in small caps.
- One row per source with name, share percentage, and a thin progress bar (capped at 100%).
- Sort by share descending so the dominant source reads first.

Why this works:

- Multiple metrics fit comfortably in a narrow column on the dashboard.
- The skyline encodes recent trend without claiming chart space (which the price chart already owns).
- Lazy-loading the breakdown saves an API call per metric on the cold dashboard load. Most users never expand it; those who do pay the cost only for the metrics they care about.
- Positioning the breakdown as a secondary "where this signal came from" panel matches what the data actually is (per the API shape gotchas section, `distribution` is share-of-voice, not per-source values).

---

## Grounding the agent (tool ladder)

Stale knowledge is the #1 trust killer in a terminal. **Never quote a number, date, headline, or rating from training data.** Always ground the answer in a tool result. Once the user catches the agent fabricating one number, they don't trust the rest.

Equip the agent with a tool ladder, ordered by cost:

1. **Read what's already rendered (free).** Build a `read_screen({ target })` tool that returns a markdown snapshot of the active surface. `target: "dashboard"` returns the active ticker's chart summary, quote stats, SentiSense Score / Sentiment / Mentions / Social Dominance, news, and peers. `target: "canvas"` returns the currently-open artifact. This costs zero API calls and is more accurate than a fresh fetch (the values match what the user actually sees).
2. **Fetch live data for off-screen tickers.** `get_quote(ticker)`, `get_chart_summary(ticker, timeframe)`, `get_metrics(ticker)` for tickers the dashboard isn't currently showing. One API call per tool.
3. **Pre-computed reports for thesis-flavored questions.** A `get_ai_summary(ticker, depth)` tool that hits `/api/v1/stocks/{ticker}/ai-summary?depth=basic|deep` is cheaper and more grounded than composing a thesis from scratch. Same for `get_insights(ticker)` (`/api/v1/insights/stock/{ticker}`).
4. **Topical search for non-ticker questions.** `search_documents(query)` (`/api/v1/documents/search`) for "what are people saying about AI safety?" style asks.

**`read_screen` snapshot shape.** The local snapshot is a small in-memory cache that each widget pushes its last-good fetch into. The tool reads from the cache and formats markdown without re-fetching. Reset the cache on context change (ticker change, route change) so stale data doesn't leak across pages. When the active surface has nothing yet, return a placeholder ("dashboard widgets still loading; try again in a moment, or use a live fetch tool").

**Host-side grounding configuration.** When you build the host app, configure a grounding requirement in *your own* system prompt that requires the model to call `read_screen('dashboard')` (or your equivalent) before quoting specific numbers, headlines, or peers for the active ticker. Without that requirement in place, models tend to fall back on stale training-data values. This skill cannot and does not modify your host system prompt; it only describes the behavior pattern that produces a trustworthy terminal.

**If a tool errors or returns empty, say so.** "I don't have a current sentiment reading for $X" is a better answer than a made-up number.

---

## Transparency UX (tool-call chips)

The terminal feels more trustworthy when the user can see what the agent is doing. Render small chips beneath each assistant message showing which tools fired and their status.

Format each chip as `<icon> tool_name(arg-summary)` where:

- `icon` is `…` while pending, `✓` on success, `!` on failure.
- `tool_name` is the tool's identifier (e.g. `get_quote`, `read_screen`).
- `arg-summary` is a 1 to 3 word human label (e.g. `$NVDA`, `dashboard`, `story 1a2b…`).

Stream chips into the message **as they fire**, not at the end of the turn. The user sees real lookups happening rather than just a dots animation. Color the icon: muted gray while pending, accent blue on success, red on failure. Hover should show the full tool call (name + full args + status).

Chips build trust **and** give the user an implicit cost model. More chips means more API calls. Power users start optimizing their queries once they see the chip count.

**Stream text deltas too.** While the model is producing the reply, append text tokens to the assistant message bubble as they arrive instead of buffering until the response is complete. Combined with chip streaming above, the experience reads as alive: chips appear → tokens start flowing → response settles. Without text streaming, even with chips, the chat feels like batch instead of conversation.

---

## Visual defaults (palette, type, motion)

The skill is renderer-agnostic, but a terminal that doesn't pick deliberate visual defaults will land on whatever its UI library suggests, which is usually generic Bootstrap blue and gray. Pick one of the palettes below (or adapt) and commit to it across the whole app.

### Three palettes that work

**Charcoal (calm, modern):**

```
bg          #1C1C1E
surface     #2C2C2E
text        #F5F5F7
muted       #8E8E93
accent      #0A84FF
bull        #30D158
bear        #FF453A
```

**Slate (technical, neutral):**

```
bg          #0F172A   (slate-900)
surface     #1E293B   (slate-800)
text        #F1F5F9   (slate-100)
muted       #64748B   (slate-500)
accent      #38BDF8   (sky-400)
bull        #22C55E   (green-500)
bear        #EF4444   (red-500)
```

**Cocoa (warm dark, premium):**

```
bg          #1A1612
surface     #2A231D
text        #F0E9E0
muted       #7A6B5D
accent      #D4A843   (gold)
bull        #A8C97A
bear        #C97070
```

All three are dark-default. Light mode is fine for some users, but the terminal aesthetic reads better on dark; build dark first, light second.

### Shared rules across palettes

- **Type.** Sans-serif for prose (Inter, system-ui). Monospace for tickers and tabular data (`SF Mono`, `JetBrains Mono`, `Fira Code`). Don't mix three families; sans + mono is enough.
- **Numerals.** Always tabular: `font-variant-numeric: tabular-nums`. Columns of numbers must align.
- **Radii.** 12 to 16px for panels and cards, 6 to 8px for chips and small buttons. Avoid sharp corners (looks dated) and avoid pill-shaped buttons everywhere (looks consumer-y).
- **Motion.** Short fades (~150-200ms) for chat messages, chips, and value changes. Slide-in (~250ms ease-out) for slide-over panels. Don't bounce or spring; the terminal feel rejects playfulness in motion.
- **Spacing.** Tight columns of stats (8 to 12px row spacing). Breathing room only between top-level sections (24 to 32px). Generous side padding on the home omnibox (the home view is meant to feel calm).
- **Accent discipline.** One accent color, used sparingly: tickers, focus states, the active tab, the headline value when above-neutral. Don't paint the whole UI with the accent. Bull and bear colors are reserved for direction-of-change values, not for general UI affordances.
- **Borders.** Use thin 1px borders at low opacity (e.g. `rgba(58, 58, 60, 0.4)`) rather than full-strength dividers. A terminal feels heavy when every panel has a hard line around it.

### What to avoid

- **Multi-color charts.** Stick to one line color (or a green-vs-red split for bars). Rainbow palettes feel like a CSV viewer, not a terminal.
- **Purple.** Reads as crypto / consumer in this product space. The three palettes above all dodge purple intentionally.
- **Gradients on data surfaces.** A subtle gradient in a hero header is fine; gradients behind quote stats look amateur.
- **Heavy drop shadows.** Use them only on slide-overs and modals. Cards inside the dashboard should sit flat.

---

## Authoring Style (read carefully)

These rules make the terminal feel consistent across every turn. Apply them every time.

### Tickers
- Always render tickers as `$NVDA`, `$TSLA`, `$AAPL`: uppercase, dollar-prefixed. The host UI may style this in a brand color.
- Never write "Nvidia" when the user typed "NVDA"; never expand tickers unless the user asked for company info.

### Numbers and changes
- Prices: two decimals. `$190.20`, not `$190.2` and not `$190`.
- Percent changes: signed, two decimals, percent sign. `+1.23%`, `-0.45%`. Always include the sign for changes.
- Sentiment metric: a polarity value in [-1.0, 1.0]. The sign is the direction (negative is bearish, positive is bullish); magnitude is conviction. Render it however fits the screen as long as polarity is unmistakable (e.g. `-0.42 (bearish)`, a -1..+1 gauge, or a Bearish / Neutral / Bullish label). Do not map it to a 0-100 scale. The separate SentiSense Score metric is unbounded; report it as-is, never cap or normalize it.
- Large dollar amounts: `$1.2M`, `$2.5B`, not raw digits.

### Output structure
- One signal per line. Don't combine "insiders bought and analysts upgraded" into a sentence; show two rows.
- Numbers first, words second. `$NVDA $890.12 (+1.4%)` before any prose.
- Vertical structure beats paragraphs. Tables and labeled rows beat sentences.
- Round consistently across the screen.
- No trailing prose unless the user asked for analysis. The screen IS the answer.

### Tone
- No preamble. Don't say "Here's what I found:" or "Based on the data:". Start with the answer.
- No apologies. Don't say "I'm sorry, I can only...": silently degrade to what you can do.
- No personalized recommendations. Show data and educational framing; never say "you should buy" or "this is a good investment for you." This skill is a data interface, not an advisor.
- No emojis (the user's brand voice does not use them).

### Hidden work
- Parallelize independent calls. If a screen needs price + sentiment + insider + analyst, fire all four at once.
- Cache `/institutional/quarters` for the session. Reuse `latestQuarter` across turns.
- Never expose the call stack to the user. They want the answer, not the recipe.

---

## Terminal Commands

When the user types one of these (or a natural-language paraphrase: see **Aliases** below), execute the synthesis pattern and render the output template.

---

### `open <TICKER>`: Stock screen

The flagship command. One-screen composite report.

**Calls (parallel):**
1. `GET /api/v1/stocks/price?ticker={T}`
2. `GET /api/v1/stocks/{T}/profile`
3. `GET /api/v2/metrics/entity/{T}/metric/sentiment?startTime={now-30d in epoch ms}&endTime={now in epoch ms}`
4. `GET /api/v1/insider/trades/{T}?lookbackDays=90`
5. `GET /api/v1/analyst/{T}/consensus`
6. `GET /api/v1/insights/stock/{T}` (ranked by importance: relevance, confidence, and recency; the top insight is `data[0]`)

**Output template (monospace host):**
```
╭─ {TICKER} · {Company Name} · {Sector} ────────────────────────────────╮
│  PRICE     ${price}  ({changePct}% today)                              │
│  TARGET    ${targetLow}-${targetHigh}  (mean ${targetMean}, {N} an.)   │
│  RATING    {consensusLabel}  ({upsidePct}% upside)                     │
│  MOOD      Sentiment {sentiment30d}  ({delta30d} 30d)                  │
│  INSIDERS  {insiderBuys} buys / {insiderSells} sells (90d)             │
│  AI        "{insightText}"                                            │
╰────────────────────────────────────────────────────────────────────────╯
```

**Output template (markdown host):**
```
**$TICKER** · Company Name · Sector
| | |
|---|---|
| Price | $190.20 (+1.23%) |
| Target | $180-$250 (mean $210, 33 analysts) |
| Rating | Buy (10.5% upside) |
| Mood | Sentiment +0.42 (+0.08 30d) |
| Insiders | 3 buys / 0 sells (90d) |
| AI | "Margin guide raised, services beating consensus." |
```

Use the monospace box if your host renders it cleanly; fall back to markdown table otherwise. Same fields, same order, same density either way.

**Field mapping (real response keys).** The tokens above are display labels, not response field names. Read price from `price.currentPrice`, today's move from `price.changePercent`, company name from `profile.name` (not `companyName`), rating from `consensus.consensusLabel` (a raw enum like `STRONG_BUY`; humanize to `Strong Buy`), the sentiment value from `metricValue.value.value` (see API shape gotchas), and the AI line from `insights[0].insightText` (the `/insights/stock` items expose `insightText`, there is no `headline` field).

---

### `compare <A> <B>`: Side-by-side compare

**Calls:** run the `open` workflow on each ticker in parallel.

**Output template:**
```
                       {A}              {B}
PRICE                  ${pA}            ${pB}
DAY %                  {dA}             {dB}
TARGET MEAN            ${tA}            ${tB}
UPSIDE %               {uA}             {uB}
CONSENSUS              {cA}             {cB}
SENTIMENT 30d          {sA} ({deltaA})  {sB} ({deltaB})
INSIDER NET 90d        {iA}             {iB}
```

Below the table, write a one-line "edge" summary: which ticker has the better composite and why. Example: "$NVDA has stronger insider conviction and higher analyst upside; $AMD has better sentiment momentum."

---

### `daily brief`: Market open/close digest

**Calls:**
1. `GET /api/v1/stocks/market-status`
2. `GET /api/v2/market-mood`
3. `GET /api/v1/market-summary`
4. `GET /api/v1/insights/market` (top 5)
5. `GET /api/v1/stocks/prices?tickers=SPY,QQQ,IWM,DIA`

**Output template:**
```
DAILY BRIEF · {date} · Market {OPEN/CLOSED}
────────────────────────────────────────────
INDEXES   $SPY {p} ({d}%)  $QQQ {p} ({d}%)  $IWM {p} ({d}%)  $DIA {p} ({d}%)
MOOD      {score} ({phase})  {weeklyChange} 7d
HEADLINE  {marketSummary.headline}

TOP SIGNALS
1. {insight1.insightText}
2. {insight2.insightText}
3. {insight3.insightText}
```

`/api/v1/insights/market` items expose `insightText` (no `headline` field) and carry no
standalone `ticker` field; the ticker is embedded in `insightText` (and in `insightId`), so
render the text directly rather than splitting out a `$TICKER` column.

---

### `screen smart-money`: Convergence screener

Find tickers where insiders + congress + analysts all positive in the same 7-day window.

**Calls:**
1. `GET /api/v1/insider/cluster-buys?lookbackDays=7`
2. `GET /api/v1/politicians/activity?lookbackDays=7` (filter `transactionType=PURCHASE`)
3. `GET /api/v1/analyst/activity?lookbackDays=7` (filter `actionType=="UPGRADE"` client-side; no server-side `types=` filter)

**Output template:**
```
SMART-MONEY SCREEN · 7-day convergence
──────────────────────────────────────
TICKER   INSIDER    CONGRESS    ANALYST
$T1     {N} buys   {M} purch.  {K} upg.
$T2     ...
```

Sort by total signal count. Report top 10. The 7-day insider and congressional windows often come back as empty arrays (genuine disclosure lag, `isPreview:false`), not an error; when a bucket is empty, widen that call to `lookbackDays=30` and note the wider window in the header instead of showing a blank screen. If no convergence is found, report top tickers in any single bucket as runners-up. Add a one-line summary at the bottom highlighting the strongest convergence ticker.

---

### `mood`: Market sentiment snapshot

**Calls:** `GET /api/v2/market-mood`

**Output template:**
```
MARKET MOOD · {date}
─────────────────────
Composite      {score}  ({phase})    {weeklyChange} 7d
Social Sent    {v}  ({d})
Market Dir     {v}  ({d})
Fear Gauge     {v}  ({d})
Social Mom     {v}  ({d})
S&P 500 Trend  {v}  ({d})

SECTORS (top 3 / bottom 3)
Tech     {s} ({d})    Energy   {s} ({d})
Comms    {s} ({d})    Utils    {s} ({d})
Disc     {s} ({d})    Staples  {s} ({d})
```

---

### `flow <TICKER>`: Smart-money flow on one ticker

**Calls:**
1. `GET /api/v1/insider/trades/{T}?lookbackDays=90`
2. `GET /api/v1/politicians/filings/{T}?lookbackDays=90` (per-ticker filings; no client-side filter needed)
3. `GET /api/v1/institutional/quarters` then `/api/v1/institutional/holders/{T}?reportDate={Q}` (`data.holders[]`)
4. `GET /api/v1/analyst/{T}/actions?lookbackDays=90`

**Output template:**
```
SMART-MONEY FLOW · $TICKER · 90d
─────────────────────────────────
INSIDERS    {N} buys (${$buys})  {M} sells (${$sells})  Net: {NET}
CONGRESS    {K} purchases  {L} sales
TOP 13F     1. {Inst1}  {shares1}  ({changeType1} {sharesChangePct1}%)
            2. {Inst2}  {shares2}  ({changeType2} {sharesChangePct2}%)
            3. {Inst3}  {shares3}  ({changeType3} {sharesChangePct3}%)
ANALYSTS    {U} upgrades  {D} downgrades  (recent: "{lastAction}")
```

---

### `news <TICKER>`: Sentiment-tagged news + embeds

This is the command where the terminal feel really differentiates from a quote-and-dump tool. SentiSense returns documents (URLs + sentiment + source). The public document API provides derived analytics, not source content; it does NOT include the publisher's article headline. You produce the headline yourself using the **Headline Resolution** pattern below. Any retrieval from source URLs is your agent application's independent action, subject to the source platform's terms.

**Calls:**
1. `GET /api/v1/documents/ticker/{T}?limit=8` for the document feed
2. `GET /api/v2/metrics/entity/{T}/metric/sentiment` for context (server default 7-day window)

**Output template:**
```
NEWS · $TICKER · 7d sentiment {score} ({delta})
─────────────────────────────────────────────────
1. [{sentiment}]  {resolvedHeadline}
   {source} · {time}
   {url}
2. ...
```

For Reddit/X URLs, render an embed card instead of a plain link (see **Social Embeds** below).

---

### `stories`: Pre-clustered story feed

A curated alternative to raw `news`: SentiSense clusters related documents into named stories with our own AI-generated cluster titles. These titles are OUR content and are safe to display verbatim (no publisher copyright concern). The list endpoint returns the title, sentiment, size, and tickers per cluster; the full narrative summary lives on the story detail endpoint, not in the list.

**Calls:**
1. `GET /api/v1/documents/stories?limit=10`

**Output template:**
```
TODAY'S STORIES · {date}
────────────────────────
1. {cluster.title}                                           [{sentiment}]
   Tickers: $T1 $T2 $T3   ·   {cluster.clusterSize} sources
2. ...
```

The list cluster has no body/summary field. Real shape: `{ id, title, createdAt, clusteredAt, clusterSize, averageSentiment }`. For a narrative summary, fetch the story detail (`GET /api/v1/documents/stories/{id}`).

For per-ticker stories: `GET /api/v1/documents/stories/ticker/{T}?limit=5`.

---

### `earnings [this|next]`: Earnings calendar

Forward-looking earnings calendar: which companies report, when, and the consensus EPS. The value is **lead time**, not what reports tonight. This is the kind of forward calendar professional data services sell on upgraded plans; here it is free for the current week and full on PRO. Use it to build a pre-earnings watchlist and to anchor the `EARNINGS PREVIEW` composition (below) to a real date.

**Calls:**
1. `GET /api/v1/calendar/earnings?week={this|next}` (default `this`; or `?ticker={T}` for one name)

**Output template:**
```
EARNINGS · week of {windowStart}
─────────────────────────────────
{date}  {BMO/AMC}   $TICKER   est. EPS {eps}   {✓}
{date}  {BMO/AMC}   $TICKER   est. EPS {eps}
...
{totalCount} report in the next 30 days  ·  PRO unlocks the full window
```

Group by date ascending. Map `earningsTime`: `before_open` -> BMO, `after_close` -> AMC, `during_market` -> MID, `unknown` -> blank. Show `est. EPS ${estimatedEps}` when present; omit when null. Mark `confirmed:true` rows with a ✓; leave projected dates unmarked. On a Free key the response is `isPreview:true`, limited to the current week, and carries `totalCount` (events across the full ~30-day window): render the footer line only on a preview. PRO gets the full window, so drop the footer.

---

### `help` or unrecognized input

Print the command list. Don't say "I don't understand": show what you can do.

```
COMMANDS
  open <TICKER>          stock screen
  compare <A> <B>        side-by-side
  daily brief            market digest
  screen smart-money     convergence screener
  flow <TICKER>          smart-money flow
  mood                   market sentiment
  news <TICKER>          recent news with embeds
  stories                pre-clustered story feed
  earnings [this|next]   forward earnings calendar

OR ASK NATURALLY
  "is NVDA a buy here?"  "what's hot today?"
  "compare TSLA and RIVN" "WTF is going on with AAPL"
```

---

## Natural Language Aliases

The user will rarely type the exact command syntax. Recognize the intent and run the closest workflow. Never ask "did you mean `open NVDA`?": just run it.

| User says | Run |
|-----------|-----|
| "show me $TICKER", "tell me about $TICKER", "what's $TICKER doing" | `open` |
| "is $TICKER a buy", "should I look at $TICKER", "$TICKER thoughts" | `open` + add a one-line educational framing summary at the bottom (data context, not a recommendation) |
| "what's hot today", "market today", "what's moving" | `daily brief` |
| "smart money", "what are insiders buying", "what's the smart money doing" | `screen smart-money` |
| "compare $A and $B", "$A vs $B" | `compare` |
| "what's the market mood", "fear/greed", "is the market scared" | `mood` |
| "WTF $TICKER", "why is $TICKER moving", "what's happening with $TICKER" | `flow` + `news` (compose into one screen) |
| "news on $TICKER", "what's the news", "any headlines on $TICKER" | `news` |
| "what's the story today", "what stories are happening" | `stories` |
| "before earnings on $TICKER", "$TICKER earnings preview", "when does $TICKER report" | `flow` + analyst estimates anchored to `/calendar/earnings?ticker=$TICKER` (use the pre-earnings synthesis below) |
| "earnings calendar", "who reports this week", "what's reporting next week", "earnings this week" | `earnings` |

When the user asks something that doesn't map cleanly, default to `open` if a ticker is present, `daily brief` if not, and `help` only if neither.

---

## Headline Resolution Pattern

The SentiSense public document API returns `{ id, url, source, sourceName, published, averageSentiment, reliability, sentiment }` for each document, and the per-ticker feed wraps them as `{ documents, totalCount, searchTicker, source, startDate, endDate }` (read `response.documents[]`). Two field-name traps in the `news` template: the timestamp is `published` (epoch **seconds**), not `timestamp`; and the scalar polarity is `averageSentiment` (a float in [-1,1]) while `sentiment` itself is a per-entity array (`[{ ticker, name, entityType, sentiment }]`), not a scalar. So `{time}` reads `published` and `{sentiment}` reads `averageSentiment`. By API design it does **not** include the publisher's article headline, and there is no `summary` field. The API provides derived analytics, not source content. If your application needs to display titles, resolve them yourself from the `url` field. Any content retrieval from source URLs is your agent application's independent action, subject to the source platform's terms.

Use this two-phase pattern, in order:

### Phase 1: oEmbed for social URLs (fastest path)

If the URL is from a major social platform, fetch the platform's oEmbed endpoint. These are free, public, no-auth, and return rich pre-rendered content.

| Domain | oEmbed endpoint |
|--------|----------------|
| `reddit.com`, `*.reddit.com` | `https://www.reddit.com/oembed?url={ENCODED_URL}` |
| `x.com`, `twitter.com` | `https://publish.twitter.com/oembed?url={ENCODED_URL}&omit_script=true&dnt=true` |
| `youtube.com`, `youtu.be` | `https://www.youtube.com/oembed?url={ENCODED_URL}&format=json` |

The response includes `title`, `author_name`, and (for Reddit/X) an `html` field with a pre-styled embed. If the host UI supports inline HTML, use the `html` block. Otherwise extract the `title`.

### Phase 2: Fetch + parse `<title>` for general URLs

For non-social URLs, if your tool surface includes a URL fetcher (e.g. WebFetch, Browse, fetch_url), call it on the URL and extract the `<title>` tag.

Optimization: only the first ~16KB of the page is needed (the `<title>` is in `<head>`, near the top). Don't read the full document.

Google News aggregator URLs (`news.google.com/rss/...`) are redirect wrappers that defeat both oEmbed and `<title>` extraction. Skip straight to the Phase 3 slug fallback (or label them by the document's `source`) for those.

Pseudo-pattern:
```
title = fetch(url, range=0-16384).extract("<title>")
if title and len(title) > 3:
  return title
```

### Phase 3: URL slug fallback (zero-cost)

If you cannot fetch the URL (no fetch tool available, or fetch failed), derive a humanized title from the URL slug:

```
url:    https://www.reuters.com/technology/nvidia-q1-revenue-beats-2026-04-30/
slug:   nvidia-q1-revenue-beats
title:  "Nvidia Q1 Revenue Beats" (replace - with space, title-case, strip dates/hashes)
output: "Nvidia Q1 Revenue Beats: reuters.com"
```

Degrade gracefully so the news view never shows naked URLs.

### Caching

If your environment supports session memory, cache resolved titles for 30 minutes keyed by URL. The same article often appears across multiple `news` queries.

---

## Social Embeds

When rendering Reddit, X/Twitter, or YouTube URLs in the `news` view, the host UI may support rich embeds. Three rendering tiers, in order of preference:

1. **Native embed.** If the host supports embedded iframes or widgets (e.g. a webview agent), inject the oEmbed `html` block directly. You get the platform's native look-and-feel.
2. **Card render.** If the host supports markdown blockquotes or callout boxes, render as a quote card:
   ```
   > **Reddit · r/wallstreetbets** · 4h ago
   > "{post title or excerpt}"
   > {url}
   ```
3. **Plain link.** Worst case, the standard `news` line format with the resolved title.

Never strip the `url` even when embedding: users want the option to click through.

---

## Composition Templates

For complex queries the user may ask, you may need to compose multiple commands into one screen. Three reusable shapes:

### Earnings preview

When the user asks "before earnings on $X" or "$X earnings preview":

```
EARNINGS PREVIEW · $TICKER · ER {date} ({daysOut}d out)
────────────────────────────────────────────────────────
SETUP       Sentiment {s30d} ({d30d} 30d) ·  Insiders {netInsider}
CONSENSUS   EPS ${epsMean}  (range ${epsLow}-${epsHigh}, {N} analysts)
SURPRISES   {recent beats/misses from surprises[], e.g. "beat 3 of last 4"}
ACTIONS     {U} upgrades, {D} downgrades (30d)
            Recent: "{lastAction}"
THESIS      {one-line synthesis: bullish/bearish/mixed}
```

Calls: `/calendar/earnings?ticker={T}`, `/profile`, `/analyst/{T}/estimates`, `/analyst/{T}/actions?lookbackDays=30`, sentiment 30d, insider 60d. The report **date** and `daysOut` come from `/calendar/earnings?ticker={T}` (`data.earnings[0].earningsDate` and `confirmed`); if that returns empty, the company is outside the forward window, so omit the date line rather than guessing. Note: `/estimates` returns `data.estimates[]` (each `{ periodLabel, periodType, estimateLow, estimateMean, estimateHigh, numberOfAnalysts }`) plus `data.surprises[]` (each `{ periodLabel, reportDate, estimateEps, actualEps, surprisePercent }`); read the consensus band from `data.estimates[0]`, not from `data` directly. It has no revenue figure and no revision history, so do not render `Rev` or "revised from".

### Sector deep-dive

When the user asks "what's happening in tech today" or "energy sector":

```
SECTOR · Technology · {date}
─────────────────────────────
MOOD       {sectorScore} ({phase})    {weeklyChange} 7d
TOP MOVERS $T1 +X%   $T2 +X%   $T3 +X%
LAGGARDS   $T4 -X%   $T5 -X%
DRIVERS    "{topInsight1}"
           "{topInsight2}"
```

Calls: `/market-mood` (read the named sector out of `response.sectors`), `/insights/market` (returns market-wide; client-side filter `data[]` by tickers known to belong to the sector), `/stocks/popular` (client-side filter by sector). Neither `/market-mood` nor `/insights/market` accepts a sector query param; both are full-payload responses you slice in-memory.

### Watchlist brief

When the user provides multiple tickers (e.g. "watch NVDA AMD INTC"):

```
WATCHLIST · {date}
───────────────────
$NVDA   {price} {chgPct}   Mood {s}    {smartMoneyFlag}
$AMD    {price} {chgPct}   Mood {s}    {smartMoneyFlag}
$INTC   {price} {chgPct}   Mood {s}    {smartMoneyFlag}
```

The `smartMoneyFlag` is `↑` if any of (insider cluster buy, congress purchase, recent upgrade) hit in 7d; `↓` for the inverse; blank if neutral.

---

## Synthesis Rules (recap)

The "terminal feel" comes from being predictable. Every screen follows these rules.

1. **Vertical structure.** Tables and labeled rows beat paragraphs.
2. **Fixed widths.** When showing comparisons, align columns so the user can scan top-to-bottom.
3. **Numbers first, words second.** Lead each line with the value.
4. **One signal per line.** Don't combine.
5. **Round consistently.** Two decimals for prices, integer percent for changes, two decimals for the [-1, 1] sentiment value.
6. **`$TICKER` always.** Uppercase, dollar-prefixed.
7. **Sign every change.** `+1.23%`, `-0.45%`, never bare numbers.
8. **No prose unless asked.** The screen IS the answer.
9. **Parallelize calls.** `open` fires 6 calls at once; don't await sequentially.
10. **Cache the quarter.** `/institutional/quarters` rarely changes.

---

## Anti-Patterns (Don't Do These)

These are the failure modes the skill is designed to steer around.

- **Don't narrate the work.** "Let me look that up..." or "I'll need to call several endpoints..." is anti-pattern. The terminal does the work silently.
- **Don't apologize.** "I'm sorry, I can only show preview data" is anti-pattern. Silently render what you have; flag `(preview)` in the corner if the user is on Free.
- **Don't issue personal recommendations.** "$NVDA is a strong buy" or "you should sell $TSLA" is anti-pattern. This skill is a data interface, not an advisor. Show data and educational framing; let the user draw conclusions.
- **Don't ask follow-up clarifying questions for unambiguous asks.** "Did you want price or sentiment for $NVDA?" is anti-pattern. Run the full `open` screen: it shows both.
- **Don't pretty-print one number.** A user asking "$NVDA price" gets a one-line answer (`$NVDA $890.12 (+1.4%)`). They don't get a 30-line `open` screen for a price quote.
- **Don't hand-craft headlines.** If the document API didn't return one, use the Headline Resolution pattern. Don't invent.
- **Don't hallucinate endpoints.** No `/api/v1/options/flow`, `/api/v1/dark-pool`, `/api/v1/alerts`, `/api/v1/chat`, `/api/v1/congress` (use `/politicians`). The earnings calendar IS `/api/v1/calendar/earnings` (not `/api/v1/earnings`).
- **Don't show the API key in user-facing output.** Ever.
- **Don't push PRO unless the user is hitting the wall.** Free tier delivers great terminal experience. Mention PRO when a `(preview)` truncation is meaningfully limiting the answer.
- **Don't quote a price, percent move, headline, analyst rating, or earnings result from training data.** That data is stale by definition. Fetch it every turn, even if the user just asked the same question minutes ago. The cost of one wrong number outweighs the cost of an extra `get_quote`.

---

## API shape gotchas (worth memorizing)

Real shapes differ from what a naive reading of the endpoint URL might suggest. These cost time to discover the hard way; here they are upfront.

**`stocks/chart` returns a bare `ChartDataPoint[]`** at the top level, not `{ data: [...] }`. Accept both shapes defensively:

```
const points = Array.isArray(raw) ? raw : (raw?.data ?? []);
```

Each point has both a `timestamp` (Unix ms) and a pre-formatted display `date` string. Read x-axis values from `timestamp`. Parsing the formatted `date` string falls back to the current year on some JS date parsers (e.g. `Apr 6` becomes the current year instead of the year the bar belongs to).

**`entityMetrics/metrics` returns `ServingMetric[]` where the scalar lives at `metricValue.value.value`** (nested). Rank info, when present, is at `metricValue.value.properties.{rank, percentile, totalStocks}` or `metricValue.properties.{rank, percentile, totalStocks}`. Top-level `value: number` is a legacy fallback; handle it but don't rely on it.

```
function extractMetric(m) {
  return m?.metricValue?.value?.value
      ?? m?.metricValue?.value
      ?? m?.metricValue
      ?? m?.value
      ?? null;
}
```

**`entityMetrics/distribution` wraps the payload in `distribution`** (singular), not `distributions`:

```
{ entityId, metricType, timestamp, dimension: "source",
  distribution: { News: 37.4, Reddit: 37.4, X: 18.2, Substack: 7.0 } }
```

The values are share-of-voice percentages summing to roughly 100, **not** per-source sentiment scores. Render the breakdown as a "where this signal came from" panel, not as four sentiment bars.

**`v2/market-mood` nests the composite under `market`.** The response is flat (no `isPreview/data` envelope), but the fear/greed score, phase, weekly change, and sub-signals live one level down at `response.market.{ currentScore, phase, weeklyChange, signals[] }`, and per-sector breakdowns at `response.sectors.{SectorName}.{ currentScore, phase, weeklyChange }` (NOT at the root). Map the `mood` / `daily brief` tokens accordingly: `{score}` = `market.currentScore`, `{phase}` = `market.phase`, `{weeklyChange}` = `market.weeklyChange`, and each signal `{v}`/`{d}` = `market.signals[i].value`/`.change`.

**`GET /api/v1/stocks/images?tickers={T}` (comma-separated, plural `tickers`) returns third-party CDN logo URLs that don't carry an embedded API key.** Direct `<img src>` will 401/403. Wrap with the SentiSense anonymous image proxy:

```
https://app.sentisense.ai/api/v1/stocks/proxy-image?imageUrl=<encoded-url>
```

**Story detail (`documents/stories/:id`) is a flat `PublicStoryDetailDto`**, not the nested `{ cluster, entities, documents }` you might expect. Inside `aspectPerspectives[i]`, the fields `bullishView` and `bearishView` are *structured objects* (`hook`, `risksOrCatalysts: string[]`, `conclusion`, `confidence`), not markdown strings. The top-level `bullishView` / `bearishView` ARE markdown strings. Same field names, different shapes. Type-check before calling string methods.

**Chart timeframes accepted by `stocks/chart`:** `1D / 5D / 1W / 1M / 3M / 6M / 1Y / ALL`. Anything else falls back to `1M` and logs a warning.

**`institutional/quarters` is a bare array** `[{ value, label, reportDate, pending }]` (not wrapped in `data`). Take `[0].reportDate` as the latest quarter to pass to `institutional/holders`.

**Sentiment, SentiSense Score, news clustering, AI summaries, and insights are batch metrics.** Quote / price / chart points are real-time. Show the `generatedAt` timestamp on insight and AI summary surfaces so the user knows how fresh the analysis is. Don't claim "real time" on analytical surfaces.

---

## Endpoint Quick Reference

For full schemas: https://sentisense.ai/skill.md.

```
PRICE         GET /api/v1/stocks/price?ticker={T}
              GET /api/v1/stocks/prices?tickers=A,B,C
              GET /api/v1/stocks/chart?ticker={T}&timeframe=1M|3M|6M|1Y
              GET /api/v1/stocks/{T}/profile
              GET /api/v1/stocks/market-status

SENTIMENT     GET /api/v2/metrics/entity/{T}/metric/sentiment?startTime={epochMs}&endTime={epochMs}   (omit for server default 7d)
              GET /api/v2/market-mood

DOCUMENTS     GET /api/v1/documents/ticker/{T}?limit=N    (no titles)
              GET /api/v1/documents/stories?limit=N       (cluster.title is OURS, safe)
              GET /api/v1/documents/stories/ticker/{T}?limit=N

INSIDER       GET /api/v1/insider/cluster-buys?lookbackDays=N
              GET /api/v1/insider/trades/{T}?lookbackDays=N

CONGRESS      GET /api/v1/politicians/activity?lookbackDays=N
              GET /api/v1/politicians/filings/{T}?lookbackDays=N         (per-ticker filings)
              GET /api/v1/politicians/member/{slug}      (recent trades nested at data.recentTrades)

INSTITUTIONAL GET /api/v1/institutional/quarters    (always FIRST)
              GET /api/v1/institutional/holders/{T}?reportDate={Q}      (data.holders[] sorted by largest position)

ANALYST       GET /api/v1/analyst/{T}/consensus
              GET /api/v1/analyst/{T}/actions?lookbackDays=N
              GET /api/v1/analyst/{T}/estimates
              GET /api/v1/analyst/activity?lookbackDays=N               (market-wide; filter actionType client-side)

INSIGHTS      GET /api/v1/insights/stock/{T}        (ranked by importance: relevance, confidence, recency; Public preview, free top 3; take data[0])
              GET /api/v1/insights/stock/{T}/types
              GET /api/v1/insights/market

CALENDAR      GET /api/v1/calendar/earnings?week=this|next     (Public preview: free=this week, PRO=full ~30d; data.earnings[])
              GET /api/v1/calendar/earnings?ticker={T}          (next report date + consensus EPS for one name)

MARKET        GET /api/v1/market-summary
```

**Wrap vs flat (verify per endpoint, do not assume).** Read these FLAT, with no `.data`: `price`, `prices`, `chart`, `popular`, `market-mood`, `stocks/{T}/profile`, `descriptions`, and `sentiment` (bare array). `institutional/quarters` is a bare array too (`[0].reportDate` is the latest quarter). `documents/ticker` has its own shape `{ documents, totalCount, ... }` (read `.documents[]`). These ARE wrapped in `{ isPreview, previewReason, data }` (read `.data`): `insider/*`, `analyst/*`, `insights/*`, `politicians/*`, `institutional/holders`. When unsure, accept both: `const rows = Array.isArray(raw) ? raw : (raw?.data ?? raw)`.

---

## Cost discipline

A cold ticker dashboard typically fans out 10 to 12 API calls on first load:

| Surface element | Calls |
|---|---|
| Profile + logo | 1 to 2 |
| Quote (header) | 1 (plus refresh interval) |
| Chart | 1 |
| Metrics panel (4 metrics in parallel) | 4 |
| Recent stories | 1 |
| Peers (similar + batch prices) | 2 |
| **Cold total** | **10 to 12** |

A grounded chat turn adds another 1 to 4 calls on top, depending on the tool ladder depth.

**Mitigations:**

- Use `Promise.allSettled` for parallel widget fetches; widgets render independently as data arrives. Don't gate the page on the slowest call.
- Module-level cache for popular-ticker lists and logos so they fetch once per session, not per visit.
- Lazy-load source mix breakdowns when the user expands them. Don't fetch source distribution eagerly with the time-series.
- Don't poll quotes faster than ~60s on the header. Tabular price grids don't need to poll at all.

**Rate limits.** Per-minute limits exist (Free 30 req/min, PRO 300 req/min). Exceeding them returns 429 with a `Retry-After` hint. Surface 429s gracefully ("rate limit reached, retrying in N seconds") rather than silently retrying or rendering a stale value.

**Per-stock budget mental model.** A heavy daily-driver visiting 15 tickers and chatting on each (~15 grounded turns × 3 calls) eats ~225 calls per session, comfortably under the PRO daily envelope. A light user (3 tickers per day, no chat) uses ~50. Plan defaults around that envelope so a typical user never sees a 429 in normal use.

---

## Tier Summary

| Command | Free | PRO |
|---------|------|-----|
| open | Full screen, AI insight preview-gated (top 3) | Full insight list |
| compare | Two tickers anytime | Unlimited |
| daily brief | Once per day comfortably (5 calls) | Unlimited refreshes |
| screen smart-money | Top items per bucket | Full ranked lists |
| flow | Preview slice | Full holder list, full history |
| mood | Full data, no quota cost | Same |
| news | 8 most recent | Full feed |
| stories | 10 most recent | Full feed |
| earnings | Current week | Full ~30-day forward window |

PRO at $15/month: https://app.sentisense.ai/pricing?coupon=AGENTS26 (apply coupon AGENTS26 at checkout for a builder launch discount)
