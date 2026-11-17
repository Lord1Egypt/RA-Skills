# SP3ND Agent Skill

The SP3ND Agent Skill lets an agent buy shipped products and tokenized Collector Crypt cards with USDC on Solana. SP3ND fetches prices, accepts payment, and handles fulfillment. For Collector Crypt, SP3ND staff manually purchase the exact card and transfer the NFT to the paying wallet.

## Install

```bash
npx skills add kent-x1/sp3nd-agent-skill
```

The skill follows the [Agent Skills](https://agentskills.io) format. For a manual installation, copy `SKILL.md` together with `references/` and `scripts/` into the skill directory so its linked checkout instructions and examples are available. This release is version **1.11.0**; users with older installed copies should update them to discover Collector Crypt checkout.

## Collector Crypt

Give the agent a canonical `https://collectorcrypt.com/assets/solana/<asset-address>` link, or ask it to search eligible live listings. Approved API credentials work without a separate Collector Crypt opt-in.

```text
one card URL -> live quote -> wallet-delivery order
  -> partnerPayment prepare -> buyer signs exact bytes -> submit
  -> confirmed USDC payment to SP3ND
  -> manual purchase -> manual NFT transfer -> Delivered
```

One card per order, quantity `1`, with no shipping address. Quotes last five minutes. The payer and NFT recipient must be the same wallet; paying from an agent wallet means the NFT is delivered to that agent wallet. The listing is not reserved on Collector Crypt, so an unavailable card may require review and a refund.

Read [Collector Crypt checkout](references/collector-crypt.md) for request examples, transaction verification, exact-byte retries, and manual delivery tracking. Card payments use only `partnerPayment`; the x402 helper and `createPartnerTransaction` do not support cards. `Paid` confirms receipt of USDC, not NFT delivery.

## Shipped-product lifecycle

```text
product URL + quantity
  -> server-priced cart
  -> idempotent order
      -> Ready for Payment
      -> or Awaiting Review until SP3ND supplies a quote
          -> Ready for Payment
  -> shipping selection when required
  -> server-issued x402 requirements
  -> payment
  -> fulfillment tracking
```

Mixed or unverified carts remain one order. An agent must not pay while `payment_ready` is false, while a quote is expired, or while a required shipping option is unselected. Canonical current orders use `pricing_status: "ready_for_payment"`; deprecated `quoted` may appear on legacy orders, but never makes an order payable by itself.
An `Awaiting Review` order must reach **Ready for Payment** before it becomes `Paid`; it must never skip that gate.

SP3ND is authoritative for listing data and all monetary fields. Agents submit product URLs and quantities; caller-supplied prices, totals, currency, payment recipients, and memos must never control a purchase.

For end-user purchases, send `user_wallet` so order history and points are attributed to the correct wallet.

## Shipped-product x402 example

This existing example is for non-card orders only. Use the [Collector Crypt flow](references/collector-crypt.md) for tokenized cards.

Install the example dependencies:

```bash
npm install @solana/web3.js @solana/spl-token @solana/spl-memo dotenv
```

Copy `.env.example` to `.env`, provide the required values, and run:

```bash
node scripts/x402-pay-with-memo.mjs
```

The example:

- creates an order with a stable `Idempotency-Key`;
- stops or polls when SP3ND is reviewing the order;
- requires an opaque server-returned shipping option when applicable;
- refreshes and validates quote revision, expiry, and payment readiness;
- constructs payment only from the HTTP 402 amount, asset, recipient, memo, and resource;
- submits the signed payload only to SP3ND, which owns verification and settlement;
- reads the order before any retry when settlement or confirmation is uncertain.

## Documentation and discovery

- API documentation: <https://sp3nd.shop/partner-api/docs>
- Partner dashboard: <https://sp3nd.shop/partner-api/dashboard>
- Agent card: <https://sp3nd.shop/.well-known/agent-card.json>
- Published skill: <https://sp3nd.shop/skill.md>
- Support: <support@sp3nd.shop>

## License

Apache 2.0
