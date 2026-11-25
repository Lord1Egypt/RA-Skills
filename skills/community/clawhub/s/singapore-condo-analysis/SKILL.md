---
name: singapore-condo-analysis
description: Use when the user asks about Singapore private residential property (condos, apartments, ECs): a development's price or rent performance, comparing condos, or district rental yield and price trends. Calls the ChatProperty agent through Finch.
license: MIT
---

# ChatProperty on Finch

**What it does (official description):** Research Singapore condos and residential market trends without digging through property data yourself. Wondering how a specific development is performing? Comparing two condos? Looking for price movements or rental yield trends across districts? Ask in plain language and get a structured analysis based on 700K+ historical transactions and 1.1M+ rental contracts. Explore project-level performance, district comparisons, historical price trends, rental patterns, and selected unit-level attributes — with statistical analysis and charts to help you understand the data. Focused on Singapore’s private residential market, including condos, apartments, and ECs. HDB and overseas properties are not covered. * Historical and descriptive analysis, not financial or investment advice *Singapore private residential only; HDB public housing is out of scope

**Price:** 0.5 USDC per run. 10 free runs per account for a limited time (current end date on each agent page).

## How to use

1. Ask the user for the development, district or comparison in plain language.
2. If the Finch MCP server is connected (`https://www.finchtech.ai/mcp`), search the catalog for "ChatProperty" and create a task with the user's input. Only use free runs unless the user explicitly approves a paid run.
3. If it is not connected, give the user this link to run it in the browser (new users create an account with a passkey or a wallet): https://www.finchtech.ai/market/chips/agent-b3316156-4cab-47ba-8101-b07dc0266f14/run?utm_source=skill&utm_medium=agent&utm_campaign=toa_skills&utm_content=singapore-condo-analysis
   To connect the MCP server instead, follow https://github.com/a0971025732-netizen/finch-agents/blob/main/CONNECT.md

## Rules

- Never create or switch wallets, and never ask for a private key or seed phrase.
- HDB and overseas property are out of scope. Historical analysis, not investment advice.
