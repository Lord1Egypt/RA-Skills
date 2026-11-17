# Stripe Connect as Platform Infrastructure

**Date:** 2026-02-25
**Status:** Plan. Needs external review (GPT, Grok) and Stripe conversation.

---

## The Pitch

We're building the marketplace for AI agent capabilities. Three products, one payment rail. Every developer on our platform becomes a Stripe connected account. Every consumer transaction flows through Stripe. We're Stripe's distribution channel into the agent economy.

---

## The Three Products

### 1. AI CASH (Paywalled Content)

Consumer's AI agent hits a 402 paywall. Consumer taps Apple Pay. Our pool wallet signs the x402 payment in USDC. Content unlocks.

**Stripe's role:** Process the consumer's card payment via Checkout. Hold the funds. We instruct Stripe on the split: $0.25 to us (platform fee), rest covers the x402 USDC cost and card processing.

**Connected accounts:** None needed for this product. The 402 seller gets paid in USDC on-chain, not through Stripe. Stripe only touches the consumer's fiat side. We're the merchant of record.

**Chargeback risk:** On us. We're MoR. Our risk doc covers this: $25 cap, refund-first philosophy, tiered seller vetting, <0.9% dispute rate target.

### 2. AI CASH Connectors (Middleware Economy)

Consumer's agent orchestrates multiple paid capabilities. Research, image gen, translation. Consumer approves one budget ("up to $0.60"). Agent executes. Multiple developers get paid.

**Stripe's role:** Process the consumer's pre-authorization via Checkout or Payment Intents. Hold the funds. After task completes, we tell Stripe how to split: $X to developer A's connected account, $Y to developer B's connected account, our application_fee to us. Unused portion is not captured.

**Connected accounts:** Every connector developer is a Stripe connected account. They onboard via Express (Stripe handles KYC, bank linking, 1099s). We never touch their funds.

**Chargeback risk:** Split. If a connector fails to deliver, we auto-refund from our platform balance (dispute avoided). If a consumer disputes a completed task, Stripe routes it to us as the platform. We handle evidence submission using task logs, connector output hashes, and pre-authorization records.

**Settlement model:**
- Consumer pays once (pre-authorization with capture)
- Agent executes, we log each connector call + cost
- Task completes, we capture the actual amount (not the full authorization)
- We instruct Stripe to transfer to each developer's connected account
- Developers get payouts on their schedule (daily, weekly, monthly)
- We never hold funds. Stripe does.

### 3. Partner Stores (Stripe Marketplace)

Consumer's agent finds a product on a partner's Shopify store or SaaS site. Consumer pays the product price. No extra fees for the consumer. The partner pays a channel fee (2-5%).

**Stripe's role:** Process the consumer's payment. Route it to the partner's connected account minus our application_fee. Partner is merchant of record.

**Connected accounts:** Every Stripe partner (Shopify stores, SaaS companies, physical goods merchants) is a connected account. They onboard via Express or Standard Connect.

**Chargeback risk:** On the partner (they're MoR). Stripe handles disputes with the connected account directly. We're not in the middle. This is the cleanest product from a risk perspective.

---

## Why Stripe Wants This Partnership

### We bring them a new market

The agent economy is nascent. Hundreds of millions of AI users. None of them can buy things through their agents today. We're the on-ramp. Every transaction we enable is a transaction Stripe processes.

### We bring them connected accounts at scale

Every connector developer is a new Stripe customer. Every partner store that isn't already on Stripe needs to sign up. We're a distribution channel for Stripe's core business: getting more businesses onto their platform.

### Volume projections (conservative)

```
Year 1:
  100 connector developers (connected accounts)
  50 partner stores (connected accounts)
  10,000 consumers
  ~$500K GMV

Year 2:
  1,000 connector developers
  500 partner stores
  100,000 consumers
  ~$10M GMV

Year 3:
  10,000 connector developers
  5,000 partner stores
  1M consumers
  ~$100M+ GMV
```

At scale, we're bringing Stripe thousands of connected accounts and millions of transactions they wouldn't have otherwise. That's valuable.

### What we want from Stripe

1. **Custom processing rates.** Standard is 2.9% + $0.30. At volume, we need better. Especially for micro-transactions where $0.30 fixed fee eats the margin.
2. **Micropayment optimization.** Pre-authorization + partial capture model for connector batching. Minimal per-transaction overhead.
3. **Dedicated account manager.** For chargeback strategy, dispute optimization, fraud rule tuning specific to our transaction patterns.
4. **Co-marketing.** Featured on Stripe's Connect marketplace / case studies.
5. **Faster payouts for developers.** Instant payouts or next-day for connected accounts. Developers who get paid fast stay on the platform.

### What Stripe gets

1. Thousands of new connected accounts (connector devs + partner stores)
2. A new transaction category (agent-to-agent commerce)
3. First-mover advantage in the agent economy payment stack
4. Case study: "Stripe Connect powers the first middleware economy for AI agents"

---

## Money Flow Diagrams

### AI CASH (402)

```
Consumer                    Stripe                      Us                    402 Seller
   |                          |                          |                        |
   |-- Apple Pay ($5.70) ---->|                          |                        |
   |                          |-- Hold funds ----------->|                        |
   |                          |                          |-- Sign x402 (USDC) --->|
   |                          |                          |<-- Content ------------|
   |                          |<-- Capture $5.70 --------|                        |
   |                          |-- $0.25 to platform ---->|                        |
   |                          |-- Stripe keeps ~$0.47 ---|                        |
   |<-- Content via agent ----|--------------------------|                        |
```

### AI CASH Connectors

```
Consumer                    Stripe                      Us                    Dev A    Dev B    Dev C
   |                          |                          |                      |        |        |
   |-- Apple Pay ($0.60) ---->|                          |                      |        |        |
   |                          |-- Auth hold $0.60 ------>|                      |        |        |
   |                          |                          |-- Call A ($0.03) --->|        |        |
   |                          |                          |-- Call B ($0.03) ------------>|        |
   |                          |                          |-- Call C ($0.04) ---------------------->|
   |                          |                          |                      |        |        |
   |                          |<-- Capture $0.35 --------|                      |        |        |
   |                          |   (actual spend, not $0.60)                     |        |        |
   |                          |-- $0.0285 to Dev A ----->|  (minus 5% fee)      |        |        |
   |                          |-- $0.0285 to Dev B -------------------------------->|        |
   |                          |-- $0.038 to Dev C ------------------------------------------>|
   |                          |-- $0.005 to platform --->|  (application_fee)   |        |        |
   |                          |-- $0.25 to platform ---->|  (flat fee)          |        |        |
   |<-- Results via agent ----|--------------------------|                      |        |        |
```

### Partner Stores

```
Consumer                    Stripe                      Us                    Partner Store
   |                          |                          |                        |
   |-- Apple Pay ($50.00) --->|                          |                        |
   |                          |-- $50 to partner -------------------------------->|
   |                          |   minus processing (~$1.75)                       |
   |                          |   minus application_fee ($1.75 = 3.5%)            |
   |                          |-- $1.75 to platform ---->|                        |
   |<-- Product via agent ----|--------------------------|------------------------|
```

---

## Regulatory Position

### Why we're NOT a money transmitter

1. **We never hold consumer funds.** Stripe receives, holds, and distributes all funds.
2. **We never receive funds into our account and re-distribute.** Stripe transfers our platform fee (application_fee) to us. We don't touch the rest.
3. **Stripe is the payment processor.** They handle KYC on connected accounts, 1099 reporting, sanctions screening, AML compliance.
4. **We're a technology platform.** We provide the software that instructs payment routing. We don't transmit money.

### What we still need

1. **LLC or Corp.** Required to be a Stripe Connect platform. Non-negotiable.
2. **Terms of Service.** For consumers, connector developers, and partner stores.
3. **Privacy Policy.** What data we collect, how connector queries are handled.
4. **Stripe Connect agreement.** Their standard platform agreement.
5. **Legal review.** Confirm our specific model doesn't trigger state MTL requirements. The Stripe Connect model is well-established, but a lawyer should confirm.

---

## Chargeback Strategy (All Three Products)

### Prevention (shared across all products)

- **3D Secure on all transactions.** Shifts liability to card issuer.
- **Stripe Radar.** ML-based fraud detection. Custom rules for our patterns.
- **Clear billing descriptors.** "AI CASH * [service name]" so consumers recognize charges.
- **Instant receipts.** Email receipt with exactly what was purchased.
- **Refund-first philosophy.** If someone asks for a refund under $25, just give it. Cheaper than a dispute.

### Per-product chargeback handling

**AI CASH (402):** We're MoR. We fight it with: x402 proof of delivery, Stripe session logs, Apple Pay device confirmation, pre-authorization consent record.

**Connectors:** We're MoR. We fight it with: task authorization log, connector call/response records, output delivered confirmation, pre-auth consent.

**Partner Stores:** Partner is MoR. Stripe handles it with the connected account. Not our problem.

### Dispute rate targets

- Platform-wide: <0.9% (Stripe's threshold)
- AI CASH: <0.5% (low-value, high-consent transactions)
- Connectors: <0.3% (pre-authorized, agent-mediated, no surprises)
- Partner Stores: per-partner monitoring (delist partners above 1%)

---

## Technical Implementation

### Stripe Products We Use

| Stripe Product | What We Use It For |
|---|---|
| **Connect (Express)** | Onboard connector devs + partner stores |
| **Checkout** | Consumer payment for 402 + partner stores |
| **Payment Intents** | Pre-authorization + partial capture for connectors |
| **Transfers** | Split payments to connected accounts |
| **Radar** | Fraud detection |
| **Billing** | Optional: recurring connector subscriptions |
| **Webhooks** | Payment confirmation, dispute alerts, payout notifications |

### Worker Routes (New/Updated)

| Route | Product | What |
|---|---|---|
| `POST /pool/pay` | AI CASH | Create Checkout for 402 payment |
| `POST /pool/confirm` | AI CASH | Confirm + sign x402 |
| `POST /connect/onboard` | All | Create Express connected account for dev/partner |
| `POST /connect/dashboard` | All | Link to Stripe Express dashboard for dev/partner |
| `POST /task/authorize` | Connectors | Create PaymentIntent with auth hold |
| `POST /task/capture` | Connectors | Capture actual spend after task completes |
| `POST /task/cancel` | Connectors | Cancel unused authorization |
| `POST /partner/checkout` | Partner Stores | Create Checkout with application_fee |

### KV Storage (New)

| Key Pattern | What |
|---|---|
| `connect:{email}` | Connected account ID, onboarding status |
| `task:{taskId}` | Task authorization, connector calls, spend log |
| `intent:{intentId}` | PaymentIntent mapping to task |

---

## Timeline

### Phase 1: Foundation (Weeks 1-2)
- [ ] Form LLC
- [ ] Apply for Stripe Connect
- [ ] Set up Express onboarding flow
- [ ] Build `POST /connect/onboard` route

### Phase 2: AI CASH on Connect (Weeks 3-4)
- [ ] Migrate pool mode from basic Stripe Checkout to Connect
- [ ] Platform fee via application_fee (not manual split)
- [ ] Test with Morning Stew / Pawr 402 gates

### Phase 3: Partner Stores (Weeks 4-5)
- [ ] Build partner Checkout with application_fee
- [ ] Onboard Modern Weaving as first connected account
- [ ] Test end-to-end: agent finds product, consumer pays, partner gets paid

### Phase 4: Connectors (Weeks 5-8)
- [ ] Build PaymentIntent auth/capture flow
- [ ] Build task authorization + settlement logic
- [ ] Build 3 demo connectors (deep-research, image-gen, pdf-export)
- [ ] Test multi-connector task with single Apple Pay approval
- [ ] Launch registry

---

## The Ask to Stripe

When we're ready to talk to them:

> "We're building a marketplace for AI agent capabilities. Three products, all on Stripe Connect.
>
> AI CASH lets consumers pay for paywalled content through their AI agents via Apple Pay. Connectors let developers publish paid AI capabilities with zero billing infrastructure. Partner Stores let merchants sell through AI agents with no extra setup.
>
> Every developer and merchant on our platform is a Stripe connected account. We expect 150+ connected accounts in year one, scaling to 10,000+ by year three. All consumer transactions flow through Stripe.
>
> We want to be a Stripe Connect platform partner. We need: custom rates for micro-transactions, a dedicated account manager, and support for our pre-authorization + partial capture model for batched agent workflows."

---

## Open Questions

1. **LLC vs Corp?** LLC is simpler. Corp (C-Corp or S-Corp) if we're raising money.
2. **State of incorporation?** Delaware is standard for tech. Wyoming for simplicity.
3. **Do we need a lawyer before Stripe?** Probably yes. Quick consult on MTL exemption under Connect.
4. **Stripe Connect tier?** Express is easiest. Custom gives more control. Start Express.
5. **Micropayment rates?** Stripe's $0.30 fixed fee kills us on sub-$1 transactions. Can we negotiate? Or do we batch to amortize?
6. **International?** Stripe Connect works globally but adds complexity. US-only for v1?
