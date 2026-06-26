# Skylens Transaction Analysis

CertiK Skylens skill for transaction-level investigation on supported EVM-compatible chains.

## Files

- `SKILL.md`: agent-facing instructions and investigation workflow
- `scripts/skylens.py`: CLI for trace, source code, balance, storage, and nonce inspection

## Prerequisites

- Python `>=3.10`
- Outbound HTTPS access to `skylens.certik.com`
- A zstd backend:
  - Python `3.14+` with `compression.zstd`, or
  - Python package `zstandard`

## Quick Start

Run commands from this directory:

```bash
python3 scripts/skylens.py get-trace --TX 0x... --CHAIN eth
python3 scripts/skylens.py balance-change --TX 0x... --CHAIN eth --HOLDER 0x...
python3 scripts/skylens.py state-change --TX 0x... --CHAIN eth --ADDRESS 0x...
python3 scripts/skylens.py nonce-change --TX 0x... --CHAIN eth --ADDRESS 0x...
python3 scripts/skylens.py list-source-files --TX 0x... --CHAIN eth --ADDRESS 0x...
python3 scripts/skylens.py get-source-file --TX 0x... --CHAIN eth --ADDRESS 0x... --FILE_INDEX 0
```

## Recommended Workflow

1. Run `get-trace` to identify the important calls and contracts.
2. Run `list-source-files` for suspicious contracts.
3. Run `get-source-file` to inspect the relevant source code.
4. Run `state-change` for contract storage deltas.
5. Run `nonce-change` for sender or triggered addresses.
6. Run `balance-change` for holder asset impact.

## Commands

| Command             | Purpose                                                                              |
| ------------------- | ------------------------------------------------------------------------------------ |
| `get-trace`         | Return readable execution trace lines, optionally paged with `--OFFSET` and `--SIZE` |
| `balance-change`    | Return native, token, and NFT balance deltas for one holder                          |
| `state-change`      | Return storage slot changes for one address                                          |
| `nonce-change`      | Return nonce before and after for one address                                        |
| `list-source-files` | Enumerate available contract source files for a transaction                          |
| `get-source-file`   | Return one source file by index, or save it with `--OUTPUT`                          |

## Supported Chains

`eth`, `bsc`, `polygon`, `optimism`, `arb`, `base`, `blast`, `avalanche`, `scroll`, `linea`, `sonic`, `kaia`, `world`, `unichain`, `hyperliquid`, `plasma`

## Parameter Rules

- `--TX`: full transaction hash with `0x`
- `--CHAIN`: one of the supported chain keys
- `--ADDRESS` / `--HOLDER`: accepts either `0x...` or the raw hex body, case-insensitive
- `--FILE_INDEX`: use the index from `list-source-files`

## Output Notes

- `get-trace` prints lines in `{index}({depth}) {op} {description}` format.
- `balance-change` prints only changes for the requested holder.
- `state-change` and `nonce-change` print only changes for the requested address.
- `get-source-file --OUTPUT <path>` writes the file to disk instead of printing the full content to stdout.
