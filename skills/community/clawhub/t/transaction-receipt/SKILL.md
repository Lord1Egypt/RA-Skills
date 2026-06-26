---
name: transaction-receipt
version: 1.1.2
description: >
  Human-readable on-chain transaction receipt. Resolve tx status, fees, and intent:
  simple transfers, swaps/trades, token approvals, DeFi staking-style calls, and NFT
  mint/transfer. Optional Tokenview API key; falls back to public read-only sources
  when unset or invalid. Timeouts, rate limits, and response validation included.
author: Antalpha AI Team
requires: [curl]
metadata:
  repository: https://github.com/AntalphaAI/transaction-receipt
  install:
    type: instruction-only
  env:
    - name: TOKENVIEW_API_KEY
      description: Tokenview API key for comprehensive transaction data
      required: false
      sensitive: true
    - name: TRANSACTION_RECEIPT_MAX_PER_HOUR
      description: Hourly query limit (default 30)
      required: false
    - name: TRANSACTION_RECEIPT_RATE_FILE
      description: Custom path for rate limit log file
      required: false
---

# transaction-receipt (On-chain receipt translator)

## Environment and configuration

| Variable | Required | Secret | If missing |
|----------|----------|--------|------------|
| `TOKENVIEW_API_KEY` | No | Yes | Do not call Tokenview; use **public Fallback** (below). Recommend users obtain a key at [tokenview.io](https://tokenview.io) for richer, more uniform payloads. |
| `TRANSACTION_RECEIPT_MAX_PER_HOUR` | No | No | Default **30**: cap all on-chain lookups (Tokenview or Fallback) at **30 per hour** per machine user. |
| `TRANSACTION_RECEIPT_RATE_FILE` | No | No | Default to `~/.openclaw/state/transaction-receipt/rate-limit.log`. Use this to relocate state safely (for read-only home dirs, containers, or custom persistence paths). |

**Dependency:** `curl` must be available. If not, explain that this skill cannot run and suggest installing `curl`. Optional: `jq` for JSON checks; otherwise use `python3 -c` (macOS usually ships Python 3).

---

## API key flow (user-first, then public, then friendly failure)

1. **Prefer the user’s key:** At onboarding or before the first lookup of a session, **gently** ask whether they have configured `TOKENVIEW_API_KEY` in their environment or OpenClaw settings (do **not** ask them to paste the full key in chat).
2. **If a key is configured (non-empty):** Use Tokenview as the primary path.
3. **If no key is configured:** Use **only** the public Fallback path—this is normal, not an error.
4. **If a key is configured but invalid / expired:** After detecting auth failure, **automatically** switch to Fallback and briefly tell the user: e.g. “Your Tokenview key could not be used; results are from a public data source instead.”
5. **If both paths fail or the tx cannot be found:** Give a **short, friendly** message (network issue, wrong chain, not yet broadcast, hash typo, or rate limit). **Do not** dump raw responses.

Never echo, display, or ask the user to paste a complete API key.

---

## Onboarding (first-time users)

If the user seems new, say something like:

> Welcome! For the steadiest results, configure `TOKENVIEW_API_KEY` in your settings. If you skip it, we’ll use public read-only endpoints (they may be slower or rate-limited). You can get a key at [tokenview.io](https://tokenview.io).

---

## When to activate

Enable when the user uses this skill or when a message contains an extractable on-chain hash:

1. **BTC txid:** exactly **64** hex chars (`0-9`, `a-f`, `A-F`), **no** `0x` prefix.
2. **EVM tx hash:** starts with **`0x`**, total length **66**, next **64** chars are hex.

**Bounded input:** After `trim`, take the **first** token that passes validation. Reject overlong strings, multiple hashes in one blob, or illegal characters.

---

## Rate limiting (P0 — before any on-chain request)

**Goal:** Avoid burning Tokenview quota or getting public nodes blocked.

1. Resolve hourly cap: `MAX="${TRANSACTION_RECEIPT_MAX_PER_HOUR:-30}"`.
2. Resolve state path in this order:
   - If `TRANSACTION_RECEIPT_RATE_FILE` is set, use it directly.
   - Else use `~/.openclaw/state/transaction-receipt/rate-limit.log`.
   - If `HOME` is unavailable, fallback to `${TMPDIR:-/tmp}/transaction-receipt-rate-limit.log`.
3. Ensure the parent directory exists (`mkdir -p`), then ensure file permissions are private where possible (`chmod 600 "$RATE_FILE" 2>/dev/null || true`).
4. **Before each** planned on-chain request (Tokenview or Fallback):
   - `NOW=$(date +%s)`, `CUTOFF=$((NOW - 3600))`.
   - If the file exists: keep only numeric timestamps newer than `CUTOFF`, rewrite the file.
   - Enforce a hard cap on retained rows (e.g. keep the most recent 10,000 lines) to prevent unbounded growth.
   - `COUNT=$(wc -l < "$RATE_FILE" | tr -d ' ')`; if `COUNT` ≥ `MAX`, **do not** send the request; tell the user they hit the hourly limit and may retry later or raise `TRANSACTION_RECEIPT_MAX_PER_HOUR`.
   - If under cap: `echo "$NOW" >> "$RATE_FILE"`, then proceed.
5. If the state file cannot be written (permission or filesystem issue), continue with an in-memory/session-only counter and clearly note that rate limiting persistence is degraded.

Rate limiting is **per machine, per OS user** by default; no cross-device sync inside this skill.

---

## Actions (data routing)

### Shared: curl timeouts (P0)

Every `curl` call **must** include:

`--connect-timeout 5 --max-time 30`

### 1. Extract hash and environment

Extract `HASH` from user input. Treat non-empty `TOKENVIEW_API_KEY` as “key configured.”

### 2. Source selection

- **Key configured:** Tokenview first.
- **Key not configured:** Fallback only.
- **Key configured but invalid:** after auth failure, Fallback (do not stop the flow).

### 3-A. Primary: Tokenview (GET)

After rate limit, run (expand `HASH` / key in the shell; **never** print full URL or key to the user):

**EVM** (`HASH` starts with `0x`):

```bash
curl -sS --connect-timeout 5 --max-time 30 \
  "https://services.tokenview.io/vipapi/tx/eth/${HASH}?apikey=${TOKENVIEW_API_KEY}"
```

**BTC** (64 hex, no `0x`):

```bash
curl -sS --connect-timeout 5 --max-time 30 \
  "https://services.tokenview.io/vipapi/tx/btc/${HASH}?apikey=${TOKENVIEW_API_KEY}"
```

Doc shorthand: `https://services.tokenview.io/vipapi/tx/eth|btc/{{hash}}?apikey={{TOKENVIEW_API_KEY}}` (still use curl timeouts).

### 3-B. Fallback: public read-only (no key or bad key)

Use when **no key** or **Tokenview auth failure**. Same rate limit and curl timeouts.

**EVM:** JSON-RPC POST (example mainnet: `https://ethereum.publicnode.com`; one silent retry on another public endpoint such as `https://1rpc.io/eth` is allowed—do **not** paste verbose retry logs to the user).

1. `eth_getTransactionByHash`:

```bash
curl -sS --connect-timeout 5 --max-time 30 -X POST \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getTransactionByHash\",\"params\":[\"${HASH}\"],\"id\":1}" \
  "https://ethereum.publicnode.com"
```

2. If `result` is not null, call `eth_getTransactionReceipt` with the same URL and `params: ["${HASH}"]` for success/failure (`status`) and **logs** (needed to classify Swap / Approve / NFT / staking).

**Optional enrichment (Fallback, EVM):** If you need token metadata for decoded amounts, you may call `eth_call` to `symbol()` / `decimals()` on the contract address—still respect rate limits and timeouts.

**BTC:** GET Blockstream:

```bash
curl -sS --connect-timeout 5 --max-time 30 \
  "https://blockstream.info/api/tx/${HASH}"
```

404 / 429: map to friendly errors; never paste huge raw JSON.

### 3-C. Tokenview key validity

If `TOKENVIEW_API_KEY` is set:

1. HTTP **401/403** → switch to Fallback.
2. Body indicates invalid key / forbidden / unauthorized (case-insensitive) → Fallback.
3. If Fallback also fails, one short user-facing error—no dual full payloads.

---

## Scope of txid interpretation (beyond “plain transfer”)

The skill applies to **any** valid BTC or EVM tx hash. After you have validated JSON (Tokenview or RPC), **classify** the interaction and tailor the narrative:

### A. Simple transfer (native or ERC-20)

- **Goal:** State clearly **who sent what to whom** (from → to, asset, human-readable amount).
- Use `from` / `to` / `value` for native transfers; for ERC-20, infer from **Transfer** logs (`topics[0]` typically `0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef`) and decode sender, recipient, and amount (respect token decimals when known).

### B. Swap / trade (DEX aggregation, router calls, etc.)

- **Goal:** Summarize **what the user paid** and **what they received** (assets + approximate amounts).
- Use decoded logs (e.g. Swap/Sync/Mint/Burn style events), Tokenview’s decoded fields if present, or internal transfers—**best effort**. If legs are ambiguous, say what is certain and mark the rest as “not fully decoded.”

### C. Approve (ERC-20 allowance)

- **Goal:** Use a **warning tone**.
- Clearly state: the user **authorized a spender** (typically `spender` in the **Approval** log) to move up to **X** of **token Y** on their behalf. Explain in plain language that this is **permission for the contract to spend their tokens**, not necessarily an immediate transfer.
- Do **not** panic-monger; be factual and prominent (e.g. “⚠️ Approval: you granted spending rights…”).

### D. DeFi: stake / unstake / deposit / withdraw / claim (and similar)

- Describe the **observable** asset movements and the **contract** the user called.
- If decoding is incomplete: **fallback** to: “You interacted with a smart contract at `0x…` (short + full address). The exact DeFi action could not be fully summarized from available data.”

### E. NFT: mint / transfer (ERC-721 / ERC-1155)

- **Mint:** e.g. “You minted” or “NFT(s) were minted to your address,” with collection/name if available from logs or metadata hints.
- **Transfer:** who sent which NFT id (and quantity for 1155) to whom.
- If only `Transfer` with unknown collection, still report addresses and token id.

### F. Other complex contract calls

- If the tx is not clearly A–E above: use the **plain-language fallback**: “You performed an on-chain interaction with smart contract `0x…`.” Summarize **gas**, **status**, and any **large ETH/token movements** you can infer without guessing specific protocol semantics.

**Never invent** token amounts, counterparties, or protocol names not supported by validated data.

---

## Response validation (P1)

Before writing the receipt, **validate** structure. On failure, say something like: “The data format looks unexpected or the upstream API changed; please try again later.” **Do not fabricate** balances or status.

**General:** Body must be valid JSON (`python3 -c 'import json,sys; json.load(sys.stdin)'` or `jq`).

**Tokenview:** Recognizable tx object under root or `data`, or structured error fields—map errors, do not print the whole body.

**EVM JSON-RPC:** `jsonrpc` is `"2.0"`; `eth_getTransactionByHash` `result` object should include `hash` and `from` (or equivalent); `null` means not found (wrong hash, wrong chain, or not broadcast).

**BTC Blockstream:** top-level must include `txid`.

Validation is **internal**; do not print schemas or raw bodies to the user.

---

## Errors and degradation

- Non-2xx HTTP, timeouts, curl errors: short human explanation; **no** full upstream body.
- No key: Fallback only—normal path.
- Bad key: Fallback after detection; brief notice.
- **Nothing found after both paths:** friendly message (check network, chain, spelling, pending tx).

---

## Voice and output shape

**Voice:** Calm, patient **Web3 concierge**.

**Internally** decode and classify; **externally** avoid raw hex jargon unless needed for a hash/address line.

**Receipt must include:**

1. **Status:** success / failed / pending (with plain wording).
2. **Overview:** chain (BTC / EVM), **full** tx hash, time if known, block / height if known, confirmations if known.
3. **Interaction summary:** per classification above (transfer / swap paid↔received / ⚠️ approve / NFT / DeFi / generic contract).
4. **Fees:** clear units; EVM include `gasUsed` and effective gas price when available; BTC include fee rate if available.
5. **One-line takeaway:** plain-language wrap-up.
6. **Footer (required, last line only):** `Data aggregated by Antalpha AI`

### Final checks before send (mandatory)

1. If the body lacks the footer, append **one** line: `Data aggregated by Antalpha AI`
2. Remove any of these if they appear in the body:
   - `Sourced from public Ethereum RPC`
   - `transaction-receipt v1.1.1`
3. Do **not** print version banners (e.g. `transaction-receipt v*`, bare `v1.x.x`).
4. The **last line** of the message must be **exactly** `Data aggregated by Antalpha AI` (no trailing text, blank lines, or ellipsis after it).

**Presentation:**

- Addresses: short form + full when space allows (e.g. `0x12ab…89ef (0x12ab…full…)`).
- Numbers: human-readable with sane precision; note unit conversions when helpful (e.g. wei → ETH).
- Missing fields: say “not returned” / “unavailable,” never leave silent gaps.
- Never paste raw JSON blobs, long hex dumps, or full RPC payloads.

---

## Security (production)

- **Never** print full raw JSON responses or full API bodies.
- **Never** print `TOKENVIEW_API_KEY`.
- User-facing content = receipt summary + short errors only.

---

## Versioning

- Skill id: `transaction-receipt`; this document `version: 1.1.1`. Bump `version` and distribution together when you change behavior.
