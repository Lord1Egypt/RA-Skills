## Description:

Helps coding agents capture bug patterns, errors, and reusable development insights in project-local learning notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to record coding errors, debugging insights, and improvement ideas for later review and possible promotion into project standards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning notes may contain private code, paths, stack traces, or credentials.

Mitigation: Redact sensitive details and review .learnings before committing or sharing it.

Risk: Installed hooks may keep prompting across later sessions.

Mitigation: Opt in only when wanted and keep hooks project-scoped rather than installing them globally.

Risk: Promoted rules or extracted skills may introduce incorrect coding guidance.

Mitigation: Review proposed changes and generated skills before applying or publishing them.

## Reference(s):

- [Examples](artifact/references/examples.md)
- [Hook setup](artifact/references/hooks-setup.md)
- [OpenClaw integration](artifact/references/openclaw-integration.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown notes with optional command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-local learning logs and optional hook reminders]

## Skill Version(s):

1.1.2 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
