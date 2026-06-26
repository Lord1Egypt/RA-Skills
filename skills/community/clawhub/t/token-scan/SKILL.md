---
name: token-scan
description: Scan token contract security risk and return a structured summary including score, tax, holder concentration, and LP lock status. Supported chains are bsc, eth, solana, arbitrum, base, polygon, avax, tron, ton, plasma, and sui. Trigger when the user provides a chain and contract address and asks for token risk analysis, security review, high-risk item identification, tax interpretation, or holder distribution analysis.
license: MIT
compatibility: Compatible with Cursor/Codex Agent Skills, Claude Agent Skills runtimes (Claude Code/claude.ai/API), and OpenClaw Skills. Requires Python >=3.9, outbound HTTPS access to open.api.certik.com, and permission to execute `{skillDir}/scripts/token_scan.py`.
metadata:
  url: https://open.api.certik.com/token-scan
  script: <skillDir>/scripts/token_scan.py
  primary-commands: scan
---

# Token Scan

Use `{skillDir}/scripts/token_scan.py` to inspect one token contract with the CertiK token scan API.

Use this skill when the user wants a token risk review for a specific chain and contract address.

## When to use this skill

- Analyze token contract security risk
- Review high-risk findings and alert severity
- Interpret buy or sell tax fields
- Check holder concentration and LP lock status

## Supported chains

`bsc`, `eth`, `solana`, `arbitrum`, `base`, `polygon`, `avax`, `tron`, `ton`, `plasma`, `sui`

If the user provides a chain outside this list, do not call the API. Tell the user the chain is not supported yet and list the supported chains.

## Workflow

1. Confirm the chain is supported.
2. Validate the address format when the chain format is obvious from the input.
3. Prefer the bundled Python script for execution.
4. If Python is unavailable, use the documented `curl` fallback.
5. If the result is still running, report that the scan is in progress instead of pretending the scan is complete.
6. Return the result in this order:
   - risk overview
   - alert list
   - additional token signals such as tax, holder concentration, and LP lock
7. Only include raw fields when the user explicitly asks for audit-level detail.

## Execution

> Important: `--chain` only supports `bsc|eth|solana|arbitrum|base|polygon|avax|tron|ton|plasma|sui`.
> If the user provides a chain outside this list, do not call the API. Reply that the chain is not supported yet and include the supported chain list so the user can switch.

Prefer Python first:

```bash
python3 scripts/token_scan.py --chain "bsc" --contract "0x..."
```

If Python is unavailable, use `curl`:

```bash
curl -sG "https://open.api.certik.com/token-scan" \
  -H "Accept: application/json, text/plain, */*" \
  --data-urlencode "chain=bsc" \
  --data-urlencode "address=0x..."
```

## Output requirements

1. Risk overview must include `score`, `alert_count`, and the highest alert level.
2. Alert list must be sorted by `Critical -> Major -> Medium -> Minor` and show up to 8 items.
3. If `alert_count > 8`, explicitly say: `Total N alerts, showing the top 8 highest-priority items`.
4. Clarify that values like `skyknight_score.details.buy_tax` and `skyknight_score.details.sell_tax` are deduction factors, not the real tax percentage.
5. Prefer the real buy or sell tax value from `security_summary.*.extended_data.*` when it exists.

## Public API

- Endpoint: `GET https://open.api.certik.com/token-scan`
- Query parameters:
  - `chain` (required)
  - `address` (required)

Example:

```bash
curl -sG "https://open.api.certik.com/token-scan" \
  -H "Accept: application/json, text/plain, */*" \
  --data-urlencode "chain=eth" \
  --data-urlencode "address=0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"
```

Supported chain formats:

- `arbitrum`: EVM hex `0x...` with 42 chars
- `avax`: EVM hex `0x...` with 42 chars
- `base`: EVM hex `0x...` with 42 chars
- `bsc`: EVM hex `0x...` with 42 chars
- `eth`: EVM hex `0x...` with 42 chars
- `plasma`: EVM hex `0x...` with 42 chars
- `polygon`: EVM hex `0x...` with 42 chars
- `solana`: Base58 public key
- `sui`: Hex `0x...` with module path
- `ton`: `EQ` or `UQ` prefix, 46-48 chars
- `tron`: Base58check, starts with `T`, 34 chars

## Result notes

- If `message` is `in progress`, the scan has not finished.
- If `message` is `success`, the scan is complete and can be summarized.
- If `message` is `error`, return the upstream error information.
- `skyknight_score.details.buy_tax` and `skyknight_score.details.sell_tax` are deduction factors, not literal tax percentages.
- Prefer actual tax values from:
  - `security_summary.buy_tax.extended_data.buy_tax`
  - `security_summary.sell_tax.extended_data.sell_tax`
