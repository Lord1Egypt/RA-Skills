## Description:

Ralph Mode helps agents run sustained autonomous development loops with structured planning, iteration limits, backpressure gates, and completion criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richginsberg](https://clawhub.ai/user/richginsberg)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to plan, execute, validate, and track multi-iteration coding work. It is intended for projects that need acceptance criteria, test, lint, typecheck, or build gates before work is treated as complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous development loops can make broad code changes or commit incorrect work if goals and validation gates are underspecified.

Mitigation: Set explicit acceptance criteria, iteration limits, time limits, and validation commands before use, and review resulting file changes or commits before trusting them.

Risk: High sub-agent parallelism can consume substantial compute, token, or API resources.

Mitigation: Use bounded concurrency and cost limits, and avoid the 250-subagent discovery pattern unless there is a deliberate resource budget and monitoring.

Risk: Overlapping autonomous sessions on the same codebase can create file conflicts or lose work.

Mitigation: Check for existing sessions before starting a new loop, isolate workspaces when possible, and require PROGRESS.md updates after every iteration.

## Reference(s):

- [Backpressure Gates Reference](references/backpressure.md)
- [Code Patterns Reference](references/patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/richginsberg/skills/ralph-mode)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update planning, progress, and operational files such as IMPLEMENTATION_PLAN.md, PROGRESS.md, AGENTS.md, and specs.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
