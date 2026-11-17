## Description:

Current geo-tagged world news for agents, split into viewpoints with a count of the media, social and on-the-ground posts behind each.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quorumz](https://clawhub.ai/user/quorumz)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent for current geo-tagged news and distinct viewpoints about a country, conflict, or public story, including supporting source counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to sign server-requested payments without an approval step or spending limit.

Mitigation: Keep automatic wallet signing disabled unless payments are explicitly authorized with per-call and total budgets, and validate recipients, tokens, and networks. Do not let an exhausted API-key balance trigger automatic wallet payments.

## Reference(s):

- [Quorumz agent service](https://sense.quorumz.com/agents)
- [Quorumz agent documentation](https://sense.quorumz.com/agents/docs)
- [Quorumz API OpenAPI specification](https://api.quorumz.com/openapi.json)
- [x402 payment discovery](https://api.quorumz.com/.well-known/x402)
- [Quorumz machine-readable overview](https://sense.quorumz.com/llms.txt)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Concise news summaries with labeled viewpoints and supporting source counts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Current results vary with the requested country, stream, and available coverage.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
