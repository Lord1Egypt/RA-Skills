# Lēsa Review — 2026-02-24

## Full Product Review (after reading all plans, partners pages, thesis docs)

I've read everything now. Here's my honest take after absorbing the full picture:

**This is significantly more thought-through than I realized.** My earlier feedback was based on just the CASH.md readme. The plans underneath are a real product architecture.

**What CC built here is genuinely good:**

The two-product split is clean and correct. Agent Cash = consent (Apple Pay, normal humans, no crypto knowledge). Agent Wallet = sovereignty (bring your own wallet, MIT, no fees). That's not a marketing distinction, it's an architectural one. Different trust models, different risk surfaces, same pipeline underneath.

The pool mode is clever. Parker fronts USDC, user pays fiat via Apple Pay, Parker always nets $0.25. Simple, sustainable, no incorporation needed for v1. The $25 cap is the right safety valve.

The chargeback strategy is mature. Refund-first philosophy, tiered seller network, dispute rate as the north star metric. This reads like someone who's actually run a payments business, not someone theorizing about one.

**The two partner pages are the real unlock.** You've got two-sided onboarding:
- Stripe partners (Shopify stores, SaaS): "AI agents are already finding your products. Let them buy."
- 402 partners (Morning Stew, Pawr): "Users don't have wallets. We bridge fiat to your 402 gate."

**Now — comparing to Stripe's letter:**

Stripe says "agentic commerce is coming" and lists five levels. They're building SDKs for merchants. You're building the thing that sits between the agent and those merchants. Stripe is the engine, you're the ignition. They benefit from you existing because you drive transaction volume through their rails.

The real positioning isn't "competing with Stripe." It's: **Agent Cash is to Stripe what Shopify was to Stripe.** A layer on top that makes Stripe useful in a new context. Shopify made Stripe work for e-commerce. Agent Cash makes Stripe work for AI-initiated commerce.

**One thing I'd flag:** The "teach your AI how to pay" prompt in CASH.md is genuinely viral-worthy. That's the distribution mechanism. No app store. No install. Just paste a prompt and your AI onboards itself. That's native to how people actually use AI tools today.

---

## VIP Network & Chargeback Strategy

The pool is what makes it cool. The VIP list IS the product. Not the code, not the protocol. The curated network with a bouncer at the door.

"You want in? Cool. You chargeback? You're out. Forever."

That's how you keep the Stripe account healthy AND make it exclusive. Low dispute rate isn't just risk management, it's a feature. The network stays clean because bad actors get one shot.

And the pool mode is what makes it frictionless. No wallet setup, no USDC, no Coinbase account. Just Apple Pay. Parker's float absorbs the crypto complexity. The user never knows USDC exists. They just said "let's go" and got their article.

The VIP angle also flips the chargeback problem from defensive to offensive. Stripe's chargeback nightmare is "how do we fight disputes." Ours is "you dispute, you lose access to the network." That's way more powerful because the access is worth more than whatever they'd claw back on a $0.42 transaction.
