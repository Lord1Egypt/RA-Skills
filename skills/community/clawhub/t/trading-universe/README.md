# 🎯 Trading Universe

All-in-one trading-analysis skill for AI agents — ICT intraday setups, macro fundamentals, alerts, and a local dashboard with a persistent trade log. Zero npm dependencies; the technical engine is deterministic and uses keyless market-data sources.

> **Everything this skill outputs is an order *plan*, never an executed trade. It never connects to a broker, never places orders, and never gives position-sizing or leverage advice. Not financial advice.**

---

## What it does

| Mode | What you get | Data source |
|---|---|---|
| **TECHNICAL** | The highest-probability ICT setup right now, as a ready-to-place order ticket: order type, entry, invalidation (SL), TP1/TP2, RR, star rating, and a deterministic bull/bear debate verdict. Plus a whole-watchlist scan and per-timeframe structure reads. | `scripts/ict-levels.mjs` (live OHLC) |
| **FUNDAMENTALS** | A plain-language bullish/bearish verdict with a 1–5 conviction meter, scored by a fixed ±1-factor rubric over web-searched macro data — plus a whole-watchlist leaderboard. | Agent web search + the rubric in `SKILL.md` |
| **DASHBOARD** | A loopback-only browser dashboard: order tickets, structure heatmap, fundamentals, live prices, alerts, configurable FVG/OB entry depth, optional auto-tracking, and a schema-v2 ledger with automatic candle replay (pending → filled → TP1/breakeven → TP2/SL), MFE/MAE, ambiguity handling, R analytics, lessons, immutable activation snapshots, and a full modification audit trail. | `scripts/dashboard.mjs` |

**Default watchlist (15 assets):** XAUUSD (gold), XAGUSD (silver), EURUSD, GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD, NZDUSD, GBPJPY, AUDJPY, EURJPY, DJ30, NAS100, US500. The pair selector supports 33 non-exotic instruments.

## The engine in one paragraph

`scripts/ict-levels.mjs` computes everything a discretionary ICT trader reads from a chart — swing structure with CHoCH/BOS per timeframe (D/H4/H1/M15), the 4H dealing range (premium/discount), labeled liquidity pools with confirmed-sweep timestamps (PDH/PDL anchored to the New York trading day, session highs/lows, equal highs/lows), stateful fair value gaps and order blocks (fresh/partial/CE-tested/mitigated/invalidated), killzones, ATR budget, and upcoming high-impact news — then applies a fixed playbook (8 setups, led by the *2022 model*: liquidity raid → displacement → entry at the origin) to emit ranked order tickets. Every ticket must survive a deterministic adversarial debate (killzone, structure alignment, macro board, draw on liquidity, entry location in the reversal leg, news, RR); rejected tickets never surface. Zones are created from **closed candles only**, then later closed or forming candles update mitigation/touches; structure signals still require closed candles, and every number in the output comes from the script — the model copies, it never calculates. Full rules: [`references/playbook.md`](references/playbook.md).

## Requirements

- **Node.js 18+** (uses the built-in `fetch`; no npm packages at all)
- An agent runtime that reads skills ([OpenClaw](https://openclaw.ai), Claude Code, or any framework that can read `SKILL.md` and run shell commands) — or no agent at all: the scripts run standalone (see [Direct CLI](#direct-cli-no-agent-needed))

## Installation

**OpenClaw (from ClawHub):**

```
openclaw skills install trading-universe
```

**OpenClaw (manual):** copy this folder to `<workspace>/skills/trading-universe/` and restart the daemon (`openclaw daemon restart`). Verify with `openclaw skills list`.

**Claude Code:** copy this folder to `~/.claude/skills/trading-universe/`.

**Anything else:** point your agent at `SKILL.md` — it is self-contained. Relative paths inside it resolve against this folder.

## Usage with an agent

Invoke `$trading-universe` explicitly, then ask. Explicit invocation keeps this financial-analysis workflow from activating in unrelated conversations:

- *"Any setup on gold?"* / *"XAUUSD entry"* → one order-ticket card
- *"Scan the watchlist"* / *"any valid entries right now?"* → one card per valid entry + summary
- *"Structure EURUSD"* → per-timeframe bias card with continuation stars
- *"Is silver bullish or bearish?"* / *"fundamentals leaderboard"* → rubric-scored verdict / leaderboard
- *"Open the dashboard"* → launches the local dashboard and replies with the URL
- *"Deep read GBPJPY"* → frontier reasoning models may reason over the full JSON and overrule the scripted pick (smaller models always copy the script's ticket verbatim — determinism is the point)

## Direct CLI (no agent needed)

```
node scripts/ict-levels.mjs XAUUSD            # full analysis JSON for one asset (ends with the winning ticket)
node scripts/ict-levels.mjs scan              # whole watchlist: valid entries / stand-downs / errors
node scripts/ict-levels.mjs structure EURUSD  # per-timeframe structure + continuation scores
node scripts/ict-levels.mjs universe          # full output for all 15 assets (feeds the dashboard, ~150 KB)
node scripts/dashboard.mjs                    # dashboard at http://127.0.0.1:8788 (auto-opens the browser)
```

### Desktop app (Windows)

Install **Trading Universe** shortcuts in the Desktop and Start Menu. The shortcut points directly to the detected `node.exe`, starts the dashboard minimized, and opens the browser UI:

```
powershell -ExecutionPolicy Bypass -File scripts\install-desktop.ps1
```

Remove it with `... install-desktop.ps1 -Uninstall`. The icon is generated (zero-dependency) by `node scripts/make-icon.mjs` → `assets/trading-universe.ico`; the installer regenerates it when a registry package omits the generated ICO. The installer creates only the two requested `.lnk` files—no VBS launcher, service, scheduled task, autorun key, or background persistence.

Run `... install-desktop.ps1 -ValidateOnly` to verify Node, dashboard and icon prerequisites without creating shortcuts.

## Configuration (all optional)

| Env var | Default | Effect |
|---|---|---|
| `TRADING_MODEL_CLASS` | *(unset)* | `reasoning` or `deterministic` — force how the agent handles tickets. Reasoning models fully debate every ticket and show a drafted `Verdict:`; deterministic models copy the scripted pick. Unset → the model self-identifies. Surfaces as `meta.modeOverride`. |
| `UNIVERSE_ASSETS` | *(unset)* | Comma-separated watchlist for `scan`/`universe` (the dashboard's pair selector sets this). Empty → the default 15. |
| `DASH_PORT` | `8788` | Dashboard port (always binds `127.0.0.1` only). |
| `TRADE_DATA_DIR` | `~/.trading-universe` | Where the dashboard reads/writes runtime data. |
| `TRADES_FILE` | `<data dir>/live-trades.json` | Trade-log file override (useful for sandboxed testing). |
| `DASH_NO_OPEN` | *(unset)* | Set to suppress auto-opening the browser. |
| `ICT_ASSUME_OPEN` | *(unset)* | Testing only: treat stale weekend data as an open market. |
| `ICT_CE_PCT` | `50` | Direct CLI FVG entry depth: `0` immediate touch, `50` CE midpoint, `100` far edge. The dashboard stores this in Engine & automation. |
| `ICT_OB_PCT` | `0` | Direct CLI order-block entry depth: `0` immediate proximal touch, `50` midpoint, `100` far edge. The dashboard stores this independently from FVG depth. |

Data comes from keyless Yahoo Finance — no API key or signup required. FX spot (`<PAIR>=X`) matches typical broker feeds closely; metals and indices use futures (GC=F, SI=F, YM=F, NQ=F, ES=F) which trade at a small constant offset. Every card's `Data:` line tells you which feed produced it and flags futures — map those levels onto your **TradingView** chart by the reference each one names (FVG, OB, EQH/EQL or POI) rather than the raw price, since the offset shifts the absolute number but not the structure.

## Data & privacy

- The web server binds to `127.0.0.1`; the dashboard UI is not exposed to other machines.
- Runtime data—fundamentals, trades, alerts, requests, settings, backups, and an optional saved reasoning key—lives in `~/.trading-universe/`, outside the skill folder. Updating or sharing the skill does not include that directory.
- Technical scans call Yahoo Finance; calendar/news grounding can call ForexFactory, Yahoo headlines, and macro RSS feeds. The footer version check contacts ClawHub.
- Reasoning is opt-in. When NVIDIA NIM, OpenAI, or OpenRouter is configured, the dashboard sends the selected ticket or fundamentals grounding pack to that provider. OpenRouter's online model may also perform provider-side web retrieval.
- Claude/Codex subscription modes send the same prompt to the locally installed CLI. Those child processes receive only a curated environment (paths, user config directories, locale, temp, proxy/certificate settings), not the dashboard process's full environment or unrelated API-key variables.
- API keys are held in memory unless **Save key** is selected. Saved keys are written to `reasoning-config.json`; they are masked in the UI and redacted from errors. Review provider terms before enabling any external reasoner.

## Repository layout

```
SKILL.md                    agent instructions: routing, workflows, card formats, hard rules
scripts/ict-levels.mjs      the deterministic ICT engine (single file, zero deps)
scripts/dashboard.mjs       dashboard server + embedded UI (single file, zero deps)
scripts/trade-lifecycle.mjs lifecycle schema, migration, replay and R statistics
scripts/trade-reconcile.mjs dry-run/apply CLI for ledger reconciliation
scripts/symbols.mjs         shared 33-instrument registry and pip precision
scripts/make-icon.mjs       zero-dep generator for the app icon (.ico)
scripts/install-desktop.ps1 installs direct-Node Desktop / Start Menu shortcuts
assets/trading-universe.ico  app icon (three-bar logo, matches the browser icon)
assets/trading-universe.svg  icon source
references/playbook.md      the full ICT playbook: setups, stop engineering, debate, deep-read rules
references/dashboard.md     dashboard endpoints, env vars, data-file formats
references/asset-map.md     asset aliases + fundamentals search queries per asset class
LICENSE                     canonical SPDX MIT-0 license
```

## Disclaimer

This software produces educational market analysis. Trading foreign exchange, metals, and indices carries substantial risk of loss. Nothing here is investment advice, and past patterns do not predict future results. You alone are responsible for any trade you place.

## License & credits

MIT-0 (MIT No Attribution) — see [LICENSE](LICENSE).

Built and maintained by **T / Illimited Enterprise** · engineered with relentless iteration to make the tool better for traders. Feedback: [@MrTangoEco on X](https://x.com/MrTangoEco).
