# Command Map

| Command | Description | Required Flags | Optional Flags |
| --- | --- | --- | --- |
| `convert` | Convert an amount between currencies | `--from`, `--to` | `--amount`, `--date` |
| `latest` | Show latest rates for a base currency | `--from` | `--to` |
| `history` | Show rate on a specific date | `--from`, `--date` | `--to` |
| `series` | Show rate trend over a date range | `--from`, `--start`, `--end` | `--to` |
| `currencies` | List all supported currencies | - | - |

## Flag Details

| Flag | Format | Example |
| --- | --- | --- |
| `--from` | ISO 4217 currency code | `USD`, `CNY`, `EUR` |
| `--to` | One or more codes, comma-separated | `CNY`, `CNY,JPY,EUR` |
| `--amount` | Positive number | `100`, `1500.50` |
| `--date` | `YYYY-MM-DD` | `2025-06-15` |
| `--start` | `YYYY-MM-DD` | `2025-01-01` |
| `--end` | `YYYY-MM-DD` | `2025-01-31` |

## Exit Codes
- `0`: success
- `2`: input or config error (invalid currency code, bad date format, etc.)
- `3`: network / timeout / HTTP transport error
- `4`: API business error
- `5`: unexpected internal error

## API Base URL
- `https://api.frankfurter.dev/v1`
- No API key required.
