# Anvil Cheat Sheet (Grimoire)

Use this when running Grimoire preview/dry-run workflows against local forked state.

Scope:

- Anvil is EVM-only.
- Do not use Anvil workflows for offchain venues (for example `hyperliquid`).
- For Hyperliquid checks, use venue commands such as `grimoire venue hyperliquid meta --format json`.

## 0) Install Foundry (Anvil + Cast)

```bash
curl -L https://foundry.paradigm.xyz | bash && foundryup
anvil --version
cast --version
```

If your shell does not find the commands immediately, start a new shell session.

## 1) Start a Forked Anvil Node

Baseline:

```bash
anvil \
  --fork-url "$FORK_RPC_URL" \
  --chain-id "$CHAIN_ID" \
  --host 127.0.0.1 \
  --port 8545
```

Reproducible (pinned block + persisted state):

```bash
anvil \
  --fork-url "$FORK_RPC_URL" \
  --chain-id "$CHAIN_ID" \
  --fork-block-number "$FORK_BLOCK" \
  --state .grimoire/anvil/state.json \
  --state-interval 60 \
  --host 127.0.0.1 \
  --port 8545
```

Notes:

- `--fork-url` is the same as `--rpc-url` in Anvil.
- Keep Grimoire `--chain` equal to Anvil `--chain-id`.

## 2) Run Grimoire Against Anvil

Preview only:

```bash
<grimoire-cmd> simulate <spell-path> \
  --chain "$CHAIN_ID" \
  --rpc-url "http://127.0.0.1:8545"
```

Dry-run with wallet path (preview-only, wallet wiring included):

```bash
<grimoire-cmd> cast <spell-path> \
  --dry-run \
  --chain "$CHAIN_ID" \
  --rpc-url "http://127.0.0.1:8545" \
  --key-env PRIVATE_KEY
```

## 3) Preflight and Sanity Checks

Check that Grimoire is using the endpoint you expect:

```bash
<grimoire-cmd> venue doctor \
  --adapter uniswap \
  --chain "$CHAIN_ID" \
  --rpc-url "http://127.0.0.1:8545" \
  --json
```

Quick RPC checks:

```bash
cast chain-id --rpc-url http://127.0.0.1:8545
cast block-number --rpc-url http://127.0.0.1:8545
```

## 4) High-Value Anvil Flags

- `--fork-block-number <n>`: pin fork for repeatability.
- `--state <path>`: load and dump state automatically.
- `--dump-state <path>` / `--load-state <path>`: explicit state lifecycle.
- `--auto-impersonate`: enables impersonation workflows.
- `--compute-units-per-second <n>`: tune upstream provider throughput.
- `--retries <n>`: retry transient upstream errors.
- `--no-rate-limit`: disable local provider rate limiting.
- `--fork-header "Key: Value"`: pass authenticated headers to upstream RPC.

## 5) Useful RPC Controls During Debugging

```bash
cast rpc evm_increaseTime 3600 --rpc-url http://127.0.0.1:8545
cast rpc evm_mine --rpc-url http://127.0.0.1:8545

SNAP=$(cast rpc evm_snapshot --rpc-url http://127.0.0.1:8545)
cast rpc evm_revert "$SNAP" --rpc-url http://127.0.0.1:8545

cast rpc anvil_impersonateAccount 0x... --rpc-url http://127.0.0.1:8545
cast rpc anvil_stopImpersonatingAccount 0x... --rpc-url http://127.0.0.1:8545
```

## 6) Common Failure Patterns

- Chain mismatch:
  - align Anvil `--chain-id` and Grimoire `--chain`.
- Wrong RPC endpoint used:
  - pass `--rpc-url` explicitly and verify `rpcUrl` in `venue doctor --json`.
- Upstream fork instability:
  - set `--fork-block-number`, raise `--retries`, tune `--compute-units-per-second`.
