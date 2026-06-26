---
name: wei-cross-research
version: 1.0.4
description: Cross-validate research answers by querying multiple LLMs in parallel with judge-based synthesis. Reduces hallucination and surfaces model disagreements for high-stakes questions. 交叉研究：多模型并行查询与裁判合成，通过交叉验证降低幻觉、暴露分歧，适用于高 stakes 决策。
execution:
  timeout: 600
  longRunning: true
env:
  OPENROUTER_API_KEY:
    description: API key for OpenRouter. You can modify config.json to use other providers (bailian, openai_compliant) instead.
    required: true
  DASHSCOPE_API_KEY:
    description: API key for DashScope/Bailian (only required if models in config.json use DashScope)
    required: false
metadata:
  {
    "openclaw": {
      "emoji": "🔍",
      "homepage": "https://github.com/MikeHanKK/wei-skills/tree/main/skills/wei-cross-research",
      "requires": {
        "bins": ["bun"],
        "env": ["OPENROUTER_API_KEY"],
      },
      "primaryEnv": "OPENROUTER_API_KEY",
      "install": [
        {
          "id": "brew",
          "kind": "brew",
          "formula": "oven-sh/bun/bun",
          "bins": ["bun"],
          "label": "Install Bun (brew)",
          "os": ["darwin", "linux"]
        },
        {
          "id": "powershell",
          "kind": "download",
          "url": "https://bun.sh/install.ps1",
          "bins": ["bun"],
          "label": "Install Bun (PowerShell)",
          "os": ["win32"]
        },
        {
          "id": "npm",
          "kind": "node",
          "package": "bun",
          "bins": ["bun"],
          "label": "Install Bun (npm)"
        }
      ]
    }
  }
---

# Wei Cross Research Skill

## Overview

Use **wei-cross-research** when you need a reliable answer — not just one model's opinion.

This skill queries multiple LLMs in parallel and uses a judge model to synthesize 
their responses into a single cross-validated answer. When models agree, confidence 
is high. When they disagree, the disagreement is surfaced — not silently resolved.

Best for:

* High-stakes questions where a wrong answer has real consequences
* Topics where a single model may have blind spots or biases
* Analysis that benefits from multiple independent viewpoints
* Reducing hallucination via cross-model comparison

> **Cost note:** This skill queries 2–3 models per request. Expect approximately 
> 2–3x the token usage of a single-model query. Use it when answer quality 
> justifies the cost; avoid it for simple or low-stakes questions.

---

## Requirements

- [Bun](https://bun.sh) >= 1.0

### Install Bun

```bash
curl -fsSL https://bun.sh/install | bash
```

Or on macOS with Homebrew:

```bash
brew install oven-sh/bun/bun
```

### Environment Variables

bun supports accessing environment variables from `.env` file in the project root.

> **Note:** If you don't have an OpenRouter API key, you can modify `config.json` to use other providers. Change the `provider` field from `"openrouter"` to `"bailian"` or `"openai_compliant"` and update the `api_key_env` to point to your available API key.

### Configuration Files

> **遇到模型访问问题？** 请参考 `README.md` 了解如何根据你的网络环境选择和配置 `config.json`。

### Install Dependencies

```bash
bun install
```

## Usage

```bash
bun run scripts/index.ts "your question"
bun run scripts/index.ts -t financial "美联储2026年会降息吗？"
```

### Domain-Specific Judges

When `queryType` is set to `"financial"`, the judge step uses a finance-specialized prompt that produces:

- **Base Case Analysis** — probabilistic scenario with data-driven reasoning
- **Bull Case** — arguments for upside scenario
- **Bear Case** — arguments for downside scenario
- **Key Variables / Risks** — macro events, earnings, policy changes, market sentiment

This avoids deterministic predictions and enforces probability ranges (e.g., 60–70% likelihood). Use it for investment, macroeconomic, and market analysis questions.

**Example:**
```json
{
  "query": "美联储2026年会降息吗？",
  "queryType": "financial"
}
```

---
# Supported Models

All models are accessed via OpenRouter or other configured providers. Answering models may use live retrieval depending on the provider configuration.

The system selects **2–3 answering models** in parallel (based on roles) and uses a **judge model** to synthesize the final response.

## Model Roles

Each model in `config.json` is tagged with one or more **roles** indicating its capabilities:

| Role | Description | Typical Use |
|------|-------------|-------------|
| `retrieval` | Has web/live data access | Current events, real-time info |
| `coding` | Strong programming capability | Technical implementation, debugging |
| `social` | Social media data access | X/Twitter sentiment, trending |
| `reasoning` | Deep analytical capability | Complex analysis, synthesis |
| `creative` | Creative writing strength | Storytelling, open-ended tasks |
| `longcontext` | Large context window | Document analysis, long inputs |
| `general` | Broad balanced capability | Fallback, ambiguous queries |
| `judge` | Answer synthesis | Final synthesis (judge models only) |

> **Note:** Specific model names and their roles are defined in `config.json` → `models`. Refer to that file for the current model roster.

## Judge Models

Judge models **synthesize answers already in context** and normally do not require retrieval.

They are configured in `config.json` with role `"judge"` and selected via the `judge_model` config key.

Judge models are **independent of answering models** and may synthesize outputs from any answering pool.

---

## Model Selection

Model selection is controlled via `config.json` using a **roles-based routing** system. Instead of hard-coding model names, you select models by the **capabilities (roles)** they provide.

## How to Select Models

As the calling model, follow this process:

1. **Classify the query** — Match keywords to determine the `queryType`
2. **Pass `queryType`** — The skill will look up the `routing.xxx.models` in `config.json`
3. **(Optional) Pass explicit models** — Use the `models` parameter to bypass auto-selection

## Query Types (Domain)

| queryType | Description |
|----------|------------|
| financial | Markets, investing, macroeconomics |
| technical | Programming, systems, engineering |
| social | Public opinion, social media sentiment |
| current_events | Recent news and real-time information |
| scientific | Objective knowledge, definitions, theories |
| creative | Writing, design, ideation |
| general | Default fallback |


## Intent (Task Type)

In addition to `queryType`, queries may include an optional `intent` field. `queryType` defines the domain (what the question is about),
while `intent` defines the task (what to do with the question).
If `intent` is not provided, the system defaults to `analysis` for complex queries and `lookup` for simple factual queries.

| intent | Description |
|--------|------------|
| lookup | Retrieve factual information |
| analysis | Deep reasoning and explanation |
| comparison | Compare multiple entities |
| prediction | Forecast future outcomes (used in financial) |
| generation | Create content (text, ideas, design) |

Example:

{
  "query": "美联储2026年会降息吗？",
  "queryType": "financial",
  "intent": "prediction"
}


## Selection Algorithm

```
1. Analyze query → match keywords → determine queryType
2. Pass queryType to skill → skill looks up `routing.<queryType>.models` in config.json
3. Skill selects top 2–3 models from the routing config
4. If queryType === 'financial', skill uses judge_financial.txt for synthesis
```

## Examples

### Example 1: Financial Query

Query: "美联储2026年会降息吗？"

Selection process:
1. **Keywords**: 美联储, 降息 → queryType: `financial`
2. **Pass to skill**: `{ "query": "...", "queryType": "financial" }`
3. **Skill looks up**: `config.json` → `routing.financial.models`
4. **Skill selects**: First 2 models from the routing config
5. **Judge**: Uses `judge_financial.txt` (Bull/Bear/Base Case analysis)

### Example 2: Technical Query

Query: "How do I implement a distributed transaction?"

Selection process:
1. **Keywords**: implement, distributed → queryType: `technical`
2. **Pass to skill**: `{ "query": "...", "queryType": "technical" }`
3. **Skill looks up**: `config.json` → `routing.technical.models`
4. **Skill selects**: Models configured for technical queries

### Example 3: Social Query

Query: "What are people saying about SpaceX on Twitter?"

Selection process:
1. **Keywords**: Twitter, saying → queryType: `social`
2. **Pass to skill**: `{ "query": "...", "queryType": "social" }`
3. **Skill looks up**: `config.json` → `routing.social.models`
   - Note: `grok-4.1` has `social`, `sentiment`, `trending` roles + X data access

## When to Reference Specific Models

Only hard-code model names when:

1. **Special data access** — e.g., `grok-4.1` for X/Twitter data, `kimi-k2.5` for 200K context
2. **Known strengths** — e.g., `qwen3.5` for coding tasks based on benchmarks
3. **Avoiding specific models** — e.g., excluding models known to underperform for certain tasks

In these cases, document **why** that specific model is needed, not just its name.


---

# When To Use This Skill

**Use this skill when:**

* The user asks a complex research question
* The question requires high confidence or cross-validation
* The topic has multiple competing viewpoints
* A factual error would have significant consequences

**Do NOT use this skill for:**

* Simple factual lookups
* Quick definitions or summaries
* Trivial tasks a single model can answer reliably
* Time-sensitive queries where 8–15s latency is unacceptable

---

# Skill Parameters

| Parameter | Type | Description |
|---|---|---|
| query | string | The research question |
| queryType | string | Domain classification (financial, technical, etc.) |
| intent | string | Task type (analysis, prediction, etc.) |
| models | array | Override model selection |
| maxModels | number | Max models |
| depth | string | simple / tree |
| judgeModel | string | Override judge |
> **Note:** The `domain` parameter has been deprecated. Use `queryType: 'financial'` instead for financial queries.

**Example:**

```json
{
  "query": "What are the economic impacts of AI agents?",
  "queryType": "general",
  "intent": "analysis"
}
```

```json
{
  "query": "美联储2026年会降息吗？",
  "queryType": "financial",
  "maxModels": 2
}
```

## Depth Modes

| Mode | Behavior | Use When |
|---|---|---|
| `simple` (default) | Single-pass: each model answers the query once, judge synthesizes | Most research questions |
| `tree` | Multi-pass: follow-up sub-queries are generated and answered before synthesis | Complex topics requiring decomposition (adds ~10–20s latency) |

---

# Output Format

**Success (all models respond):**

```json
{
  "query": "user question",
  "models_used": ["glm-5", "kimi-k2.5"],
  "answers": [
    { "model": "glm-5", "answer": "..." },
    { "model": "kimi-k2.5", "answer": "..." }
  ],
  "final_answer": "...",
  "confidence": 0.85
}
```

**Partial failure (one model timed out or errored):**

```json
{
  "query": "user question",
  "models_used": ["glm-5"],
  "models_failed": [
    { "model": "kimi-k2.5", "reason": "timeout" }
  ],
  "answers": [
    { "model": "glm-5", "answer": "..." }
  ],
  "final_answer": "...",
  "confidence": 0.61,
  "warning": "Synthesis based on partial responses. Confidence may be reduced."
}
```

**Full failure:**

```json
{
  "query": "user question",
  "models_used": [],
  "models_failed": [
    { "model": "glm-5", "reason": "timeout" },
    { "model": "kimi-k2.5", "reason": "api_error" }
  ],
  "final_answer": null,
  "error": "All models failed. Please retry."
}
```

> **Confidence scale:** All confidence values use a **0–1 scale** (e.g., `0.85` = 85% confidence). This applies consistently across normalizer outputs and judge outputs.

---

# Result Files

Each run produces files identified by a shared `timestamp` in `YYYY-MM-DDTHH-MM-SS` format (ISO 8601, colons replaced with hyphens).

The timestamp is logged at the start of execution:
```
[ResearchAgent] Timestamp: 2026-03-19T14-30-05
```

### File Locations

| File | Path | Content |
|---|---|---|
| **Report** | `reports/report-{timestamp}.txt` | Final synthesized answer from judge |
| **Model responses** | `intermediate/{model}-{timestamp}.txt` | Raw response from each answering model |
| **Judge raw** | `intermediate/{judge}-{timestamp}.txt` | Raw judge synthesis output |

### Example

For a run at `2026-03-19T14:30:05` with models `kimi-k2.5` and `gpt-5.4`, judge `glm-5`:

```
reports/report-2026-03-19T14-30-05.txt        ← final answer
intermediate/kimi-k2.5-2026-03-19T14-30-05.txt
intermediate/gpt-5.4-2026-03-19T14-30-05.txt
intermediate/glm-5-judge-raw-2026-03-19T14-30-05.txt
```

> Use the timestamp from console output to locate all files from a specific run.

---

# Performance Characteristics

| Stage | Typical Latency |
|---|---|
| Router | ~1s (skipped when `models` passed directly) |
| Model inference (parallel) | 20–100s |
| Judge synthesis | 20-60s |
| **Total** | **40–120s** |

Timeout per model: `60-120 seconds`
Retries per model: `1`

---

# Failure Handling

The skill tolerates partial failures:

* If a model times out or errors, the skill continues with remaining responses
* The judge synthesizes available answers and notes missing models in output
* If all models fail, a structured error is returned (see Output Format above)
* The router has a default fallback pair (`glm-5` + `kimi-k2.5`) if routing fails

---

# Security Notes

* User-supplied `query` values are included in prompts sent to external model APIs. Avoid passing unsanitized inputs from untrusted sources.
* The skill does not validate or filter query content — callers are responsible for input sanitization upstream.
* Do not include secrets, PII, or confidential data in queries unless the target model APIs are approved for that data classification.

---

# Quality Evaluation

A synthesized answer is considered high quality when:

* Consensus points across models are clearly identified
* Disagreements are surfaced (not silently resolved)
* Confidence ≥ 0.75
* The judge does not fabricate citations or sources

For ongoing quality tracking, log `confidence`, `models_used`, and `models_failed` per request.

---

# Best Practices

## Recommended Model Combinations

| intent | Role Combination | Example |
|--------|------------------|---------|
| lookup | `retrieval` + `general` | Quick factual lookup + balanced fallback |
| analysis | `reasoning` + `retrieval` | Deep analysis + live data context |
| prediction | `reasoning` + `synthesis` | Forecast with multi-source synthesis |
| comparison | `reasoning` + `structured` | Evaluate options systematically |
| generation | `creative` + `synthesis` | Create + refine output |

| queryType | Recommended Roles | Why |
|---------|---------------|-----|
| financial | `retrieval` + `research` | Live data + analysis |
| technical | `coding` + `general` | Technical + broader context |
| social | `social` + `retrieval` | Sentiment + current context |
| creative | `creative` + `synthesis` | Generate + refine |


## Why Role Diversity Matters

Combining models with different roles improves reliability:

- **`retrieval` + `reasoning`**: Up-to-date facts + deep analysis
- **`coding` + `general`**: Technical accuracy + broader context
- **`social` + `retrieval`**: Platform-specific sentiment + general web context

Benefits:
* Higher reliability through capability diversity
* Reduced hallucination via cross-validation
* Improved reasoning quality on ambiguous topics

---

# Example Usage

```
use cross-research

query="What are the major AI breakthroughs in the past 12 months?"
queryType="current_events"
```

Selection process:
1. Keywords: "past 12 months" → implies `current_events`
2. Pass `queryType: "current_events"` to skill
3. Skill looks up `config.json` → `routing.current_events.models`
4. Judge synthesizes responses

Example result:

```
Final Answer:
AI breakthroughs in the last year include...

Consensus:
- Agent frameworks matured significantly
- Multimodal models expanded in capability
- Inference costs decreased substantially

Confidence: 0.87
```

---

# Changelog

| Version | Changes |
|---|---|
| 1.0.3 | updated metadata |
| 1.0.2 | model updates; bug fixes |
| 1.0.0 | Initial release |