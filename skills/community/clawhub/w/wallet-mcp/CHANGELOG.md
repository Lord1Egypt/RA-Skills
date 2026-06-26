# Changelog

All notable changes to wallet-mcp are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.5.0] — 2026-04-12

### Added
- **`add_wallet`** — import a single wallet by private key; public address is derived
  automatically from the key so users never need to look up or provide the address.
  Available in both `openclaw/wallet.py` and documented in `SKILL.md`.
- **`--from-label`** on `send_native_multi` — resolves sender private key from stored
  wallet label instead of passing the raw key through chat. Prevents model refusals
  and avoids exposing private keys in messaging platforms.
- **`--to-label`** on `sweep_wallets` — resolves destination address from stored wallet
  label, consistent with `--from-label` approach on send.
- **`wallet-mcp openclaw-setup --force`** — overwrites an existing TOOLS.md entry with
  the latest template, enabling updates without manual file editing.

### Fixed
- **`python` → `python3`** in all `SKILL.md` examples and `TOOLS.md` entry — VPS
  environments typically lack a bare `python` binary, causing agent to fail execution.
- **`export_wallets` path guidance** — removed `--path` from SKILL.md examples;
  agent was inventing random file paths (`/root/`, `/root/.openclaw/workspace/`).
  Standard usage now omits `--path` and auto-saves to `~/.wallet-mcp/exports/`.
- **`import_wallets` hint** — returns `hint` field when all failures are due to missing
  `private_key`, explaining that the source file must be re-exported with `--include-keys`.
- **`send_native_multi` clarification** — documented as group send only (one-to-many);
  agent was inventing a non-existent `send_native_single` command.
- **`scan_token_accounts` vs `scan_token_balances` disambiguation** — added comparison
  table to SKILL.md; agent was calling built-in `SOLANA()` tool instead of `wallet.py`
  and confusing single-address scan with group scan.
- **`group_summary` no-args note** — agent was appending `--label` or other flags to
  a command that takes no arguments.
- **Synchronous execution note** — agent was hallucinating background tasks
  (`process --action poll`, session IDs, PIDs) because SKILL.md did not state that
  `wallet.py` is fully synchronous and returns JSON immediately.
- **`openclaw-setup --force`** in `TOOLS.md` template and `OPENCLAW.md` update section.

---

## [1.4.0] — 2026-04-10

### Added
- **`wallet-mcp openclaw-setup`** — new CLI subcommand that automatically appends the
  wallet-mcp skill entry to `~/.openclaw/workspace/TOOLS.md`.
  Prevents the OpenClaw agent from forgetting wallet-mcp after `/new` by registering
  it in the persistent agent memory file that is loaded on every session.
  Idempotent — safe to run multiple times; skips if entry already present.
- **`OPENCLAW.md` Part 5b** — documents the `openclaw-setup` command with expected output,
  idempotency note, and verification steps.

---

## [1.3.0] — 2026-04-10

### Added
- **OpenClaw integration update** — `openclaw/SKILL.md` bumped to v1.2.0 with full docs
  for all 13 tools including `sweep_wallets`, `scan_token_balances`, `export_wallets`,
  `import_wallets`
- **`openclaw/wallet.py`** updated with 4 new CLI commands matching the new tools
- **`OPENCLAW.md`** fully rewritten — step-by-step install guide covering:
  - Linux/macOS and Windows uv install
  - OpenClaw install via npm
  - Telegram, Discord, WhatsApp channel configuration
  - AI model setup (Claude, OpenAI, Gemini, OpenRouter)
  - SKILL.md + wallet.py deployment
  - RPC endpoint configuration with provider comparison table
  - systemd service setup
  - Wallet storage security hardening
  - Natural language → command mapping table for all 13 tools
  - Troubleshooting table and update instructions

---

## [1.2.0] — 2026-04-10

### Added
- **`export_wallets`** — export any filtered wallet group to a JSON or CSV file;
  `include_keys=False` by default for safety; path auto-generated under
  `~/.wallet-mcp/exports/` when not specified
- **`import_wallets`** — import wallets from a JSON or CSV file into local storage;
  duplicate addresses are auto-skipped; label/tags can be overridden at import time;
  format auto-detected from file extension

---

## [1.1.0] — 2026-04-10

### Added
- **`sweep_wallets`** — collect all SOL/ETH from a wallet group back to one destination address; supports retry, random delay, and per-wallet skip when balance is too low to cover fees
- **`scan_token_balances`** — scan SPL token balances across a Solana wallet group (all tokens or filter by mint), or ERC-20 token balances across an EVM group (contract address required); returns `wallets_with_balance` summary

### Fixed
- `signed.rawTransaction` → `signed.raw_transaction` in `evm.py` (`send_eth`) — web3.py v6 renamed the attribute; every EVM send would crash without this fix
- `wallet_exists()` in `generator.py` was reading the entire CSV on every iteration (O(n²) for large batches) — now loads existing addresses once into a `set` before the loop

---

## [1.0.0] — 2026-04-09

### Added
- **FastMCP server** (`src/wallet_mcp/server.py`) with 9 registered tools
- **`generate_wallets`** — generate N EVM or Solana wallets, save to CSV
- **`send_native_multi`** — send SOL/ETH from one wallet to a labeled group with retry, random delays, randomized amounts
- **`list_wallets`** — list wallets with chain/label/tag filters; private keys masked by default
- **`get_balance_batch`** — fetch native balances for a wallet group
- **`close_token_accounts`** — close empty SPL token accounts, reclaim rent SOL
- **`scan_token_accounts`** — read-only scan of SPL token accounts
- **`tag_wallets`** — add tags to a wallet group
- **`group_summary`** — show wallet groups with per-chain counts
- **`delete_group`** — permanently delete a wallet group
- **CSV storage** at `~/.wallet-mcp/wallets.csv` (configurable via `WALLET_DATA_DIR`)
- **python-dotenv** support — `.env` loaded automatically at server startup
- **Retry logic** in `core/utils.py` with `attempts >= 1` guard
- **Docker support** — multi-stage `Dockerfile` + `docker-compose.yml` with persistent volume
- **GitHub Actions** — `ci.yml` (test on push/PR, Python 3.11 + 3.12) and `release.yml` (build + GitHub Release on tag)
- **MCP Inspector** support via `mcp dev src/wallet_mcp/server.py`
- **Architecture diagram** — `assets/architecture.png` + `assets/architecture.md`
- `INSTALLATION.md`, `EXAMPLES.md`, `openclaw/SKILL.md`, `CONTRIBUTING.md`

### Fixed
- `rpc_url=None` no longer crashes core functions — all RPC functions fall back to `DEFAULT_RPC` when `None` is passed
- `get_token_accounts_by_owner` uses `TokenAccountOpts(program_id=...)` (correct solana-py API, not raw dict)
- Token account data parsing handles both `dict` and object forms across solana-py versions
- `retry(attempts=0)` raises `ValueError` instead of `TypeError: raise None`
- Variable shadowing (`w`) in `manager.py` batch balance loop

### Security
- Private keys masked in `list_wallets` output by default (`show_keys=False`)
- `.gitignore` excludes `wallets.csv`, `.env`, `__pycache__`, logs
- Docker runs as non-root `mcpuser`
