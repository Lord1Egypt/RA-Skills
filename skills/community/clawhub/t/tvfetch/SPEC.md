# tvfetch Technical Specification

## Architecture

tvfetch is a two-layer system:

1. **Library layer** (`tvfetch/`) — Pure Python package implementing the TradingView
   reverse-engineered WebSocket protocol, SQLite caching, Yahoo/CCXT fallback,
   and automatic pagination. No CLI, no output formatting.

2. **Skill layer** (`scripts/`, `SKILL.md`, `plugin.json`) — Claude Code skill
   interface. Parses natural language intents, calls the library, formats results
   using the tagged output protocol, and handles config/auth resolution.

## Output Protocol (Tagged Sections)

All skill scripts emit output in tagged sections for reliable Claude parsing:

```
[BARS]
ts,o,h,l,c,v
1734480000,62000.00,62450.12,61780.50,62310.44,2341.8
...
[/BARS]

[ANALYSIS]
...
[/ANALYSIS]

[ERROR]
...
[/ERROR]
```

Rules:
- One top-level tag per section; sections appear in deterministic order.
- `[BARS]` is always CSV with header row.
- `[ANALYSIS]` and `[INDICATORS]` use `key: value` lines.
- `[ERROR]` contains a single line: `error_type: message`.
- Scripts must never mix tagged output with free-text stdout.

## Exit Code Contract

| Code | Meaning                        |
|------|--------------------------------|
| 0    | Success                        |
| 1    | General / unknown error        |
| 2    | Invalid arguments              |
| 3    | Symbol not found               |
| 4    | Auth required but missing      |
| 5    | Network / WebSocket failure    |
| 6    | Rate-limited                   |
| 7    | Data quality warning (partial) |

## Auth Resolution Order

Credentials are resolved in this order (first wins):

1. `TV_SESSION` / `TV_SESSION_SIGN` environment variables
2. `.env` file in project root
3. System keyring (`keyring` package, optional `[secure]` extra)
4. Anonymous mode (limited to 5000 bars, no premium indicators)

## Mock Fixture Naming

Fixture files follow this naming convention:

```
{action}_{exchange}_{pair}_{timeframe}_{count}bars.json   — fetch fixtures
{action}_{query}_{type}.json                               — search fixtures
error_{error_type}.json                                    — error fixtures
fetch_default.json                                         — fallback fixture
```

Examples:
- `fetch_binance_btcusdt_1d_100bars.json`
- `search_bitcoin_crypto.json`
- `error_symbol_not_found.json`

## Bar Limits

| Auth Mode   | Max Bars per Request | Max Total (paginated) |
|-------------|---------------------|-----------------------|
| Anonymous   | 5,000               | 5,000                 |
| Free user   | 5,000               | 20,000                |
| Plus        | 5,000               | 20,000                |
| Premium     | 5,000               | 100,000               |
| Pro+        | 5,000               | 100,000               |

Pagination: the library automatically chains requests using the `from` timestamp
of the oldest received bar. Each page requests up to 5,000 bars.

## Timeframe Codes

| Code  | Meaning        |
|-------|----------------|
| `1`   | 1 minute       |
| `3`   | 3 minutes      |
| `5`   | 5 minutes      |
| `15`  | 15 minutes     |
| `30`  | 30 minutes     |
| `45`  | 45 minutes     |
| `60`  | 1 hour         |
| `120` | 2 hours        |
| `180` | 3 hours        |
| `240` | 4 hours        |
| `1D`  | 1 day          |
| `1W`  | 1 week         |
| `1M`  | 1 month        |
| `3M`  | 3 months       |
| `6M`  | 6 months       |
| `12M` | 1 year         |

Numeric codes are minutes. Letter-suffixed codes are calendar periods.

## Symbol Format

Symbols follow TradingView's `EXCHANGE:TICKER` format:

- `BINANCE:BTCUSDT` — crypto
- `NASDAQ:AAPL` — US stock
- `FX:EURUSD` — forex
- `COMEX:GC1!` — futures (front month)
- `AMEX:SPY` — ETF
- `TVC:DXY` — index

The skill layer supports aliases (e.g., `BTC` resolves to `BINANCE:BTCUSDT`,
`AAPL` resolves to `NASDAQ:AAPL`). Over 100 common symbols have aliases.

## Data Quality Checks

The library validates returned bars for:
- Monotonically increasing timestamps
- `low <= open, close <= high` (OHLCV consistency)
- No duplicate timestamps
- Gap detection (missing bars beyond 2x expected interval)
- Volume non-negative

Violations are logged and optionally surfaced via exit code 7.

## Config File

Optional `~/.tvfetch/config.toml`:

```toml
[auth]
session = "..."
session_sign = "..."

[defaults]
timeframe = "1D"
bars = 100

[cache]
enabled = true
ttl_seconds = 300
db_path = "~/.tvfetch/cache.db"

[fallback]
yahoo = true
ccxt = false
```
