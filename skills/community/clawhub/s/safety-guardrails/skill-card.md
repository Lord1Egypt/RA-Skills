## Description:

Pre-execution safety guardrails for autonomous agents that classify proposed actions by risk and return ALLOW, CONFIRM, or DENY decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill to screen agent or pipeline actions before execution, especially commands, database changes, deployments, outbound messages, and other side-effecting operations that may need denial or human confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guardrail may be bypassed by caller-provided approval flags for critical actions.

Mitigation: Require independent human authorization outside the skill and make critical actions non-overridable before relying on it for autonomous execution.

Risk: Unknown or unmatched commands may be treated as low risk.

Mitigation: Fail closed for unknown actions or route them to manual review until the policy has explicit coverage.

Risk: The learning module persists usage and preference data.

Mitigation: Disable or remove learning unless users explicitly opt in and retention, review, and deletion controls are documented.

Risk: Audit logging may not provide durable evidence for safety-critical decisions.

Mitigation: Store audit records in a durable external log before using the skill as part of production approval workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/safety-guardrails)
- [Publisher profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with command examples and JSON gate decisions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Gate decisions include a decision value, note, risk level, reasons, and audit record when used through the bundled script.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
