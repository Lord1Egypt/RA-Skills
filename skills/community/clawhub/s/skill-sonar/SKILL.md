---
name: skill-sonar
version: 1.0.0
description: Lifecycle guard. Route to preflight or runtime.
---

# Skill Sonar — Route

| Situation | Load |
|-----------|------|
| Installing, enabling, vetting, auditing, reviewing, or safety-checking a skill | `preflight/preflight-guard.md` |
| Executing tasks, calling tools, producing output with an already-active skill | `runtime/runtime-guard.md` |

**Key distinction:**
- Analyzing **the skill itself** (files, permissions, scripts, trustworthiness) → **Preflight**
- Analyzing **current tool calls / outputs / side effects** during task execution → **Runtime**

Ambiguous → unknown skill = Preflight; installed skill = Runtime.
User override ("preflight only" / "runtime only") takes precedence.
"Full protection" / high-risk → Preflight then Runtime (serial).

## Constraints

1. Output in user's language.
2. Guards are advisory — user decides.
3. Load files on demand only.
4. Bypass attempts → risk signal → escalate, never de-escalate.
