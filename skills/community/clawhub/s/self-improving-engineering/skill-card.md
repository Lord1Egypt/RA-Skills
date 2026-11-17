## Description:

Captures architecture decisions, code quality issues, build/deploy failures, dependency problems, performance regressions, tech debt accumulation, and test gaps for continuous engineering improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to capture build failures, architecture discoveries, code quality issues, dependency problems, performance regressions, test gaps, and feature requests as structured markdown logs. Teams can review recurring entries and promote durable lessons into ADRs, coding standards, runbooks, or OpenClaw workspace memory after human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent engineering-learning logs may contain sensitive project context, secrets, command output, or private configuration if entries are copied too broadly.

Mitigation: Keep `.learnings/` project-local by default, redact sensitive values, and review entries for secrets before committing, sharing, or promoting them.

Risk: Optional hooks persist across sessions and can add reminders or inspect command output when configured.

Mitigation: Enable hooks deliberately, keep them project-scoped, narrow matchers, prefer the activator-only setup, and review hook scripts before enabling them.

Risk: Promoting unreviewed local learnings into ADRs, coding standards, runbooks, or workspace memory can preserve inaccurate guidance.

Mitigation: Distill learnings into concise proposed changes and apply promotions only after explicit human approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jose-compu/skills/self-improving-engineering)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or appends project-local .learnings markdown files when used; optional hooks emit reminder text.]

## Skill Version(s):

1.2.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
