# Datasets: buy fine-tuning data with a wallet

Generate a validated JSONL training dataset from a one-sentence description
plus a handful of example conversations. Pay per example in USDC. No account,
no dashboard, no human: an agent can buy its own training data.

**API base:** `https://compute.x402layer.cc`
Dashboard (wallet-session users): https://cloud.x402compute.cc/network/datasets

## The shape of the flow (read this first)

Generation takes MINUTES (a 2000-row job can take far longer), so the purchase
never waits on it:

```
POST /datasets/x402/synth                  -> 402 + quote (price, rows, model)
POST /datasets/x402/synth  (X-Payment)     -> 202 + dataset_id + claim_token   (~1s)
GET  /datasets/x402/jobs/<id>  (Bearer claim_token) -> progress, then download
```

Do NOT hold a connection waiting for the file, and do not treat the 402 as an
error: it is the price quote. Poll the status URL, or pass `webhook_url` and be
told when it is done.

## Pricing

`GET /datasets/config` (no auth) returns everything needed to quote a job:

```json
{ "synth": { "rates_per_100_usd": {"fast":0.2,"balanced":0.35,"best":1.0,"grid":0.15},
             "verify_rate_per_100_usd": {"managed":0.1,"grid":0.03},
             "max_rows": 2000,
             "models": [{"id":"deepseek-v3.1","tier":"fast","in_per_m":0.55,"out_per_m":1.65}, …20 models] } }
```

**Price = (generation rate + verification rate) x rows / 100.** Every dataset is
CHECKED by default (see below), and that check is its own price line, so quote
with both: 200 rows managed `fast` = $0.60, 200 rows on the grid = $0.36, 2000
on `best` = $22. Send `"verify": false` to skip checking and pay generation only.
The per-million-token numbers are the provider's published rates, shown for
comparison only: the buyer pays the flat per-example price, never per token.

Sizes: 50 to 2000 rows. Seeds: 5 to 20 example conversations (required, they
teach the generator the format and tone).

**House rules** (`rules`, up to 12 strings of 200 chars): what the assistant must
NEVER do, e.g. "Never promise a refund", "Never state a delivery time you cannot
verify". Set them whenever the task involves policy, money, or commitments: a
standing instruction says what to do, rules say what is forbidden, and without
them the model invents a policy and applies it differently every row (a real
200-row support set produced twelve different refund offers). Policy/figure
consistency is enforced by default even with no rules.

## Verification (on by default)

Every generated row is read back by a SECOND model and scored against the house
rules before it is allowed into the dataset. A row that breaks a rule is thrown
away and regenerated, so the buyer gets a full-size dataset of rows that passed,
not a full-size dataset with failures in it.

WHO CHECKS depends on the provider, and this is the important part:

- **Managed** jobs are checked by a separate FRONTIER model, never the model
  that wrote the rows (a model marks its own homework badly). $0.10 per 100.
- **Grid** jobs are checked BY THE GRID, using the network's own models, so
  nothing leaves the confidential network even to be verified. $0.03 per 100.
  Honest trade: on-grid models are smaller, so it is a weaker check than the
  frontier judge, which is why it costs a third as much.

The status response carries the receipt: `checked`, `rejected` (thrown away and
regenerated) and, if the call budget ran out before a batch could be judged,
`unchecked`. A job never claims a check it did not perform.

WHY this exists: a real 200-row support dataset generated WITHOUT rules or
checking invented twelve different compensation policies, including 13 full
refunds, because nothing ever verified the output against a policy. Rules are
prevention; verification is the check.

**Two providers.** Managed models (`model_tier` fast/balanced/best, or an exact
`model_id` from the catalog) are fastest with the best data quality. The
decentralized grid (`grid_model`, implies `provider: "grid"`) runs on our own
confidential end-to-end encrypted network, so nothing goes to an outside
provider: cheaper, slower, and if a node drops mid-job the next most
appropriate model on the network takes over automatically.

## Buying it

1. **Quote.** POST the job with no payment header. The 402 carries the standard
   x402 `accepts` array plus a `singularity` block: `quote_id`, `rows`, `tier`,
   `price_usd`, `quote_expires_at`.

```bash
curl -X POST https://compute.x402layer.cc/datasets/x402/synth \
  -H 'Content-Type: application/json' \
  -d '{"description":"Classify a support message as billing, technical, or account",
       "seed_examples":[ …5 to 20 {"messages":[{"role":"user",…},{"role":"assistant",…}]} … ],
       "target_rows":200, "model_tier":"fast", "network":"base",
       "rules":["Never promise a refund"], "verify":true}'
```

2. **Pay.** Send the SAME body plus `quote_id`, with the signed `X-Payment`
   header. Returns **202** with `dataset_id`, `status_url`, `claim_token`,
   `price_paid_usd`, `tx_hash` (and `webhook_secret` if a webhook was given).

3. **Collect.** `GET /datasets/x402/jobs/<dataset_id>` with
   `Authorization: Bearer <claim_token>`:
   - running -> `{"status":"generating","rows_done":120,"rows_target":200,"checked":120,"rejected":4}`
   - done -> `{"status":"complete","row_count":205,"download_url":"…","format":"jsonl"}`
     (presigned, 5 minutes, re-issued on every poll)
   - failed -> `{"status":"failed","refund_status":"applied"|"pending"}`

## Rules that will bite you if ignored

- **SAVE THE CLAIM TOKEN.** It is returned once, stored only as a hash, and is
  the only way to read the job or download the file. Lost token = lost dataset.
- **The payment is bound to the quoted job.** The server hashes the job
  definition; paying with a different body is refused. Send the identical body
  on both calls (a `webhook_url` may differ, it does not change the goods).
- **Quotes expire in 10 minutes**, and the price is snapshotted at quote time,
  so a rate change can never alter what is charged.
- **Validate before quoting, not after paying:** an invalid body returns 400 at
  the quote step, never a 402 you would then pay against.
- **Refunds are credits, not on-chain reversals**, and `refund_status` is read
  from the ledger rather than asserted.
- **Behind a WAF:** send a real `User-Agent`. Default library agents get 403.

## Chains

USDC on **Base** and **Solana**, USDG on **Robinhood Chain**, USDM on
**MegaETH** (18-decimal, the rest are 6). Choose with `"network"`; the
challenge returns the right asset and amount.

## Webhooks

Pass `webhook_url` (public HTTPS) at quote time and the terminal state is
POSTed to it, so polling is optional:

```
X-SGL-Signature: t=<unix>,v1=<hex hmac>
body: {"event":"dataset.synth.completed","event_id":"<order>:completed","dataset_id":…,"download_url":…}
```

Verify `HMAC-SHA256(webhook_secret, "<t>.<raw body>")` against `v1` and reject a
stale `t` (that timestamp is what makes a captured delivery non-replayable).
Redirects are not followed; only 2xx counts. Three attempts (1m, 5m, 25m) then
it stops. Delivery never affects the job, so polling is always the fallback.

## MCP

The same flow as four tools on `https://mcp.x402layer.cc/mcp`:
`list_dataset_pricing`, `request_dataset_payment`,
`create_dataset_with_payment`, `get_dataset_status`.

## What the buyer actually gets

Not raw model output. Every line is schema-checked and dropped if malformed;
near-duplicate and reworded repeats of an earlier scenario are rejected instead
of padding the count; generation is steered across a rotating set of coverage
axes so edge cases appear rather than fifty variants of one; and every row
carries the same standing instruction so the file is uniform. If the usable
floor is not reached, the fee is refunded.
