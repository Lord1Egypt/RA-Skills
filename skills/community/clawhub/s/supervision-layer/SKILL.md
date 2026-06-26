---
name: supervision-layer
version: 1.0.0
description: "Wrap every tool call with timeouts, circuit breakers, audit logging, and crash loop protection. Enforcement the agent cannot bypass."
license: MIT
tags: [supervision, circuit-breaker, timeout, audit-logging, crash-loop, safety, reliability, agent-control, middleware, production]
source: el-rudo-larios/supervision-layer
trigger: "agent supervision timeout circuit breaker audit protection"
metadata:
  openclaw:
    emoji: "🛡️"
---

# Supervision Layer

**Stop trusting agents to police themselves.** Supervision Layer wraps every tool call in timeouts, circuit breakers, and audit logs — enforcement the agent cannot bypass.

## Before vs After

| | Without Supervision | With Supervision |
|---|---|---|
| **Runaway calls** | Agent loops infinitely on a failing API | Circuit breaker trips after 3 failures |
| **Stuck sessions** | Tool hangs silently, agent waits forever | Timeout kills it after 30s |
| **Audit trail** | No record of what happened | Every call logged with timestamp, outcome, cost |
| **Crash loops** | Subagent restarts infinitely | After 3 crashes, marked permanently failed |

## Quick Start

```python
from supervision import get_supervisor

supervisor = get_supervisor()
result = await supervisor.execute(
    tool="web_fetch",
    fn=fetch_fn,
    agent_id="worker-1",
    session_id="sess-abc",
)
```

## Components

1. **TimeoutWrapper** — Per-tool configurable timeouts (default 30s)
2. **CircuitBreaker** — 3-state machine (CLOSED → OPEN → HALF_OPEN)
3. **AuditLogger** — Structured JSONL logging, 50MB rotation, queryable
4. **CrashLoopProtector** — Track restarts, mark failed after 3 within window
5. **SupervisedCall** — All-in-one: crash check → circuit check → audit → timeout → audit

## Testing

```bash
cd scripts/ && python -m pytest test_supervision.py -v
```

58 tests. 0 external dependencies. Works with any async Python project.

## License

MIT
