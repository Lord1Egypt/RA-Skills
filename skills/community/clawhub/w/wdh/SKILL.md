---
name: wdh
description: Call any of seven paid-per-call CLI utilities on WDH.sh — big-file transfer (≤5 GB), URL shortening, Chart.js rendering, hosted markdown pages, QR codes, paid feature requests, paid support tickets — settled in USDC on Base mainnet via x402 with no signup or API key. Use when the user wants any of these utilities and has an EVM wallet, or mentions x402, USDC, micropayment, pay-per-call, or any of the wdh.sh hostnames (files.wdh.sh, short.wdh.sh, charts.wdh.sh, md.wdh.sh, qr.wdh.sh, feedback.wdh.sh, support.wdh.sh). Costs $0.001–$5.00 USDC per call depending on tool.
version: 0.2.0
metadata:
  openclaw:
    requires:
      env:
        - WDH_WALLET_PRIVATE_KEY
      anyBins:
        - bunx
        - npx
        - wdh
    primaryEnv: WDH_WALLET_PRIVATE_KEY
    envVars:
      - name: WDH_WALLET_PRIVATE_KEY
        required: true
        description: Hex-encoded EVM private key (starts with 0x) for a wallet funded with USDC on Base mainnet. Every CLI command signs an x402 payment with this key.
    emoji: "🦸"
    homepage: https://wdh.sh
---

# WDH.sh

A family of seven small, paid-per-call HTTP services for agents and humans.
One CLI wraps every endpoint and signs payments automatically using the
agent's wallet — no signups, no API keys, no subscriptions. Every call is
settled in USDC on Base mainnet via the [x402](https://x402.org) protocol.

## Prerequisites

- An EVM wallet with **USDC on Base mainnet** (`eip155:8453`). $1 of USDC
  covers thousands of calls except for `feedback` ($1) and `support` ($5).
- Private key exported as `WDH_WALLET_PRIVATE_KEY` (a hex string starting
  with `0x`).
- Node.js 20+ (the CLI ships as [`@wdhsh/cli`](https://www.npmjs.com/package/@wdhsh/cli) on npm and runs anywhere Node runs).

The buyer never submits an on-chain transaction directly. The Coinbase
x402 facilitator handles settlement and pays gas. See
[https://x402.org](https://x402.org) for protocol detail.

## Services Overview

| Tool | Cost (USDC) | Purpose |
|---|---|---|
| `files` | $0.001 – $0.10 (size-tiered) | Big-file transfer to a public expiring URL (≤5 GB, ≤7 days) |
| `short` | $0.001 | URL shortener — links never expire by default |
| `charts` | $0.005 | Chart rendering proxy (Chart.js payload → PNG) |
| `md` | $0.002 | Publish a markdown file as a hosted HTML page (≤30 days) |
| `qr` | $0.001 | QR code image (PNG or SVG) |
| `feedback` | $1.00 | Paid feature request — opens a Linear issue on the WDH team's tracker |
| `support` | $5.00 | Paid support ticket — opens a high-priority Linear issue |

## Install

The CLI is published as [`@wdhsh/cli`](https://www.npmjs.com/package/@wdhsh/cli) on npm.
Use it via `bunx` or `npx` for zero-install, or install globally:

```bash
bunx @wdhsh/cli --help        # zero-install, one-shot
npm i -g @wdhsh/cli && wdh --help
```

```bash
export WDH_WALLET_PRIVATE_KEY=0x...
```

Once the env var is set, every command pays automatically. Without it the
CLI refuses to run.

## Commands

### `files upload` — Big-file transfer

Multipart upload to `files.wdh.sh`. Returns a public download URL.

```bash
bunx @wdhsh/cli files upload ./report.pdf --expires 7d
bunx @wdhsh/cli files upload ./build.tar.gz                   # 24h default TTL
```

| Flag | Required | Default | Description |
|---|---|---|---|
| `<path>` | yes | — | Path to the file to upload (up to 5 GB) |
| `--expires <ttl>` | no | `24h` | TTL like `30m`, `24h`, `7d`. Max 7 days |

Size-tiered pricing: $0.001 (≤10 MB), $0.005 (≤100 MB), $0.02 (≤500 MB),
$0.05 (≤2 GB), $0.10 (≤5 GB).

### `short create` — URL shortener

Returns a short `https://short.wdh.sh/<slug>` URL. **Links never expire by
default** — safe for business cards, printed materials, anywhere a permanent
redirect target is wanted.

```bash
bunx @wdhsh/cli short create https://example.com/very/long/path
bunx @wdhsh/cli short create https://example.com --slug launch
bunx @wdhsh/cli short create https://example.com --expires 30d
```

| Flag | Required | Default | Description |
|---|---|---|---|
| `<url>` | yes | — | URL to shorten (http or https only) |
| `--slug <s>` | no | auto-generated | Custom slug. Matches `^[A-Za-z0-9_-]{3,32}$` |
| `--expires <ttl>` | no | never | TTL like `24h`, `30d`. Omit and the link persists indefinitely |

### `charts plot` — Chart.js rendering

Proxies a [Chart.js](https://www.chartjs.org/) payload to the chartsplat
renderer. Writes raw PNG bytes to stdout (or to `--out` if provided).

```bash
bunx @wdhsh/cli charts plot \
  --type bar \
  --data '{"labels":["Q1","Q2","Q3","Q4"],"datasets":[{"label":"Revenue","data":[50,75,60,90]}]}' \
  > chart.png
```

| Flag | Required | Default | Description |
|---|---|---|---|
| `--type <kind>` | yes | — | Chart.js chart type (`bar`, `line`, `pie`, `doughnut`, `radar`, etc.) |
| `--data <json>` | yes | — | Chart.js JSON payload as a string (parsed and forwarded as the request body) |

See [chartsplat docs](https://chartsplat.com/docs) for the full schema and
supported chart types.

### `md publish` — Hosted markdown pages

Publishes a local markdown file as a styled HTML page on `md.wdh.sh`.
Returns the public URL.

```bash
bunx @wdhsh/cli md publish ./notes.md
bunx @wdhsh/cli md publish ./post.md --title "Launch notes"
bunx @wdhsh/cli md publish ./scratch.md --expires 24h
```

| Flag | Required | Default | Description |
|---|---|---|---|
| `<file>` | yes | — | Path to a local markdown file (max 1 MB) |
| `--title <t>` | no | `Shared markdown` | Page title for the rendered HTML |
| `--expires <ttl>` | no | `7d` | TTL like `24h`, `7d`, `30d`. Max 30 days |

Renderer is `markdown-it` with HTML escaped and `javascript:` / `data:` /
`vbscript:` / `file:` links dropped.

### `qr generate` — QR code images

Renders a QR code as a PNG (default) or SVG.

```bash
bunx @wdhsh/cli qr generate "https://wdh.sh" --out wdh.png
bunx @wdhsh/cli qr generate "wifi:T:WPA;S:...;P:..." --size 1024 > wifi.png
bunx @wdhsh/cli qr generate "ping" --format svg > ping.svg
```

| Flag | Required | Default | Description |
|---|---|---|---|
| `<data>` | yes | — | Text or URL to encode (max 2048 chars) |
| `--size <px>` | no | `512` | Output size in pixels. Clamped to 64–2048 |
| `--format <png\|svg>` | no | `png` | Output format |
| `--out <file>` | no | stdout | Write the image to a file path instead |

### `feedback` — Paid feature requests

Files a $1.00 paid feature request as a Linear issue on the WDH team's
tracker. Returns the issue URL.

```bash
bunx @wdhsh/cli feedback "Add Solana support" --body "We'd use this for..."
echo "long-form body here" | bunx @wdhsh/cli feedback "Title goes here"
bunx @wdhsh/cli feedback "Bug in qr" --body "..." --contact me@example.com
```

| Flag | Required | Default | Description |
|---|---|---|---|
| `<title>` | yes | — | Issue title (max 200 chars) |
| `--body <text>` | no | from stdin | Issue body (max 10 000 chars). Omit to read from stdin |
| `--contact <email>` | no | — | Optional reply-to address |

### `support` — Paid support tickets

Files a $5.00 paid support ticket as a high-priority Linear issue.
Severity maps to Linear priority. `--contact` is required so the team can
follow up.

```bash
bunx @wdhsh/cli support "Files endpoint 500s" \
  --contact me@example.com \
  --body "every /init returns 500 since 14:00 UTC" \
  --severity high

cat incident.md | bunx @wdhsh/cli support "x402 settlement timing out" \
  --contact me@example.com --severity critical
```

| Flag | Required | Default | Description |
|---|---|---|---|
| `<title>` | yes | — | Ticket title (prefixed with `[support]`, max 200 chars) |
| `--contact <email>` | yes | — | Reply-to email |
| `--body <text>` | no | from stdin | Ticket body (max 10 000 chars). Omit to read from stdin |
| `--severity <lvl>` | no | `medium` | `low \| medium \| high \| critical` → Linear priority 4\|3\|2\|1 |

## Output Handling

- Most commands print a **single line to stdout**: the resulting URL
  (`files`, `short`, `md`, `feedback`, `support`) or the path that was
  written (`qr --out <file>`).
- `qr` (without `--out`) and `charts` write **raw image bytes** to stdout —
  always pipe to a file: `> chart.png`.

## Tips

- **Wallet hygiene.** Use a throwaway Base wallet for the agent — load it
  with the budget you're willing to spend and revoke by deleting the key.
- **Idempotency for `feedback` / `support`.** Those endpoints accept an
  `Idempotency-Key` header server-side (24h cache). The CLI doesn't surface
  that flag yet — re-running a command will file a duplicate Linear issue
  and charge again.
- **Short links are permanent by default.** Omitting `--expires` on
  `short create` means the redirect persists indefinitely — fine for
  business cards, printed QR targets, social bios. Add `--expires` only
  if you want it to lapse.
- **Files are temporary.** `files upload` defaults to a **24-hour** TTL.
  Pass `--expires 7d` for the maximum.
- **Charts payload.** The `--data` JSON is a full Chart.js config (or just
  the inner `data` object — chartsplat accepts both). For OHLC /
  candlestick charts pass `{ x, o, h, l, c }` points.

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| `WDH_WALLET_PRIVATE_KEY env var is required` | Env var unset | `export WDH_WALLET_PRIVATE_KEY=0x...` |
| 402 retry fails / `insufficient funds` | Wallet has no USDC on Base | Top up; even $1 covers thousands of small calls |
| `failed: 413` on `files upload` | File >5 GB | Split the upload; 5 GB is the per-call max |
| `failed: 400` on `md publish` | Markdown >1 MB | Trim or split the document |
| `invalid duration` | Bad `--expires` value | Use formats like `30m`, `24h`, `7d` |
| `failed: 503` on `short create --slug` | 8 slug collisions in a row | Pick a different slug or let it auto-generate |

## Related

- CLI on npm: [`@wdhsh/cli`](https://www.npmjs.com/package/@wdhsh/cli)
- Per-service web docs: [wdh.sh/docs](https://wdh.sh/docs)
- The x402 protocol: [x402.org](https://x402.org)
- The standalone chartsplat-x402 skill (uses chartsplat directly without
  WDH's proxy markup): `chartsplat-x402` on ClawHub.
