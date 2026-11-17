## Description:

Automates ClawHub skill creation, local validation, and publishing from a user's prompt and feature description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bustes01](https://clawhub.ai/user/bustes01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to turn a feature idea into a ClawHub-compatible SKILL.md, supporting files, validation steps, and publish commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated skills may include unsafe command templates or user-provided names in shell commands.

Mitigation: Use simple validated names and slugs, quote command arguments, and review every generated shell command before execution.

Risk: The skill can publish new agent instructions to ClawHub.

Mitigation: Review generated SKILL.md files, run dry-run validation and privacy/security scans, and publish only after human confirmation.

Risk: Generated memory or usage-tracking patterns can create persistence and privacy concerns.

Mitigation: Treat memory and usage tracking as opt-in and document what is stored before enabling it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bustes01/skills/skill-builder-pro)
- [ClawHub Homepage Metadata](https://clawhub.ai/BusTes01/skill-builder-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with YAML, file-structure examples, and bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing instructions for skill generation, validation, privacy checks, and publishing.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
