---
name: grimoire
description: Install and operate Grimoire, author .spell files with full syntax coverage (including advisory decision logic), and run compile/validate/simulate/cast safely. Use when users ask to create, edit, debug, validate, simulate, execute, or explain Grimoire strategies.
compatibility: "Requires one of: global grimoire CLI, npx access to @grimoirelabs/cli, or repo-local Bun execution."
metadata:
  version: "2.6"
  focus: "installation usage syntax advisory execution"
---

# Grimoire CLI Skill

This skill is the base operating playbook for Grimoire.

## When To Use

Use this skill when the task includes:

- install/setup of Grimoire tooling
- creating or editing `.spell` files
- syntax questions about DSL capability
- advisory (`advise`) authoring, debugging, and replay workflows
- setup/compile/validate/simulate/cast/resume workflows
- debugging spell compile/runtime failures

## Mandatory Loading Rules

All `references/` and `docs/` paths below are relative to this skill directory (`skills/grimoire/`). These rules are **required** — they solve syntax coverage gaps that cause authoring errors.

**STOP — read this first:** Do NOT search the codebase, grep for syntax patterns, or rely on memory for DSL syntax. The reference files bundled with this skill are the single source of truth. IMMEDIATELY use the Read tool on the files listed below before writing or editing any spell content.

1. For any `.spell` authoring/editing task — IMMEDIATELY read these files using the Read tool before doing anything else:
   - `references/syntax-capabilities.md`
   - `references/authoring-workflow.md`
2. For CLI flag details — IMMEDIATELY read using the Read tool:
   - `references/cli-quick-reference.md`
3. For any advisory task (`advise`, `advisors`, replay) — IMMEDIATELY read using the Read tool:
   - `docs/how-to/use-advisory-decisions.md`
   - `docs/explanation/advisory-decision-flow.md`
4. For local fork preview workflows — IMMEDIATELY read using the Read tool:
   - `references/anvil-cheatsheet.md`
   - `docs/how-to/simulate-on-anvil-fork.md`
5. For wallet setup and execution key flows — IMMEDIATELY read using the Read tool:
   - `docs/how-to/use-wallet-commands-end-to-end.md`
6. For RPC/signer/transaction diagnostics — IMMEDIATELY read using the Read tool:
   - `references/cast-cheatsheet.md`

## Installation Resolution

Select the first working invocation and reuse it for the session.

1. Global:
   - `npm i -g @grimoirelabs/cli`
   - command prefix: `grimoire`
2. No-install:
   - command prefix: `npx -y @grimoirelabs/cli`
3. Repo-local:
   - command prefix: `bun run packages/cli/src/index.ts --`

If one path fails, move to the next path automatically.

If `grimoire venue doctor ...` fails with `Unknown venue adapter "doctor"`, prefer repo-local invocation (`bun run packages/cli/src/index.ts`) or upgrade global CLI.

When using repo-local Bun execution, always keep the trailing `--` so Bun forwards flags to Grimoire instead of consuming them.

## Fast Start (Immediate Success Path)

Use this sequence before writing custom spells:

1. `<grimoire-cmd> --help`
2. `<grimoire-cmd> setup` (guided interactive execute onboarding)
3. `<grimoire-cmd> validate spells/compute-only.spell`
4. `<grimoire-cmd> simulate spells/compute-only.spell --chain 1`

If all three pass, proceed to spell authoring.

Setup security/runtime expectations:

- setup prompts for hidden passwords and never echoes input
- blank RPC input falls back to chain default public RPC
- setup may write `.grimoire/setup.env` unless `--no-save-password-env` is used
- CLI auto-loads nearest `.grimoire/setup.env` at startup without overriding existing env vars

## Authoring and Execution Policy

1. Read syntax references first (mandatory rule above).
2. Author/update spell.
3. Run `format` to canonicalize layout before validation.
4. Run `validate` (use `--strict` for advisory-heavy spells).
5. Fix errors/warnings and re-run until validation passes.
6. Run `simulate`.
7. Before venue metadata queries or value-moving runs, execute `venue doctor` for the target adapter/chain.
   - Example: `<grimoire-cmd> venue doctor --adapter uniswap --chain 1 --rpc-url <rpc> --json`
8. Before value-moving runs on EVM venues, verify endpoint and signer state with Foundry Cast quickchecks (`chain-id`, `block-number`, `balance`, `nonce`).
   - Do not apply Anvil/Cast checks to offchain venues such as `hyperliquid`.
9. For advisory steps intended for deterministic execution, record and then use `--advisory-replay <runId>` in dry-run/live cast.
10. If spell includes irreversible actions, require `cast --dry-run` before any live cast.
11. Ask for explicit user confirmation before live value-moving `cast`.
12. For cross-chain mode, require explicit per-chain RPC mappings:
   - `--rpc-url <sourceChainId>=<url>`
   - `--rpc-url <destinationChainId>=<url>`
13. For cross-chain Morpho actions, require explicit market mapping via:
   - `--morpho-market-id <actionRef>=<marketId>` (repeatable), or
   - `--morpho-market-map <path>`
14. For Morpho supply-only strategies, prefer `vault_deposit` / `vault_withdraw` (explicit vault address).
   - If vault address is missing, list candidate vaults and require user to pick one; never auto-select.
15. For Morpho market strategies (borrow/collateral/lend), require explicit `market_id` and use explicit actions:
   - `morpho_blue.supply_collateral(asset, amount, market_id)`
   - `morpho_blue.withdraw_collateral(asset, amount, market_id)`
16. Use bare `0x...` address literals in action token fields; quoted address-like strings trigger `QUOTED_ADDRESS_LITERAL`.
17. For Morpho doctor readiness checks, set wallet env explicitly (`GRIMOIRE_WALLET_ADDRESS` preferred, fallback `WALLET_ADDRESS`).
18. If a cross-chain run is left waiting, continue with `resume <runId>` (use `--watch` to poll settlement).
19. Never place passwords/private keys in agent prompts or inline command assignments.
20. Prefer keystore + `--password-env` over `--private-key` for dry-run/live casts.
21. Treat `.grimoire/setup.env` as plaintext secret material: keep local-only and rotate/remove when no longer needed.
22. For commands run outside the project tree, set `GRIMOIRE_SETUP_ENV_FILE=/abs/path/to/.grimoire/setup.env` when needed.

## Command Surface (Core)

- `init`
- `setup`
- `format`
- `compile`
- `compile-all`
- `validate`
- `triggers`
- `simulate`
- `cast`
- `venues`
- `venue`
- `venue doctor`
- `history`
- `log`
- `resume`
- `wallet` (`generate`, `address`, `balance`, `import`, `wrap`, `unwrap`)

Use `references/cli-quick-reference.md` for concise command signatures and safety-critical flags.

## Runtime Behavior Model

- One runtime semantics: preview first, commit only for execute paths.
- `simulate` and `cast --dry-run` are preview-only flows.
- Live `cast` can commit irreversible actions when policy and runtime checks pass.
- `simulate` supports explicit `--rpc-url`, with precedence: `--rpc-url` -> `RPC_URL_<chainId>` -> `RPC_URL`.
- Phase 1 cross-chain execution uses two-spell orchestration (`--destination-spell`) with one logical run id and resume support.
- Use `triggers <spell>` to discover stable handler ids natively before targeted execution.
- `simulate` and `cast` support selected-trigger execution via `--trigger-id`, `--trigger-index`, and legacy `--trigger`.
- For multi-handler spells, prefer `--trigger-id`; `--trigger` is label-based and can be ambiguous.
- Cross-chain `simulate` / `cast` must forward the same selected trigger into per-chain execution.
- In `--json` mode, parse stdout only; progress and spinner output can still appear on stderr.

## Query Functions (price / balance / apy / metric)

**Always prefer query functions over advisory for structured data fetching.** These are deterministic, fast, and don't require LLM calls.

- `price(BASE, QUOTE[, SOURCE])` — live token price via query provider (requires Alchemy RPC URL)
- `balance(ASSET[, ADDRESS])` — on-chain token balance via RPC (any RPC URL)
- `apy(VENUE, ASSET[, SELECTOR])` — venue-backed APY surface (for example Aave and Morpho)
- `metric(SURFACE, VENUE[, ASSET[, SELECTOR]])` — generic protocol metric surface
- Selector guidance:
- market/vault id selector: `apy(morpho, USDC, "wbtc-usdc-86")`
- vault selector (Morpho): `metric("vault_net_apy", morpho, USDC, "vault=0xVaultAddress")`
- Morpho `vault_apy` / `vault_net_apy` require explicit selector; do not rely on implicit defaults.
- key/value selector: `metric("quote_out", uni_v3, USDC, "asset_out=WETH,amount=1000000,fee_tier=3000")`
- Never use an advisory (`advise`) just to fetch prices, balances, APYs, or other structured metrics

Use advisory only when the task requires LLM judgment, reasoning, or interpretation.

## Advisory Operating Rules

- Advisory must be explicit statement form: `x = advise advisor: "prompt" { ... }`.
- Treat advisory outputs as typed contracts; enforce schema with `output`.
- Require `timeout` and `fallback` in every advisory block.
- Prefer `validate --strict` when advisory logic gates value-moving actions.
- Use replay for determinism when moving from preview/dry-run to live execution.
- For runtime debugging, use `--advisory-trace-verbose` (non-JSON mode) to stream detailed advisory traces.

## Venue Metadata and Snapshots

Use venue skills for snapshot parameters and market metadata:

- `grimoire-aave`
- `grimoire-uniswap`
- `grimoire-morpho-blue`
- `grimoire-hyperliquid`
- `grimoire-pendle`
- `grimoire-polymarket`

Formatting policy for venue CLI output:

- prefer `--format json` for automation or nested payloads
- use `--format table` for human-readable summaries

## References

- `references/syntax-capabilities.md`
- `references/authoring-workflow.md`
- `references/anvil-cheatsheet.md`
- `references/cast-cheatsheet.md`
- `references/cli-quick-reference.md`
- `docs/how-to/simulate-on-anvil-fork.md`
- `docs/how-to/use-wallet-commands-end-to-end.md`
- `docs/how-to/use-advisory-decisions.md`
- `docs/how-to/compare-protocol-metrics.md`
- `docs/explanation/advisory-decision-flow.md`
- `docs/reference/cli.md`
- `docs/reference/spell-syntax.md`
- `docs/reference/grimoire-dsl-spec.md`
- `docs/reference/compiler-runtime.md`
