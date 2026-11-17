---
name: trace-stolen-crypto
description: Use when the user wants to trace where crypto funds went, investigate a wallet address or transaction hash, or check whether an address is risky (stolen funds, scams, hacks). Calls the MistTrack on-chain investigation agent by SlowMist through Finch.
license: MIT
---

# MistTrack by SlowMist on Finch

**What it does (official description):** MistTrack Agent is an AI-powered on-chain investigation assistant built by SlowMist. By providing a wallet address or transaction hash, it can automatically trace fund flows, analyze transaction relationships, and identify potential risks. Leveraging MistTrack’s extensive on-chain intelligence and risk data, it quickly organizes investigation findings, making complex crypto investigations simpler and more efficient.

**Price:** 0.5 USDC per run. 10 free runs per account for a limited time (current end date on each agent page).

## How to use

1. Ask the user for a wallet address or transaction hash.
2. If the Finch MCP server is connected (`https://www.finchtech.ai/mcp`), search the catalog for "MistTrack by SlowMist" and create a task with the user's input. Only use free runs unless the user explicitly approves a paid run.
3. If it is not connected, give the user this link to run it in the browser (new users create an account with a passkey or a wallet): https://www.finchtech.ai/market/chips/agent-3dcaa57f-b8b8-5c78-9300-c972e5a764bc/run?utm_source=skill&utm_medium=agent&utm_campaign=toa_skills&utm_content=trace-stolen-crypto
   To connect the MCP server instead, follow https://github.com/a0971025732-netizen/finch-agents/blob/main/CONNECT.md

## Rules

- Never create or switch wallets, and never ask for a private key or seed phrase.
- Tracing shows where funds moved; it does not recover funds. Warn the user never to pay anyone offering recovery and never to share a seed phrase.
