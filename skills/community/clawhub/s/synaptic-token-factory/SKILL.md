---
name: synaptic-token-factory
description: Deploy, mint, and trade autonomous SRC-20 tokens on SynapticChain Layer-1 in a single command.
version: 1.0.0
author: Synaptics-Lab
---

# 🪙 SynapticChain SRC-20 Token Factory Skill for OpenClaw

This skill enables OpenClaw agents to permissionlessly create, deploy, and initialize custom SRC-20 tokens on SynapticChain with deterministic static gas scheduling.

---

## 🚀 Quick Token Creation

```bash
# Deploy a custom token for your agent swarm
synlang deploy-token --name "AgentCoin" --symbol "BOT" --supply 1000000 --decimals 18
```

- **Standards:** SRC-20 compliant with `transfer`, `balanceOf`, `approve`, and `transferFrom`.
- **Concurrency:** Fully integrated with 256-lane parallel execution.
- **RPC:** `https://nodes.synapticchain.xyz/rpc`
- **Explorer:** `https://explorer.synapticchain.xyz`
- **Telegram:** `https://t.me/synapse402`
