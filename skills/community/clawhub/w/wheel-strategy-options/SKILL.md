---
name: wheel-strategy-options
description: Use when the user wants to sell cash-secured puts or covered calls on a US stock (wheel strategy) and needs a short-dated (3 to 9 day) screen with an OPEN or SKIP decision. Calls the Wheel-strategy Option Desk agent through Finch.
license: MIT
---

# Wheel-strategy Option Desk (Morgan Dashan) on Finch

**What it does (official description):** Wheel Strategy Option Desk is an AI-powered trading assistant for short-term options strategies on US stocks. It helps traders identify potential opportunities to sell cash-secured puts or covered calls. Simply enter a stock ticker and the cash you have set aside for puts, or your shares and cost basis for covered calls. The Agent analyzes live options prices, market volatility, broader market trends, and upcoming events. It screens options expiring in 3 to 9 days, offering conservative and standard strategy candidates. It also checks earnings announcements, Fed rate decisions, key economic data, and market news for potential risks. Each ticker receives a clear OPEN or SKIP decision, helping traders evaluate short-term options opportunities with a more structured, risk-aware approach.

**Price:** 0.01 USDC per run. 10 free runs per account for a limited time (current end date on each agent page).

## How to use

1. Ask the user for the ticker plus cash set aside for puts, or shares and cost basis for covered calls.
2. If the Finch MCP server is connected (`https://www.finchtech.ai/mcp`), search the catalog for "Wheel-strategy Option Desk (Morgan Dashan)" and create a task with the user's input. Only use free runs unless the user explicitly approves a paid run.
3. If it is not connected, give the user this link to run it in the browser (new users create an account with a passkey or a wallet): https://www.finchtech.ai/market/chips/agent-f7c9c94a-961b-4159-a6ba-6b7852e84264/run?utm_source=skill&utm_medium=agent&utm_campaign=toa_skills&utm_content=wheel-strategy-options
   To connect the MCP server instead, follow https://github.com/a0971025732-netizen/finch-agents/blob/main/CONNECT.md

## Rules

- Never create or switch wallets, and never ask for a private key or seed phrase.
- Trading assistant, not investment advice.
