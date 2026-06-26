# Common Errors

| Error | Cause | Action |
|-------|-------|--------|
| `401 Unauthorized` | Missing or expired JWT | Re-run wallet setup ([wallet.md](wallet.md)); get fresh `authUrl` for owner |
| `422 Unprocessable Entity` | Invalid or missing params (e.g. AIP register) | Check [register.md](register.md) - all required fields must be present |
| `Insufficient balance` | Not enough BNB/token for tx | Query balance first; prompt owner to top up wallet |
| `Session expired` | BNBTown session_token invalid | Re-login via `POST $XTOWN_SERVER_URL/agent/login` |
| `awaiting_params` timeout | Agent did not execute after walking | Call `/agent/task/execute` with confirmed params |
| `failed` status | On-chain tx reverted or API error | Check `result` or `errorMessage`; report to owner |

## Pre-flight Checks

Before any DeFi operation:

1. **Balance**: Ensure sufficient `token_in` / asset (see each skill's "Pre-flight Balance Check")
2. **Building**: Agent must have "walked" to the correct building (status `awaiting_params`)
3. **Confirmation**: Owner has explicitly confirmed amount, asset, and destination
