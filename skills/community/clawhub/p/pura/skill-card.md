## Description:

Cut your OpenClaw agent's LLM costs 40-60%. Automatic model selection routes simple tasks to cheap providers, complex tasks to premium ones. Free for 5,000 requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[espetey](https://clawhub.ai/user/espetey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use Pura to route LLM requests through an OpenAI-compatible gateway that automatically selects lower-cost providers while preserving access to premium models for harder requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, account data, and bearer credentials may be routed to a configurable external gateway.

Mitigation: Use only a trusted HTTPS gateway and avoid setting PURA_GATEWAY_URL unless you control the endpoint.

Risk: Generated API keys can be printed by setup or verification flows and may appear in logs or transcripts.

Mitigation: Rotate any key exposed in logs or transcripts and avoid sharing command output that contains generated keys.

Risk: Report, income, and wallet commands are account-administrative actions that may expose spending or funded-balance information.

Mitigation: Run those commands only in authorized accounts and environments approved for account and balance operations.

## Reference(s):

- [Pura Website](https://pura.xyz)
- [Pura Documentation](https://pura.xyz/docs)
- [Pura Gateway](https://api.pura.xyz)
- [Pura ClawHub Skill Page](https://clawhub.ai/espetey/skills/pura)
- [Pura GitHub Repository](https://github.com/puraxyz/puraxyz)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, Python examples, configuration values, and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PURA_API_KEY; PURA_GATEWAY_URL can optionally override the default gateway.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
