---
name: self-improving-ai
description: "Injects AI/LLM self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"🤖","events":["agent:bootstrap"]}}
---

# AI Self-Improvement Hook

Injects a reminder to evaluate AI/model learnings during agent bootstrap.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Adds an AI-specific reminder block to check `.learnings/` for relevant entries
- Prompts the agent to log model quality issues, inference failures, prompt optimization discoveries, hallucinations, context overflows, RAG retrieval problems, and multimodal pipeline errors
- Emphasizes **NEVER logging API keys, model access tokens, or customer data**

## Reminder Content

The hook injects reminders to log to the appropriate file based on what occurred:

| Trigger | Target File | Category |
|---------|-------------|----------|
| Model response quality issue | `MODEL_ISSUES.md` | model regression |
| Latency or cost anomaly | `MODEL_ISSUES.md` | inference/cost |
| Better model/config discovered | `LEARNINGS.md` | `model_selection` |
| Prompt pattern improved output | `LEARNINGS.md` | `prompt_optimization` |
| Hallucination detected | `LEARNINGS.md` | `hallucination_rate` |
| Context overflow | `LEARNINGS.md` | `context_management` |
| Multimodal input failed | `MODEL_ISSUES.md` | modality_gap |
| Missing AI capability | `FEATURE_REQUESTS.md` | feature request |

## Promotion Targets

| Learning Type | Promote To |
|---------------|------------|
| Model behavior patterns | `SOUL.md` |
| Model workflows and routing | `AGENTS.md` |
| Model/tool configuration | `TOOLS.md` |

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable self-improving-ai
```
