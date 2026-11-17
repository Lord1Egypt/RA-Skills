# MPP (Machine Payments Protocol) vs Agent Pay

**Date:** 2026-03-18
**Authors:** Parker Todd Brooks, Claude Code (cc-mini)
**Status:** Research note. Informs product strategy.

---

## What MPP Is

Machine Payments Protocol. Open protocol for machine-to-machine payments. Co-authored by Tempo (stablecoin blockchain) and Stripe. Submitted to IETF as "Payment HTTP Authentication Scheme." Standardizes HTTP 402 for payment flows.

Three primitives: Challenges (server says "pay me"), Credentials (client proves payment), Receipts (server confirms).

SDKs in Python, Rust, TypeScript. Middleware for Express, Next.js, Hono. MCP transport for AI tool calls.

**URL:** https://mpp.dev

## What MPP Has Today

50+ live services. Real money flowing. Including:

- **AI**: Anthropic, OpenAI, Gemini, OpenRouter, Perplexity, Replicate, ElevenLabs, fal.ai, Suno
- **Web**: Firecrawl, Browserbase, Oxylabs, Browser Use
- **Data**: Dune, Alchemy, Codex (blockchain), StableEnrich, Hunter, BuiltWith, Diffbot
- **Search**: Exa, Parallel, SerpApi, SpyFu
- **Media**: StableStudio (image/video gen), Stability AI
- **Storage**: S3/R2-compatible object storage, code storage (Git repos)
- **Other**: Google Maps, weather, flight tracking, sneaker data, CAPTCHA solving, SEC EDGAR, real estate

These are NOT the raw APIs. They're wrapped services on MPP's payment protocol. `anthropic.mpp.tempo.xyz` is Anthropic's API proxied through MPP's payment layer. The developer doesn't need an Anthropic API key. They pay per request through MPP.

Same for all 50+. No API keys. No accounts. No billing setup. Just pay per request.

## How MPP Payments Work

1. Agent calls a service endpoint
2. Service returns HTTP 402 with a Challenge (price, payment methods accepted)
3. Agent's client library resolves the Challenge
4. Payment happens (Tempo stablecoin, Stripe card, Lightning)
5. Agent sends Credential (proof of payment)
6. Service returns content + Receipt

**Payment methods:**
- **Tempo**: Stablecoins on Tempo blockchain. Requires wallet. `tempo wallet login`.
- **Stripe**: Cards via "Shared Payment Tokens." Requires Stripe integration on client side.
- **Lightning**: Bitcoin over Lightning Network. Requires Lightning wallet.
- **Custom**: Build your own payment method.

**The consumer funding problem:** To use MPP today, you need either:
- A Tempo wallet funded with stablecoins (crypto-first)
- A Stripe integration in your client app (developer work)
- A Lightning wallet with sats

There is no "tap Apple Pay and go" moment for normal people.

## What Agent Pay Is (Our Product)

Agent Pay is the checkout experience for the agent economy. Three modes:

**AI Cash (Pool Mode):** Agent hits a paywall. Apple Pay checkout opens. User taps Face ID. We settle the payment from our pool. Content returned. The user never sees crypto. Never sets up a wallet. Never configures anything.

**Agent Wallet (Mode C):** Power users pre-fund a wallet (Coinbase CDP or Privy). Agent spends autonomously within budget limits. No Apple Pay tap per transaction. Fast. No fees from us.

**Link:** For agents without tool access. One-time payment URL. User pastes it back. Done.

## Where We're Different

### 1. The Human Is In The Loop

MPP is machine-to-machine. The agent has credentials and pays autonomously. No human approval per transaction.

Agent Pay puts the human in the approval loop. Every AI Cash transaction requires Face ID. The agent REQUESTS payment. The human APPROVES it. This is a feature, not a limitation. It's how you build trust with consumers who've never let their AI spend money.

### 2. No Wallet Required

MPP requires a funded wallet (Tempo, Lightning) or Stripe credentials. The agent must have payment credentials pre-configured before it can use any service.

Agent Pay's AI Cash mode requires nothing. No wallet. No credentials. No setup. The user taps Apple Pay at the moment of need. We handle everything behind the scenes.

### 3. Physical Goods and Stripe Partners

MPP is API-to-API. It pays for digital services (search results, embeddings, compute). It does not handle Shopify stores, physical goods, subscriptions, or anything that goes through traditional e-commerce.

Agent Pay has Stripe Connect partners. Modern Weaving (handcrafted leather goods) is live. Any Shopify store can join. The agent can buy a bag, a subscription, a physical product. That's commerce, not infrastructure.

### 4. Chargeback Protection (The Partner Network)

When AI Cash settles a payment, WE are on the hook for chargebacks. Visa comes to us, not the service provider.

This is why the partner network exists. Tiered vetting. Transaction caps. Monitoring periods. Refund cooperation agreements. Every service in our network has been evaluated for chargeback risk.

MPP has no concept of this. It's an open protocol. Any service can accept MPP payments. If a service delivers garbage, the consumer has no recourse through MPP. They'd have to dispute with their payment method provider directly.

Our partner directory is the trust layer. It's not just a list of services. It's a list of services we're willing to take financial risk on.

### 5. The Autonomous Wallet

No one else is building: "Load $50. Set a $2 per-transaction limit. Let the agent spend autonomously. Get a receipt at the end."

MPP's Tempo sessions come close (deposit into escrow, agent spends via signed vouchers). But that requires stablecoins, a Tempo wallet, and understanding blockchain escrow. Our version: tap Apple Pay for $50, set a limit, forget about it.

## Where MPP Is Ahead

- **Protocol formalization.** IETF submission. Stripe as co-author. This is becoming the standard.
- **Service directory.** 50+ live services. Real money flowing. We have a plan on paper.
- **SDKs.** Python, Rust, TypeScript. Battle-tested. We have a Node.js CLI.
- **MCP transport.** Formal spec for AI tool calls with payment. We have MCP tools but no formal transport spec.
- **Multi-rail support.** Cards, stablecoins, Lightning, custom. We have x402 (Coinbase) and Stripe.

## The Strategy

### Don't compete on protocol. Compete on experience.

MPP is trying to be HTTP for payments. We don't compete with HTTP. We build products on it.

Agent Pay should be an MPP payment method. When an agent hits any of those 50+ MPP services, AI Cash settles it. MPP gets consumer adoption. We get access to 50+ services without partner onboarding.

### Keep the partner network for commerce.

Stripe partners (Shopify stores, physical goods) don't speak MPP. They speak Stripe. Our Stripe Connect integration is the bridge. Keep building that. MPP won't touch it.

### Build the autonomous wallet on MPP.

The pre-funded wallet with budget limits is the killer feature. Build it on MPP instead of x402-only. Broader ecosystem. More services. Same UX.

### Two channels, one product:

1. **API services:** Use MPP as settlement. AI Cash as the consumer funding layer. Partner vetting for chargeback protection.
2. **Commerce (Stripe):** Direct Stripe Connect. Physical goods, subscriptions, Shopify. MPP doesn't play here.

## Partnership Opportunity

Reach out to MPP/Tempo team. Pitch:
- "We're the fiat on-ramp for MPP. Normal people can't use Tempo wallets. AI Cash lets them tap Apple Pay."
- "We bring consumer adoption. You bring the service directory."
- "AI Cash becomes an MPP payment method. Your 50+ services get accessible to anyone with a phone."

## Open Questions

1. Does MPP's Stripe integration already support Apple Pay under the hood? If yes, how far are they from surfacing it?
2. Can we implement AI Cash as a custom MPP payment method without forking the protocol?
3. What's the revenue model if we're a payment method on someone else's protocol? Per-transaction fee? Channel fee?
4. Tempo is a stablecoin blockchain we've never used. Do we need to understand it, or can we ignore it and just use the Stripe rail?
5. Who at Tempo/Stripe is the right contact for a partnership conversation?

---

*Research by Parker Todd Brooks and Claude Code. March 18, 2026.*
