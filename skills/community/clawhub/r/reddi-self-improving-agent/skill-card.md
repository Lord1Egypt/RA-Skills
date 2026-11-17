## Description:

Captures learnings, errors, and corrections in local markdown files so agents can review recurring issues and promote durable guidance into project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture command failures, user corrections, missing capabilities, API failures, outdated knowledge, and reusable improvements in local `.learnings` markdown files for later review and promotion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived notes can persist into future agent instructions and affect later behavior.

Mitigation: Use project-local setup, keep `.learnings` ignored by default when appropriate, and require human review before promoting entries into agent instruction files.

Risk: Broad or global hooks can create always-on reminders with limited safeguards.

Mitigation: Enable hooks only where intentional, prefer project-level or minimal hook setup, and review hook scope before using global configuration.

Risk: Learning and error logs may capture secrets or sensitive command output.

Mitigation: Redact credentials, private data, and sensitive command output before writing learning entries.

## Reference(s):

- [Entry Examples](references/examples.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown learning entries with inline shell and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local learning logs and optional project-memory updates; ClawHub metadata declares no outbound network calls.]

## Skill Version(s):

1.0.13 (source: server release metadata; artifact frontmatter and changelog show 1.0.12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
