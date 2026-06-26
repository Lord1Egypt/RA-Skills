---
name: Decision Economic Optimizer
description: Deterministic decision-ranking API with HTTP 402 payments and outcome credits.
version: 0.1.0
homepage: https://which-llm.com
credentials_required: true
primary_credential: WALLET_CREDENTIALS
sensitivity: high
always_on: false
disable_model_invocation: false
install_mechanism: instruction_only
writes_to_disk_on_install: false
downloads_code_on_install: false
---

# Which‑LLM: Outcome‑Driven Decision Optimizer

## Overview

Use this skill when you need a deterministic recommendation for which LLM to use under explicit constraints such as cost and quality.

This skill is for calling the Which‑LLM API. It does not run an LLM itself. For paid requests, the AI bot needs access to a crypto wallet.

## When to use it

- Pick the cheapest model that still meets a quality target
- Choose a fallback model if the preferred one fails
- Keep model selection deterministic and auditable
- Report execution results and earn credits for later requests

## Quick Reference

- **API base URL:** `https://api.which-llm.com`
- **Primary paid endpoint:** `POST /decision/optimize`
- **Outcome endpoint:** `POST /decision/outcome`
- **Free discovery endpoints:** `GET /capabilities`, `GET /pricing`, `GET /status`
- **Payment asset:** `USDC`
- **Supported chains:** Base, Ethereum, Arbitrum, Optimism, Avalanche

## Registry Summary Expectations

- `Primary credential`: `WALLET_CREDENTIALS`
- `Install mechanism`: instruction-only
- `Writes to disk on install`: `false`
- `Downloads code on install`: `false`

## Prerequisites

Before using this skill, have the following ready:

- Ability to make HTTPS requests to `https://api.which-llm.com`
- Ability to send and receive JSON
- AI bot access to a crypto wallet for paid requests

## What this skill does

- Sends requests to the Which‑LLM API
- Uses `POST /decision/optimize` to get a recommended model and fallback plan
- Uses `POST /decision/outcome` to report real execution results
- Explains the request and response shapes for the public API
- Describes how to retry requests after payment has been satisfied externally

## What this skill does not do

- It does not call an LLM directly
- It does not execute arbitrary code from your prompt
- It does not require unrelated files or system access beyond API usage and payment handling

## Runtime Scope

- `always_on: false`: the skill is not force-installed and does not run continuously
- `disable_model_invocation: false`: an agent may invoke it on demand
- The skill is limited to outbound HTTP API usage and response handling
- For paid requests, the AI bot needs access to a crypto wallet

## Payment Model

Paid calls may use HTTP `402 Payment Required`.

High-level flow:

1. Call `POST /decision/optimize`
2. If the API returns `402`, inspect fields such as `required_amount`, `accepts`, and `payment_reference`
3. Satisfy the payment requirement outside this skill using host- or client-managed infrastructure
4. Retry the same request with payment proof headers if available

This skill documents the API behavior and payment-related response handling. The wallet requirement is limited to paid requests.

## Endpoints

### `GET /capabilities`

Use this to discover supported constraints, decision types, and payment behavior.

### `GET /pricing`

Use this to check current pricing and supported chains before making a paid request.

### `GET /status`

Use this for service-health checks.

### `POST /decision/optimize`

This is the main endpoint. Send the goal and constraints, then receive:

- `recommended_model`
- `fallback_plan`
- decision metadata and explainability fields

Typical request shape:

```json
{
  "goal": "Summarize customer feedback emails into a 5-bullet executive summary",
  "constraints": {
    "min_quality_score": 0.8,
    "max_cost_usd": 0.01
  },
  "workload": {
    "input_tokens": 1200,
    "output_tokens": 300,
    "requests": 1
  },
  "task_type": "summarize"
}
```

If payment is required, the API may first return `402` with fields such as:

- `required_amount`
- `currency`
- `accepts[].chain`
- `accepts[].pay_to`
- `payment_reference`

Retry the request after external payment handling with:

- `X-Payment-Chain`
- `X-Payment-Tx`
- `X-Payer`
- `X-Payment-Amount`
- `X-Payment-Asset`

If you have a valid credit token, also send:

- `X-Credit-Token`

### `POST /decision/outcome`

Use this after running the recommended model. Report what actually happened so the system can issue a credit token for future use.

Typical request shape:

```json
{
  "decision_id": "d4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f90",
  "option_used": "openai/gpt-4o-mini",
  "actual_cost": 0.008,
  "actual_latency": 650,
  "quality_score": 0.86,
  "success": true
}
```

Typical response includes:

- `status`
- `decision_id`
- `outcome_hash`
- `refund_credit.credit_token`

## Request Strategy For Agents

- Call `GET /capabilities` or `GET /pricing` first if you need to discover current payment behavior
- Use `POST /decision/optimize` only when you actually need model selection help
- Reuse the returned decision data rather than repeatedly asking the same question
- After running the chosen model, call `POST /decision/outcome` to earn credits
- Use the host or client payment flow when a paid request requires wallet-backed settlement

## Troubleshooting

### `PAYMENT_REQUIRED`

The endpoint needs payment first. Read the `402` response, satisfy the payment requirement externally, then retry with payment proof headers if available.

### `PAYMENT_INVALID`

Check:

- exact amount sent
- correct chain
- correct recipient
- confirmed transaction
- headers match the actual transaction

### `NO_FEASIBLE_OPTIONS`

Your cost and quality constraints are too strict for the available models. Relax the budget or quality threshold and retry.

### `RATE_LIMIT_EXCEEDED`

Back off and retry later. Use an idempotency key for safe retries.
