# Training Lab — fine-tune a model (API key or x402)

Teach a small open model your task: pick a dataset you own, a base model and a GPU
block, pay once, and get the model back (LoRA adapter + score report, plus a GGUF when `gguf_available`).

**API base:** `https://compute.x402layer.cc` · Dashboard: https://cloud.x402compute.cc/network/training
· Docs: https://docs.x402layer.cc/cloud/training/overview

Base models today: `qwen2.5-0.5b-instruct`, `qwen2.5-1.5b-instruct`. Price = hours x the
GPU's hourly training price (prepaid block; finishing early or cancelling does not refund).
If the GPU cannot start or the run never reports in, the charge comes back as credits.

## Path A — no account, pay per run over x402 (`scripts/train_x402.py`)

```
GET  /training/x402/catalog                         -> models, GPUs, prices, networks (no auth)
POST /training/x402/runs                            -> 402 + quote (quote_id, price_usd, billed_hours)
POST /training/x402/runs  (X-Payment, + quote_id)   -> 202 { quote_id, status_url, claim_token, run_id? }  (run_id appears once the run exists)
GET  /training/x402/orders/<quote_id>  (Bearer claim_token) -> state + run progress
```

Body: `{ owner_wallet, dataset_id, base_model, gpu_plan_id, budget_hours, network, recipe? }`.

Rules an agent must follow:
- SIGN the quote request with `owner_wallet` (X-Auth-* wallet signature, same scheme as the
  compute API, or an API key of that wallet). The paid request needs no auth headers.
- `owner_wallet` must OWN the dataset, the dataset must be APPROVED, and the SAME wallet
  must pay. Payer != owner is refused before any money moves.
- Networks: whatever `catalog.networks` lists: today `base` (USDC), `solana` (USDC) and `robinhood` (USDG). EVM payers sign EIP-3009; Solana payers sign an SPL transfer transaction (`--network solana`, `SOLANA_SECRET_KEY`). MegaETH is not offered for training. Asking for an unlisted network returns 400 before anything is charged.
- Sign EXACTLY `maxAmountRequired`. Any other signed value is refused.
- EVM: `validBefore` must be no more than `maxTimeoutSeconds` (3600) from now (Solana transactions expire with their blockhash). Standard x402 signers already do this; a longer authorization is refused before anything is charged.
- Resend the SAME body plus `quote_id`. A changed body (hours, GPU, recipe) is refused.
- Keep the `claim_token` (shown once). Status states: `payment_pending` (do NOT pay again),
  `starting`, `run`, `not_paid` (no money moved: request a fresh quote),
  `credited_not_started` (the payment becomes credits on the wallet's account; when `refund`
  is settled, start a run with a wallet-signed `POST /training/runs`; while it is
  `returning` or `unknown`, keep polling).
- Replaying the same payment never charges again; it returns the same ORDER outcome
  (which may be pending or credited, not necessarily a run).
- Results, for a run that SUCCEEDED: the adapter and score report, plus a GGUF only when
  `gguf_available` is true. A block is prepaid and is not checked against your data size:
  a run that does not finish inside its block is stopped at the deadline with no refund
  and no artifacts. Size it first with a wallet-signed `POST /training/estimate`.
- Lost response after paying? Never re-quote. `train_x402.py` saves the signed payment and
  `resume --quote-id <id>` resends that SAME payment, which is never charged twice.
- `409 settlement_pending` = outcome not confirmed yet: poll, never pay twice.
- Limits: $500 per order, 3 paid runs per wallet per 24h, quote valid 10 minutes.
  Auto-tune and resume are not sold over x402 (use Path B).

```bash
python scripts/train_x402.py catalog
python scripts/train_x402.py run --dataset-id <id> --base-model qwen2.5-0.5b-instruct \
  --gpu-plan-id <id> --hours 1 --network base   # or robinhood, solana
python scripts/train_x402.py status --quote-id <id> --claim-token <token>
```

Getting a dataset with no account: buy one over x402 (`references/datasets.md`), or upload
with a wallet-signed `POST /training/datasets/presign` (`{"bytes": N}` -> `upload_url`),
`PUT` the JSONL, then wallet-signed `POST /training/datasets/<id>/approve`.

## Path B — API key (`X-API-Key`), paid from credits

Scopes: `datasets:read|write` (datasets) and `training:read|write` (runs rent GPUs; a
datasets-only key cannot start one). Scoped keys created before 2026-10-21 keep the
training access their datasets scope gave them.

```
GET  /training/catalog
POST /training/datasets/presign        {"bytes": N}  -> { dataset_id, upload_url }
PUT  <upload_url>                      (JSONL, one {"messages":[...]} per line)
POST /training/datasets/<id>/approve
POST /training/estimate                { dataset_id, base_model, gpu_plan_id, budget_hours }
POST /training/runs   (Idempotency-Key) { dataset_id, base_model, gpu_plan_id, budget_hours, recipe?, autotune? }
GET  /training/runs/<run_id>
POST /training/runs/<run_id>/cancel    (no refund of the block)
POST /training/runs/<run_id>/deploy    -> short-lived download URLs (adapter, report; GGUF when gguf_available)
```

Always send an `Idempotency-Key` on `POST /training/runs` so a retry can never start a
second paid run.
