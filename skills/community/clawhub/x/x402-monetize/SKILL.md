---
name: x402-monetize
version: 1.0.15
description: |
  Creates paid API endpoints using the x402 micropayment protocol. Wraps existing
  Zo skills and tools behind per-request payment walls. Each call costs $0.001–$0.10,
  settled on-chain. No crypto custody risk — the x402 facilitator handles payment.
compatibility: Zo Computer, Node.js, @x402/core, @x402/express
metadata:
  author: ssyopros.zo.computer
  category: monetization
  tags: x402, micropayments, paid-api, passive-# x402-monetize

Create paid API endpoints that earn micropayments every time they're called.

## What This Does

1. Wrap any Python script or Zo tool as an HTTP API endpoint
2. Add x402 payment middleware (client pays per-call via USDC on Base)
3. Register the endpoint as a Zo user service on port 4020
4. The endpoint runs 24/7 and deposits earnings 
```bash
cd /home/workspace/MoneyMachine/x402_server
node index.js
```

## Endpoints Included

| Endpoint | Price | Description |
|---|---|---|
| `/api/signals/:ticker` | $0.01 | Options trading signal (bull/bear/neutral) |
| `/api/whale/:ticker` | $0.01 | Whale flow alert (size, direction, conviction) |
| `/api/wave/:ticker` | $0.01 | Elliott Wave count + Fibonacci levels |
| `/api/maxpain/:ticker` | $0.005 | Max pain level + strike wall zones |
| `/api/backtest` | $0.05 | Run options strategy backtest |
| `/api/services` | free | List all paid endpoints |

## Adding a New Paid Endpoint

```javascript
const { paymentMiddleware } = require('@x402/express');

// Add to index.js:
app.get('/api/my-endpoint', paymentMiddleware(), async (req, res) => {
  // Your logic here
  res.json({ result: 'paid data', price: '$0.01' });
});
```

## Payment Flow

1. Client requests `/api/signals/AAPL`
2. Server returns `402 Payment Required` with payment details
3. Client pays USDC to facilitator
4. Client retries with payment proof
5. Server returns data

## Docs

- https://docs.x402.org/getting-started/quickstart-for-sellers
