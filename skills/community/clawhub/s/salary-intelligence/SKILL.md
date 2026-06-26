---
name: salary-intelligence
description: EU salary data, AI job displacement risk, Latvia wage statistics — 30+ countries, NACE/ISCO classification
user-invocable: true
metadata: {"openclaw":{"requires":{"env":[]}},"homepage":"https://sputnikx.xyz","author":"SputnikX","version":"1.0.0","tags":["salary","wages","ai-risk","labor","eurostat"]}
---

# Salary Intelligence

EU salary database with AI job displacement risk indicators. 30+ countries, NACE sector and ISCO occupation classification. Cross-referenced with trade data for economic analysis.

## Base URL

`https://sputnikx.xyz/api/v1/agent`

## Key Endpoints

### Salary Overview ($0.10 x402)
```bash
curl "https://sputnikx.xyz/api/v1/agent/salary/overview"
```
Returns: Database metadata, country coverage, available metrics.

### AI Job Displacement Risk ($0.10 x402)
```bash
curl "https://sputnikx.xyz/api/v1/agent/salary/ai-risk?nace=C&country=DE"
```
Returns: OECD AI exposure indicators by sector and occupation.

### Latvia Detailed Wages ($0.10 x402)
```bash
curl "https://sputnikx.xyz/api/v1/agent/salary/lv-wages?sector=manufacturing"
```
Returns: CSP (Central Statistical Bureau) granular wage data by sector and occupation.

## MCP Server
```
Endpoint: https://mcp.sputnikx.xyz/mcp
Tools: salary_overview, salary_ai_risk, salary_lv_wages
```

## Data Sources
- Eurostat: earn_mw_cur, lc_lci_r2_q, nama_10_a64, lfsa_egais, earn_ses_annual
- CSP Latvia: PxWeb detailed wages
- OECD: AI Exposure indicators

## When to use this skill
- Research salary levels across EU countries by sector
- Assess AI job displacement risk for specific occupations
- Analyze Latvia wage trends in detail
- Cross-reference salary data with trade flows for economic modeling
