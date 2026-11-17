## Description:

Print the current effective username. Simple identity query for scripts, session tracking, and access control verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to request current-user identity information for shell sessions, scripts, session tracking, and permission checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Identity results may be misleading if used for authorization, privilege checks, auditing, or automation that depends on the real effective OS user.

Mitigation: Review before installing and avoid security-sensitive decisions until the implementation uses kernel-backed identity APIs and the documented options are implemented or removed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/whoami-tool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell command examples; command output may be plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identity output should be reviewed before use in security-sensitive automation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
