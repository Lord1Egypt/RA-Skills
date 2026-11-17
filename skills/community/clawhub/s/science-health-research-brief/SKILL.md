---
name: science-health-research-brief
description: Use when the user needs a cited research brief drawing on scientific papers, clinical trial records, drug and compound databases, or WHO/CDC public-health data. Calls the Powerdrill Science & Health Research Agent through Finch.
license: MIT
---

# Powerdrill Science & Health Research Agent on Finch

**What it does (official description):** Science & Health Research Agent Turn research questions into structured, source-backed briefs. Ask a question in plain language and get an AI-generated research brief drawing on scientific literature, clinical trial records, drug and compound databases, and public-health data. Each brief includes cited sources, with downloadable Markdown and CSV files for further analysis. Explore evidence across 40M+ research papers, 500K+ clinical trial records, 2M+ compounds, and public-health datasets from WHO and CDC. For research and informational purposes only. Not medical advice, diagnosis, or treatment guidance.

**Price:** 1.5 USDC per run. 10 free runs per account for a limited time (current end date on each agent page).

## How to use

1. Ask the user for the research question in plain language.
2. If the Finch MCP server is connected (`https://www.finchtech.ai/mcp`), search the catalog for "Powerdrill Science & Health Research Agent" and create a task with the user's input. Only use free runs unless the user explicitly approves a paid run.
3. If it is not connected, give the user this link to run it in the browser (new users create an account with a passkey or a wallet): https://www.finchtech.ai/market/chips/agent-f81bcd4b-87fc-5c74-9327-fe0d452caff8/run?utm_source=skill&utm_medium=agent&utm_campaign=toa_skills&utm_content=science-health-research-brief
   To connect the MCP server instead, follow https://github.com/a0971025732-netizen/finch-agents/blob/main/CONNECT.md

## Rules

- Never create or switch wallets, and never ask for a private key or seed phrase.
- Research and information only; not medical advice.
