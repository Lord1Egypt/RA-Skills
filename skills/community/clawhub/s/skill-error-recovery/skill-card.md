## Description:

Detect, attempt recovery from, report, and log errors to prevent silent data loss and ensure proper human intervention when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptratcn](https://clawhub.ai/user/aptratcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make agents recognize failures, attempt bounded recovery, report unresolved errors, and retain troubleshooting notes for future runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent troubleshooting logs can capture secrets, personal data, or sensitive operational details.

Mitigation: Redact secrets and personal data before saving error details, and avoid committing or sharing raw logs.

Risk: Suggested updates to agent instructions, skills, or workflows could introduce incorrect recovery behavior.

Mitigation: Require user review before applying changes to AGENTS.md, skill files, workflow rules, or similar agent instructions.

Risk: Automatic retries can repeat unsafe or ineffective actions when the error requires human judgment.

Mitigation: Keep retries bounded, change parameters between attempts, and report immediately for authentication, permission, validation, or destructive-operation failures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aptratcn/skills/skill-error-recovery)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell command examples and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes bounded retry guidance, structured error reports, and optional persistent troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
