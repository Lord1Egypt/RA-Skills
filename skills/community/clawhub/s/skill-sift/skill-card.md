## Description:

Sift provides execution-governance instructions that require agents to authorize consequential actions through the Sift API before execution and proceed only with signed ALLOW receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walkojas-boop](https://clawhub.ai/user/walkojas-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use Sift to add authorization checks, signed receipts, fail-closed denials, and audit trails before agents perform consequential actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Action metadata is sent to a third-party service for authorization.

Mitigation: Review and limit the parameters sent in authorization requests before deploying the skill.

Risk: The skill gives the Sift service broad mandatory control over consequential agent actions.

Mitigation: Install only when Sift governance is intended, and confirm the configured policy matches the agent's operating scope.

Risk: Prompt-level enforcement can be bypassed if the agent does not follow the skill instructions.

Mitigation: Use a platform-enforced plugin when deterministic pre-execution control is required.

Risk: Fail-closed behavior can block work when the Sift API is unavailable or returns errors.

Mitigation: Plan operational handling for Sift outages and denial responses before relying on the skill in production workflows.

## Reference(s):

- [Sift ClawHub Skill](https://clawhub.ai/walkojas-boop/skills/skill-sift)
- [Sift Authorization API](https://api.sift.walkosystems.com/authorize)
- [Sift Challenge API](https://api.sift.walkosystems.com/auth/challenge)
- [Sift Service Setup](https://api.sift.walkosystems.com)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires tenant credentials, an agent identity, a nonce, and signed authorization requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
