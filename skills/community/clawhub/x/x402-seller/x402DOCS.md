# x402 for Agent Sellers: Your Guide to Monetization

This is your reference guide for implementing x402 payment collection on your services and APIs. Use this to understand the protocol, set up payment endpoints, and monetize the work you perform.

---

## Table of Contents

1. [What is x402?](#what-is-x402)
2. [Why Use x402 for Agents](#why-use-x402-for-agents)
3. [Core Concepts](#core-concepts)
   - [Payment Flow](#payment-flow)
   - [Roles: Seller vs Buyer vs Facilitator](#roles-seller-vs-buyer-vs-facilitator)
   - [HTTP 402 Status Code](#http-402-status-code)
4. [Payment Schemes](#payment-schemes)
5. [Setting Up an x402 Server](#setting-up-an-x402-server)
   - [Python with FastAPI](#python-with-fastapi)
   - [Python with Flask](#python-with-flask)
   - [Go with Gin](#go-with-gin)
   - [TypeScript with Express](#typescript-with-express)
6. [Facilitators and Networks](#facilitators-and-networks)
7. [Best Practices for Agent Sellers](#best-practices-for-agent-sellers)

---

## What is x402?

x402 is an open payment protocol that enables you to collect instant, programmatic payments in stablecoins (primarily USDC) directly over HTTP. It uses the HTTP 402 Payment Required status code to charge for access without requiring:

- User accounts or authentication systems
- Manual payment processing
- Traditional payment intermediaries
- State management on your end

### Key Features for You

- **Direct On-Chain Settlement:** Your payments settle on-chain (Base, Polygon, Arbitrum, World, Solana)
- **Stablecoin Payments:** Accept USDC, EURC, or other ERC-20/SPL tokens
- **Built for Agent-to-Agent Commerce:** Other agents can pay you programmatically with no human intervention
- **Stateless:** No sessions, cookies, or user management needed
- **Permissionless:** Buyers can access your services without your approval
- **Gas Sponsorship:** The facilitator pays gas fees, not you or the buyer

---

## Why You Should Use x402

When you implement x402:

1. **You Don't Manage Blockchain:** No wallet keys, no node operations—the facilitator handles verification and settlement for you
2. **Fast Monetization:** Add payment requirements to any HTTP endpoint in under 10 lines of code
3. **Cheap Micropayments:** Charge per call, computation, or result with fees of only $0.001/tx after your free 1,000 monthly transactions
4. **Verified & Trustless:** Payments are cryptographically verified on-chain—no risk of chargebacks or fraud
5. **Built for Your Peers:** Other agents can discover and pay you automatically; x402 is designed for agent-to-agent commerce
6. **Flexible Revenue Models:** Change prices, payment schemes, and billing models on the fly without redeploying

---

## Core Concepts

### Payment Flow

Here's how payment flows through the system:

```
1. Buyer requests your protected resource
   GET /api/service HTTP/1.1
   
2. You respond with 402 + your payment requirements
   HTTP/1.1 402 Payment Required
   PAYMENT-REQUIRED: scheme=exact;price=$0.001;payTo=0x...;network=eip155:8453
   
3. Buyer constructs payment and retries
   GET /api/service HTTP/1.1
   PAYMENT-SIGNATURE: <signed_payment_payload>
   
4. You verify with facilitator
   POST https://facilitator/verify
   
5. You settle payment via facilitator
   POST https://facilitator/settle
   
6. You deliver your resource
   HTTP/1.1 200 OK
   PAYMENT-RESPONSE: <settlement_details>
   <response_body>
```

**Critical:** You never handle buyer funds directly. The facilitator:
- Validates the payment signature
- Executes the transaction on-chain
- Escrows funds until confirmation
- Returns proof to you

### Your Role vs Buyer vs Facilitator

**Your Role (Agent Seller)**
- You define your protected endpoints and their prices
- You send 402 responses with payment requirements
- You verify incoming payments (through the facilitator)
- You settle payments (through the facilitator)
- You deliver your resource once payment confirms

**The Buyer**
- Makes HTTP requests to your endpoints
- Receives your 402 + payment requirements
- Signs payment authorization with their wallet
- Retries the request with signed proof
- Receives your resource and settlement confirmation

**The Facilitator (e.g., Coinbase Developer Platform)**
- Takes your verification requests
- Validates payment signatures and schemes
- Submits transactions on-chain
- Monitors confirmation
- Returns results to you
- Charges fees after free tier (1,000 tx/month free, then $0.001/tx)

### HTTP 402 Status Code

HTTP 402 Payment Required is your primary signal. When a buyer requests your protected resource without payment:

```http
HTTP/1.1 402 Payment Required
Content-Type: application/json
PAYMENT-REQUIRED: scheme=exact;price=$0.001;payTo=0x1234...;network=eip155:8453

{
  "error": "payment_required",
  "message": "Access to this resource requires payment",
  "requires_payment": {
    "scheme": "exact",
    "price": "$0.001",
    "currency": "USDC",
    "network": "eip155:8453",
    "payTo": "0x1234...",
    "description": "API call to data processing service"
  }
}
```

The `PAYMENT-REQUIRED` header gives the buyer everything they need to pay you.

---

## Payment Schemes

Choose from three payment models depending on what you're selling:

### 1. Exact (Fixed Price)

**When to Use This:** API calls, data queries, pre-computed results

**How It Works:**
- You declare a fixed price (e.g., $0.001)
- Buyer authorizes exactly that amount
- They're charged precisely what you declared
- Works on all networks (EVM, Solana)

**Example:**
```python
routes: dict[str, RouteConfig] = {
    "GET /api/query": RouteConfig(
        accepts=[
            PaymentOption(
                scheme="exact",
                pay_to=pay_to,
                price="$0.001",
                network="eip155:84532",
            ),
        ],
        description="Query the database",
    ),
}
```

### 2. Upto (Usage-Based Billing)

**When to Use This:** LLM inference, variable compute, data processing

**How It Works:**
- You declare a maximum price (e.g., $0.10)
- Buyer authorizes the maximum
- You measure actual usage (tokens, compute time, bytes served)
- You charge only what was actually consumed
- Buyer never pays more than their authorized maximum
- EVM networks only

**Example:**
```python
routes: dict[str, RouteConfig] = {
    "POST /api/generate": RouteConfig(
        accepts=[
            PaymentOption(
                scheme="upto",
                pay_to=pay_to,
                price="$0.10",  # Maximum
                network="eip155:84532",
            ),
        ],
        description="LLM text generation billed by tokens",
    ),
}

# In handler:
@app.post("/api/generate")
async def generate(response: Response):
    result = llm_generate(prompt)
    actual_cost = compute_token_cost(result.tokens)
    
    set_settlement_overrides(response, {"amount": str(actual_cost_atomic)})
    return {"result": result.text, "tokens": result.tokens}
```

### 3. Batch Settlement (Payment Channels)

**When to Use This:** High-volume sessions, streaming APIs, rapid requests

**How It Works:**
- Buyer opens an on-chain payment channel with a deposit
- Each subsequent request is a signed off-chain voucher (no on-chain tx per request)
- Your ChannelManager collects vouchers
- Single on-chain settlement batches them at session end
- Gas costs spread across many requests, reducing per-request fees
- EVM networks only

---

## Setting Up Your x402 Server

Pick your framework and language below. All examples use the CDP facilitator, which is production-ready.

### Python with FastAPI

**Installation:**
```bash
pip install "x402[fastapi]"
```

**Minimal Server:**
```python
from typing import Any
from fastapi import FastAPI
from x402.http import FacilitatorConfig, HTTPFacilitatorClient, PaymentOption
from x402.http.middleware.fastapi import PaymentMiddlewareASGI
from x402.http.types import RouteConfig
from x402.mechanisms.evm.exact import ExactEvmServerScheme
from x402.server import x402ResourceServer

app = FastAPI()

# Your receiving wallet address (where payments are sent)
PAY_TO = "0xYourWalletAddress"

# Create facilitator client (testnet)
facilitator = HTTPFacilitatorClient(
    FacilitatorConfig(url="https://x402.org/facilitator")
)

# Create x402 resource server
server = x402ResourceServer(facilitator)
server.register("eip155:84532", ExactEvmServerScheme())  # Base Sepolia

# Define protected routes
routes: dict[str, RouteConfig] = {
    "GET /api/data": RouteConfig(
        accepts=[
            PaymentOption(
                scheme="exact",
                pay_to=PAY_TO,
                price="$0.001",
                network="eip155:84532",
            ),
        ],
        mime_type="application/json",
        description="Fetch premium data",
    ),
    "POST /api/compute": RouteConfig(
        accepts=[
            PaymentOption(
                scheme="exact",
                pay_to=PAY_TO,
                price="$0.005",
                network="eip155:84532",
            ),
        ],
        mime_type="application/json",
        description="Run computation",
    ),
}

# Add payment middleware
app.add_middleware(PaymentMiddlewareASGI, routes=routes, server=server)


@app.get("/api/data")
async def get_data() -> dict[str, Any]:
    return {"data": "valuable information", "timestamp": "2024-01-01T00:00:00Z"}


@app.post("/api/compute")
async def compute_result(prompt: str) -> dict[str, Any]:
    result = perform_computation(prompt)
    return {"result": result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**To Receive Real Payments (mainnet):**
Update your facilitator configuration:
```python
facilitator = HTTPFacilitatorClient(
    FacilitatorConfig(
        url="https://api.cdp.coinbase.com/platform/v2/x402",
        headers={"Authorization": f"Bearer {os.getenv('CDP_API_KEY')}"}
    )
)
server.register("eip155:8453", ExactEvmServerScheme())  # Base mainnet
```

### Python with Flask

**Installation:**
```bash
pip install "x402[flask]"
```

**Minimal Server:**
```python
from flask import Flask, jsonify
from x402.http import FacilitatorConfig, HTTPFacilitatorClientSync, PaymentOption
from x402.http.middleware.flask import payment_middleware
from x402.http.types import RouteConfig
from x402.mechanisms.evm.exact import ExactEvmServerScheme
from x402.server import x402ResourceServerSync

app = Flask(__name__)

PAY_TO = "0xYourWalletAddress"

facilitator = HTTPFacilitatorClientSync(
    FacilitatorConfig(url="https://x402.org/facilitator")
)

server = x402ResourceServerSync(facilitator)
server.register("eip155:84532", ExactEvmServerScheme())

routes: dict[str, RouteConfig] = {
    "GET /api/data": RouteConfig(
        accepts=[
            PaymentOption(
                scheme="exact",
                pay_to=PAY_TO,
                price="$0.001",
                network="eip155:84532",
            ),
        ],
        mime_type="application/json",
        description="Fetch premium data",
    ),
}

payment_middleware(app, routes=routes, server=server)


@app.route("/api/data")
def get_data():
    return jsonify({"data": "valuable information"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

### Go with Gin

**Installation:**
```bash
go get github.com/x402-foundation/x402/go
```

**Minimal Server:**
```go
package main

import (
    "net/http"
    "time"

    x402 "github.com/x402-foundation/x402/go"
    x402http "github.com/x402-foundation/x402/go/http"
    ginmw "github.com/x402-foundation/x402/go/http/gin"
    evm "github.com/x402-foundation/x402/go/mechanisms/evm/exact/server"
    "github.com/gin-gonic/gin"
)

func main() {
    PAY_TO := "0xYourWalletAddress"
    network := x402.Network("eip155:84532") // Base Sepolia

    r := gin.Default()

    // Create facilitator client
    facilitatorClient := x402http.NewHTTPFacilitatorClient(&x402http.FacilitatorConfig{
        URL: "https://x402.org/facilitator",
    })

    // Apply x402 payment middleware
    r.Use(ginmw.X402Payment(ginmw.Config{
        Routes: x402http.RoutesConfig{
            "GET /api/data": {
                Accepts: x402http.PaymentOptions{
                    {
                        Scheme:      "exact",
                        PayTo:       PAY_TO,
                        Price:       "$0.001",
                        Network:     network,
                        Description: "Fetch premium data",
                    },
                },
                MimeType: "application/json",
            },
        },
        Facilitator: facilitatorClient,
        Schemes: []ginmw.SchemeConfig{
            {Network: network, Server: evm.NewExactEvmScheme()},
        },
        Initialize: true,
        Timeout:    30 * time.Second,
    }))

    // Protected endpoint
    r.GET("/api/data", func(c *gin.Context) {
        c.JSON(http.StatusOK, gin.H{
            "data":      "valuable information",
            "timestamp": "2024-01-01T00:00:00Z",
        })
    })

    r.Run(":8000")
}
```

### TypeScript with Express

**Installation:**
```bash
npm install @coinbase/cdp-sdk @x402/express @x402/core @x402/evm dotenv
```

**Minimal Server:**
```typescript
import "dotenv/config";
import express from "express";
import { createX402Server } from "@coinbase/cdp-sdk/x402";
import { paymentMiddlewareFromHTTPServer } from "@x402/express";

const app = express();

// Reads CDP_API_KEY_ID, CDP_API_KEY_SECRET, CDP_WALLET_SECRET from env
// Automatically provisions a receiver wallet and wires CDP facilitator
const server = await createX402Server({
  environment: "development", // testnet; omit or use "production" for mainnet
  routes: {
    "GET /api/data": {
      price: "$0.001",
      description: "Fetch premium data",
    },
    "POST /api/compute": {
      price: "$0.005",
      description: "Run computation",
    },
  },
});

// Apply payment middleware
app.use(paymentMiddlewareFromHTTPServer(server));

// Protected endpoints
app.get("/api/data", (req, res) => {
  res.json({ data: "valuable information" });
});

app.post("/api/compute", (req, res) => {
  res.json({ result: "computation result" });
});

app.listen(8000, () => {
  console.log(`Server listening at http://localhost:8000`);
  console.log(`Receiving EVM payments at ${server.payToEvmAddress}`);
});
```

---

## Your Facilitator Options

### CDP-Hosted Facilitator (Use This for Production)

**URL:** `https://api.cdp.coinbase.com/platform/v2/x402`

**Networks You Can Use:**
- Base (mainnet & Sepolia testnet)
- Polygon
- Arbitrum
- World (mainnet & Sepolia testnet)
- Solana (mainnet & Devnet)

**Your Costs:**
- Free: First 1,000 transactions per month
- Paid: $0.001 per transaction over 1,000/month

**Setup:**
You need CDP API keys:
```
CDP_API_KEY_ID
CDP_API_KEY_SECRET
```

**Why Choose This:**
- Gas fees paid by facilitator (not you or buyers)
- Compliance screening built-in
- Works across all networks with one account
- Production support with guarantees

### x402.org Facilitator (Testing Only)

**URL:** `https://x402.org/facilitator`

**Networks Available:**
- Base Sepolia (testnet)
- Solana Devnet

**Advantages:**
- No signup required
- Free, no fees
- Perfect for testing

**Limitations:**
- Testnet only—not for real payments
- No guarantees

### Moving from Testing to Production

When you're ready to accept real payments, update your configuration:

**Python:**
```python
# Your testnet setup
facilitator = HTTPFacilitatorClient(
    FacilitatorConfig(url="https://x402.org/facilitator")
)

# Switch to production
facilitator = HTTPFacilitatorClient(
    FacilitatorConfig(
        url="https://api.cdp.coinbase.com/platform/v2/x402",
        headers={"Authorization": f"Bearer {os.getenv('CDP_API_KEY')}"}
    )
)
```

**TypeScript (with CDP SDK):**
```typescript
const server = await createX402Server({
  environment: "production",  // Switches to Base mainnet
  routes: {...}
});
```

**Go:**
```go
facilitatorClient := x402http.NewHTTPFacilitatorClient(&x402http.FacilitatorConfig{
    URL: "https://api.cdp.coinbase.com/platform/v2/x402",
    Headers: map[string]string{
        "Authorization": fmt.Sprintf("Bearer %s", os.Getenv("CDP_API_KEY")),
    },
})
```

### Network Identifiers (CAIP-2 Format)

Use these identifiers when configuring your server:

- Base mainnet: `eip155:8453`
- Base Sepolia: `eip155:84532`
- Polygon: `eip155:137`
- Arbitrum: `eip155:42161`
- World: `eip155:480`
- World Sepolia: `eip155:4801`
- Solana mainnet: `solana:5eykt4UsFv2P6ysqq27A3FKk1CLy`
- Solana Devnet: `solana:EtWTRABZaYq6iMfeYKUxV6PGrQpAB8zMTwSDF9zBZort`

---

## Your Best Practices

### 1. Design Your Routes

Structure your endpoints clearly:
```
GET /api/v1/data/:type          # Query data by type
POST /api/v1/analyze            # Submit analysis request
GET /api/v1/results/:id         # Retrieve results
```

For variable-cost endpoints, use wildcards:
```
GET /api/*                      # Catch-all with single pricing
```

Keep free and paid endpoints separate:
```
GET /api/public/health          # Free (unprotected)
GET /api/paid/premium-data      # Paid (protected)
```

### 2. Price Your Services

**For Exact Pricing:**
- Base price on computational cost
- Remember: facilitator costs $0.001 after free tier
- Examples: $0.001 for queries, $0.01 for LLM calls, $0.05 for complex work

**For Usage-Based (Upto):**
- Set max price above expected cost
- Measure actual usage (tokens, time, bytes served)
- Always charge the lower of: actual usage or max authorized
- Example: Buyer authorizes $0.10, you charge $0.03 for 100 tokens

### 3. Handle Errors Correctly

Give buyers clear feedback:

```python
@app.get("/api/data")
async def get_data():
    try:
        result = process_data()
        return result
    except ValueError as e:
        # Transparently report errors—they paid, you deliver
        return {"error": str(e)}, 400
```

### 4. Test on Testnet First

Before you go live:
- Use Base Sepolia or Solana Devnet
- Fund your wallet via [CDP Faucet](https://portal.cdp.coinbase.com)
- Test all routes end-to-end
- Verify facilitator responses

### 5. Monitor Your Revenue

- Log all payment requests and settlements
- Track facilitator latency
- Alert on failed payments
- Identify patterns in your revenue

### 6. Accept Payments on Multiple Networks

Let buyers choose their network:

```python
server.register("eip155:84532", ExactEvmServerScheme())  # Base Sepolia
server.register("eip155:137", ExactEvmServerScheme())    # Polygon
server.register("solana:EtWTRA...", ExactSvmServerScheme())  # Solana
```

Buyers automatically select their preferred network.

### 7. Publish Yourself (Bazaar Discovery)

Let other agents find your services:

```python
routes: dict[str, RouteConfig] = {
    "GET /api/data": RouteConfig(
        accepts=[...],
        description="Query blockchain data",  # Bazaar indexes this
        mime_type="application/json",
    ),
}
```

Buyers discover you:
```
GET https://api.cdp.coinbase.com/platform/v2/x402/discovery/search?query=data
```

### 8. Your Mainnet Launch Checklist

Before going live with real payments:
- [ ] Switch to CDP facilitator URL
- [ ] Update networks to mainnet (e.g., `eip155:8453` for Base)
- [ ] Price your services realistically
- [ ] Test thoroughly with CDP credentials
- [ ] Monitor settlement confirmations
- [ ] Plan your rollback strategy
- [ ] Enable logging and alerting
- [ ] Register on Bazaar so others find you

---

## Summary

With x402, you can:
1. Respond with HTTP 402 + your payment requirements
2. Let the facilitator verify and settle automatically
3. Receive on-chain payment with near-zero overhead
4. Choose from fixed-price, usage-based, or batched billing

**The bottom line:** In under 10 lines of code, you can monetize any HTTP endpoint with full blockchain settlement, no account setup, and zero friction between you and your buyers.

