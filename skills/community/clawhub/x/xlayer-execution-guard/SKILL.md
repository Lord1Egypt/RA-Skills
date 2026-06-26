---
name: xlayer-execution-guard
description: "Run an executable X Layer pre-execution guard for autonomous agents: OnchainOS DEX route judgment, honeypot and price-impact checks, proof-mode evidence, and optional Agentic Wallet execution via onchainos. Use when OpenClaw/Codex needs to test, block, resize, or execute an X Layer swap intent with judge-ready proof."
---

# X Layer Execution Guard

Use this skill to turn an agent swap intent into a guarded execution decision and proof artifact.

The installed skill includes its own Python runtime in `runtime/` and two scripts in `scripts/`:

- `scripts/run_execution_guard.py` runs the guard CLI.
- `scripts/check_agentic_wallet.py` checks whether `onchainos` and Agentic Wallet are reachable.

## Operating Rules

1. Default to `--no-execute` or `--execution-mode proof` while evaluating a request.
2. Only use `--live` or `--execution-mode agentic-wallet` after explicit user approval for a real wallet action.
3. Treat `proof` mode as simulated execution evidence. Only `agentic-wallet` mode can return a real transaction hash.
4. If OnchainOS API credentials are missing, the runtime returns a mock install-smoke result. Do not present mock output as live proof.
5. For live X Layer runs, use chain `196` unless the user explicitly chooses another chain.

## OpenClaw Quick Start

Set the skill directory first. In OpenClaw it is usually:

```bash
SKILL_DIR="$HOME/.openclaw/skills/xlayer-execution-guard"
```

If installed into a local workdir with ClawHub, use:

```bash
SKILL_DIR="$PWD/skills/xlayer-execution-guard"
```

Install the only runtime dependency if needed:

```bash
python3 -m pip install --user -r "$SKILL_DIR/requirements.txt"
```

Check the Agentic Wallet environment:

```bash
python3 "$SKILL_DIR/scripts/check_agentic_wallet.py"
```

Run a safe pre-execution judgment:

```bash
PYTHONPATH="$SKILL_DIR/runtime" python3 "$SKILL_DIR/scripts/run_execution_guard.py" \
  --agent strategy-office \
  --intent-id strategy-office-round-001 \
  --from USDC \
  --to USDT \
  --amount 10 \
  --amount-mode readable \
  --slippage 0.5 \
  --max-impact 1.20 \
  --no-execute \
  --output guard-proof.json
```

Run proof-mode closed-loop evidence without touching the wallet:

```bash
PYTHONPATH="$SKILL_DIR/runtime" python3 "$SKILL_DIR/scripts/run_execution_guard.py" \
  --agent strategy-office \
  --intent-id strategy-office-proof-001 \
  --from USDC \
  --to USDT \
  --amount 10 \
  --amount-mode readable \
  --execution-mode proof \
  --output guard-proof.json
```

Run a live Agentic Wallet execution only after user approval:

```bash
PYTHONPATH="$SKILL_DIR/runtime" python3 "$SKILL_DIR/scripts/run_execution_guard.py" \
  --agent strategy-office \
  --intent-id strategy-office-live-001 \
  --from USDC \
  --to USDT \
  --amount 10 \
  --amount-mode readable \
  --slippage 0.5 \
  --execution-mode agentic-wallet \
  --wallet default \
  --chain 196 \
  --output guard-live-proof.json
```

`--live` is an alias for `--execution-mode agentic-wallet`.

## Required Environment

For real OnchainOS route judgment, export API credentials in the OpenClaw environment or `~/.config/onchainos.env`:

```bash
export ONCHAINOS_API_KEY="..."
export ONCHAINOS_API_SECRET="..."
export ONCHAINOS_API_PASSPHRASE="..."
export ONCHAINOS_CHAIN_INDEX="196"
```

For live wallet execution, `onchainos` must be installed and logged in:

```bash
onchainos wallet login
onchainos wallet status
```

## What The Guard Checks

The runtime uses OnchainOS DEX Aggregator APIs for:

- token discovery through `/api/v6/dex/aggregator/all-tokens`
- liquidity source discovery through `/api/v6/dex/aggregator/get-liquidity`
- aggregated and per-DEX quote comparison through `/api/v6/dex/aggregator/quote`

The output includes:

- `pre_execution.verdict`: `execute`, `resize`, `retry`, or `block`
- `pre_execution.checks`: quote availability, price impact, fallback coverage, token tax, honeypot flags, gas and fee fields
- `execution.status`: `simulated_success`, `success`, `broadcasted`, `failed`, or `not_executed`
- `post_execution.proof_id` and `moltbook_summary`
- `closed_loop_validation`: whether the pre-execution verdict matched the post-execution outcome

## Failure Handling

- Missing API credentials: output is mock mode and suitable only for install verification.
- `wallet_ready=false`: run `onchainos wallet login` in the same OpenClaw environment.
- `verdict=block`: do not execute; show the block reason.
- `verdict=resize`: execute only if the user accepts the resized risk outcome.
- Live execution returns no tx hash: preserve the full JSON output and inspect `execution.error`.
