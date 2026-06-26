# Spraay Compute & Futures — Quickstart Examples 💧

All examples assume an x402-aware client with a funded USDC wallet on Base mainnet (or Solana mainnet). The client handles the `402 → sign → retry` loop; below we show the logical request/response.

Base URL: `https://gateway.spraay.app`

---

## 1. Plan before you spend (free)

```bash
# What will this cost?
curl -s https://gateway.spraay.app/api/v1/compute/estimate \
  -H "Content-Type: application/json" \
  -d '{ "type": "text-inference", "model": "auto", "messages": [{ "role": "user", "content": "..." }] }'

# Which models are available?
curl -s https://gateway.spraay.app/api/v1/compute/models
```

---

## 2. Per-call compute

### LLM inference ($0.03)
```js
import { wrapFetchWithPayment } from "@x402/fetch";
const fetchPay = wrapFetchWithPayment(fetch, wallet);

const res = await fetchPay("https://gateway.spraay.app/api/v1/compute/text-inference", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    messages: [{ role: "user", content: "Summarize this contract: ..." }],
    model: "auto",
  }),
});
// → { provider, model, choices: [{ message: { content } }], usage, price_usdc: "0.030" }
```

### Image generation ($0.03)
```js
await fetchPay("https://gateway.spraay.app/api/v1/compute/image-generation", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ prompt: "A futuristic city powered by decentralized compute", model: "auto", width: 1024, height: 1024 }),
});
// → { images: [{ url, width, height }], model: "black-forest-labs/flux-schnell", price_usdc: "0.030" }
```

### GPU run on Replicate ($0.06)
```js
await fetchPay("https://gateway.spraay.app/api/v1/gpu/run", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ model: "flux-pro", input: { prompt: "a serene mountain lake at sunset" } }),
});
// → { id, status: "succeeded", model, output: ["https://replicate.delivery/..."] }
```

### Async video generation ($0.50) + polling
```js
const start = await fetchPay("https://gateway.spraay.app/api/v1/compute/video-generation", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ prompt: "A drone flyover of a mountain range at golden hour", duration_seconds: 4 }),
});
// → { status: "processing", prediction_id: "abc123", poll_url: "/api/v1/compute/status/abc123" }

// Poll until done ($0.001 per poll)
const done = await fetchPay(`https://gateway.spraay.app/api/v1/compute/status/${start.prediction_id}`);
// → { status: "completed", video_url: "https://..." }
```

### Batch — 50 mixed jobs, 10% discount ($0.05 + per-job)
```js
await fetchPay("https://gateway.spraay.app/api/v1/compute/batch", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    jobs: [
      { type: "text-inference", messages: [{ role: "user", content: "Classify 0x..." }] },
      { type: "image-generation", prompt: "Company logo" },
      { type: "embeddings", input: "Decentralized AI compute marketplace" },
    ],
  }),
});
// → { batch_id, jobs_submitted: 3, total_cost_usdc, results: [...] }
```

---

## 3. Compute futures lifecycle (prepay → draw down → refund)

Best when an agent runs many jobs or wants a known budget. One deposit, then jobs cost only a `$0.001` settlement with the tier discount applied.

```js
// Step 1 — open a $50 account ($0.01). $50 lands in the 10% "scale" tier.
const acct = await fetchPay("https://gateway.spraay.app/api/v1/compute-futures/deposit", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ depositor: "0xYourAddress", amount: "50" }),
});
const futuresId = acct.computeFuture.id; // "CFE-ABC12345"
// → { computeFuture: { id, tier: "scale", discount: "10% discount", balanceRemaining: "50 USDC" } }

// Step 2 — run jobs against the balance ($0.001 settlement each, discount applied to model cost)
const job = await fetchPay("https://gateway.spraay.app/api/v1/compute-futures/execute", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ futuresId, type: "text-inference", messages: [{ role: "user", content: "Hello" }] }),
});
// → { status: "completed", billing: { charged: "$0.027", balanceRemaining: "$42.473 USDC" }, compute: { model: "Llama 3.3 70B" } }

// Step 3 — check what's left ($0.001) and the full ledger ($0.002)
await fetchPay(`https://gateway.spraay.app/api/v1/compute-futures/balance?futuresId=${futuresId}`);
await fetchPay(`https://gateway.spraay.app/api/v1/compute-futures/history?futuresId=${futuresId}`);

// Step 4 — refund the unused balance to the depositor ($0.01). Depositor-only.
await fetchPay("https://gateway.spraay.app/api/v1/compute-futures/refund", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ futuresId, caller: "0xYourAddress" }),
});
// → { status: "refunded", refund: { refundAmount: "42.50 USDC", jobsExecuted: 15 } }
```

---

## Notes
- `model: "auto"` lets the gateway route to a sensible default for the job type.
- `execute` requires sufficient prepaid balance; it does not fall back to a per-call payment.
- `refund` only succeeds when `caller` equals the original `depositor`.
- Poll async jobs (`video-generation`, in-flight `batch` items) via `/compute/status/:jobId` until `status: "completed"`.
