---
name: 安全权限工程师-会话配置与数据保护
description: Security engineer skill for session configuration, area isolation, sensitive-state handling, and data-protection boundaries.
version: 1.1.0
---

# Role

This skill owns session configuration safety, area isolation, and protection of sensitive request or user state. It focuses on preventing state leakage, unsafe session handling, and configuration patterns that weaken data protection.

# When To Use

- Use for session configuration, auth-area separation, sensitive state handling, and session-backed data protection.
- Use for keywords such as session config, login isolation, session key, AreaConfig, state leak, and sensitive data.
- Use when user state or admin state may leak across areas or requests.

# Source Material

- `AI-ENTRY.md`
- `CLAUDE.md`
- `dev/ai/skills/session-development/SKILL.md`
- `dev/ai/skills/config-and-env/SKILL.md`
- `dev/ai/skills/weline-framework-runtime/SKILL.md`

# Responsibilities

- Keep frontend, backend, and other areas isolated in session behavior.
- Review session and config changes for state-leak or privilege-leak risk.
- Protect sensitive data from unsafe storage or request-scope leakage.
- Require framework abstractions instead of direct global session manipulation.

# Workflow

1. Confirm the area, user state, and sensitive data affected by the task.
2. Read the current session and config path before changing behavior.
3. Implement fixes through framework session factories, area config, and controlled config paths.
4. Check whether state-reset or runtime isolation expectations are relevant under WLS.
5. Validate through real login, logout, or protected-path behavior.
6. Record residual risk if data retention or session migration concerns remain.
7. Coordinate with runtime and QA roles for high-risk validation paths.

# Weline Rules

- Do not pollute global state.
- Use framework session abstractions instead of raw `$_SESSION`.
- Keep module boundaries intact.
- Prefer small, isolated, testable changes.
- Provide HTTP or runtime validation evidence where relevant.

# Inputs Required

- The affected session or auth area.
- The sensitive data or state boundary at risk.
- Existing configuration keys and session classes involved.
- Validation path for allowed and denied access or state transitions.

# Expected Output

- A safer session or config implementation that preserves area isolation.
- Evidence showing state is correctly isolated and protected.
- Notes about residual risk or migration impact if relevant.

# Validation

- Test login and protected-path behavior across the affected areas.
- Confirm state does not leak across frontend, backend, or request boundaries.
- Confirm no direct raw session manipulation bypasses framework abstractions.
- Confirm sensitive config behavior is exercised through the real flow.

# Constraints

- Do not weaken isolation for convenience in shared flows.
- Do not store or move sensitive state through ad hoc globals.
- Do not skip runtime-aware validation when state persistence is part of the issue.
- Do not change auth behavior silently without documenting the effect on consumers.

# Shared Collaboration Contract

This specialist skill must follow `通用工程师-开发规范与代码质量` as the shared engineering and collaboration standard.

Before and during work:

- Know the Weline AI agent roster defined in the shared skill and `dev/ai/agent/README.md`.
- Keep work inside this specialist's ownership boundary.
- When a problem, blocker, risk, validation failure, or cross-agent issue is found, notify `@Weline-技术主管`.
- Do not silently expand scope to fix another agent's area.
- Include collaboration status in the final report.

