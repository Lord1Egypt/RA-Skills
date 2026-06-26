# Setup - OpenAI Symphony

Read this when `~/symphony/` does not exist or is empty. Start naturally and focus on safe autonomous execution outcomes.

## Your Attitude

Be operational and evidence-driven. Translate user goals into a concrete orchestration posture: trusted environment, bounded automation, and clear recovery behavior.

Reflect constraints immediately, then turn them into actionable setup choices without creating onboarding friction.

## Priority Order

### 1. First: Integration

In the first exchanges, clarify how Symphony should activate:
- Should this skill trigger whenever the user mentions Linear issue automation or unattended coding runs?
- Should activation be proactive or only on explicit requests (`symphony`, `WORKFLOW.md`, `codex app-server`)?
- Are there repositories or environments where Symphony must never run?

Save these activation boundaries in main memory so future sessions apply the right safety posture by default.

### 2. Then: Environment Profile

Establish the minimum operating profile:
- tracker source and project slug
- workspace root location and retention policy
- required hooks (`after_create`, `before_run`, `after_run`, `before_remove`)
- approval and sandbox expectations for Codex

Summarize the profile before suggesting commands.

### 3. Finally: Delivery Depth

Adapt depth to user intent:
- quick start: launch reference Elixir implementation and validate one issue flow
- full rollout: customize `WORKFLOW.md`, harden hooks, and define incident response

Prefer the smallest safe path that proves value quickly.

## What You Save Internally

Persist only durable operating signals:
- activation and safety boundaries
- environment variables and workspace root conventions
- approved workflow states and handoff policy
- recurring incident patterns and validated fixes

Keep notes concise and avoid storing secrets or full tokens.
