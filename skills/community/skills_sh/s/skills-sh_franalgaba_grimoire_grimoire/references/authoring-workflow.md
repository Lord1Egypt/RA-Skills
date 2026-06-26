# Authoring Workflow (Agent Procedure)

Use this procedure whenever creating or editing `.spell` files.

## 1. Load Context

1. Read `references/syntax-capabilities.md`.
2. Identify the target spell path and trigger intent (`manual`, `hourly`, etc.).
3. Identify whether the spell has value-moving actions.
4. If using EVM custom RPC/fork or signing transactions, run Foundry Cast quickchecks from `references/cast-cheatsheet.md`.
5. For offchain venues (for example `hyperliquid`), skip Cast/Anvil checks and validate via venue API commands.

## 2. Author With Minimal Safe Skeleton

Start from:

```spell
spell Hello {
  params: {
    amount: 42
  }

  on manual: {
    doubled = params.amount * 2
    emit hello(amount=params.amount, doubled=doubled)
  }
}
```

Then incrementally add venues/actions/guards/advisory blocks.

**Decision guide — query functions vs advisory:**

- Need a price? Use `price(BASE, QUOTE)`. Do NOT use an advisory to fetch prices.
- Need a balance? Use `balance(ASSET)` or `balance(ASSET, address)`. Do NOT use an advisory.
- Need lending APY from a venue? Use `apy(VENUE, ASSET[, selector])`.
- Need cross-venue protocol comparison (quotes/mids/custom surfaces)? Use `metric(SURFACE, VENUE[, ASSET[, selector]])`.
- Need LLM judgment, reasoning, or interpretation? Use `advise`.

Query functions are deterministic, fast, and free. Advisory calls invoke an LLM and should only be used when human-like reasoning is required.

## 3. Compile/Validate Loop

Run:

```bash
<grimoire-cmd> validate <spell-path>
```

If validation fails:

1. fix the highest-impact error first
2. re-run `validate`
3. repeat until success

For advisory-heavy spells:

```bash
<grimoire-cmd> validate <spell-path> --strict
```

Use strict mode to force explicit advisory hygiene (`context`, `within`, explicit `on_violation`).

## 4. Preview Loop

Run:

```bash
<grimoire-cmd> simulate <spell-path> --chain <id>
```

Recommended RPC preflight:

```bash
cast chain-id --rpc-url <rpc>
cast block-number --rpc-url <rpc>
```

Skip this preflight for offchain venues such as `hyperliquid`.

For local forked preview (Anvil):

```bash
<grimoire-cmd> simulate <spell-path> --chain <id> --rpc-url http://127.0.0.1:8545
```

If simulate fails:

1. identify phase (`compile`, `preview policy`, adapter/data, etc.)
2. patch spell/params/config
3. re-run simulate

For advisory flows, inspect whether failure is:

1. model/tooling resolution (`advisory_failed`)
2. output schema mismatch (`Advisory output violated schema`)
3. replay data mismatch (missing advisory output for step id)

## 5. Value-Moving Safety Path

For spells with irreversible actions:

1. verify signer state:

```bash
cast balance <address> --rpc-url <rpc>
cast nonce <address> --rpc-url <rpc>
```

For offchain venues, replace signer-RPC checks with venue-specific health/meta checks.

2. require dry-run first:

```bash
<grimoire-cmd> cast <spell-path> --dry-run --chain <id> --key-env PRIVATE_KEY --rpc-url <rpc>
```

3. summarize risks and expected behavior
4. request explicit user confirmation before live cast

If advisory gates execution policy, prefer deterministic path:

1. preview and capture run id
2. dry-run cast with `--advisory-replay <runId>`
3. live cast with `--advisory-replay <runId>` after confirmation

## 6. Snapshot/Data Inputs

If spell depends on venue snapshots:

1. use matching venue skill command with `--format spell`
2. paste/merge params carefully
3. enforce freshness policy where needed (`--data-max-age`, `--on-stale`)

## 7. Done Criteria

A spell task is done only when:

1. syntax matches supported capabilities
2. `validate` passes
3. `simulate` passes or failure is explicitly documented
4. dry-run is performed for value-moving flows
5. live-cast confirmation gate is respected

For advisory-driven spells, also require:

1. advisory output schema is explicit and validated
2. fallback behavior is acceptable under failure
3. replay policy is documented when deterministic behavior is required
