# Trunkate AI: Proactive Context Hook

## Overview

This hook implements a proactive "pre-flight" optimization layer for the agent's context window. It ensures that before any request is sent to the LLM, the history is evaluated and, if necessary, compressed via the Trunkate AI API to prevent reasoning degradation.

## Lifecycle Events

| Event | Script | Description |
| --- | --- | --- |
| `PreRequest` | `hooks/openclaw/pre_request.py` | Intercepts the outgoing prompt to evaluate token usage. |
| `OnError` | `scripts/error_detector.py` | Reactive circuit breaker for API-level failures (429, 5xx). |

## Trigger Logic

* **Condition**: `OPENCLAW_CURRENT_TOKENS` > (`OPENCLAW_TOKEN_LIMIT` * `TRUNKATE_THRESHOLD`).
* **Default Threshold**: 0.8 (80% of context window).
* **Action**: Executes a deterministic call to `scripts/activator.py`, which invokes the `trunkate.py` API client.

## Data Flow

1. **Interceptor**: The `PreRequest` event triggers the Python hook.
2. **Evaluation**: The script compares current session tokens against the model limit.
3. **Execution**: If over threshold, the `CompressorPipeline` is engaged via the backend `/optimize` endpoint.
4. **State Injection**: The session history is updated via the `OPENCLAW_ACTION:SET_HISTORY` directive.

---

## Security & Privacy Annex

### Local-First Redaction

Before any data is transmitted to the Trunkate API, it passes through a multi-layered local redaction filter in `scripts/activator.py`. This includes:

* **Structural Isolation**: Blocks wrapped in `[KEEP]` or `<system>` are stripped and replaced with UUID placeholders.
* **Secret Discovery**: Heuristic regex patterns for `Bearer` tokens, `KEY=value` assignments, and high-entropy 32+ character strings.
* **Deterministic Restoration**: Protected blocks are only merged back into the optimized text after the compressed response is received locally.

### Hook Isolation

The `pre_request.py` hook uses an environment whitelist. Only `TRUNKATE_*`, `OPENCLAW_*`, and `PATH` variables are inherited by the optimization subprocess, ensuring unrelated workspace credentials (like `.git` tokens or cloud keys) remain completely inaccessible to the skill logic.
