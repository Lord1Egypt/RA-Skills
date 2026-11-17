## Description:

Helps scientific and ML researchers capture experiment issues, methodology corrections, and reusable lessons in project-local learning logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, data scientists, and ML developers use this skill to log reproducibility problems, data quality issues, and methodological lessons, then review and promote useful findings into research guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent hooks may trigger unwanted reminders outside the intended project.

Mitigation: Keep hooks project-scoped, use narrow matchers, and review hook code before enabling it.

Risk: Research logs may expose sensitive data or secrets.

Mitigation: Avoid logging secrets or raw sensitive data.

Risk: Generated skill scaffolds may contain unreviewed guidance.

Mitigation: Manually review generated skills before use or publication.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jose-compu/skills/self-improving-science)
- [Examples](references/examples.md)
- [Hooks setup](references/hooks-setup.md)
- [OpenClaw integration](references/openclaw-integration.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown learning logs and guidance with optional shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional generated skill scaffold requires human review before use.]

## Skill Version(s):

1.1.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
