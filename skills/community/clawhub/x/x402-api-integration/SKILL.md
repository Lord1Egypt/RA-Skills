---
name: x402-api-integration
description: Turn any function into a revenue-generating API endpoint using x402 HTTP-native payments — zero dependencies, Node 16 stdlib only.
metadata:
  openclaw:
    emoji: 💰
    homepage: https://tinycoderstudio.gumroad.com/l/7-agent-skills-pack
---
# Skill 5: x402 API Integration — Build Pay-Per-Call Services

## Overview
Turn any function into a revenue-generating API endpoint using x402 (HTTP-native payments). Zero dependencies, Node 16 stdlib only.

## Problem
Monetizing APIs requires Stripe, auth, billing, invoicing — complex overhead for simple services.

## Solution
x402 protocol: Client pays USDC per call via HTTP headers. No accounts, no subscriptions, no invoicing.

## Core Server (Node 16, Zero Deps)

```javascript
// x402-server.js — 250 lines, pure Node 16 stdlib
const http = require('http');
const https = require('https');
const crypto = require('crypto');
const url = require('url');

const PORT = process.env.PORT || 3000;
const NETWORK = 'base';
const PRICE_USD = '0.001';
const PAY_TO = '0xYourWalletAddress';

// Build x402 payment requirements
function buildPaymentRequirements(path, method, price = PRICE_USD, description) {
  return {
    x402Version: 1,
    accepts: [{
      scheme: 'exact',
      network: NETWORK,
      maxAmountRequired: price,
      resource: `https://your-api.com${path}`,
      description: description || `Service — $${price} USDC per call`,
      mimeType: 'application/json',
      payTo: PAY_TO,
      extra: { name: 'USDC', icon: 'https://raw.githubusercontent.com/messari/token-icons/master/raw-USDC.svg' }
    }]
  };
}

function encodePaymentHeader(obj) {
  return Buffer.from(JSON.stringify(obj)).toString('base64');
}

function decodePaymentHeader(str) {
  try { return JSON.parse(Buffer.from(str, 'base64').toString()); } catch { return null; }
}

function getPaymentHeader(req) {
  return req.headers['payment-signature'] || req.headers['x-payment'];
}

function checkPayment(req, res, path, method, price, description) {
  const paymentHeader = getPaymentHeader(req);
  if (!paymentHeader) {
    const reqs = buildPaymentRequirements(path, method, price);
    sendJSON(res, 402, { error: 'Payment required', paymentRequired: reqs }, {
      'X-PAYMENT-REQUIRED': encodePaymentHeader(reqs)
    });
    return null;
  }
  const payload = decodePaymentHeader(paymentHeader);
  if (!payload) { sendJSON(res, 400, { error: 'Invalid payment header' }); return null; }
  // Demo mode: accept any valid-looking payment
  // TODO: Enable facilitator verification in production
  return true;
}

function sendJSON(res, status, obj, headers = {}) {
  const body = JSON.stringify(obj);
  res.writeHead(status, { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body), ...headers });
  res.end(body);
}

// Your service function
function yourService(input) {
  // Your logic here
  return { result: `Processed: ${input}` };
}

// Route handler
const routes = {
  'POST /api/your-service': async (req, res) => {
    const payment = checkPayment(req, res, '/api/your-service', 'POST', '0.001', 'Your service — $0.001/call');
    if (!payment) return;
    
    try {
      const body = JSON.parse(req._rawBody || '{}');
      const result = yourService(body.input);
      sendJSON(res, 200, result);
    } catch (err) {
      sendJSON(res, 500, { error: 'Internal error' });
    }
  }
};

// Server
const server = http.createServer(async (req, res) => {
  // ... CORS, rate limiting, routing (see full server.js)
});

server.listen(PORT, () => console.log(`🔮 API running on port ${PORT}`));
```

## Deploy in 3 Commands

```bash
# 1. Save as server.js
# 2. Run
nohup node server.js > server.log 2>&1 &

# 3. Expose via Cloudflare Tunnel (free)
cloudflared tunnel --url http://localhost:3000
# Returns: https://random-words.trycloudflare.com
```

## Add Your Service

```javascript
// Replace yourService with anything:
function securityScan(code) { /* scan logic */ return findings; }
function humanizeText(text) { /* replace AI phrases */ return humanized; }
function analyzeContent(text) { /* stats, sentiment */ return insights; }
function generateImage(prompt) { /* call image API */ return url; }
function scrapeSite(url) { /* browser automation */ return data; }
```

## Pricing Examples

| Service | Price | Use Case |
|---------|-------|----------|
| Task routing | $0.001 | Agent orchestration |
| Text humanize | $0.005 | Content cleanup |
| Security scan | $0.01 | Code review |
| Content analyze | $0.003 | SEO, sentiment |
| Image gen | $0.05 | Thumbnails, assets |
| Web scrape | $0.02 | Data extraction |

## Enable Real Payments (Production)

```javascript
// In checkPayment(), replace demo mode with:
async function verifyPayment(payload, requirements) {
  const body = JSON.stringify({ paymentPayload: payload, paymentRequirements: requirements });
  const res = await fetch('https://x402.org/facilitator/verify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body
  });
  const result = await res.json();
  return result.valid === true;
}

// Then in checkPayment:
const valid = await verifyPayment(payload, requirements);
if (!valid) { sendJSON(res, 402, { error: 'Payment verification failed' }); return null; }
```

## Deploy Options

| Platform | Cost | Best For |
|----------|------|----------|
| Cloudflare Tunnel | Free | Dev, testing, low traffic |
| Railway | $5/mo | Production, auto-deploy |
| Fly.io | ~$5/mo | Global, containers |
| VPS + Nginx | $5-10/mo | Full control |

## Value
- **Setup**: 10 minutes from zero to live
- **Cost**: $0 infrastructure (Cloudflare Tunnel free)
- **Revenue**: Immediate, per-call, no minimums
- **Scale**: Handles 1000s req/min on $5 VPS
- **Ownership**: Your wallet, your code, your rules