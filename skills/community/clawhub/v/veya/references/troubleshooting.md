# Troubleshooting

Every message below is returned by the server code. Match the text, then apply the fix.

## Access

| Message | Cause | Fix |
|---|---|---|
| `apiKey required` | Scoped or write tool called without `apiKey` | Ask the user for their product key and pass it as `apiKey` |
| `Create a product API key at https://app.veyanet.tech (System → API Keys) and fund your wallet. Guest sessions cannot write from MCP.` | Value is a guest JWT or not a `veya_dev_`/`veya_live_` key | Create a key at https://app.veyanet.tech (System → API Keys) |
| `Product API rejected this apiKey (HTTP <status>)` | Key unknown or revoked | Check with `veya_account`; mint a new key |
| HTTP 401 `{ "error": "unauthorized" }` | Self-hosted server with `MCP_API_KEY` | Send `Authorization: Bearer <key>` |
| `{ "httpStatus": 403, … }` | Guest or key without access to that environment | Use the key that owns the environment |

## Limits

| Message | Fix |
|---|---|
| `API key limit: 30 requests per minute` | Wait until the next minute, then retry once |
| `Daily seal limit: 20 relayer sends for this API key` | Pass the user's funded wallet, or wait until 00:00 UTC |
| `Daily seal limit: 100 relayer sends for this host` | Same as above |
| HTTP 429 | Over 120 `/mcp` requests per minute from one IP; slow down |

## Wallet and writes

| Message | Fix |
|---|---|
| `Your wallet has no ETH on Robinhood Chain. Add funds and try again.` | Mainnet: add ETH to the wallet bound to the key |
| `You don't have testnet tokens. Please get them for the transaction.` | Testnet: https://faucet.testnet.chain.robinhood.com/ |
| `payerPrivateKey does not match the wallet on this API key. Use the same wallet that minted the key on the product site.` | Use the wallet shown by `veya_account` |
| `payerPrivateKey required. Pass it as a tool argument or set VEYA_PAYER_PRIVATE_KEY. …` | Provide the wallet for this write |
| `payerPrivateKey must be a 0x-prefixed 32-byte hex private key` | Fix the format (`0x` + 64 hex) |
| `MAINNET_UNPUBLISHED: Veya.sol is not published on Robinhood Chain mainnet. Nothing was sent.` | Host has no Mainnet contract configured; use a host with `VEYA_MAINNET_CONTRACT_ADDRESS` |
| `environmentId or environmentUuidHex required` | `veya_register_environment` needs one of them |
| `CHAIN_MISMATCH` / `expected chain id …` | Server RPC is not on the selected profile; operator must fix the RPC |
| Result has `warning: "On-chain register succeeded; product console confirm failed after retries. …"` | Write is done. Share the explorer link; do not resend |

## Inputs

| Message | Fix |
|---|---|
| `Pass exactly one of text, json, or txHash.` | `veya_prove` takes one source |
| `json must be a JSON value.` | Pass valid JSON as a string |
| `SEAL_ENVIRONMENT_REQUIRED: on mainnet, pass environmentId…` | Create and register an environment on Robinhood Chain (`veya_create_environment` → `veya_register_environment`) and pass its id as `environmentId` |
| `Do not use names like "…" (test/demo/tmp/sandbox)` (`CONFLICT`, 409) | Rename the environment, e.g. `VEYA Treasury Ops` |
| `No VEYA proof found in this transaction` (`NOT_VEYA_TX`, 404) | That tx is not a commitment. Use `veya_verify_transaction` for registration txs |
| `decision must be a JSON object.` | `veya_seal_decision.decision` must parse to an object, e.g. `"{\"action\":\"approve\"}"` |
| `Expected even-length hex string` | Hex has an odd number of characters |
| `Expected <n> bytes, got <m>` | UUIDs are 16 bytes (32 hex), digests 32 bytes (64 hex) |
| `refusal: "transaction did not target Veya.sol — not a VEYA proof"` | The tx went to another contract; ask for the right hash |

## Fleet and network

| Symptom | Fix |
|---|---|
| `consensus_reached: false`, `agreed_blake3_hash: null` | Validators disagreed or were offline. Check `veya_api_health`; retry later. Do not attest |
| `code: "SEALED_UNREACHABLE"` | Sealed node offline. Nothing was sent. Check `veya_api_health` |
| `veya_api_health` → `status: "degraded"` | Fleet partly down; reads still work |
| `timeout` | Product API took longer than 20 s; retry |
| `API not reachable` | Product API is offline; check `veya_api_health` |
| `Internal server error` (JSON-RPC `-32603`) | Retry the call |
| Tools missing in the agent | MCP not connected: add `https://mcp.veyanet.tech/mcp` and reload the client |

## Diagnostic order

1. `veya_describe` → right network?
2. `veya_ping_chain` → RPC alive?
3. `veya_api_health` → fleet and product API?
4. `veya_account` → key valid, which wallet?
5. `veya_writes_status` → which wallet sends writes.
