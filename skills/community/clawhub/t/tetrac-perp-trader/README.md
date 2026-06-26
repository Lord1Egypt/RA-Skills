# tetrac-perp-trader

A ClawHub skill that gives any OpenClaw agent a safe, multi-exchange perpetuals
trading CLI. Bundles a prebuilt Rust binary — no Rust toolchain, no `npm
install`, no PATH mutation. The agent reads `SKILL.md` and shells out to
`scripts/skill-trading`.

Target audience is an **AI agent**, not a human at a terminal — every command
has a structured output (table / JSON / CSV) and the SKILL.md encodes the
pre-order checklist and error-recovery protocol the agent must follow.

---

## Supported exchanges

15+ venues, all routed through the TTC Box API:

Orderly · Bybit · Binance · Hyperliquid · dYdX · OKX · Bitget · BloFin ·
AsterDEX · WooFi Pro · Backpack · Aevo · Drift · Vertex · Paradex.

The CLI never calls exchange APIs directly — every call goes through
`https://ttc.box/api/v1`, which holds the per-exchange credentials and
encrypted-wallet logic.

## What it can do

| Capability | Command |
|---|---|
| Place / cancel orders | `order limit`, `order market`, `order cancel`, `order cancel-all` |
| Manage positions | `position get`, `position close`, `position pnl` |
| Account state | `account balance`, `account leverage`, `account hedge` |
| Market data (no API key) | `market hybrid-tickers`, `market funding-rates`, `market open-interest`, `market scanner` |
| Risk | `risk sl`, `risk tp`, `risk trail-watch` |
| Strategies | `order dca`, `twap`, `twap-slice`, `market-maker` |
| Reports | `portfolio summary`, `brief`, `status` |

Full per-command documentation lives in `references/api-reference.md`.

## Install

### Via OpenClaw (recommended)

```bash
openclaw skills install tetrac-perp-trader
```

### Via ClawHub CLI

```bash
npx clawhub@latest install tetrac-perp-trader
```

Either path drops the bundle into `~/.openclaw/workspace/skills/tetrac-perp-trader/`.

### Supported platforms

| Platform | Binary |
|---|---|
| macOS Apple Silicon | `scripts/skill-trading-darwin-arm64` |
| Linux x86_64 | `scripts/skill-trading-linux-x64` |

The POSIX launcher at `scripts/skill-trading` detects `uname -s`/`-m` and execs
the right binary. Darwin x86_64, Linux ARM64, and Windows are not bundled — the
launcher will print `binary for <OS>-<ARCH> not bundled` if you try.

## First-run setup

The skill needs two TTC Box session credentials in your environment.

| Env var | Purpose |
|---|---|
| `TTC_AUTH_TOKEN` | 24h session token from `register` / `login` |
| `TTC_PASSKEY` | 64-char hex key that encrypts the local wallet |

Plus per-exchange credentials for the venues you trade on, e.g.
`ORDERLY_API_KEY` + `ORDERLY_API_SECRET` + `ORDERLY_API_PASSPHRASE`.

```bash
# Get session credentials
scripts/skill-trading register   # new account → also generates encrypted wallet
scripts/skill-trading login      # existing account

# Verify everything works
scripts/skill-trading status
# → STATUS: READY  if API + session token + exchange creds are all good
```

**Never put credentials in `config.toml`.** Secrets go in `.env` only.
`config.toml` is for non-secret preferences (default exchange, output format,
watchlist, portfolio thresholds).

## Security

- **Wallet keys are generated and encrypted locally** before any network call.
  PBKDF2-SHA1 derives the encryption key from `TTC_PASSKEY`; AES-256-CBC
  encrypts the wallet. Private keys are **never** transmitted in plaintext.
- **`--dry-run` is supported on every order command**, so the agent (or you)
  can preview an action before execution.
- **Read vs write classification** in SKILL.md — the agent is instructed to
  treat read ops as idempotent and write ops as non-idempotent, with a strict
  verification protocol before retrying any write that fails in flight.

If a downstream OpenClaw scan flags this skill as suspicious, the source repo
is right here for review and the binary is reproducible from
[`tetrac-official/rust-cli-ttc-api`](https://github.com/tetrac-official/rust-cli-ttc-api) Rust
sources.

## Quick examples

```bash
# Morning brief — runs everything in parallel, ~2-5s
scripts/skill-trading brief -e orderly

# Watchlist scan, HIGH confidence only, R/R ≥ 3
scripts/skill-trading market scanner --only-high --min-rr 3.0

# DCA $150 across 10 levels, 1% apart (always dry-run first)
scripts/skill-trading order dca -e orderly -s NEARUSDT --buy --amount 150 -d 1 --dry-run

# TWAP into a position over 1h in 5-minute slices
scripts/skill-trading twap -e orderly -s NEARUSDT --buy --total-usd 500 --duration 60 --slice-interval 5

# Trailing stop watcher (foreground loop)
scripts/skill-trading risk trail-watch -e orderly -s NEARUSDT --trail-pct 2.0
```

## Repo layout

```
tetrac-perp-trader/
├── SKILL.md                   # agent instructions (operational rules, checklists)
├── README.md                  # this file (humans)
├── scripts/
│   ├── skill-trading                    # POSIX launcher
│   ├── skill-trading-darwin-arm64       # macOS Apple Silicon binary
│   └── skill-trading-linux-x64          # Linux x86_64 binary
└── references/
    ├── api-reference.md       # full TTC Box REST API
    ├── exchanges.md           # per-exchange credential setup
    └── troubleshooting.md     # error → cause → fix
```

## License

MIT. See `SKILL.md` frontmatter and the source repo for the full text.
