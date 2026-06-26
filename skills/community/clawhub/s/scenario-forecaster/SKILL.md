---
name: Scenario Forecaster
description: "AI-driven event forecasting skill. Collects multi-source data, cross-validates facts, maps future scenarios with probabilities, and delivers actionable recommendations for investors, managers, and policymakers."
---

# Scenario Forecaster

> Stop guessing. Start forecasting. Let AI systematically map every possible future path and give you a tailored action checklist.

---

## Core Capabilities

| Feature | Description |
|---------|-------------|
| **Multi-source data** | News, academic papers, social media sentiment, government reports |
| **Cross-validation** | Verify facts across 2+ independent sources with confidence ratings |
| **PESTEL analysis** | Structured driver identification across 6 dimensions |
| **Scenario mapping** | Generate 3-5 logically self-consistent future paths |
| **Probability assessment** | Bayesian-informed probability estimates per scenario |
| **Role-based recommendations** | Tailored do/don't lists for investors, managers, policymakers |

---

## Execution Protocol

1. **Collect** - Gather information from 5 source types
2. **Validate** - Cross-check facts, rate confidence
3. **Analyze** - Identify drivers using PESTEL framework
4. **Map scenarios** - Build paths with triggers and milestones
5. **Assess probability** - Assign Bayesian-informed estimates
6. **Recommend** - Generate role-specific action checklists

---

## Input Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| event_description | string | required | Event or topic to forecast |
| time_horizon | string | 6 months | Forecast period |
| focus_dimensions | list | Economic, Political, Technological | PESTEL dimensions |
| num_paths | int | 3 | Number of scenario paths (3-5) |

---

## Quick Start

```text
Forecast: Impact of Fed rate cuts over 6 months on global tech stocks.
Focus: Economic and Technological dimensions.
```

Full example in `examples/output_fed_rate.md`.
