## Description:

SafeExec wraps OpenClaw agent shell command execution with danger-pattern detection, risk assessment, approval prompts, pending-request management, and audit logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucky-2968](https://clawhub.ai/user/lucky-2968)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use SafeExec to route agent shell commands through a local safety wrapper that can flag destructive operations, request approval, and log decisions before commands run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact shell commands may execute without a separate human approval event.

Mitigation: Review before installing and do not rely on the skill as a security boundary until approval and parsing issues are fixed.

Risk: Use on systems with important data, shared accounts, production credentials, passwordless sudo, or broad filesystem access increases potential impact.

Mitigation: Limit use to low-impact environments or restrict permissions and filesystem access before enabling the wrapper.

Risk: The artifact supports disabling or bypassing protection through configuration or direct command execution.

Mitigation: Deploy with clear operating rules, review audit logs, and verify that agents consistently invoke SafeExec for shell commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lucky-2968/skills/safe-exec-0-3-2)
- [SafeExec README](https://github.com/OTTTTTO/safe-exec/blob/master/README.md)
- [SafeExec Usage Guide](docs/USAGE.md)
- [SafeExec v0.3.2 Release Notes](RELEASE_v0.3.2.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local pending-request and audit-log files when used as documented.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact release notes describe SafeExec v0.3.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
