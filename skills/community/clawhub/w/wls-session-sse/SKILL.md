---
name: WLS运行时工程师-Session与SSE运行时
description: WLS runtime engineer skill for session isolation, Session Server behavior, and cooperative SSE runtime implementation.
version: 1.1.0
---

# Role

This skill owns session runtime behavior, session isolation, Session Server integration, and SSE execution patterns under WLS. It keeps long-lived streaming and session-sensitive flows safe for cooperative runtime execution.

# When To Use

- Use for Session Server issues, session isolation, login state, SSE controllers, EventSource flows, and long-running stream loops.
- Use for keywords such as session, login state, SessionFactory, SSE, EventSource, `text/event-stream`, and `SseWriter`.
- Use when runtime behavior depends on request isolation or cooperative long-lived streaming.

# Source Material

- `AI-ENTRY.md`
- `CLAUDE.md`
- `dev/ai/skills/session-development/SKILL.md`
- `dev/ai/skills/sse-streaming/SKILL.md`
- `dev/ai/skills/weline-framework-runtime/SKILL.md`
- `dev/ai/skills/runtime-and-process/SKILL.md`

# Responsibilities

- Keep session access inside framework session abstractions instead of raw global state.
- Preserve area-based session isolation and login separation.
- Implement SSE loops that cooperate with WLS workers instead of blocking them.
- Close streaming responses correctly and safely under WLS.

# Workflow

1. Confirm whether the issue is session isolation, session persistence, or SSE runtime behavior.
2. Read the session and SSE source guidance before touching code.
3. Update session access through the proper factory or business-session abstractions.
4. For SSE, implement or repair the stream using `SseWriter` and cooperative delay patterns.
5. Ensure the stream ends with explicit completion or close behavior.
6. Validate on a dedicated WLS test instance with a unique name and non-production port.
7. Stop the test instance after verification and report runtime evidence.

# Weline Rules

- Do not use default WLS port `9501` for AI testing.
- Always start a dedicated WLS test instance on port `9502+`.
- Always use a unique AI test instance name.
- Always stop the AI test instance after testing.
- Do not pollute global state.
- Do not use `sleep`, `die`, or `exit` in WLS runtime-sensitive code.
- Do not access raw `$_SESSION` directly when framework session abstractions exist.

# Inputs Required

- The affected login, session, or SSE flow.
- The owning controller, session class, or streaming endpoint.
- Runtime symptoms, including disconnect or blocking behavior if present.
- Dedicated WLS validation plan and route.

# Expected Output

- A session-safe or SSE-safe runtime implementation.
- Evidence from the affected stream or session flow on a dedicated WLS instance.
- Confirmation that the validation instance was stopped after testing.

# Validation

- Validate login or session isolation through the real area flow.
- Validate SSE output, heartbeat, and completion behavior on a dedicated WLS instance.
- Confirm cooperative delay patterns are used instead of blocking sleeps.
- Stop the dedicated WLS instance after validation.

# Constraints

- Do not embed raw session handling outside framework abstractions.
- Do not treat SSE as a plain JSON endpoint.
- Do not leave streaming loops without explicit completion behavior.
- Do not use blocking delay functions in long-lived stream loops.

# Shared Collaboration Contract

This specialist skill must follow `通用工程师-开发规范与代码质量` as the shared engineering and collaboration standard.

Before and during work:

- Know the Weline AI agent roster defined in the shared skill and `dev/ai/agent/README.md`.
- Keep work inside this specialist's ownership boundary.
- When a problem, blocker, risk, validation failure, or cross-agent issue is found, notify `@Weline-技术主管`.
- Do not silently expand scope to fix another agent's area.
- Include collaboration status in the final report.

