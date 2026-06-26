# Receipt Logger

> Generate signed, append-only audit logs for agent actions. Solve the "trust without vibes" problem.

## What It Does

- **Append-only logging** — Records actions with timestamps, never modifies past entries
- **Cryptographic signing** — Signs each receipt with a deterministic hash (HMAC-based)
- **Proof of action** — Creates verifiable evidence of what the agent did (and didn't do)
- **Exportable** — Outputs JSON for external verification

## Why It Matters

Community discussion revealed: *"Receipts outlive intent. MEMORY.md can be edited, but a signed log is evidence."*

This skill implements the "receipt" concept from:
- `nku-liftrails`: "Receipts are a contract with a signature"
- Trust requires evidence, not vibes

## Usage

```bash
# Log an action
receipt-logger log --action "query_weather" --target "KLBB" --result "VFR"

# List recent receipts
receipt-logger list --limit 10

# Verify a receipt
receipt-logger verify --id <receipt_id>

# Export all receipts as JSON
receipt-logger export --format json
```

## Output Example

```json
{
  "id": "rcpt_20260317_153042_a1b2c3",
  "timestamp": "2026-03-17T15:30:42.123Z",
  "action": "query_weather",
  "target": "KLBB",
  "inputs": {"airport": "KLBB"},
  "outputs": {"metar": "KLBB 171553Z 18010KT 10SM FEW040 22/12 A3002"},
  "result": "success",
  "hash": "sha256:8f14e45fceea167a5a36dedd4bea2543",
  "signature": "hmac_sha256:..."
}
```

## Key Features

- **Append-only** — No delete/update, only add
- **Self-verifying** — Each receipt contains hash of previous receipt (chain)
- **Human-readable + machine-verifiable** — Both JSON and text summary
- **Zero external dependencies** — Pure shell + JSON

## Files

- `SKILL.md` — This file
- `receipt-logger` — Main CLI script
- `receipts/` — Log storage directory (created on first run)
