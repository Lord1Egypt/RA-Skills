# Trading Universe Dashboard — reference

Zero-dependency Node server + embedded single-page UI. No npm packages or CDNs. It binds to **127.0.0.1 only** and requires Node.js ≥ 18. Technical scans use Yahoo Finance; news/fundamentals grounding can use ForexFactory, Yahoo headlines and macro RSS; the version check contacts ClawHub. Optional reasoning providers are documented under [Privacy and trust boundaries](#privacy-and-trust-boundaries).

## Run

```
node <skill>/scripts/dashboard.mjs        # serves http://127.0.0.1:8788, auto-opens browser
```

If an instance is already running, a new launch opens the existing browser URL and exits.

Environment overrides:

| Var | Default | Purpose |
|---|---|---|
| `DASH_PORT` | `8788` | listen port |
| `TRADE_DATA_DIR` | `~/.trading-universe` | where runtime data lives |
| `TRADES_FILE` | `<data dir>/live-trades.json` | trade-log store (point tests at a sandbox — NEVER the real one) |
| `DASH_NO_OPEN` | unset | set to suppress the browser auto-open |
| `ICT_CE_PCT` | `50` | direct-process FVG entry depth; the dashboard normally persists this through Engine & automation |
| `ICT_OB_PCT` | `0` | direct-process OB entry depth; independent from FVG depth |

## Data directory (`~/.trading-universe`)

Runtime data lives OUTSIDE the skill folder so updating/sharing/publishing the skill never touches personal data. Created automatically.

- **`fundamentals.json`** — saved fundamentals leaderboard, rendered as the bottom strip (click a row for the full read). Written by the assistant after each leaderboard run. Format:
  `{ "asOf": "<ISO date>", "context": "<one-line macro summary>", "items": [ { "asset", "direction": "Bullish|Bearish|Neutral", "score": 1-5, "reason", "factors": ["+1 …", "-1 …"], "flip": "<what reverses the verdict>" } ] }`
  (`factors`/`flip` optional but recommended — the click-through modal shows them; the engine reads this file for the macro ticket gate, stale >36h ignored.)
- **`live-trades.json`** — schema v2: `{ "schemaVersion": 2, "trades": [...] }`. New records keep immutable `originalTicket` activation data alongside the editable current ticket, `events[]`, legacy-compatible `history[]`, and `dataQuality`. Migrated records label a recovered snapshot honestly when no older pre-edit state exists. Status flows `pending` → `open` → `closed`/`cancelled`; `ambiguous` means candle granularity cannot prove intrabar ordering. Replay stores fills, TP1/breakeven, terminal result, MFE/MAE and R. `dataQuality.excludedFromStats` removes uncertain records from analytics without deleting history.
- **`live-trades.json.bak`** — rolling backup written before every mutation; the previous state always survives one write. An unreadable store is quarantined as `.corrupt-<timestamp>` instead of being overwritten.
- **`engine-config.json`** — FVG/OB entry depths, scan interval, selected assets and auto-track settings.
- **`alerts.json` / `alert-queue.json`** — armed/fired price and level alerts plus the optional OpenClaw delivery queue.
- **`reasoning-config.json`** — provider/model settings and only, when explicitly selected, a saved API key.
- **`fundamentals-request.json` / `verify-request.json` / `verify-result.json` / `refresh-status.json`** — dashboard-to-provider or dashboard-to-agent request/status files.

## Endpoints

| Route | What |
|---|---|
| `GET /` | the UI |
| `GET /api/universe` | full `ict-levels.mjs universe` output (all assets, complete analysis); cached 10 min; `?force=1` bypasses |
| `GET /api/prices` | light price poll (Yahoo 1m meta), 20 s cache; the client polls every 60 s |
| `GET /api/ohlc` | selected asset's current price and latest 1-minute OHLC/day range |
| `GET /api/fundamentals` | contents of `fundamentals.json`, or `null` |
| `GET /api/fundamentals/request` | the pending refresh request (`{status:"pending", requestedAt, assets}`) or `{status:"none"}` |
| `POST /api/fundamentals/request` | the **Refresh fundamentals** button writes `{status:"pending", requestedAt}` to `fundamentals-request.json`. With a reasoning provider configured (🧠 Reasoning), the **server fulfills it itself**: it builds a grounding pack **fetched fresh at click** (ForexFactory week calendar with released actuals, Yahoo per-asset headlines + macro RSS titles [sanitized, untrusted-data], fresh prices with 1d/5d % change, previous board), makes one rubric call to the provider (OpenRouter gets `model:online` = provider-side web), validates every watchlist asset, writes `fundamentals.json` and sets the request `{status:"done"}` (or `{status:"failed", error}`). No provider → stays queued for a chat agent. The panel spinner auto-loads the new board when `asOf` advances. |
| `GET /api/verify/request` | the pending ticket review request (`{status:"pending", asset, ticket, nonce}`) or `{status:"none"}` |
| `POST /api/verify/request` | the per-ticket **🔍 Review (reasoning)** button writes `{status:"pending", asset, ticket, nonce}` to `verify-request.json`. With a provider configured the **server fulfills it directly**: fresh `ict-levels.mjs <asset>` run (includes `out.ohlc`) → a single checklist review call, or the **Collaborative Decision Review** when enabled → writes `verify-result.json` with the same nonce. Response carries `reasoning:{configured, advanced, provider}` so the card is honest when nothing will run. No provider → request stays queued for a chat agent (amber box). Card polls; timeout 5 min (8 min CDR) → "deterministic verdict stands". Files never deleted. |
| `GET /api/verify/result` | `?nonce=` returns the LIVE stage while a review is in flight: `{status:"running", nonce, stage, at}` (from an in-memory, nonce-keyed cache — protects against a second, different-asset review overwriting this one's result in the shared file before it's read). Once finished: contents of `verify-result.json` (`{status:"done", asset, nonce, verdict: TAKE\|MODIFY\|WAIT\|REPLACE\|PASS, revisedTicket, review:[{lens,line}], adr:{confidence,winner,evidenceScores,majorRisks,requiredConditions,advisorTicket}\|null, note, provider, model, mode, asOf}`) or `{status:"none"}` |
| `GET /api/reasoning/config` | current reasoning config (key **masked**): `{provider, model, saveKey, advanced, keySet, keyMasked, providers:{id:{label,models[],type:"api"\|"cli"}}}` — model lists are curated **reasoning-capable models only** |
| `POST /api/reasoning/config` | the **⚙ More → 🧠 Reasoning** panel: `{provider: nvidia\|openai\|openrouter\|claude-cli\|codex-cli, model, apiKey?, saveKey, advanced, clearKey?}`. The two `*-cli` providers are **subscription CLIs** (`type:"cli"`): the server spawns the locally installed `claude -p` / `codex exec` (read-only sandbox, prompt over stdin) and the user's logged-in subscription does the reasoning — **no API key**; `keySet` reports true whenever a CLI provider is selected. For API providers: empty `apiKey` keeps the current one; switching provider WITHOUT a fresh key clears it instead of carrying the old provider's key over. The key is persisted to `reasoning-config.json` **only when `saveKey` is ticked** (otherwise held in server memory — survives page refreshes, not restarts); never logged, redacted from all errors. `advanced` switches Review to the Collaborative Decision Review (Analyst · Risk Analyst · Financial Advisor × 2 rounds + Judge, ~7 calls). |
| `POST /api/reasoning/test` | tiny ping call to the configured provider → `{ok, ms, provider, model}` or `{ok:false, error}` (key-redacted) |
| `GET /api/engine/config` | FVG/OB depth, 5/10/15/20/30/60-minute cadence, auto-track threshold/notification, last assets and replay time |
| `POST /api/engine/config` | validate and persist engine/automation settings; depth changes invalidate the universe cache and cadence changes re-arm the scheduler |
| `GET /api/alerts` | armed alert definitions plus the bounded fired history |
| `POST /api/alerts` | create an arbitrary-price, liquidity, FVG or OB cross/touch/zone alert |
| `POST /api/alerts/delete` | delete one alert |
| `POST /api/alerts/rearm` | re-arm one previously fired alert |
| `GET /api/alerts/fired` | alerts fired after `?since=<ms>` plus armed count |
| `POST /api/alerts/clear-fired` | clear one fired event or the full fired history |
| `GET /api/refresh-status` | live refresh indicator: `{active, label, since, finishedAt}` (or `{active:false}`) |
| `POST /api/refresh-status` | `{active:true, label}` while rebuilding data, `{active:false}` when done — drives the dashboard's pulsing "refreshing…" banner and, on finish, a brief "refreshed just now" confirmation + auto-reload of the board. Stored in `refresh-status.json`. |
| `GET /api/trades` | schema-v2 trade ledger (v1 is migrated in memory and on startup) |
| `POST /api/trades/add` | validate and track a ticket; limit orders start `pending`, market orders start filled/`open` |
| `POST /api/trades/update` | audited note/reopen/close/edit operations plus `{excludeFromStats, qualityReason}`; edits must remain finite and correctly ordered, but the fresh-ticket RR gate is deliberately not applied |
| `POST /api/trades/reconcile` | fetch fresh lifecycle candles and replay all active records immediately (the server also does this every 60 s) |
| `GET /api/trades/export` | formula-safe CSV export |
| `GET /api/version` | local package version, latest ClawHub version and update flag |
| `POST /api/shutdown` | loopback-only graceful shutdown; rejects non-local/mismatched-origin requests |
| `GET /favicon.svg` | tab icon |

Automatic replay is the primary result source. The plan model takes 50% at TP1, moves the remainder to breakeven, and runs to TP2. Same-bar conflicts are `ambiguous` pending review; R analytics report total R, expectancy and profit factor and exclude flagged data-quality records.

## UI map

### Header and workspaces

- **Tickets:** All / Valid / Stand-down, instrument search, live stats, best ticket and a separate feed-error box.
- **Structure:** four-timeframe heatmap with continuation scores and board read.
- **Trade log:** Pending/Open/Closed/Unfilled/Auto plus Long/Short/Wins/Losses filters, semantic search, collapsible green Active and amber History sections, asset/RR/pips/date sorting where relevant, R analytics, lessons and CSV export.
- **Alerts:** arbitrary price plus liquidity/FVG/OB edge, CE/mid and zone triggers; current price/latest 1-minute OHLC helpers; re-arm/delete/clear history; chime, toast, desktop notification and flashing title.
- **Automation controls:** Auto scan refreshes the open tab; Auto-track runs headlessly while the dashboard process is alive. Both use the selected 5/10/15/20/30/60-minute cadence. On restart, candle replay catches up fills, TP and SL events.

### Ticket and detail views

- Cards show area names with exact feed prices in tooltips, validity/forming/printed times, structured bull/bear debate boxes, draw plus next draw, Wyckoff location/next tell/suggested action, and optional sparklines.
- Deep detail supports Tabs, Scroll and Grid. Its sticky asset header remains visible while scrolling. Overview, Structure, Liquidity, Wyckoff, Debate and Raw include the 4H range anchors, indicators, three SL rails per side and full event timelines.
- Completed reasoning reviews collapse to a badge. The popup shows full role names, evidence meters, transcript and revised-ticket comparison.
- Clicking any trade row opens the immutable original activation ticket, current adjusted ticket when different, context, review snapshot, provenance, result and timeline. Legacy migrations disclose when an earlier pre-edit state could not be reconstructed.
- Draw-on-liquidity excludes swept, visited and too-close pools. If no forward-relevant pool remains, it shows no draw rather than recycling an irrelevant area.

**🎨 Display panel (⚙ More menu):** theme palette — **nine looks** rendered as a grid of mini dashboard previews (each card mocks the theme's bg/panel/accents with a tiny sparkline, click to apply): `nebula` (default, the deep-space `:root` set), `quasar` (indigo/sky), `aurora` (emerald/teal), `solar` (amber/orange), `andromeda` (violet/magenta), `polaris` (arctic blue/silver), `deep-red`, `supernova` (renamed from `crimson`), `ember` (renamed from `blood`) — applied as `html[data-theme=…]` CSS-variable overrides (the client migrates old stored `crimson`/`blood` values); semantic bull/bear/news tokens (`--grn`/`--red`/`--amb` + tints) are identical in every theme by design; the header logo gradient uses `--vio`/`--cyn`, so it re-skins with the theme. Sparklines: OFF by default; the panel enables them and picks the default timeframe. Data comes from the engine's `sparks` field — **halved windows** `{m15:[24 closes ≈6h], h1:[24 ≈1d], h4:[21 ≈3.5d], d:[15 ≈3wk]}` with a parallel `sparkTs` timestamp array (legacy 20-point `spark` kept for back-compat). Each sparkline wears a glossy centered `TF · span` banner pill (fades while hovering) and a **mouse-tracked hover crosshair** — vertical rule, point dot and a tooltip with the exact close + candle time (`sparkTs`; older scans fall back to an ≈-marked estimate); clicking a sparkline cycles that card's timeframe for the session only. Preferences persist in browser localStorage: `tuTheme` (string), `tuSpark` (`{on:bool, tf:"m15"|"h1"|"h4"|"d"}`), `tuDetailView` (`"tabs"|"all"|"grid"`), alongside the existing `tuPairs`. The `verify-request.json` ticket snapshot now also carries `entryLabel`/`tp1Label`/`tp2Label` (additive — external fulfillers can ignore them).

**Footer:** brand/version, session duration, `🔒 loopback UI`, price cadence, glossary, risk disclaimer, feedback link and sponsor link.

## Privacy and trust boundaries

The browser UI is loopback-only; that does not mean every optional feature is offline. Technical scans and grounding use the sources named above, and the version check contacts ClawHub. Enabling an API reasoning provider sends the selected ticket or fundamentals grounding pack to that provider. CLI reasoning sends the prompt to the installed Claude/Codex CLI with a curated environment rather than inheriting unrelated secrets. Keys remain in memory unless **Save key** is selected. Treat `~/.trading-universe` as private user data.

Every ticket shown is a PLAN, not an open position — the dashboard executes nothing.
