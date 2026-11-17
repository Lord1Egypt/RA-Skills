## Description:

Praesidia helps agents verify AI agents, check 0-100 trust scores, fetch A2A agent cards, discover marketplace agents, and apply security, compliance, and moderation guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msoica](https://clawhub.ai/user/msoica)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to evaluate whether agents are trustworthy, discover suitable public agents, inspect A2A agent cards, and manage security or compliance guardrails for their agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live guardrails for agents.

Mitigation: Confirm guardrail changes before applying them and test guardrail behavior before enabling production use.

Risk: The skill can send sensitive content or API keys to configurable API endpoints.

Mitigation: Use trusted HTTPS API destinations, avoid production keys with custom or local endpoints, and do not submit secrets, regulated data, or confidential messages unless that data transfer is acceptable.

## Reference(s):

- [Praesidia homepage](https://praesidia.ai)
- [Praesidia API documentation](https://app.praesidia.ai/docs/api)
- [A2A protocol](https://a2a-protocol.org)
- [ClawHub skill listing](https://clawhub.ai/msoica/skills/skills-a2a)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with inline JavaScript, JSON, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses PRAESIDIA_API_KEY and may call a configured Praesidia API endpoint.]

## Skill Version(s):

1.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
