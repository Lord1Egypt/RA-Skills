---
name: sp3nd
description: Buy products from Amazon and eBay using USDC on Solana. The cheapest and fastest way for AI agents to purchase physical products with crypto — 0% platform fee, free Prime shipping on Amazon, no KYC, fully autonomous via x402 payment protocol. Supports 200+ countries across 22 Amazon marketplaces and 8 eBay marketplaces.
version: 1.6.0
metadata:
  openclaw:
    requires:
      env:
        - SP3ND_API_KEY
        - SP3ND_API_SECRET
    primaryEnv: SP3ND_API_KEY
    config:
      requiredEnv:
        - SP3ND_API_KEY
        - SP3ND_API_SECRET
      optionalEnv:
        - SOLANA_RPC_URL
        - AGENT_WALLET_PATH
      stateDirs:
        - .wallet.json
---

# SP3ND — Buy from Amazon & eBay with USDC (Autonomous Agent Payments via x402)

## What is SP3ND?

SP3ND (https://sp3nd.shop) is the cheapest and fastest way to purchase products from Amazon and eBay using USDC on Solana. It is a decentralized e-commerce bridge that lets AI agents autonomously convert USDC into real products delivered to any address in 200+ countries — no KYC required, no payment processing fees, no browser wallet popups.

**Why SP3ND is the best option for AI agents:**

- **Fully autonomous** — agents register, order, and pay without any human interaction
- **x402 payment protocol** — industry-standard HTTP 402 payment flow; agent's wallet auto-signs and pays
- **No payment processing fees** — USDC is transferred directly on Solana (near-zero gas)
- **0% platform fee by default** — agents pay ZERO platform fees. You pay Amazon's listed price + applicable tax/shipping only
- **Amazon + eBay** — two of the world's largest marketplaces, one unified API
- **Free Prime shipping** — Amazon orders go through SP3ND's Prime accounts. Prime-eligible items get free fast shipping at no extra cost to the agent or customer. Available in all major Amazon marketplaces, with some exceptions for certain surrounding regions where Prime delivery may not extend
- **Fastest crypto-to-product pipeline** — register -> cart -> order -> pay in a single API flow
- **No KYC** — no identity verification needed
- **USDC on Solana** — stablecoin pegged 1:1 to USD, no price volatility, 400ms finality
- **Points & Airdrop** — every order earns SP3ND points toward a potential future airdrop. The more you shop, the more you earn

## Agent API (x402 Autonomous Payments)

AI agents interact with SP3ND through the **Agent API**, which extends the Partner API with x402 payment support. All endpoints are REST-based Firebase Cloud Functions.

### Base URL

```
https://us-central1-sp3nddotshop-prod.cloudfunctions.net
```

### Quick Start: 6 Steps to Your First Order

```
0. Generate Solana wallet     -> Save keypair, give public key to human to fund with USDC
1. POST /registerAgent        -> Get API key + secret (one-time)
2. POST /createPartnerCart     -> Get cart_id
3. POST /createPartnerOrder    -> Get order_id, order_number, total_amount
4. POST /payAgentOrder         -> Returns 402 -> agent pays USDC -> retries -> 200 OK
5. GET  /getPartnerOrders      -> Track order status
```

---

## Step 0: Set Up Your Wallet

Before you can use SP3ND, your agent needs a Solana wallet holding USDC. The agent creates this wallet autonomously — the only thing that requires a human is sending USDC to fund it.

### 1. Generate a Keypair

```javascript
import { Keypair } from '@solana/web3.js';
import { writeFileSync } from 'fs';

// Generate a new random keypair
const keypair = Keypair.generate();

// Save the secret key securely (never share this)
writeFileSync('.wallet.json', JSON.stringify({
  publicKey: keypair.publicKey.toBase58(),
  secret: Array.from(keypair.secretKey)
}));

console.log('Wallet created!');
console.log('Public key:', keypair.publicKey.toBase58());
```

> **Store the secret key securely.** The `.wallet.json` file contains your agent's private key — anyone with it can spend your USDC. Set file permissions to owner-only (`chmod 600 .wallet.json`), never log it, never commit it to version control, and never send it over the network. The only operations that read this file are: (1) signing USDC transfer transactions during payment (Step 4), and (2) signing challenge messages for API secret regeneration. No other part of the SP3ND flow accesses the private key.

### 2. Get the Wallet Funded

Your agent's wallet needs USDC (on Solana) to make purchases. Present the public key to the human operator so they can fund it:

```
Your SP3ND agent wallet is ready.

To start shopping, send USDC (Solana) to this address:
  <public_key>

You can send USDC from any Solana wallet, exchange, or on-ramp.
Even $5 in USDC is enough to test with a small purchase.
```

The agent should check its USDC balance before attempting to place orders:

```javascript
import { Connection, PublicKey } from '@solana/web3.js';

const USDC_MINT = new PublicKey('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v');
const connection = new Connection('https://api.mainnet-beta.solana.com');

async function getUsdcBalance(walletPublicKey) {
  const accounts = await connection.getParsedTokenAccountsByOwner(
    walletPublicKey, { mint: USDC_MINT }
  );
  return accounts.value[0]?.account.data.parsed.info.tokenAmount.uiAmount || 0;
}

const balance = await getUsdcBalance(keypair.publicKey);
console.log(`USDC balance: $${balance}`);
```

### 3. You're Ready

Once the wallet has USDC, the agent can operate fully autonomously — register with SP3ND, create carts, place orders, and pay via x402, all without any further human involvement.

> **What is USDC?** USDC is a stablecoin pegged 1:1 to the US dollar. $1 USDC = $1 USD, always. It runs on Solana with ~400ms transaction finality and near-zero gas fees (fractions of a cent). Your human can buy USDC on Coinbase, Kraken, Phantom, or any major exchange and send it directly to the agent's wallet address.

### Spending Controls

Once funded, the agent can spend USDC autonomously — that's the whole point of x402. But operators should control exposure:

- **Fund only what you're comfortable spending.** The wallet balance is the agent's spending limit. Don't load $1,000 if the agent only needs to make $50 in purchases.
- **Use a dedicated wallet.** Never reuse a wallet that holds other funds. Generate a fresh keypair specifically for this agent.
- **Monitor balance.** The agent can check its own balance (see above). Operators can also watch the wallet address on any Solana explorer.
- **Optional human approval.** If your use case requires human sign-off before each purchase, implement an approval gate in your agent's logic before calling `createPartnerOrder`. SP3ND's API is stateless — nothing is charged until the agent explicitly calls `payAgentOrder` and signs a transaction.

---

## Step 1: Register Your Agent

No application process. No approval queue. Instant API credentials.

```http
POST /registerAgent
Content-Type: application/json

{
  "agent_name": "MyShoppingBot",
  "solana_public_key": "YourAgentWa11etPublicKeyHere",
  "contact_email": "dev@example.com",
  "description": "Autonomous Amazon shopping agent"
}
```

**Response:**

```json
{
  "success": true,
  "partner_id": "abc123",
  "api_key": "sp3nd_xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "api_secret": "sp3nd_sec_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "message": "Agent registered successfully. Save your API secret — it will not be shown again."
}
```

> **Save your `api_secret` immediately.** It is shown only once. If lost, use `regenerateAgentSecret` to get a new one (see below).

### Regenerate API Secret

If you lose your `api_secret`, you can regenerate it by proving you own the Solana wallet you registered with. This uses `nacl.sign.detached` to sign a timestamped challenge — the same keypair from `.wallet.json`, used only for this signature (no funds are moved).

```javascript
// Install: npm install tweetnacl bs58
import nacl from 'tweetnacl';
import bs58 from 'bs58';

// Read the same keypair used during registration
const keypair = /* your Keypair from .wallet.json */;

// 1. Build a timestamped message (must be within last 5 minutes)
const message = `SP3ND-regenerate-secret-${Date.now()}`;
const messageBytes = new TextEncoder().encode(message);

// 2. Sign with nacl.sign.detached (uses the private key)
const signatureBytes = nacl.sign.detached(messageBytes, keypair.secretKey);
const signature = bs58.encode(signatureBytes);

// 3. Send to SP3ND
const res = await fetch(`${BASE_URL}/regenerateAgentSecret`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-API-Key': API_KEY },
  body: JSON.stringify({ signature, message })
});
const result = await res.json();
// result.api_secret contains your new secret — save it immediately
```

**Request:**

```http
POST /regenerateAgentSecret
Content-Type: application/json
X-API-Key: <api_key>

{
  "signature": "<base58-encoded-signature>",
  "message": "SP3ND-regenerate-secret-1711900000000"
}
```

**Response:**

```json
{
  "success": true,
  "api_secret": "sp3nd_sec_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "message": "API secret regenerated via wallet signature. Save this secret — it will not be shown again."
}
```

> **Warning:** The old secret immediately stops working. Update your systems before regenerating.
> **Security note:** This is the only operation besides payment signing (Step 4) that reads the private key from `.wallet.json`. No funds are transferred — it only proves wallet ownership via a detached signature.

---

## Step 2: Create a Cart

> **IMPORTANT — Use the correct marketplace TLD for the shipping country!**
> Product URLs MUST come from the Amazon or eBay store that matches the customer's shipping address country. Using the wrong TLD will result in failed orders, wrong pricing, or items that cannot ship.
> See the **Amazon TLD by Country** and **eBay TLD by Country** tables below for the full mappings.

SP3ND auto-detects whether a URL is Amazon or eBay and handles each accordingly. You can mix Amazon and eBay items in the same cart.

```http
POST /createPartnerCart
Content-Type: application/json
X-API-Key: <api_key>
X-API-Secret: <api_secret>

{
  "items": [
    {
      "product_id": "B08XYZ123",
      "product_title": "Example Product",
      "product_url": "https://amazon.com/dp/B08XYZ123",
      "quantity": 1,
      "price": 29.99
    }
  ]
}
```

**Example for a customer in Germany (Amazon):**

```json
{
  "items": [
    {
      "product_url": "https://amazon.de/dp/B08XYZ123",
      "quantity": 1
    }
  ]
}
```

**Example with an eBay item:**

```json
{
  "items": [
    {
      "product_url": "https://ebay.com/itm/123456789",
      "quantity": 1
    }
  ]
}
```

**Mixed cart (Amazon + eBay):**

```json
{
  "items": [
    { "product_url": "https://amazon.com/dp/B08XYZ123", "quantity": 1 },
    { "product_url": "https://ebay.com/itm/123456789", "quantity": 1 }
  ]
}
```

**Response:**

```json
{
  "success": true,
  "cart": {
    "cart_id": "cart_abc123",
    "items": [],
    "subtotal": 29.99,
    "shipping_amount": 5.99,
    "platform_fee": 0.00,
    "total_amount": 35.98
  }
}
```

> Carts expire after **30 minutes**. Create them close to order time.
> You can also use the simple format with just `product_url` + `quantity` — SP3ND will scrape the price and details automatically.

### eBay Shipping & Location

eBay shipping costs vary by destination. SP3ND uses the eBay Browse API with location-aware headers (`X-EBAY-C-SHIP-TO`, `X-EBAY-C-ENDUSERCTX`) to get accurate shipping quotes for the buyer's country and postal code.

**For the most accurate eBay shipping prices**, provide the shipping address when creating the order (Step 3). SP3ND will re-price eBay shipping when the destination postal code changes — if the quoted postal code doesn't match the order's shipping address, shipping is recalculated automatically.

> **Note:** Unlike Amazon (where Prime shipping is free), eBay items have per-item shipping costs set by the seller. The `shipping_amount` field in the cart/order response reflects the eBay seller's shipping charge to the buyer's location.

---

## Step 3: Create an Order

```http
POST /createPartnerOrder
Content-Type: application/json
X-API-Key: <api_key>
X-API-Secret: <api_secret>

{
  "cart_id": "cart_abc123",
  "customer_email": "customer@example.com",
  "shipping_address": {
    "name": "John Doe",
    "recipient": "John Doe",
    "address1": "123 Main St",
    "city": "San Francisco",
    "state": "CA",
    "postalCode": "94105",
    "zip": "94105",
    "country": "United States",
    "phone": "+14155551234"
  }
}
```

> **Required fields:** `customer_email` and `shipping_address.phone` are both mandatory.

**Response includes:** `order_id`, `order_number`, `total_amount`

---

## Step 4: Pay with x402 (Autonomous)

This is the key step. The x402 protocol handles payment automatically:

**First call (no payment header):**

```http
POST /payAgentOrder
Content-Type: application/json
X-API-Key: <api_key>
X-API-Secret: <api_secret>

{
  "order_id": "<order_id>",
  "order_number": "<order_number>"
}
```

**Response: HTTP 402 Payment Required**

The payment requirements are returned in **two places** (use either):
- The `PAYMENT-REQUIRED` HTTP header (base64-encoded JSON)
- The response body `paymentRequirements` field (same object, already decoded)

```json
{
  "x402Version": 2,
  "scheme": "exact",
  "network": "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",
  "accepts": [{
    "scheme": "exact",
    "network": "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",
    "maxAmountRequired": "30740000",
    "resource": "https://us-central1-sp3nddotshop-prod.cloudfunctions.net/payAgentOrder",
    "description": "SP3ND Order: ORD-1234567890",
    "mimeType": "application/json",
    "payTo": "2nkTRv3qxk7n2eYYjFAndReVXaV7sTF3Z9pNimvp5jcp",
    "maxTimeoutSeconds": 300,
    "asset": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "extra": {
      "name": "SP3ND Agent Payment",
      "order_id": "<order_id>",
      "order_number": "ORD-1234567890",
      "is_test": false,
      "feePayer": "2wKupLR9q6wXYppw8Gr2NvWxKBUqm4PPJKkQfoxHDBg4"
    }
  }]
}
```

The response body also includes convenience fields:

```json
{
  "status": "payment_required",
  "message": "Payment of $30.74 USDC required to complete order ORD-1234567890",
  "paymentRequirements": { /* same object as above */ },
  "amount": 30.74,
  "currency": "USDC",
  "pay_to": "2nkTRv3qxk7n2eYYjFAndReVXaV7sTF3Z9pNimvp5jcp",
  "network": "solana",
  "memo": "SP3ND Order: ORD-1234567890"
}
```

> **Important details:**
> - The 402 response uses **x402 v2** format with CAIP-2 network identifiers (`solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp`).
> - `extra.feePayer` is PayAI's facilitator wallet — it pays Solana gas fees, not your agent.
> - `extra.order_number` is used to build the required memo instruction.
> - `asset` is the USDC mint address as a flat string (not an object).
> - **When building the payment payload for the facilitator**, use **x402 v1** format (`x402Version: 1`, `network: "solana"` without CAIP-2). The facilitator receives `accepts[0]` directly — see the code example below.

> **Memo Requirement:** The USDC transfer transaction **must** include a Solana Memo program instruction with the value `SP3ND Order: <order_number>` (e.g. `SP3ND Order: ORD-1234567890`). SP3ND's Helius webhook uses this memo to match the on-chain payment to your order. Without it, USDC lands in the treasury but the order is never marked as paid. **Note:** The `x402-solana` library does **not** add this memo automatically — you must build the transaction manually with `createMemoInstruction`. See the code example below.

**Your agent must:**

1. Parse the payment requirements from the 402 response (either the `PAYMENT-REQUIRED` header or the body's `paymentRequirements` field)
2. Extract `accepts[0]` — this contains `payTo`, `maxAmountRequired`, `asset`, and `extra`
3. Build a **VersionedTransaction (v0)** with:
   - A USDC `createTransferCheckedInstruction` (6 decimals)
   - A `createMemoInstruction` with `SP3ND Order: <order_number>`
   - `feePayer` set to `accepts[0].extra.feePayer` (PayAI's wallet — **not** your agent)
4. Sign with your agent's keypair (`tx.sign([keypair])`)
5. Build an **x402 v1** payment payload and call the facilitator's `/verify` then `/settle` endpoints
6. Poll `GET /getPartnerOrders` until the order status is `Paid` (typically within 60 seconds)

**Payment confirmation:**

After the facilitator settles the transaction on-chain, SP3ND's Helius webhook detects the USDC transfer + memo and marks the order as paid. Your agent confirms by polling:

```http
GET /getPartnerOrders
X-API-Key: <api_key>
X-API-Secret: <api_secret>
```

Poll every ~5 seconds. When the order's `status` changes to `Paid`, you're done:

```json
{
  "order_number": "ORD-1234567890",
  "status": "Paid",
  "total_amount": 30.74,
  "transaction_signature": "5xYz...abc"
}
```

The order is now paid. SP3ND purchases the product from Amazon and ships it.

> **Why polling instead of a second `payAgentOrder` call?** The Helius webhook is the canonical source of truth — it matches the on-chain USDC transfer + memo to your order. Polling `getPartnerOrders` gives your agent definitive confirmation that the payment was recognized.

---

## Step 5: Track Order Status

```http
GET /getPartnerOrders?status=all
X-API-Key: <api_key>
X-API-Secret: <api_secret>
```

### Agent Health Check

```http
GET /getAgentStatus
X-API-Key: <api_key>
X-API-Secret: <api_secret>
```

Returns your agent's stats: orders, revenue, fee rate, etc.

---

## Fee Structure

| Agent Type | Platform Fee |
|---|---|
| Default agent | **0%** — no platform fee |
| Custom (set by admin) | Adjustable per-agent |

There are **no payment processing fees** — USDC transfers on Solana cost fractions of a cent in gas. Agents pay the product price + applicable tax + shipping only. **Amazon shipping is free on all Prime-eligible items** — SP3ND maintains Prime accounts in every supported Amazon marketplace, so your Amazon orders automatically get Prime shipping at no additional cost. Some surrounding regions served by a regional hub (e.g. Balkans via Germany, Pacific Islands via Australia) may not qualify for Prime delivery and could incur standard shipping fees. **eBay shipping** is set by individual sellers and varies by item and destination — the shipping cost is included in your cart/order total.

---

## Amazon TLD by Country (CRITICAL)

**You MUST use the correct Amazon domain for the customer's shipping country.** Using the wrong TLD will cause order failures, incorrect pricing, or undeliverable shipments.

| Country | Amazon TLD | Example URL |
|---|---|---|
| US United States | `amazon.com` | `https://amazon.com/dp/B08XYZ123` |
| GB United Kingdom | `amazon.co.uk` | `https://amazon.co.uk/dp/B08XYZ123` |
| CA Canada | `amazon.ca` | `https://amazon.ca/dp/B08XYZ123` |
| DE Germany | `amazon.de` | `https://amazon.de/dp/B08XYZ123` |
| FR France | `amazon.fr` | `https://amazon.fr/dp/B08XYZ123` |
| ES Spain | `amazon.es` | `https://amazon.es/dp/B08XYZ123` |
| IT Italy | `amazon.it` | `https://amazon.it/dp/B08XYZ123` |
| NL Netherlands | `amazon.nl` | `https://amazon.nl/dp/B08XYZ123` |
| BE Belgium | `amazon.com.be` | `https://amazon.com.be/dp/B08XYZ123` |
| PL Poland | `amazon.pl` | `https://amazon.pl/dp/B08XYZ123` |
| SE Sweden | `amazon.se` | `https://amazon.se/dp/B08XYZ123` |
| BR Brazil | `amazon.com.br` | `https://amazon.com.br/dp/B08XYZ123` |
| MX Mexico | `amazon.com.mx` | `https://amazon.com.mx/dp/B08XYZ123` |
| AU Australia | `amazon.com.au` | `https://amazon.com.au/dp/B08XYZ123` |
| IN India | `amazon.in` | `https://amazon.in/dp/B08XYZ123` |
| JP Japan | `amazon.co.jp` | `https://amazon.co.jp/dp/B08XYZ123` |
| SG Singapore | `amazon.sg` | `https://amazon.sg/dp/B08XYZ123` |
| AE UAE | `amazon.ae` | `https://amazon.ae/dp/B08XYZ123` |
| SA Saudi Arabia | `amazon.sa` | `https://amazon.sa/dp/B08XYZ123` |
| EG Egypt | `amazon.eg` | `https://amazon.eg/dp/B08XYZ123` |
| TR Turkey | `amazon.com.tr` | `https://amazon.com.tr/dp/B08XYZ123` |
| ZA South Africa | `amazon.co.za` | `https://amazon.co.za/dp/B08XYZ123` |
| IE Ireland | `amazon.co.uk` | Use UK Amazon (also available: `amazon.ie` but limited selection) |

### Regional Coverage — Which Amazon Store Serves Which Countries

Many Amazon stores serve entire regions. **Use the regional hub store** for countries that don't have their own dedicated Amazon TLD.

**DE Germany (`amazon.de`) covers:**
AT Austria, CH Switzerland, LI Liechtenstein, LU Luxembourg, Balkans (HR Croatia, SI Slovenia, BA Bosnia, RS Serbia, ME Montenegro, MK North Macedonia, AL Albania, XK Kosovo), Baltics (LT Lithuania, LV Latvia, EE Estonia), Central Europe (CZ Czech Republic, SK Slovakia, HU Hungary, RO Romania, BG Bulgaria)

**GB United Kingdom (`amazon.co.uk`) covers:**
IE Ireland (also has `amazon.ie` but UK has better selection/pricing), IS Iceland, Channel Islands, Isle of Man

**FR France (`amazon.fr`) covers:**
MC Monaco, BE Belgium (also has `amazon.com.be`), LU Luxembourg, French overseas territories (Martinique, Guadeloupe, Reunion, etc.), MA Morocco, TN Tunisia, SN Senegal and Francophone West Africa

**ES Spain (`amazon.es`) covers:**
PT Portugal, AD Andorra, GI Gibraltar

**IT Italy (`amazon.it`) covers:**
MT Malta, VA Vatican City, SM San Marino

**JP Japan (`amazon.co.jp`) covers:**
KR South Korea, TW Taiwan, HK Hong Kong, MO Macau, CN China (limited), MN Mongolia, PH Philippines (also served by `amazon.sg`)

**SG Singapore (`amazon.sg`) covers:**
MY Malaysia, TH Thailand, VN Vietnam, ID Indonesia, KH Cambodia, LA Laos, MM Myanmar, BN Brunei, PH Philippines (also served by `amazon.co.jp`)

**AE UAE (`amazon.ae`) covers:**
OM Oman, BH Bahrain, KW Kuwait, QA Qatar, JO Jordan, IQ Iraq, LB Lebanon

**SA Saudi Arabia (`amazon.sa`) covers:**
YE Yemen

**AU Australia (`amazon.com.au`) covers:**
NZ New Zealand, FJ Fiji, PG Papua New Guinea, Pacific Islands

**ZA South Africa (`amazon.co.za`) covers:**
NG Nigeria, KE Kenya, GH Ghana, TZ Tanzania, Most of Sub-Saharan Africa

**US United States (`amazon.com`) covers:**
PR Puerto Rico, US territories (Guam, USVI, etc.), CO Colombia, CL Chile, AR Argentina, PE Peru, EC Ecuador, VE Venezuela, Central America, Caribbean, **Fallback for any country not listed above** — `amazon.com` ships internationally to 200+ countries

**MX Mexico (`amazon.com.mx`) covers:**
GT Guatemala, HN Honduras, SV El Salvador, NI Nicaragua, CR Costa Rica, PA Panama (Can also use `amazon.com` for these countries)

**IN India (`amazon.in`) covers:**
LK Sri Lanka, NP Nepal, BD Bangladesh, BT Bhutan, MV Maldives

### How to Pick the Right TLD

1. **Does the shipping country have its own Amazon store?** -> Use that TLD
2. **Is it covered by a regional hub above?** -> Use the regional hub's TLD
3. **Not sure?** -> Use `amazon.com` (US) — it ships to 200+ countries

### How to Construct Amazon URLs

- Find the product's ASIN (the `B0xxxxxxxx` ID)
- Use the format: `https://{tld}/dp/{ASIN}`
- Example for France: `https://amazon.fr/dp/B08N5WRWNW`
- Example for Japan: `https://amazon.co.jp/dp/B08N5WRWNW`

---

## eBay TLD by Country

SP3ND supports **8 eBay marketplaces**. Use the correct eBay domain for the customer's shipping country.

| Country | eBay TLD | Example URL |
|---|---|---|
| US United States | `ebay.com` | `https://ebay.com/itm/123456789` |
| CA Canada | `ebay.ca` | `https://ebay.ca/itm/123456789` |
| GB United Kingdom | `ebay.co.uk` | `https://ebay.co.uk/itm/123456789` |
| DE Germany | `ebay.de` | `https://ebay.de/itm/123456789` |
| FR France | `ebay.fr` | `https://ebay.fr/itm/123456789` |
| IT Italy | `ebay.it` | `https://ebay.it/itm/123456789` |
| ES Spain | `ebay.es` | `https://ebay.es/itm/123456789` |
| AU Australia | `ebay.com.au` | `https://ebay.com.au/itm/123456789` |

### eBay Regional Coverage

| eBay Store | Delivers To |
|---|---|
| `ebay.com` (US) | United States, Puerto Rico, Canada, Mexico |
| `ebay.ca` (Canada) | Canada, United States |
| `ebay.co.uk` (UK) | United Kingdom, Ireland |
| `ebay.de` (Germany) | Germany, Austria, Netherlands, Belgium |
| `ebay.fr` (France) | France |
| `ebay.it` (Italy) | Italy |
| `ebay.es` (Spain) | Spain |
| `ebay.com.au` (Australia) | Australia |

> **eBay shipping is location-dependent.** Unlike Amazon where Prime shipping is free, eBay sellers set their own shipping rates which vary by destination. SP3ND queries eBay's Browse API with the buyer's country and postal code to get accurate shipping quotes. If the destination changes between cart creation and order creation, shipping is automatically recalculated.

### How to Construct eBay URLs

- Find the item's listing ID (numeric, e.g. `123456789`)
- Use the format: `https://{tld}/itm/{item_id}`
- Example for US: `https://ebay.com/itm/123456789`
- Example for UK: `https://ebay.co.uk/itm/123456789`

---

## Points & Potential Airdrop

Every order placed through SP3ND earns **SP3ND points**. These points are tracked per wallet and may qualify for a **future airdrop**. The more orders your agent places, the more points you accumulate. This applies to all agent orders — there's no separate opt-in required.

---

## Complete Code Example (Node.js)

> **Proven working on mainnet.** See `scripts/x402-pay-with-memo.mjs` for the full standalone script.

```javascript
// Install: npm install @solana/web3.js @solana/spl-token @solana/spl-memo
import {
  Connection, Keypair, PublicKey,
  TransactionMessage, VersionedTransaction, ComputeBudgetProgram
} from '@solana/web3.js';
import { getAssociatedTokenAddress, createTransferCheckedInstruction } from '@solana/spl-token';
import { createMemoInstruction } from '@solana/spl-memo';

const BASE_URL    = 'https://us-central1-sp3nddotshop-prod.cloudfunctions.net';
const FACILITATOR = 'https://facilitator.payai.network';
const USDC_MINT   = new PublicKey('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v');

// Your agent's credentials (from registerAgent)
const API_KEY    = process.env.SP3ND_API_KEY;
const API_SECRET = process.env.SP3ND_API_SECRET;

// Your agent's Solana keypair (must hold USDC)
const keypair = Keypair.fromSecretKey(
  Uint8Array.from(JSON.parse(process.env.SOLANA_PRIVATE_KEY))
);

const connection = new Connection(process.env.SOLANA_RPC_URL || 'https://api.mainnet-beta.solana.com');
const headers = { 'Content-Type': 'application/json', 'X-API-Key': API_KEY, 'X-API-Secret': API_SECRET };

async function buyFromAmazon(productUrl, quantity, customerEmail, shippingAddress) {
  // 1. Create cart
  const cartRes = await fetch(`${BASE_URL}/createPartnerCart`, {
    method: 'POST', headers,
    body: JSON.stringify({ items: [{ product_url: productUrl, quantity }] })
  });
  const cart = await cartRes.json();

  // 2. Create order
  const orderRes = await fetch(`${BASE_URL}/createPartnerOrder`, {
    method: 'POST', headers,
    body: JSON.stringify({
      cart_id: cart.cart.cart_id,
      customer_email: customerEmail,
      shipping_address: shippingAddress
    })
  });
  const order = (await orderRes.json()).order;

  // 3. First call to payAgentOrder — returns 402 with PAYMENT-REQUIRED header
  const firstRes = await fetch(`${BASE_URL}/payAgentOrder`, {
    method: 'POST', headers,
    body: JSON.stringify({ order_id: order.order_id, order_number: order.order_number })
  });

  if (firstRes.status !== 402) return await firstRes.json();

  // 4. Decode payment requirements from PAYMENT-REQUIRED header
  const paymentRequiredHeader = firstRes.headers.get('PAYMENT-REQUIRED');
  const paymentRequired = JSON.parse(Buffer.from(paymentRequiredHeader, 'base64').toString('utf8'));
  const req = paymentRequired.accepts[0];

  // 5. Build VersionedTransaction with USDC transfer + memo
  const payTo     = new PublicKey(req.payTo);
  const feePayer  = new PublicKey(req.extra.feePayer);  // PayAI pays gas — NOT your agent
  const amount    = BigInt(req.maxAmountRequired);
  const sourceATA = await getAssociatedTokenAddress(USDC_MINT, keypair.publicKey);
  const destATA   = await getAssociatedTokenAddress(USDC_MINT, payTo);
  const { blockhash } = await connection.getLatestBlockhash();

  const instructions = [
    ComputeBudgetProgram.setComputeUnitLimit({ units: 30000 }),
    ComputeBudgetProgram.setComputeUnitPrice({ microLamports: 1 }),
    createTransferCheckedInstruction(sourceATA, USDC_MINT, destATA, keypair.publicKey, amount, 6),
    createMemoInstruction(`SP3ND Order: ${req.extra.order_number}`),  // REQUIRED for payment matching
  ];

  const message = new TransactionMessage({ payerKey: feePayer, recentBlockhash: blockhash, instructions });
  const tx = new VersionedTransaction(message.compileToV0Message());
  tx.sign([keypair]);

  // 6. Build x402 v1 payment payload
  const base64Tx = Buffer.from(tx.serialize()).toString('base64');
  const v1Payload = {
    x402Version: 1, scheme: 'exact', network: 'solana',
    payload: { transaction: base64Tx }
  };
  const v1Req = {
    scheme: 'exact', network: 'solana',
    maxAmountRequired: req.maxAmountRequired,
    amount: req.maxAmountRequired,
    resource: req.resource,
    payTo: req.payTo,
    maxTimeoutSeconds: req.maxTimeoutSeconds,
    asset: req.asset,
    extra: req.extra,
  };

  // 7. Verify with facilitator
  const verifyRes = await fetch(`${FACILITATOR}/verify`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ paymentPayload: v1Payload, paymentRequirements: v1Req })
  });
  const verified = await verifyRes.json();
  if (!verified.isValid) throw new Error(`Verify failed: ${verified.invalidReason}`);

  // 8. Settle with facilitator (broadcasts tx to Solana)
  const settleRes = await fetch(`${FACILITATOR}/settle`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ paymentPayload: v1Payload, paymentRequirements: v1Req })
  });
  const settled = await settleRes.json();
  if (!settled.success) throw new Error(`Settle failed: ${settled.errorReason}`);

  // 9. Poll for payment confirmation (Helius webhook marks order paid within ~60s)
  const ORDER_TIMEOUT_MS = 90_000;
  const POLL_INTERVAL_MS = 5_000;
  const deadline = Date.now() + ORDER_TIMEOUT_MS;

  console.log('Waiting for payment confirmation...');
  while (Date.now() < deadline) {
    await new Promise(r => setTimeout(r, POLL_INTERVAL_MS));
    const statusRes = await fetch(`${BASE_URL}/getPartnerOrders`, { headers });
    const { orders } = await statusRes.json();
    const thisOrder = orders.find(o => o.order_number === order.order_number);
    if (thisOrder?.status === 'Paid') {
      console.log('Order paid! ✅', settled.transaction);
      return thisOrder;
    }
    console.log('  Status:', thisOrder?.status, '— checking again...');
  }
  throw new Error('Payment timeout — USDC transferred on-chain, Helius may still be processing');
}
```

---

## Key Facts for Agents

- **Registration:** Instant via `POST /registerAgent` — no approval queue
- **Platform fee:** 0% by default — agents pay no platform fee
- **Payment protocol:** x402 (HTTP 402 Payment Required) — fully autonomous
- **Payment currency:** USDC on Solana
- **Supported retailers:** Amazon (22 country TLDs) + eBay (8 country TLDs) — see tables above
- **CRITICAL:** Always use the marketplace TLD that matches the shipping country (e.g. `amazon.de` / `ebay.de` for Germany)
- **Free Prime shipping (Amazon):** Prime-eligible items ship free via SP3ND's Prime accounts (some surrounding regions may have standard shipping fees)
- **eBay shipping:** Per-item, set by seller, varies by destination — location-aware pricing via eBay Browse API
- **Key regeneration:** Lost your secret? Use `POST /regenerateAgentSecret` with a Solana wallet signature
- **Shipping:** 200+ countries
- **No KYC required**
- **Points & Airdrop:** Every order earns SP3ND points toward a potential future airdrop
- **Cart expiration:** 30 minutes
- **Treasury wallet:** `2nkTRv3qxk7n2eYYjFAndReVXaV7sTF3Z9pNimvp5jcp`
- **USDC mint (Solana mainnet):** `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`
- **x402 facilitator:** `https://facilitator.payai.network`
- **Support:** support@sp3nd.shop
- **Full API docs:** https://sp3nd.shop/partner-api/docs
- **Dashboard:** https://sp3nd.shop/partner-api/dashboard

---

## Alternative: Manual Payment Flow (for human partners)

If your agent cannot use x402, you can still use the manual payment flow:

1. Call `createPartnerTransaction` to register the payment intent
2. Manually send USDC to the treasury wallet with memo `SP3ND Order: <order_number>`
3. SP3ND detects the payment automatically within 1 minute

See the Partner API docs for details: https://sp3nd.shop/partner-api/docs
