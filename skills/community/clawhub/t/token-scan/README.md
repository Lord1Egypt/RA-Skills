# Token Scan

CertiK Token Scan skill for contract-level token risk analysis across supported chains.

Use `scripts/token_scan.py` as the default entrypoint to inspect one token contract with the CertiK token scan API.

## Files

- `SKILL.md`: agent-facing instructions and summary rules
- `scripts/token_scan.py`: CLI wrapper for the public token scan endpoint

## Quick Start

Run commands from this directory:

```bash
python3 scripts/token_scan.py --chain bsc --contract 0x...
```

Fallback with `curl`:

```bash
curl -sG "https://open.api.certik.com/token-scan" \
  -H "Accept: application/json, text/plain, */*" \
  --data-urlencode "chain=bsc" \
  --data-urlencode "address=0x..."
```

## Supported Chains

`bsc`, `eth`, `solana`, `arbitrum`, `base`, `polygon`, `avax`, `tron`, `ton`, `plasma`, `sui`

## Typical Use Cases

- Review a token's overall risk posture
- Highlight the highest-priority alert items
- Explain holder concentration and LP lock signals
- Clarify tax-related fields in the result

## Workflow

1. Confirm the chain is supported.
2. Run the bundled Python script first.
3. If the API reports `in progress`, tell the user the scan has not completed yet.
4. Return findings in this order: risk overview, alert list, then extra token signals.

## Output Notes

- Risk overview should prioritize `score`, `alert_count`, and the highest alert severity.
- Alert items should be ordered `Critical -> Major -> Medium -> Minor`.
- Show at most 8 alert items, and explicitly say when additional alerts were omitted.
- `skyknight_score.details.buy_tax` and `skyknight_score.details.sell_tax` are deduction factors, not literal tax percentages.
- Prefer real tax values from `security_summary.buy_tax.extended_data.buy_tax` and `security_summary.sell_tax.extended_data.sell_tax` when available.

## API Notes

- Endpoint: `GET https://open.api.certik.com/token-scan`
- Required query parameters: `chain`, `address`
- The script sends `address=<contract>` as a query parameter, even though the CLI argument name is `--contract`
