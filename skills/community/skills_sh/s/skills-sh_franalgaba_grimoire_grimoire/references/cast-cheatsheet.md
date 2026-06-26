# Cast Cheat Sheet (Grimoire)

Use Cast for fast RPC and transaction diagnostics before or during Grimoire runs.
For networked commands, always pass `--rpc-url "$RPC_URL"` explicitly.

Scope:

- Cast diagnostics here are for EVM RPC workflows.
- Do not use Cast/Anvil diagnostics for offchain venues (for example `hyperliquid`).
- For Hyperliquid validation, use venue endpoints (`grimoire venue hyperliquid mids|l2-book|open-orders|meta --format json`).

## 0) Install Foundry (Anvil + Cast)

```bash
curl -L https://foundry.paradigm.xyz | bash && foundryup
cast --version
anvil --version
```

If your shell does not find the commands immediately, start a new shell session.

## 1) Endpoint and Chain Sanity

```bash
cast client --rpc-url "$RPC_URL"
cast chain-id --rpc-url "$RPC_URL"
cast block-number --rpc-url "$RPC_URL"
cast gas-price --rpc-url "$RPC_URL"
```

Use this before `simulate`/`cast` to verify endpoint health and chain alignment.

## 2) Account and Balance Checks

```bash
cast balance "$ADDRESS" --rpc-url "$RPC_URL"
cast nonce "$ADDRESS" --rpc-url "$RPC_URL"
```

Use when troubleshooting signer state, insufficient funds, or nonce drift.

## 3) Read Contract State

```bash
# Generic view call
cast call "$CONTRACT" "symbol()(string)" --rpc-url "$RPC_URL"

# ERC20 balance check
cast call "$TOKEN" "balanceOf(address)(uint256)" "$ADDRESS" --rpc-url "$RPC_URL"

# Raw storage slot read
cast storage "$CONTRACT" 0 --rpc-url "$RPC_URL"
```

Decode calldata selectors/signatures:

```bash
cast 4byte-calldata 0xa9059cbb000000000000000000000000...
```

## 4) Inspect Transactions and Receipts

```bash
cast tx "$TX_HASH" --rpc-url "$RPC_URL"
cast receipt "$TX_HASH" --rpc-url "$RPC_URL"
cast run "$TX_HASH" --rpc-url "$RPC_URL"
cast decode-error "$REVERT_DATA"
```

Use `cast run` for replay-style debugging of a published tx in local context.

## 5) Build/Estimate Before Sending

```bash
cast calldata "transfer(address,uint256)" "$TO" "$AMOUNT"
cast estimate "$TO" "transfer(address,uint256)" "$RECIPIENT" "$AMOUNT" --rpc-url "$RPC_URL" --from "$FROM"
```

Use this to verify calldata and approximate gas cost before committing.

## 6) Controlled Send (Stateful)

Only run after explicit confirmation for value-moving actions.

Preferred signer path (keystore + password env):

```bash
cast send "$TO" "transfer(address,uint256)" "$RECIPIENT" "$AMOUNT" \
  --rpc-url "$RPC_URL" \
  --keystore "$KEYSTORE_PATH" \
  --password-env KEYSTORE_PASSWORD
```

Raw key path (only when needed):

```bash
cast send "$TO" "transfer(address,uint256)" "$RECIPIENT" "$AMOUNT" \
  --rpc-url "$RPC_URL" \
  --private-key "$PRIVATE_KEY"
```

Prefer keystore or env vars over inline raw private keys in shared shells.
For local Anvil only, use funded dev keys and never production secrets.
If setup generated `.grimoire/setup.env`, Grimoire CLI auto-loads it, but Foundry `cast` does not; export/source env vars explicitly before Cast commands.

## 7) Anvil-Fork Debug Helpers

```bash
cast rpc evm_snapshot --rpc-url http://127.0.0.1:8545
cast rpc evm_revert "$SNAP" --rpc-url http://127.0.0.1:8545
cast rpc evm_increaseTime 3600 --rpc-url http://127.0.0.1:8545
cast rpc evm_mine --rpc-url http://127.0.0.1:8545
```

## 8) High-Value Failure Patterns

- `chain-id` unexpected:
  - wrong RPC endpoint or misconfigured env var.
- `balance`/`nonce` not as expected:
  - wrong signer address or stale fork state.
- `estimate` fails but `call` works:
  - state-changing path reverts under current sender/value.
- `receipt` status `0x0`:
  - decode error data: `cast decode-error "$REVERT_DATA"`.

## 9) JSON Output for Automation

Use JSON mode for scripting and stable machine-readable parsing:

```bash
cast tx "$TX_HASH" --rpc-url "$RPC_URL" --json
cast receipt "$TX_HASH" --rpc-url "$RPC_URL" --json
cast block "$BLOCK_NUMBER" --rpc-url "$RPC_URL" --json
```
