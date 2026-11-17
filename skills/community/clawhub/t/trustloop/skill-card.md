## Description:

TrustLoop provides an AI governance layer that logs, audits, and checks kill-switch rules for agent tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smjai](https://clawhub.ai/user/smjai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use TrustLoop to check sensitive tool calls against an external policy and audit service before execution, with dashboard visibility into logged activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tool-call arguments may contain sensitive operational details when sent to the third-party TrustLoop service.

Mitigation: Send only the minimum fields needed for policy review, keep secrets and full content out of arguments, and use a dedicated low-privilege API key.

Risk: The integration is advisory and may fail open, so it should not be treated as a hard enforcement boundary for sensitive workflows.

Mitigation: Verify fail-closed behavior and operational controls before relying on the service for high-impact actions.

Risk: Audit logs and retained tool-call metadata may create privacy or access-control obligations.

Mitigation: Review TrustLoop retention, log access, and authorization practices before deployment.

## Reference(s):

- [TrustLoop homepage](https://trustloop.live)
- [TrustLoop dashboard](https://app.trustloop.live)
- [TrustLoop skill page](https://clawhub.ai/smjai/skills/trustloop)
- [API reference](api-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit JSON allow or block decisions when using the included check script.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
