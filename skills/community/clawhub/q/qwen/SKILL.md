---
name: Qwen
slug: qwen
version: 1.0.0
homepage: https://clawic.com/skills/qwen
description: Build and route Qwen chat, coding, reasoning, and vision workflows across hosted and self-hosted endpoints with safer debugging.
changelog: Initial release with hosted and self-hosted Qwen routing, API patterns, tool-calling guidance, and troubleshooting playbooks.
metadata: {"clawdbot":{"emoji":"🧩","requires":{"bins":["curl","jq"],"env":["DASHSCOPE_API_KEY"]},"os":["linux","darwin","win32"],"configPaths":["~/qwen/"]}}
---

## When to Use

User needs Qwen to work reliably for chat, coding, reasoning, structured outputs, or vision. Agent handles surface selection, live model verification, hosted-versus-local tradeoffs, and failure recovery before the workflow reaches production.

## Architecture

Memory lives in `~/qwen/`. If `~/qwen/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/qwen/
├── memory.md         # Status, activation rules, and deployment defaults
├── routes.md         # Preferred route per workload
├── servers.md        # Known local or hosted endpoints
├── experiments.md    # Prompt, parser, and latency notes
└── logs/             # Optional sanitized repro payloads
```

## Quick Reference

Use the smallest file that resolves the blocker.

| Topic | File |
|-------|------|
| Setup process | `setup.md` |
| Memory template | `memory-template.md` |
| Hosted and local request patterns | `api-patterns.md` |
| Workload routing matrix | `routing-matrix.md` |
| Hosted versus self-hosted decisions | `deployment-paths.md` |
| Tool-calling and structured output guardrails | `tool-calling.md` |
| Debugging and recovery | `troubleshooting.md` |

## Requirements

- `curl` and `jq` for minimal endpoint checks
- Hosted Qwen usually needs a `DASHSCOPE_API_KEY`
- Self-hosted Qwen may use Ollama, vLLM, SGLang, or another OpenAI-compatible server
- Keep secrets in environment variables only

## Core Rules

### 1. Lock the Surface Before Tuning the Model
- Identify the real execution surface first: Alibaba Model Studio hosted API, another OpenAI-compatible provider, or a self-hosted server.
- Most "Qwen issues" are actually endpoint, region, server, or chat-template issues rather than model quality issues.

### 2. Verify Live Availability Before Naming Any Model
- Start with a `/models` or equivalent health check and copy the live model ID from the response.
- Never trust stale screenshots, old blog posts, or remembered IDs for production routing.

### 3. Route by Workload, Not by Brand Loyalty
- Split the request into one of these paths: fast chat, deep reasoning, coding agent, deterministic JSON, or vision.
- Pick the smallest Qwen family and server path that can reliably do that job.

### 4. Treat Structured Output as a Separate Reliability Problem
- If Qwen is feeding tools, JSON, or downstream writes, use strict schemas, low temperature, and parser validation before acting.
- If the first pass is creative or reasoning-heavy, add a second deterministic normalization pass instead of forcing one prompt to do both.

### 5. Separate Model Problems From Server Problems
- When behavior changes after migration, isolate the variable: model family, quantization, chat template, reasoning mode, parser, or backend.
- Reproduce with one minimal payload before changing prompts, infrastructure, and business logic at the same time.

### 6. Compare Hosted and Self-Hosted Explicitly
- Hosted Qwen usually wins on speed to first success and managed multimodal access.
- Self-hosted Qwen only wins when privacy, local cost control, or offline use clearly outweigh operational overhead.

### 7. Ask Before Creating Persistent State
- Work statelessly by default.
- Only create `~/qwen/` notes, saved routes, or repro logs after the user wants continuity across Qwen tasks.

## Common Traps

- Treating "Qwen" as one interchangeable thing -> hosted APIs, Ollama, vLLM, and agent frameworks behave differently.
- Hardcoding dated model IDs -> region and release cadence make old IDs fail fast.
- Mixing free-form reasoning with strict JSON output -> parsing breaks when one prompt is asked to do both.
- Blaming the model for local slowness -> Apple Silicon and Ollama often fail because of model size, quantization, or oversized context.
- Migrating from another OpenAI-compatible backend without rechecking tool-calling -> parser and chat-template differences can break automation.

## External Endpoints

Use only the smallest hosted endpoint that answers the current question.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://dashscope.aliyuncs.com/compatible-mode/v1/models | Auth header only | Mainland China model discovery |
| https://dashscope-intl.aliyuncs.com/compatible-mode/v1/models | Auth header only | International model discovery |
| https://dashscope-us.aliyuncs.com/compatible-mode/v1/models | Auth header only | United States model discovery |
| https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions | Prompt messages and options | Hosted Qwen chat completions in Beijing region |
| https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions | Prompt messages and options | Hosted Qwen chat completions in Singapore region |
| https://dashscope-us.aliyuncs.com/compatible-mode/v1/chat/completions | Prompt messages and options | Hosted Qwen chat completions in Virginia region |

No other data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- Prompt content sent to Alibaba Cloud Model Studio when using hosted Qwen
- Optional images or multimodal payloads sent to hosted Qwen vision endpoints when requested

**Data that stays local:**
- Deployment preferences and routing notes in `~/qwen/` after user approval
- Local server URLs, workload notes, and sanitized repro payloads kept for debugging

**This skill does NOT:**
- Store API keys in markdown files
- Send data to undeclared third-party endpoints
- Assume local servers are safe to expose publicly
- Modify its own skill files

## Scope

This skill ONLY:
- routes Qwen work across hosted and self-hosted execution surfaces
- chooses model families for chat, coding, reasoning, vision, and automation
- debugs migration, parser, latency, and endpoint problems
- stores lightweight local notes only after user approval

This skill NEVER:
- invent live model availability without checking
- persist secrets in `~/qwen/`
- execute destructive downstream automation without validated output
- pretend one backend's tool-calling behavior applies everywhere

## Trust

Using hosted Qwen sends prompt data to Alibaba Cloud Model Studio.
Only install if you trust that service with your data, or keep Qwen fully self-hosted.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `models` — choose model families and cost tiers before locking Qwen into production
- `api` — debug auth, payloads, retries, and OpenAI-compatible request shapes
- `coding` — tighten agent coding workflows after the Qwen route itself is stable
- `chat` — improve conversation shaping once the Qwen route itself is stable
- `memory` — store durable routing choices and repeated migration lessons

## Feedback

- If useful: `clawhub star qwen`
- Stay updated: `clawhub sync`
