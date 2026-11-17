## Description:

Implement dependency injection in PydanticAI agents using RunContext and deps_type. Use when agents need database connections, API clients, user context, or any external resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure dependency injection for PydanticAI agents, including database connections, API clients, user context, and testing overrides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copied examples that pass credentials or external clients into dependencies could expose secrets or broaden access beyond the task.

Mitigation: Pass already configured clients where possible, keep API keys out of source code, and ensure injected database or HTTP clients are trusted and scoped to the task.

Risk: Agent tools can fail at runtime if ctx.deps fields, run-time deps values, or test overrides drift from the declared deps_type.

Mitigation: Follow the skill's gate checks: verify every ctx.deps access exists on deps_type, pass matching deps on every run path that needs them, and keep test overrides aligned with production dependency shape.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anderskev/skills/pydantic-ai-dependency-injection)

## Skill Output:

**Output Type(s):** [guidance, code]

**Output Format:** [Markdown with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no commands are executed by the skill.]

## Skill Version(s):

1.0.1 (source: server release evidence, released 2026-04-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
