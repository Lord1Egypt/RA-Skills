## Description:

Creates structured session handoff documents so a fresh AI agent can resume long-running work with clear project state, decisions, next steps, and validation checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to create, validate, list, and resume session handoffs for long-running AI coding or project work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented installer uses mutable remote code.

Mitigation: Install only from a pinned, reviewed version or a trusted ClawHub distribution path.

Risk: Handoff files can contain sensitive project records.

Mitigation: Review handoff content before sharing or committing, and do not include secrets, credentials, or token values.

Risk: A resume staleness check can inspect git metadata from a project path recorded inside a handoff file.

Mitigation: Run resume and staleness checks only on trusted handoffs, or verify the recorded project path before executing them.

## Reference(s):

- [Handoff Template](references/handoff-template.md)
- [Resume Checklist](references/resume-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/wpank/skills/session-handoff)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated handoff files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or inspects .claude/handoffs/ Markdown files and reports validation or staleness results.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
