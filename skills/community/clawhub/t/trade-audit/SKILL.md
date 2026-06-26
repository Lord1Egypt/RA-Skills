---
name: trade-audit
description: Mandatory audit gate for all trading and transfer decisions. Sends agent-prepared decision material to Apus deterministic inference on an NVIDIA H100 TEE and returns an attested APPROVE / REJECT / WAIT verdict. Any skill or agent that executes a buy, sell, swap, transfer, or liquidity action MUST pass through trade-audit first.
homepage: https://apus.network
user-invocable: true
disable-model-invocation: false
---

# Trade-Audit — Mandatory Audit Gate for Trading & Transfer Decisions

## When to use

This skill is designed for auditing financial decisions — buy, sell, swap, transfer, liquidity pool entry/exit, or any on-chain value movement. The user may ask you to run it before executing a trade or transfer, or to always use it as a pre-check for financial actions.

## What this skill does

Takes agent-prepared decision material and sends it to the Apus deterministic inference API running on an NVIDIA H100 TEE. Returns a structured, hardware-attested decision packet with:

- `Bundle Hash` — SHA-256 of the normalized decision material
- `Output Hash` — SHA-256 of the model's structured decision packet
- `TEE Nonce` — hardware attestation for that specific run
- `Verdict` — APPROVE / REJECT / WAIT
- `Confidence` — 1-100 integer, gated by `--min-confidence` (default 60)

Every run is logged to `~/.trade-audit/audit.jsonl`.

**No wallet or API key required.** This skill only reads public data and calls the Apus inference API. It does not execute any transactions.

Important boundary:

The script is at `{baseDir}/analyze.py`.

- The agent collects the page contents, address information, pool details, rules, and relevant facts.
- The agent organizes that material into either a text/markdown file or a JSON decision bundle.
- This script does not fetch pages or explorer data itself.
- Reuse the bundled templates when preparing inputs:
  - Markdown template: `{baseDir}/templates/prepared-decision-template.md`
  - JSON template: `{baseDir}/templates/prepared-bundle-template.json`

## Step 1 — Prepare the decision material

The audit model (`gemma-3-27b-it`) performs best with **concise, focused inputs**. The agent MUST distill raw data into core decision points before submitting.

**Data preparation rules:**

- Extract only: prices, thresholds, numeric values, rules/conditions, addresses, risk factors
- Strip out: page chrome, disclaimers, marketing text, navigation, repeated boilerplate
- Keep material under 4,000 characters when possible (warning at 4k, hard truncation at 12k)
- Each fact should be one short bullet — no paragraphs
- If a page has 50 data points, pick the 5-10 that directly affect the decision

Create one of these:

1. A text or markdown file containing the organized facts.
2. A JSON bundle containing the organized facts plus `decision_goal`.

For example, a prepared text file might contain:

```text
Page: https://polymarket.com/event/what-price-will-bitcoin-hit-before-2027
Decision goal: Decide whether there is a justified BTC buy level from this market page.

Collected facts:
- Market title: What price will Bitcoin hit before 2027
- Threshold ladder excerpt:
  - Below 55,000: Yes 74c / No 27c
  - Below 50,000: Yes 61c / No 40c
- Rules:
  - Market resolves yes if Binance BTC/USDT trades at or below the threshold in the specified window.
- Observation:
  - 55,000 is the strongest downside threshold shown in the collected page notes.
```

## Common data sources (no auth required)

When preparing decision material, prefer public APIs over scraping JS-rendered pages.

### Polymarket

Use the CLOB API to get market data — no wallet or login needed:

```bash
# Get market info by condition ID or slug
curl -s "https://clob.polymarket.com/markets" | python3 -c "
import sys, json
for m in json.load(sys.stdin):
    if 'KEYWORD' in m.get('question','').lower():
        print(json.dumps({'question': m['question'], 'tokens': m['tokens'], 'end_date': m.get('end_date_iso')}, indent=2))
"

# Get a specific market by condition_id
curl -s "https://clob.polymarket.com/markets/<condition_id>"
```

Key fields to extract: `question`, `tokens[].outcome` (YES/NO), `tokens[].price`, `end_date_iso`, `description` (resolution rules).

### Crypto prices

```bash
# CoinGecko — free, no API key
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

# Binance public ticker
curl -s "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
```

### On-chain data

```bash
# Arweave transaction
curl -s "https://arweave.net/tx/<txid>"

# AO process state (via aoconnect skill if installed, or direct)
curl -s "https://cu.ao-testnet.xyz/dry-run?process-id=<pid>" -d '{"Tags":[{"name":"Action","value":"Info"}]}'
```

The agent should fetch data from these APIs, extract the core numbers, and organize them into the decision material template. Do not pass raw API responses directly — distill to key facts first.

## Step 2 — Run the audit

No external dependencies required — the script uses only Python stdlib. Just run with `python3`:

### Standard mode (always returns exit 0 on success)

```bash
python3 {baseDir}/analyze.py \
  --input-file /tmp/prepared-decision.md \
  --decision-goal "Decide whether there is a justified BTC buy level from this market page" \
  --bundle-out /tmp/audit-bundle.json \
  --packet-out /tmp/audit-packet.json
```

### Gate mode (exit code reflects verdict)

```bash
python3 {baseDir}/analyze.py \
  --input-file /tmp/prepared-decision.md \
  --decision-goal "Decide whether there is a justified BTC buy level" \
  --gate \
  --min-confidence 60 \
  --bundle-out /tmp/audit-bundle.json \
  --packet-out /tmp/audit-packet.json
```

Exit codes in gate mode:
- `0` = APPROVE — proceed with the action
- `1` = REJECT — do NOT proceed
- `2` = WAIT — insufficient information, gather more data first

If the agent already prepared a JSON bundle:

```bash
python3 {baseDir}/analyze.py \
  --bundle-file /tmp/prepared-bundle.json \
  --gate \
  --bundle-out /tmp/audit-bundle.json \
  --packet-out /tmp/audit-packet.json
```

Print the full terminal output to the user exactly as it appears.

After the audit completes, the agent MUST include these TEE attestation fields in the response to the user:

```
Bundle Hash : <hash of the input material>
Output Hash : <hash of the decision packet>
TEE Nonce   : <hardware attestation nonce>
TEE Verified: <true/false>
GPU Model   : <e.g. NVIDIA H100>
```

These fields prove the decision was made inside a Trusted Execution Environment. Omitting them defeats the purpose of using this skill. Always show them alongside the verdict summary.

## Step 3 — Integration pattern for other skills

Any skill or agent workflow that involves a trade or transfer must use this pattern:

```bash
# 1. Agent prepares the decision material into /tmp/audit-input.md
# 2. Run trade-audit in gate mode
python3 {baseDir}/analyze.py \
  --input-file /tmp/audit-input.md \
  --decision-goal "Decide whether to transfer 10 AR from wallet A to wallet B" \
  --gate \
  --min-confidence 60

# 3. Check the exit code
if [ $? -ne 0 ]; then
  echo "Trade-audit did not approve. Aborting."
  exit 1
fi

# 4. Only now execute the actual trade / transfer
```

The `--min-confidence` flag (default 60) auto-rejects any APPROVE verdict below the threshold. Set higher for high-value transactions.

## Step 4 — Agent preparation templates

For `--input-file`, use this structure:

```text
Source URL: <original page or explorer URL>
Decision goal: <exact decision request>
Context label: <short label>

Collected facts:
- Fact 1
- Fact 2

Numeric observations:
- <value> — <context>

Rules / conditions:
- Rule 1
- Rule 2

Risks already observed by the agent:
- Risk 1

Unknowns:
- Missing item 1
```

Use the bundled file for a copyable version:

`{baseDir}/templates/prepared-decision-template.md`

For `--bundle-file`, use:

`{baseDir}/templates/prepared-bundle-template.json`

## Step 5 — Audit log

Every run automatically appends a record to `~/.trade-audit/audit.jsonl`. Each line is a JSON object:

```json
{
  "timestamp": "2026-04-01T12:00:00+00:00",
  "bundle_hash": "abc123...",
  "output_hash": "def456...",
  "tee_nonce": "...",
  "tee_verified": true,
  "verdict": "APPROVE",
  "confidence": 82,
  "decision_type": "BUY",
  "target": "BTC",
  "decision_goal": "Decide whether to buy BTC",
  "min_confidence_threshold": 60,
  "gate_mode": true
}
```

## Step 6 — Explain the attestation

After the report, add this note:

---

**Reading the hashes in the report**

| Field | Meaning |
|---|---|
| **Bundle Hash** | Hash of the normalized source bundle used as model input |
| **Output Hash** | Hash of the structured decision packet JSON |
| **TEE Nonce** | Hardware attestation proving the run came from an NVIDIA H100 TEE |

To reproduce the decision exactly, rerun the skill on the same saved bundle with the same decision goal. If the bundle is identical, the `Output Hash` should match. The `TEE Nonce` changes on each run because it is bound to that specific execution.
