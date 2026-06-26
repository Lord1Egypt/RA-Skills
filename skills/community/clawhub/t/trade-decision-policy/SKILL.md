---
name: trade-decision-policy
description: Use when stock research, valuation, portfolio analytics, and risk outputs must be converted into structured Vietnam equity recommendation labels, target weights, invalidation rules, and approval-gated action drafts.
metadata: {"openclaw":{"emoji":"balance"}}
disable-model-invocation: false
---

# Trade Decision Policy

## Purpose

Use this skill as the final decision-policy layer for Vietnam equity recommendations. It converts upstream evidence into structured `BUY`, `ADD`, `HOLD`, `TRIM`, or `EXIT` labels and portfolio action drafts.

## Scope

- Vietnam listed equities.
- Portfolio action drafts.
- Target weights and maximum weights.
- Confidence, invalidation, and data-gap disclosure.
- User approval requirement before target-state mutation.

## Non-goals

- Do not place broker orders.
- Do not call broker APIs.
- Do not execute trades.
- Do not treat an approved target portfolio state as an executable order.
- Do not update approved target portfolio state without explicit user approval.

## Input Contract

Required inputs:

- `ticker`
- `exchange`
- `research_summary`
- `valuation_view`
- `earnings_quality_view`
- `portfolio_risk_view`
- `current_weight_pct`
- `risk_budget`
- `compliance_context`

Optional inputs:

- `liquidity_view`
- `macro_view`
- `news_view`
- `backtest_view`
- `data_gaps`

## Decision Labels

- `BUY`: initiate a new position when evidence is strong, valuation is attractive, risk budget allows it, and liquidity is acceptable.
- `ADD`: increase an existing position when the thesis remains valid and target weight remains within risk limits.
- `HOLD`: keep target weight unchanged when evidence is balanced or action is not justified.
- `TRIM`: reduce target weight when risk, valuation, concentration, or thesis quality has weakened.
- `EXIT`: reduce target weight to zero when the thesis is invalidated or compliance/risk constraints require removal.

## Required Output

Return a structured object with:

- `ticker`
- `exchange`
- `decision_label`
- `current_weight_pct`
- `target_weight_pct`
- `max_weight_pct`
- `confidence`
- `reason`
- `invalidation_condition`
- `risk_check_status`
- `compliance_check_status`
- `data_gaps`
- `requires_user_confirmation`
- `broker_execution_allowed`

`requires_user_confirmation` must be `true`.

`broker_execution_allowed` must be `false` unless a separate future execution policy explicitly enables broker integration.

## Guardrails

- Separate facts, assumptions, and inference.
- Cap confidence at `Medium` when critical financial statements, liquidity data, or portfolio weights are missing.
- Return `HOLD` when evidence is insufficient for an active change.
- Return `TRIM` or `EXIT` only with explicit risk, valuation, compliance, or thesis-invalidation reasoning.
- Never imply that a recommendation is a real order.
- Never mutate D1 approved target state directly; return an action draft for approval-gated governance processing.
