---
name: sector-returns-vs-sp500
description: Use when the user wants to compare sector or asset returns and volatility against the S&P 500, or analyze historical market trends from public financial data. Calls the Powerdrill Finance Data Agent through Finch.
license: MIT
---

# Powerdrill Finance Data Agent on Finch

**What it does (official description):** Turn financial data into clear, data-driven insights. Ask a question in plain language. Finance Data Agent retrieves relevant public financial data, performs the statistical analysis, and delivers a structured report to help you understand market performance, compare assets, and explore historical trends. From comparing sector returns and volatility against the S&P 500 to analyzing market movements over time, get the numbers and analysis you need — without having to do the data work yourself.

**Price:** 1.5 USDC per run. 10 free runs per account for a limited time (current end date on each agent page).

## How to use

1. Ask the user for the comparison or question in plain language.
2. If the Finch MCP server is connected (`https://www.finchtech.ai/mcp`), search the catalog for "Powerdrill Finance Data Agent" and create a task with the user's input. Only use free runs unless the user explicitly approves a paid run.
3. If it is not connected, give the user this link to run it in the browser (new users create an account with a passkey or a wallet): https://www.finchtech.ai/market/chips/agent-c2c55754-a942-508f-a362-d576724809f7/run?utm_source=skill&utm_medium=agent&utm_campaign=toa_skills&utm_content=sector-returns-vs-sp500
   To connect the MCP server instead, follow https://github.com/a0971025732-netizen/finch-agents/blob/main/CONNECT.md

## Rules

- Never create or switch wallets, and never ask for a private key or seed phrase.

