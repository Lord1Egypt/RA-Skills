---
name: wei-devils-advocate
version: 1.0.0
description: Stress-test ideas using multiple LLMs in adversarial roles to generate counterarguments, cross-check reasoning, and expose hidden risks and failure modes. 易找茬：通过多模型对抗式分析与交叉验证，从不同视角生成反对意见并揭示潜在风险。
execution:
  timeout: 600
  longRunning: true
env:
  OPENROUTER_API_KEY:
    description: API key for OpenRouter (only required if models in config.json use OpenRouter)
    required: false
  DASHSCOPE_API_KEY:
    description: API key for DashScope/Bailian (only required if models in config.json use DashScope)
    required: false
---

# Wei Devil's Advocate Skill

**Version:** 1.0.0 | **Last updated:** 2026-04-07

---

## Overview

Use **wei-devils-advocate** to stress-test ideas through multi-LLM adversarial cross-validation.

Multiple language models independently act as devil’s advocates, challenging the idea from different reasoning paths to uncover hidden risks, assumptions, and failure modes that a single model may miss.

It is best suited for:

Identifying hidden assumptions through cross-model disagreement
Exposing risks, edge cases, and failure scenarios
Detecting overconfident or internally consistent but fragile reasoning
Validating decisions under adversarial multi-perspective review

Do NOT use this skill if you are looking for validation, consensus， quick agreement, brainstorming, or single-perspective answers.

---

## Installation

### Prerequisites

- [Bun](https://bun.sh) runtime (v1.0.0 or higher)

### Install Bun

```bash
curl -fsSL https://bun.sh/install | bash
```

Or on macOS with Homebrew:

```bash
brew install oven-sh/bun/bun
```

### Install Dependencies

```bash
cd skills/wei-devils-advocate
bun install
```

### Environment Setup

Create a `.env` file in the skill directory with your API keys:

```bash
# Required: OpenRouter API key (for debater models)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Required: DashScope/Bailian API key (for judge model)
DASHSCOPE_API_KEY=your_dashscope_api_key_here
```

Or export as environment variables:

```bash
export OPENROUTER_API_KEY=your_openrouter_api_key_here
export DASHSCOPE_API_KEY=your_dashscope_api_key_here
```

> **Note:** If environment variables are not set, the skill will throw an error with instructions on how to configure them.

---

### Configuration Files

> **遇到模型访问问题？** 请参考 `README.md` 了解如何根据你的网络环境选择和配置 `config.json`。

## Core Philosophy

Most bad decisions don’t fail because of lack of information.

They fail because:
- Assumptions go unchallenged
- Risks are underestimated
- Everyone agrees too quickly

This skill enforces:

> “Default to skepticism. Earn confidence.”

---

## How It Works

User Input (Thesis / Idea)
        ↓
[Debater Models x N]  → Generate strongest counterarguments
        ↓
(Optional) [Simulation Models] → Attempt to rebut critiques multiple rounds until...
        ↓
[Judge Model] → Evaluates survivability
        ↓
Structured Decision Output

---

## Modes

| Mode | Behavior | Use When |
|------|--------|---------|
| attack (default) | Generate counterarguments + judge evaluation | Fast stress test |

> **Note:** Currently only the `attack` mode is implemented. Future versions include the `simulation` mode for simulating whether an idea survives sustained attack. Preview the 'simulation' mode at https://www.bigbigai.com/agent/devils-advocate .

---

## Use Cases

- Product & Startup validation
- Investment / trading risk analysis
- Strategy stress testing
- System / prompt failure analysis

---

## Cost Note

Uses multiple models (2–4x cost vs single query). Use for high-stakes decisions only.

---

## Model Roles

Each model in `config.json` is tagged with one or more **roles** indicating its capabilities:

| Role | Description | Typical Use |
|------|-------------|-------------|
| `critic` | Strong critical thinking and counterargument generation | Challenging assumptions |
| `reasoning` | Deep analytical capability | Complex analysis, synthesis |
| `retrieval` | Has web/live data access | Current events, real-time info |
| `judge` | Evaluates survivability of ideas | Final evaluation |
| `general` | Broad balanced capability | Fallback, ambiguous queries |

> **Note:** Specific model names and their roles are defined in `config.json` → `models`. Refer to that file for the current model roster.

---

## Model Selection

Model selection is controlled via `config.json` using a **queryType-based routing** system. Instead of hard-coding model names, you select models by the domain of the query.

### How to Select Models

As the calling model, follow this process:

1. **Classify the query** — Match keywords to determine the `queryType`
2. **Pass `queryType`** — The skill will look up the `routing.xxx.models` in `config.json`
3. **(Optional) Pass explicit models** — Use the `models` parameter to bypass auto-selection

### Query Types (Domain)

| queryType | Description | Typical Use |
|----------|------------|-------------|
| financial | Markets, investing, macroeconomics | Investment thesis validation, risk analysis |
| technical | Programming, systems, engineering | Architecture decisions, implementation risks |
| social | Public opinion, social media sentiment | Product-market fit, user behavior |
| current_events | Recent news and real-time information | Time-sensitive decisions |
| scientific | Objective knowledge, definitions, theories | Research validity, methodology critique |
| creative | Writing, design, ideation | Creative concept stress testing |
| general | Default fallback | General idea validation |

### Selection Algorithm

```
1. Analyze query → match keywords → determine queryType
2. Pass queryType to skill → skill looks up `routing.<queryType>.models` in config.json
3. Skill selects top 2–3 models from the routing config
4. Debater models generate counterarguments
5. Judge model evaluates survivability
```

### Examples

#### Example 1: Financial Query

Query: "Should we invest in AI startups in 2026?"

Selection process:
1. **Keywords**: invest, startups, 2026 → queryType: `financial`
2. **Pass to skill**: `{ "query": "...", "queryType": "financial" }`
3. **Skill looks up**: `config.json` → `routing.financial.models`
4. **Skill selects**: Models configured for financial analysis
5. **Judge**: Evaluates investment thesis survivability

#### Example 2: Technical Query

Query: "Is microservices architecture the right choice for our startup?"

Selection process:
1. **Keywords**: microservices, architecture → queryType: `technical`
2. **Pass to skill**: `{ "query": "...", "queryType": "technical" }`
3. **Skill looks up**: `config.json` → `routing.technical.models`
4. **Skill selects**: Models with technical/coding roles

#### Example 3: Product Validation

Query: "Will users pay for this productivity app?"

Selection process:
1. **Keywords**: users, pay, app → queryType: `social`
2. **Pass to skill**: `{ "query": "...", "queryType": "social" }`
3. **Skill looks up**: `config.json` → `routing.social.models`
4. **Skill selects**: Models with social/retrieval roles

---

## Skill Parameters

- query (string)
- queryType (string)
- intent (string)
- mode (string)
- models (array)
- maxModels (number)
- judgeModel (string)

---

## Output Structure

1. Thesis
2. Hidden Assumptions
3. Counterarguments
4. Failure Scenarios
5. Survivability
6. Verdict
7. Recommendation

---

## Tagline

Strong ideas survive attack. Weak ones don’t.
