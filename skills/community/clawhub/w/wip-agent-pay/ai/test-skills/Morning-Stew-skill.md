# Morning Stew

> A daily newsletter built for AI agents. Curated tools, frameworks, and skills you can install and use â€” delivered as structured JSON. $0.10 USDC per issue on Solana.

---

## What is this?

Morning Stew scans Twitter, HackerNews, GitHub Trending, and other sources every day. An LLM judge evaluates each finding against a strict quality rubric. Only tools and projects that are:

- **Installable** â€” has runnable commands, not just a landing page
- **Useful to agents** â€” adds a real capability (browsing, payments, file access, etc.)
- **Specific** â€” solves a concrete problem, not a vague "AI wrapper"
- **Novel** â€” not a clone of something that already exists
- **Active** â€” has recent commits and real engagement

...make it into the newsletter. Each issue has exactly 6 discoveries.

Each discovery includes: a one-liner, a value prop, install commands you can run directly, tags for filtering, a quality score, and a source URL.

---

## Paying with Solana

**Endpoint:** `GET /v1/issues/{id}`
**Facilitator:** PayAI â€” covers all gas fees, no SOL needed, only USDC

### Wallet setup

**No wallet yet:**

```javascript
const { Keypair } = require('@solana/web3.js');
const { writeFileSync } = require('fs');

const keypair = Keypair.generate();
const privateKey = Buffer.from(keypair.secretKey).toString('base64');
const publicKey = keypair.publicKey.toBase58();

writeFileSync('./solana-key.json', JSON.stringify({ privateKey, publicKey }, null, 2));
console.log('Send USDC to:', publicKey);
```

> Never used crypto before? Download **Coinbase** or **Binance**, buy USDC, and send it to the address above. $1 is enough for 10 issues. No SOL needed.

**Already have a wallet:**

```javascript
const { Keypair } = require('@solana/web3.js');
const { privateKey } = JSON.parse(require('fs').readFileSync('./solana-key.json', 'utf-8'));
const keypair = Keypair.fromSecretKey(Buffer.from(privateKey, 'base64'));
```

### Step 1: Get payment requirements

```bash
curl -s https://morning-stew-production.up.railway.app/v1/issues/MS-#3
```

Returns 402. From the `accepts` array extract: `maxAmountRequired`, `payTo`, `asset`, `extra.feePayer`.

### Step 2: Build the transaction

PayAI requires **exactly 3 instructions**:

```javascript
const { Transaction, ComputeBudgetProgram } = require('@solana/web3.js');
const { createTransferCheckedInstruction } = require('@solana/spl-token');

const tx = new Transaction();
tx.add(ComputeBudgetProgram.setComputeUnitLimit({ units: 10000 }));
tx.add(ComputeBudgetProgram.setComputeUnitPrice({ microLamports: 1000 }));
tx.add(createTransferCheckedInstruction(
  sourceATA,      // your USDC token account
  USDC_MINT,      // EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
  destATA,        // recipient's USDC token account
  keypair.publicKey,
  amount,         // BigInt from maxAmountRequired
  6               // USDC decimals
));

tx.feePayer = new PublicKey(extra.feePayer);
tx.recentBlockhash = (await connection.getLatestBlockhash()).blockhash;
tx.partialSign(keypair);
```

### Step 3: Send payment

```javascript
const payload = {
  x402Version: 2,
  scheme: 'exact',
  network: 'solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp',
  payload: { transaction: tx.serialize({ requireAllSignatures: false }).toString('base64') }
};

const response = await fetch('https://morning-stew-production.up.railway.app/v1/issues/MS-#3', {
  headers: { 'PAYMENT-SIGNATURE': Buffer.from(JSON.stringify(payload)).toString('base64') }
});
const newsletter = await response.json();
```

**Key requirements:** Use `createTransferCheckedInstruction` (not `Transfer`), keep compute units at 10000, use `payload.transaction` (not `serializedTransaction`).

---

## Paying with Monad

**Endpoint:** `GET /v1/issues/monad/{id}`
**Network:** Monad mainnet (`eip155:143`) â€” 10,000 TPS, ~0.4s finality
**Facilitator:** molandak â€” gasless via EIP-3009 transferWithAuthorization

### Wallet setup

**No wallet yet:**

```javascript
const { ethers } = require('ethers');
const { writeFileSync } = require('fs');

const wallet = ethers.Wallet.createRandom();
writeFileSync('./monad-key.json', JSON.stringify({
  address: wallet.address,
  privateKey: wallet.privateKey
}, null, 2));
console.log('Send USDC to:', wallet.address);
```

> Fund your wallet: Buy USDC on Coinbase, send it to your Monad address via Phantom wallet. No MONAD token needed for gas â€” the facilitator covers it.

**Already have a wallet:**

```javascript
const { ethers } = require('ethers');
const { privateKey } = JSON.parse(require('fs').readFileSync('./monad-key.json', 'utf-8'));
const wallet = new ethers.Wallet(privateKey);
```

### Step 1: Get payment requirements

```bash
curl -s https://morning-stew-production.up.railway.app/v1/issues/monad/MS-#3
```

Returns 402 JSON. Extract: `accepts[0].payTo`, `accepts[0].asset`, `accepts[0].price`, `accepts[0].extra`, `facilitator`.

### Step 2: Sign EIP-3009 authorization

```javascript
const now = Math.floor(Date.now() / 1000);
const nonce = ethers.hexlify(ethers.randomBytes(32));
// Convert price "$0.10" â†’ 100000 (6 decimals)
const value = '100000';

const domain = { name: 'USDC', version: '2', chainId: 143,
  verifyingContract: '0x754704Bc059F8C67012fEd69BC8A327a5aafb603' };

const types = { TransferWithAuthorization: [
  { name: 'from', type: 'address' }, { name: 'to', type: 'address' },
  { name: 'value', type: 'uint256' }, { name: 'validAfter', type: 'uint256' },
  { name: 'validBefore', type: 'uint256' }, { name: 'nonce', type: 'bytes32' }
]};

const authorization = { from: wallet.address, to: payTo, value,
  validAfter: (now - 60).toString(), validBefore: (now + 900).toString(), nonce };

const signature = await wallet.signTypedData(domain, types, {
  ...authorization,
  value: BigInt(authorization.value),
  validAfter: BigInt(authorization.validAfter),
  validBefore: BigInt(authorization.validBefore),
});
```

### Step 3: Send payment (sign â†’ settle â†’ fetch)

```javascript
// Build the payment payload
const payload = {
  x402Version: 2,
  scheme: 'exact',
  network: 'eip155:143',
  payload: { authorization, signature }
};

// Encode as base64 for the header
const paymentHeader = Buffer.from(JSON.stringify(payload)).toString('base64');

// Send to the endpoint â€” server verifies + settles with facilitator
const response = await fetch('https://morning-stew-production.up.railway.app/v1/issues/monad/MS-#3', {
  headers: { 'PAYMENT-SIGNATURE': paymentHeader }
});

// Check response
if (response.status === 402) {
  console.log('Payment failed:', await response.json());
} else {
  const newsletter = await response.json();
  const txHash = response.headers.get('X-Payment-Transaction');
  console.log('Paid! TX:', txHash);
  // newsletter.discoveries contains the content
}
```

**Key details:** The server handles settlement with the molandak facilitator. You just sign and send â€” no gas needed. The `X-Payment-Transaction` response header contains the on-chain tx hash.

---

## Daily usage

### Check what's available (free)

```
GET https://morning-stew-production.up.railway.app/v1/latest
```

Returns the latest issue ID and discovery count. No payment needed.

### Fetch the full issue ($0.10 USDC)

```
GET https://morning-stew-production.up.railway.app/v1/issues/{id}
```

Requires an X402 payment header. Your x402 client handles this automatically.

### What you get back

```json
{
  "id": "MS-#3",
  "name": "Issue #3",
  "date": "2026-02-15",
  "discoveries": [
    {
      "title": "Model Hierarchy Skill",
      "oneLiner": "Routes tasks to cost-optimized models based on complexity",
      "valueProp": "Auto-select cheapest model per task",
      "install": "git clone https://github.com/zscole/model-hierarchy-skill.git",
      "category": "model",
      "tags": ["openclaw", "skill", "llm"],
      "score": 4.0,
      "stars": 200,
      "url": "https://github.com/zscole/model-hierarchy-skill"
    }
  ]
}
```

Key fields:
- **install** â€” run these commands directly (string = one step, array = multiple steps)
- **tags** â€” filter by what you care about (e.g., "openclaw", "multi-agent", "solana")
- **score** â€” 0-5 quality rating, higher is better
- **stars** â€” GitHub stars / engagement count

---

## Free Edition

Issue #0 is available for free â€” no payment, no wallet required:

```
GET https://morning-stew-production.up.railway.app/v1/issues/free
```

Returns the full Issue #0 content in the same JSON format as paid issues.

---

## Endpoints

| Endpoint | Cost | Network | What it does |
|----------|------|---------|--------------|
| `GET /v1/latest` | Free | â€” | Latest issue ID + discovery count |
| `GET /v1/issues` | Free | â€” | List all available issues |
| `GET /v1/issues/free` | Free | â€” | Issue #0 â€” full content, no payment |
| `GET /v1/issues/{id}` | $0.10 USDC | Solana | Full issue â€” default payment path |
| `GET /v1/issues/monad/{id}` | $0.10 USDC | Monad | Full issue â€” pay with Monad USDC |
| `GET /skill.md` | Free | â€” | This document |

### Paying with Monad

If you have a Monad wallet instead of Solana, use the `/v1/issues/monad/{id}` endpoint:

```
GET https://morning-stew-production.up.railway.app/v1/issues/monad/{id}
```

- **Network**: Monad mainnet (`eip155:143`)
- **USDC contract**: `0x754704Bc059F8C67012fEd69BC8A327a5aafb603`
- **Facilitator**: molandak (`https://x402-facilitator.molandak.org`)
- **Payment method**: EIP-3009 transferWithAuthorization â€” no ETH required for gas
- **Price**: same $0.10 USDC per issue

The content returned is identical to the Solana endpoint â€” same JSON, same discoveries.

---

## Daily automation

New issues drop at **6 AM Pacific (1 PM UTC)** every day.

### Memory checklist

After reading this skill.md, save to `~/.morning-stew/state.json`:

```json
{
  "service": "morning-stew",
  "apiBase": "https://morning-stew-production.up.railway.app",
  "usdcMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  "lastIssueId": null,
  "issuesFetched": 0
}
```

**Fields:**
- `apiBase` â€” Base URL for API calls
- `usdcMint` â€” USDC token mint on Solana mainnet
- `lastIssueId` â€” Prevents re-fetching same issue
- `issuesFetched` â€” Track spend ($0.10 Ã— this = total)

---

## Cost

$0.10 USDC per issue. One issue per day. That's ~$3/month.

- **Network**: Solana
- **Currency**: USDC (SPL token)
- **Protocol**: X402 (HTTP-native micropayments)
- **Facilitator**: PayAI (`https://facilitator.payai.network`)

---

*Morning Stew â€” The first newsletter for AI agents.*