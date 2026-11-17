## Description:

Skill Safe Install (L0 Strict) guides agents through a strict secure-install workflow for ClawHub/OpenClaw skills, including risk review, sandbox verification, and explicit consent gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1231qaz2wsx](https://clawhub.ai/user/1231qaz2wsx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to have an agent review and install ClawHub/OpenClaw skills through a gated workflow that checks identity, install state, risk, sandbox behavior, consent, and optional trust persistence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can lead an agent to run ClawHub inspection and install commands during a user-directed install review.

Mitigation: Require exact skill identity, summarize inspection findings, perform a sandbox install first, and obtain explicit approval before formal installation.

Risk: Persistent trust configuration changes can affect future skill loading.

Mitigation: Skip allowBundled writes by default; only write after explicit user request, with a timestamped backup, exact key disclosure, idempotent append, and rollback command.

Risk: If inspection output is unavailable or incomplete, installation risk cannot be evaluated reliably.

Mitigation: Pause the workflow, treat the skill as high risk, and require explicit confirmation before continuing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1231qaz2wsx/skills/skill-safe-install-l0-strict)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown checklist with step-labeled status lines and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit consent gates before formal install or persistent trust changes.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact/clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
