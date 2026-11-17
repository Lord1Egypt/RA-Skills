## Description:

Safe Exec.Bak provides local command-safety tooling for OpenClaw agents, using pattern-based risk assessment, approval prompts, pending-request management, and audit logging for shell command execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gjc0909](https://clawhub.ai/user/gjc0909)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use this skill to route agent shell commands through local risk checks, approval prompts, and audit logging before or during execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Risky commands can execute without reliable human approval because the approval and risk controls are not a ready safety boundary.

Mitigation: Treat Safe Exec.Bak as a review and audit aid until approval handling, request-ID validation, fail-closed risk classification, and eval-based execution are fixed.

Risk: Local command execution can affect user files, system configuration, or privileged resources when run with broad permissions.

Mitigation: Run with least privilege, review pending requests and audit logs, and avoid using it as the only control on privileged workstations.

Risk: Automatic or non-interactive approval behavior can reduce the value of human confirmation.

Mitigation: Disable auto-confirm behavior for sensitive workflows and require explicit review for high-impact commands before deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/gjc0909/skills/safe-exec-bak)
- [Publisher profile](https://clawhub.ai/user/gjc0909)
- [Git install source from ClawHub metadata](https://github.com/OTTTTTO/safe-exec.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and local script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq and writes local pending-request and audit state under ~/.openclaw.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata also reports 0.3.4 and scripts/docs mention 0.3.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
