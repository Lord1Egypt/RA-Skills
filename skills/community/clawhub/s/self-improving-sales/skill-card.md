## Description:

Helps sales teams capture and review pipeline leaks, objections, pricing errors, forecast misses, competitor shifts, and slow-moving deals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams and their agents use this skill to log anonymized deal lessons, spot recurring patterns, and develop reusable sales guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent sales notes may contain sensitive customer or deal information.

Mitigation: Anonymize customers; avoid exact deal terms, personal data, and raw transcripts in learning files.

Risk: Optional hooks can run during agent workflows.

Mitigation: Keep hooks project-scoped, start with reminder-only hooks, and review scripts before enabling PostToolUse.

Risk: Promoting learnings may change agent instructions or create reusable skills.

Mitigation: Require an explicit reviewed diff before changing agent files, hooks, rules, or generated skills.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jose-compu/skills/self-improving-sales)
- [Sales logging examples](references/examples.md)
- [Hook setup](references/hooks-setup.md)
- [OpenClaw integration](references/openclaw-integration.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown sales logs and guidance with optional setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workspace-local learning files; optional project-scoped reminders and reviewed skill scaffolds.]

## Skill Version(s):

1.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
