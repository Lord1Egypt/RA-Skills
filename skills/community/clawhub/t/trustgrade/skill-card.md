## Description:

Helps agents assess the trust of crypto entities and AI agents, check transactions before execution, and consult crypto-security news for recent incidents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[digitalmentes7-maker](https://clawhub.ai/user/digitalmentes7-maker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check crypto entities and AI-agent identities, compare trust scores, review recent security incidents, and obtain pre-flight transaction decisions before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trust checks and crypto-security news requests depend on TrustGrade's external MCP server and API; the reviewed artifact does not include the server implementation.

Mitigation: Review the external integration before installing and independently verify consequential crypto-safety decisions.

Risk: Trust scores may be mistaken for investment advice or a guarantee of safety.

Mitigation: Treat scores as one input, not as investment advice or a substitute for independent verification.

## Reference(s):

- [TrustGrade skill on ClawHub](https://clawhub.ai/digitalmentes7-maker/skills/trustgrade)
- [TrustGrade crypto-security news archive](https://news.trustgrade.ai/archive)
- [TrustGrade crypto-security news RSS feed](https://news.trustgrade.ai/rss.xml)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Text or Markdown with trust scores, transaction decisions, and incident links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores include a letter grade, confidence, and risk level; transaction checks return an approval or rejection with reasons.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
