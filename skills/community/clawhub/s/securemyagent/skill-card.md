## Description:

Security checkup for this agent. Scores the machine 0-100 (exposed gateway, plaintext secrets, risky skills and MCP servers, broad tool scopes) and gives exact fixes. Use when asked to check, harden or score the agent, before installing a skill or MCP server, or on a weekly heartbeat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[securemyagent](https://clawhub.ai/user/securemyagent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to assess an agent setup, review skills and MCP servers before installation, and get concrete security hardening steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The weekly routine can upload security findings without clearly established user consent.

Mitigation: Keep checks local unless the user explicitly approves remote reporting and public score visibility; require that choice for recurring uploads too.

Risk: The external package implementation, redaction guarantees, and provenance were not independently verified.

Mitigation: Review the package and its data handling before enabling uploads or relying on their redaction claims.

Risk: Fix commands can change hooks, vault settings, or gateway configuration.

Mitigation: Inspect each proposed change and get user approval before applying it.

## Reference(s):

- [SecureMyAgent documentation](https://securemyagent.ai/docs)
- [Guard documentation](https://securemyagent.ai/docs/guard)
- [SecureMyAgent security page](https://securemyagent.ai/security)
- [Guard on the Entity Gateway](https://securemyagent.ai/articles/guard-every-model-call)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Text or Markdown with a security score, findings, remediation guidance, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some remediation commands change local settings and require human approval.]

## Skill Version(s):

1.5.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
