# CLI Quick Reference

Use this page for concise command signatures and high-signal options.

Assume `<grimoire-cmd>` is one of:

- `grimoire`
- `npx -y @grimoirelabs/cli`
- `bun run packages/cli/src/index.ts --`

When using the repo-local Bun entrypoint, keep the trailing `--` so command flags are passed through to Grimoire.

## Core Commands

```bash
<grimoire-cmd> init [--force] [--runtime-quickstart]
<grimoire-cmd> setup [--chain <id>] [--rpc-url <url>] [--adapter <name>] [--keystore <path>] [--password-env <name>] [--key-env <name>] [--import-key] [--no-save-password-env] [--no-doctor] [--non-interactive] [--json]
<grimoire-cmd> format <paths...> [--write|--check] [--diff] [--json]
<grimoire-cmd> format --stdin --stdin-filepath <virtual-path> [--json]
<grimoire-cmd> compile <spell> [-o <file>] [--pretty]
<grimoire-cmd> compile-all [dir] [--fail-fast] [--json]
<grimoire-cmd> validate <spell> [--strict] [--json]
<grimoire-cmd> triggers <spell> [--json]
<grimoire-cmd> simulate <spell> [options]
<grimoire-cmd> cast <spell> [options]
<grimoire-cmd> venues [--json]
<grimoire-cmd> venue <adapter> [args...]
<grimoire-cmd> venue doctor [--chain <id>] [--adapter <name>] [--rpc-url <url>] [--json]
<grimoire-cmd> resume <runId> [--watch] [--poll-interval-sec <seconds>] [--json] [--state-dir <dir>]
<grimoire-cmd> history [spell] [--limit <n>] [--json] [--state-dir <dir>]
<grimoire-cmd> log <spell> <runId> [--json] [--state-dir <dir>]
```

## Setup (Execute Onboarding)

Use before first live or dry-run casts in a new local environment:

```bash
<grimoire-cmd> setup
```

Behavior:

1. Creates local `.grimoire/` directory when missing.
2. Runs built-in smoke compile + preview checks.
3. Verifies RPC reachability.
4. Provisions wallet keystore (existing, env import, or generated).
5. Runs `venue doctor` by adapter (default `uniswap`) unless `--no-doctor`.
6. Prompts for missing required values in interactive mode.
7. Blank RPC input falls back to chain default public RPC.
8. Writes `.grimoire/setup.env` after interactive password entry (unless `--no-save-password-env`).
9. Shows password safety guidance to avoid leaking secrets in agent-run sessions.
10. CLI auto-loads nearest `.grimoire/setup.env` on startup unless env vars are already set.
11. `GRIMOIRE_SETUP_ENV_FILE` can point to an explicit setup env file path.

Password safety:

1. Do not paste passwords/private keys into Codex/Claude prompts.
2. Prefer hidden interactive prompts over inline secret values.
3. For automation, preload secret env values outside the agent and pass only env var names.
4. `.grimoire/setup.env` is plaintext secret material; keep local-only and rotate/delete when done.

## Venue Doctor (Preflight)

Use before venue metadata calls or strategy execution:

```bash
<grimoire-cmd> venue doctor --adapter uniswap --chain 1 --rpc-url <rpc> --json
```

Checks:

- adapter registration
- required env vars
- chain support
- RPC reachability

Tip:

- In `--json` output, confirm `rpcUrl` is the endpoint actually used.
- If `grimoire venue doctor ...` fails with `Unknown venue adapter "doctor"`, your installed global CLI is old; use `npx -y @grimoirelabs/cli@latest ...` or repo-local invocation.

## Simulate (Preview)

Native trigger discovery:

```bash
<grimoire-cmd> triggers <spell> --json
```

Use this before `simulate --trigger-id` or `cast --trigger-id`. It returns each compiled handler's `{ id, index, label, source }` plus trigger payload and owned step ids.

Common options:

- `-p, --params <json>`
- `--chain <id>`
- `--rpc-url <url>`
- `--trigger-id <id>`
- `--trigger-index <n>`
- `--trigger <label>` (legacy label selector)
- `--destination-spell <spell>`
- `--destination-chain <id>`
- `--handoff-timeout-sec <seconds>`
- `--poll-interval-sec <seconds>`
- `--watch`
- `--morpho-market-id <actionRef>=<marketId>` (repeatable)
- `--morpho-market-map <path>`
- `--state-dir <dir>`
- `--no-state`
- `--advisor-skills-dir <dir...>`
- `--advisory-pi`
- `--advisory-replay <runId>`
- `--advisory-provider <name>`
- `--advisory-model <id>`
- `--advisory-thinking <off|low|medium|high>`
- `--advisory-tools <none|read|coding>`
- `--advisory-trace-verbose`
- `--pi-agent-dir <dir>`
- `--data-replay <off|auto|runId|snapshotId>`
- `--data-max-age <sec>`
- `--on-stale <fail|warn>`

Important:

1. `simulate` supports `--rpc-url` for explicit per-run RPC selection.
2. RPC resolution order is `--rpc-url`, then `RPC_URL_<chainId>`, then `RPC_URL`.
3. Cross-chain mode is enabled by `--destination-spell` and requires explicit mapped RPCs for both chains: `--rpc-url <chainId>=<url>`.
4. Cross-chain Morpho actions require explicit market mapping (`--morpho-market-id` or `--morpho-market-map`).
5. When `--rpc-url` is an Alchemy URL (e.g. `https://eth-mainnet.g.alchemy.com/v2/<key>`), the API key is auto-extracted and used to enable `price()` queries via the Alchemy query provider.
6. `balance()` works with any RPC, and adapter-backed `apy()` / `metric()` do not require Alchemy.
7. `--trigger-id` is the canonical handler selector; use it for automation and event-only multi-handler spells.
8. Cross-chain simulate mode also honors selected-trigger flags.
9. In `--json` mode, parse stdout only; progress lines may still appear on stderr.

## Anvil Quickstart

Use only for EVM venues. Do not use for `hyperliquid` (offchain).

Start forked local node:

```bash
anvil \
  --fork-url "$FORK_RPC_URL" \
  --chain-id "$CHAIN_ID" \
  --fork-block-number "$FORK_BLOCK" \
  --state .grimoire/anvil/state.json \
  --host 127.0.0.1 \
  --port 8545
```

Run preview against Anvil:

```bash
<grimoire-cmd> simulate <spell> --chain "$CHAIN_ID" --rpc-url http://127.0.0.1:8545
```

Preflight endpoint and env:

```bash
<grimoire-cmd> venue doctor --adapter uniswap --chain "$CHAIN_ID" --rpc-url http://127.0.0.1:8545 --json
```

Optional Foundry Cast preflight against Anvil:

```bash
cast chain-id --rpc-url http://127.0.0.1:8545
cast block-number --rpc-url http://127.0.0.1:8545
```

## Venue Output Formats

Use `--format json` for scripts and nested payloads (for example `hyperliquid meta`).

- `auto`: table only for flat TTY-friendly outputs, otherwise JSON
- `table`: compact summary for nested arrays/objects
- `json`: full payload, stable for automation

## Cast (Dry-Run / Live)

Common options:

- `--dry-run`
- `--chain <id>`
- `--trigger-id <id>`
- `--trigger-index <n>`
- `--trigger <label>` (legacy label selector)
- `--key-env <name>`
- `--keystore <path>`
- `--password-env <name>`
- `--rpc-url <url>`
- `--destination-spell <spell>`
- `--destination-chain <id>`
- `--handoff-timeout-sec <seconds>`
- `--poll-interval-sec <seconds>`
- `--watch`
- `--morpho-market-id <actionRef>=<marketId>` (repeatable)
- `--morpho-market-map <path>`
- `--skip-confirm`
- `--state-dir <dir>`
- `--no-state`
- `--advisor-skills-dir <dir...>`
- `--advisory-pi`
- `--advisory-replay <runId>`
- `--advisory-provider <name>`
- `--advisory-model <id>`
- `--advisory-thinking <off|low|medium|high>`
- `--advisory-tools <none|read|coding>`
- `--advisory-trace-verbose`
- `--pi-agent-dir <dir>`

Safety rule:

1. run `cast --dry-run` before live cast for value-moving spells
2. require explicit user confirmation before live cast

Replay rule for advisory-gated execution:

1. use `--advisory-replay <runId>` for dry-run/live consistency
2. do not combine replay with `--no-state`

Cross-chain continuation:

1. if run status is waiting, continue with `resume <runId>`
2. use `resume --watch` to poll handoff settlement and execute destination track
3. selected-trigger flags also apply in cross-chain cast mode

JSON output guidance:

1. `simulate --json` and `cast --json` emit a single machine-readable payload on stdout
2. parse stdout only; human progress and spinner output may be written to stderr
3. selected-trigger runs include `selectedTrigger`, `events`, and `finalState` in the JSON payload

## Foundry Cast (RPC/Tx Diagnostics)

Use Foundry `cast` for endpoint/signer/transaction debugging around Grimoire runs.
Prefer explicit `--rpc-url` and JSON mode (`--json`) for automation.
These checks are EVM-only and are not applicable to offchain venues such as `hyperliquid`.

High-value quickchecks:

```bash
cast chain-id --rpc-url "$RPC_URL"
cast block-number --rpc-url "$RPC_URL"
cast balance "$ADDRESS" --rpc-url "$RPC_URL"
cast nonce "$ADDRESS" --rpc-url "$RPC_URL"
cast receipt "$TX_HASH" --rpc-url "$RPC_URL"
cast decode-error "$REVERT_DATA"
```

Signer hygiene:

- prefer `--keystore` + `--password-env` over raw `--private-key`
- if using `--private-key`, keep it in env vars and avoid shell history leaks

For expanded patterns and Anvil debug RPC calls, use `references/cast-cheatsheet.md`.

## Wallet Subcommands

```bash
<grimoire-cmd> wallet generate [--keystore <path>] [--password-env <name>] [--print-key] [--json]
<grimoire-cmd> wallet address [--keystore <path>] [--password-env <name>] [--key-env <name>] [--mnemonic <phrase>] [--json]
<grimoire-cmd> wallet balance [--keystore <path>] [--password-env <name>] [--key-env <name>] [--mnemonic <phrase>] [--chain <id>] [--rpc-url <url>] [--json]
<grimoire-cmd> wallet import [--keystore <path>] [--password-env <name>] [--key-env <name>] [--json]
<grimoire-cmd> wallet wrap --amount <eth> [--chain <id>] [--keystore <path>] [--password-env <name>] [--rpc-url <url>] [--json]
<grimoire-cmd> wallet unwrap --amount <eth> [--chain <id>] [--keystore <path>] [--password-env <name>] [--rpc-url <url>] [--json]
```

## High-Use Environment Variables

- `PRIVATE_KEY`
- `KEYSTORE_PASSWORD`
- `RPC_URL`
- `ENS_RPC_URL`
- `GRIMOIRE_SETUP_ENV_FILE`
