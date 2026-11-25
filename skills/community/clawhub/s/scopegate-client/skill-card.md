## Description:

Use ScopeGate to verify agent scope before any consequential action involving money, data writes, external API calls, or file system changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clauderodriguez2026-boop](https://clawhub.ai/user/clauderodriguez2026-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and agent operators use this skill to require ScopeGate authorization checks before consequential actions such as payments, data writes, external API calls, and file system changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives a third-party service control over whether covered agent actions proceed.

Mitigation: Install only when ScopeGate is intended to gate consequential actions, and review denials or service outages as stop conditions.

Risk: Authorization details are sent to a configurable endpoint.

Mitigation: Use trusted SCOPEGATE_URL values and narrowly scoped, revocable credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clauderodriguez2026-boop/skills/scopegate-client)
- [ScopeGate](https://scopegate.ai)
- [ScopeGate API endpoint](https://api.scopegate.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs agents to stop when ScopeGate denies or cannot verify a covered action.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
