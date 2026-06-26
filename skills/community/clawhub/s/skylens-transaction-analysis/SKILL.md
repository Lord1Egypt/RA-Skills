---
name: skylens-transaction-analysis
description: Inspects one EVM transaction with Skylens APIs and returns human-readable trace, balance, storage, and nonce changes. Use when the user asks for tx-level investigation on supported chains (for example Ethereum) via `get-trace`, `balance-change`, `state-change`, or `nonce-change`.
license: MIT
compatibility: Compatible with Cursor/Codex Agent Skills, Claude Agent Skills runtimes (Claude Code/claude.ai/API), and OpenClaw Skills. Requires Python >=3.10, outbound HTTPS access to skylens.certik.com, a zstd backend (Python 3.14+ `compression.zstd` or pip package `zstandard`), and permission to execute `{skillDir}/scripts/skylens.py`.
metadata:
  url: https://skylens.certik.com/
  script: <skillDir>/scripts/skylens.py
  primary-commands: get-trace balance-change state-change nonce-change list-source-files get-source-file
---

# Skylens Transaction Analysis

Use `{skillDir}/scripts/skylens.py` to inspect one transaction with Skylens APIs.

## When To Use This Skill

Use this skill when the user wants transaction-level investigation for a single EVM transaction on a supported chain. Typical triggers:

- The user provides a transaction hash and asks what happened.
- The user wants an execution trace or call flow for one transaction.
- The user asks which balances changed for a specific address in one transaction.
- The user asks which storage slots changed for a contract in one transaction.
- The user asks whether an address nonce changed in one transaction.
- The user wants contract source files tied to addresses touched by one transaction.

## Quick Triage Workflow

1. Run `get-trace` to identify key calls/contracts.
2. Run `list-source-files` for suspicious contract addresses to enumerate available files.
3. Run `get-source-file` with selected `--FILE_INDEX` (and optional `--OUTPUT`) to fetch source code.
4. Run `state-change` for suspicious contract addresses (storage deltas).
5. Run `nonce-change` for addresses that sent/triggered actions.
6. Run `balance-change` for holder asset impact.

## Commands

- `get-trace`: readable execution trace (paged)
- `balance-change`: balance deltas for one holder
- `state-change`: storage slot changes for one address
- `nonce-change`: nonce before/after for one address
- `list-source-files`: list contract source files (or AST-only files) by tx
- `get-source-file`: get one contract file by index from `list-source-files`

## Supported Chains

`eth`, `bsc`, `polygon`, `optimism`, `arb`, `base`, `blast`, `avalanche`, `scroll`, `linea`, `sonic`, `kaia`, `world`, `unichain`, `hyperliquid`, `plasma`

## Shared Parameter Rules

- `tx_hash`: full hash with `0x`
- `chain`: must be one of supported chains above
- `address` / `holder`: case-insensitive, accepts with or without `0x`

## `get-trace`

CLI:

`{skillDir}/scripts/skylens.py get-trace --TX <tx_hash> --CHAIN <chain> --OFFSET 0 --SIZE 100`

Output:

- Prints one readable trace line per event.
- Prints only `[offset, offset+size)`.

Output format:

`{index}({depth}) {op} {description} [source: ...]`

Source suffix (optional):

`source: [c: {contractAddress}, f:{fileIdx}, s:{start}, o:{length}]`

Current event variants:

- `callEvent`
- `createEvent`
- `storageAccessEvent`
- `logEvent`
- `keccak256Event`

## `balance-change`

CLI:

`{skillDir}/scripts/skylens.py balance-change --TX <tx_hash> --CHAIN <chain> --HOLDER <address>`

Output:

- Prints balance deltas for the target `holder`.
- May include native/token/NFT sections when available.

Printed shapes:

- `BalanceOf Native ETH: holder=... before=... after=... delta=...`
- `BalanceOf Token: token=... holder=... before=... after=... delta=...`
- `BalanceOf NFT: collection=... holder=... before=... after=... delta=...`

## `state-change`

CLI:

`{skillDir}/scripts/skylens.py state-change --TX <tx_hash> --CHAIN <chain> --ADDRESS <address>`

Output:

- Prints storage changes for the target `address` only.

Printed shape:

`Storage: address=... slot=0x... before=... after=...`

## `nonce-change`

CLI:

`{skillDir}/scripts/skylens.py nonce-change --TX <tx_hash> --CHAIN <chain> --ADDRESS <address>`

Output:

- Prints nonce before/after for the target `address`.

Printed shape:

`Nonce: address=... before=... after=...`

## `list-source-files`

CLI:

`{skillDir}/scripts/skylens.py list-source-files --TX <tx_hash> --CHAIN <chain> --ADDRESS <contract_address>`

Output:

- Lists source files for the target contract.
- Includes file indexes used by `get-source-file`.

Printed shape:

- `Contract: ...`
- `Files: ...`
- `[index] fileName (artifact=..., available=source|none)`

## `get-source-file`

CLI:

`{skillDir}/scripts/skylens.py get-source-file --TX <tx_hash> --CHAIN <chain> --ADDRESS <contract_address> --FILE_INDEX <index> [--OUTPUT <file_path>]`

Output:

- Returns source content for one selected file index.
- If `--OUTPUT` is provided, saves source content to that path.
