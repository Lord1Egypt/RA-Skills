# Deep Think — Structured Reasoning Protocol for Claude

> Forces step-by-step analysis, self-critique, and confidence scoring before answering. Reduces hallucinations and wrong answers on complex questions.

[![clawhub](https://img.shields.io/badge/clawhub-thinkdeep-blue)](https://clawhub.ai/skills/thinkdeep)
[![thinkstack](https://img.shields.io/badge/ThinkStack-2%2F3-purple)](https://clawhub.ai/skills/thinkdeep)
[![openclaw](https://img.shields.io/badge/openclaw-skill-orange)](https://openclaw.ai)

## The Problem

Fast answers feel efficient. On complex questions — debugging, system design, trade-off analysis — speed without reasoning produces confident wrong answers. Claude sounds certain even when it shouldn't be.

Deep Think forces Claude to slow down at exactly the right moments.

## What it does

**Restate** — confirms the question is understood before answering  
**Explore** — generates 3+ distinct approaches, including non-obvious ones  
**Critique** — finds the weakest point in each option before committing  
**Select** — chooses with explicit reasoning, not intuition  
**Confidence scoring** — rates certainty 1–10 and names key uncertainties upfront

## Confidence Scale

| Score | Meaning | Action |
|-------|---------|--------|
| 8–10 | Well-established ground | Proceed |
| 5–7 | Reasonable but verify | Flag key uncertainties |
| 1–4 | Significant unknowns | Lead with that, not bury it |

## Installation

```bash
openclaw install deep-think
```

## ThinkStack

Deep Think is part of the **ThinkStack** — three skills that make Claude smarter at every stage:

```
clarity-first  →  deep-think  →  task-pilot
 understand        analyze        execute
```

```bash
openclaw install clarity-first
openclaw install deep-think
openclaw install task-pilot
```

## Keywords

chain of thought · reasoning · self-critique · confidence scoring · reduce hallucinations · structured thinking · think step by step · deep reasoning · analytical thinking · better answers · slow thinking · system 2 thinking · AI reasoning · smarter Claude · agent improvement · reasoning protocol · prevent wrong answers · 深度思考 · 链式推理 · 减少幻觉 · 自我批判

---

Built for [OpenClaw](https://openclaw.ai) · Published on [clawhub.ai](https://clawhub.ai/skills/thinkdeep)
