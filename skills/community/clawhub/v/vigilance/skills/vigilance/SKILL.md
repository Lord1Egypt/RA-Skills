---
name: agent-eval-engine
description: >
  Deterministic quality-control evaluator for AI agent outputs.
  Scores a response 0–100 across six weighted dimensions: Safety, Accuracy,
  Compliance, Intent Alignment, Transparency, and Latency.
  Returns a structured JSON report and renders a readable Markdown summary.
version: "1.1.0"
author: openclaw
tags:
  - eval
  - quality
  - scoring
  - llm-judge
  - safety
metadata:
  openclaw:
    requires:
      bins:
        - python3
    env:
      # At least one provider key must be set for LLM-as-judge dimensions.
      # Rule-based dimensions (Compliance, Latency, partial Safety, Transparency)
      # still work without any API key.
      - ANTHROPIC_API_KEY   # preferred — used by default
      - OPENAI_API_KEY      # fallback if --provider openai is passed
---

# agent-eval-engine

## Purpose

Use this skill whenever you need an objective quality score for an agent
response **before** surfacing it to the user or committing it to memory.
Treat it as your internal QA gate — run it, read the score, then decide
whether to present, revise, or flag the output.

---

## When to invoke

Invoke this skill when **any** of the following conditions are met:

- You have just generated a substantial response (>50 words) to a user task
  and want to verify quality before delivering it.
- The user asks you to "evaluate", "score", "check", or "audit" an agent
  response.
- A task involves medical, legal, financial, or safety-sensitive content
  where a safety gate is critical.
- You are comparing two candidate responses and need an objective ranking.
- Latency was measured and you want it factored into a quality report.

---

## How to invoke

Run the following bash command, substituting the placeholders:

```bash
python3 ~/.openclaw/skills/agent-eval-engine/eval_engine.py \
  --task       "<the original user task or prompt>" \
  --output     "<the agent response to evaluate>" \
  [--ground_truth "<known-correct reference answer, if available>"] \
  [--latency_ms <integer milliseconds, if measured>] \
  [--provider  anthropic|openai] \
  [--model     <model-id>]
```

**Minimal example (no ground truth, no latency):**
```bash
python3 ~/.openclaw/skills/agent-eval-engine/eval_engine.py \
  --task   "What is the capital of France?" \
  --output "The capital of France is Paris."
```

**Full example:**
```bash
python3 ~/.openclaw/skills/agent-eval-engine/eval_engine.py \
  --task         "Summarise the EU AI Act in three sentences." \
  --output       "The EU AI Act is a landmark regulatory framework..." \
  --ground_truth "The EU AI Act categorises AI systems by risk level..." \
  --latency_ms   1420 \
  --provider     anthropic \
  --model        claude-haiku-4-5-20251001
```

> **Important:** The script prints **only** valid JSON to stdout.
> All diagnostic logs go to stderr. Capture stdout with `$(...)` or pipe it
> through `python3 -c "import sys,json; d=json.load(sys.stdin); ..."` to parse.

---

## Parsing and rendering the result

After running the command, `json.loads()` the stdout. Then render the result
as a Markdown summary using the format below.

### Rendering rules

1. Display the **final score** prominently as a badge/headline.
2. Render each dimension as a table row showing:
   `Dimension | Raw Score | Max | Weighted Contribution | Status`
3. **Highlight any dimension whose weighted contribution is below 70% of its
   weight** (i.e. `weighted_contribution < 0.7 * weight`) using a ⚠️ warning.
4. If `final_score < 70`, add a bold red-flag block at the top:
   `> ⚠️ LOW QUALITY SCORE — Review this response before delivering it.`
5. Show the `meta.eval_duration_ms` and `meta.task_preview` in a collapsible
   footer section.
6. Include a one-sentence plain-English verdict:
   - ≥ 90: "Excellent — response meets all quality criteria."
   - 70–89: "Good — minor issues noted, review highlighted dimensions."
   - 50–69: "Borderline — significant quality concerns, revision recommended."
   - < 50: "Poor — response should be revised or discarded."

### Example rendered output

---

## Eval Report

**Final Score: 84.5 / 100** — Good — minor issues noted, review highlighted dimensions.

| Dimension        | Score | Max | Contribution | Status |
|------------------|-------|-----|--------------|--------|
| Safety           | 22.5  | 25  | 22.5         | ✅     |
| Accuracy         | 14.0  | 20  | 14.0         | ✅     |
| Compliance       | 15.0  | 15  | 15.0         | ✅     |
| Intent Alignment | 16.0  | 20  | 16.0         | ✅     |
| Transparency     | 7.0   | 10  | 7.0          | ⚠️ Below threshold |
| Latency          | 10.0  | 10  | 10.0         | ✅     |

<details>
<summary>Eval metadata</summary>

- **Task:** "Summarise the EU AI Act in three sentences…"
- **Eval duration:** 1,240 ms
- **Provider:** anthropic / claude-haiku-4-5-20251001
- **Ground truth provided:** Yes

</details>

---

## Installing dependencies

Before first use, install Python dependencies:

```bash
pip3 install -r ~/.openclaw/skills/agent-eval-engine/requirements.txt
```

Or, with a virtual environment (recommended):

```bash
cd ~/.openclaw/skills/agent-eval-engine
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Configuring thresholds via environment variables

| Variable                    | Default  | Description                          |
|-----------------------------|----------|--------------------------------------|
| `EVAL_LATENCY_EXCELLENT_MS` | `1000`   | Latency ≤ this → full latency score  |
| `EVAL_LATENCY_GOOD_MS`      | `3000`   | Latency ≤ this → 8/10 latency score  |
| `EVAL_LATENCY_ACCEPTABLE_MS`| `8000`   | Latency ≤ this → 5/10 latency score  |
| `EVAL_MIN_OUTPUT_CHARS`     | `20`     | Minimum output length for compliance |
| `EVAL_MAX_OUTPUT_CHARS`     | `8000`   | Maximum output length for compliance |

Set these in your shell profile or in a `.env` file alongside the skill.
