---
name: synaptic-mcp-paywall
description: Generate and consume native HTTP 402 ("Payment Required") API paywalls on SynapticChain for machine-to-machine micropayments.
version: 1.0.0
author: Synaptics-Lab
---

# ⚡ SynapticChain HTTP 402 Paywall Skill for OpenClaw

This skill equips OpenClaw agents to monetize their own API endpoints or consume external paid APIs using sub-500ms on-chain micro-settlements ($0.0008) on SynapticChain Layer-1.

---

## 🚀 Quick Setup & Usage

### 1. Generating an HTTP 402 Paywalled Webhook (Express/Axum):
```javascript
// Sample Express Middleware for SynapticChain HTTP 402 Paywall
app.use('/api/premium', async (req, res, next) => {
  const txHash = req.headers['x-synaptic-tx'];
  if (!txHash) {
    return res.status(402).json({
      error: "Payment Required",
      recipient: "syn1l8agc8qzgqqqu60jtatlhmh93a8my6xvm9ml0f",
      price_sUSD: "0.0008",
      network: "SynapticChain L1"
    });
  }
  // Verify tx on-chain in <500ms via SynapticChain RPC
  next();
});
```

### 2. Auto-Settling HTTP 402 Challenges:
Agents equipped with this skill automatically sign and dispatch micro-settlement transactions across their 256 parallel lanes without blocking other workflows.

- **RPC Endpoint:** `https://nodes.synapticchain.xyz/rpc`
- **Gateway:** `https://api.synapticchain.xyz`
- **Community:** `https://t.me/synapse402`
