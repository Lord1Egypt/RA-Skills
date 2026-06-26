# Error Playbook

Use exact message matching first. Provide deterministic fixes before broad diagnosis.

## Message-to-action map

| Error text (exact or pattern) | Probable cause | Immediate fix command(s) | Verification command |
| --- | --- | --- | --- |
| `Invalid mint address format` | Mint argument is malformed or not a valid Solana public key | Replace `<mint>` with a valid mint address and rerun quote first. Example: `trends-skill-tool quote buy <mint> --in-sol 0.1` | `trends-skill-tool quote buy <mint> --in-sol 0.1` |
| `Invalid address format` or `Invalid address format. Please check mint or address arguments.` | Public key parsing failed for address or mint argument (domain validation error or normalized unexpected error) | Re-check address/mint source and rerun with corrected value | `trends-skill-tool balance <address>` or `trends-skill-tool quote buy <mint> --in-sol 0.1` |
| `Network request failed. Please check RPC/API endpoints and connectivity.` | RPC/API endpoint unavailable, DNS/timeout/connectivity issue | Set known-good endpoints and retry. Example: `trends-skill-tool config set rpcUrl https://api.mainnet-beta.solana.com` and `trends-skill-tool config set apiBaseUrl https://api.trends.fun/v1` | `trends-skill-tool quote buy <mint> --in-sol 0.1` |
| `No claimable coin creator rewards found because reward account is not initialized` | Reward PDA for current wallet has not been created yet | Query status first and stop claim. Example: `trends-skill-tool reward status` | `trends-skill-tool reward status` (expect `accountExists=false`) |
| `No claimable coin creator rewards found because reward is 0` | Reward account exists but accumulated reward is zero | Query status and wait for reward accrual before retrying claim | `trends-skill-tool reward status` (expect `rewardLamports>0` before claim) |
| `error: unknown option '--slippage-bps'` (under `trends-skill-tool create`) | `create` no longer supports slippage flag | Remove `--slippage-bps` from create command and retry | `trends-skill-tool create --name \"My Coin\" --symbol \"MYC\" --first-buy 0.01` |
| `--<option> must be a non-negative integer` | Integer option received invalid format (`1e2`, decimals, text suffix, negative) | Re-enter as plain integer digits. Example: `--slippage-bps 100`, `--count 20` | Re-run the same command with corrected integer values |
| `--count must be <= 25` | `created` or `transactions` page size out of range | Use `--count` between `1` and `25` | `trends-skill-tool created <address> --count 20` |
| `--count must be >= 1` | `--count` is zero or negative | Use `--count` at least `1` | `trends-skill-tool holdings <address> --count 20` |
| `buy requires exactly one of --in-sol or --out-token.` | Both route flags were provided or neither was provided | Keep exactly one route flag | `trends-skill-tool buy <mint> --in-sol 0.01` |
| `sell requires exactly one of --in-token or --out-sol.` | Both route flags were provided or neither was provided | Keep exactly one route flag | `trends-skill-tool sell <mint> --in-token 1` |
| `quote buy requires exactly one of --in-sol or --out-token.` | Both route flags were provided or neither was provided | Keep exactly one route flag | `trends-skill-tool quote buy <mint> --in-sol 0.1` |
| `quote sell requires exactly one of --in-token or --out-sol.` | Both route flags were provided or neither was provided | Keep exactly one route flag | `trends-skill-tool quote sell <mint> --in-token 1` |
| `Key file does not exist: <path>` | `keypairPath` points to a missing file | Initialize wallet or set a valid keypair path. Example: `trends-skill-tool wallet init` then `trends-skill-tool config set keypairPath ~/.config/solana/id.json` | `trends-skill-tool wallet address` |
| `Target file already exists: <path>, use --force to overwrite` | `wallet init` target exists and overwrite flag missing | Re-run with `--force` if overwrite is intended | `trends-skill-tool wallet init --force` then `trends-skill-tool wallet address` |
| `Unsupported config key: <key>` | `config set/get` key is not allowed | Use supported keys only (`rpcUrl`, `apiBaseUrl`, `keypairPath`, `commitment`, `defaultSlippageBps`, `computeUnitLimit`, `computeUnitPriceMicroLamports`) | `trends-skill-tool config list` |
| `commitment only supports processed | confirmed | finalized` | Invalid commitment value | Set one of supported values only | `trends-skill-tool config set commitment confirmed` and `trends-skill-tool config get commitment` |

## Fallback diagnosis when no exact match exists

Run in this order:

```bash
trends-skill-tool --version
trends-skill-tool --help
trends-skill-tool config list
trends-skill-tool wallet address
```

Then rerun the failing command with explicit values for endpoints and route flags.

Example:

```bash
trends-skill-tool quote buy <mint> --in-sol 0.1 --rpc-url https://api.mainnet-beta.solana.com --api-base-url https://api.trends.fun/v1
```
