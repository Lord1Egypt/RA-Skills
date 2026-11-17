## Description:

Analyze text sentiment on a scale from -1 (negative) to +1 (positive) using Expanso Edge pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aronchick](https://clawhub.ai/user/aronchick)

### License/Terms of Use:


## Use Case:

Developers and operators can use this skill to score submitted text as positive, negative, or neutral and receive a numeric sentiment score and confidence value.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTTP/MCP mode can expose an unauthenticated scoring endpoint that may spend the operator's OpenAI API quota.

Mitigation: Use CLI mode for local-only use, or bind the HTTP server to localhost and place any remote deployment behind authentication, request-size limits, rate limits, and OpenAI spending controls.

Risk: Submitted text may be sent to OpenAI when using the provided OpenAI-backed pipelines.

Mitigation: Do not submit sensitive text unless the operator is comfortable sending it to OpenAI.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aronchick/skills/sentiment-score)
- [Publisher Profile](https://clawhub.ai/user/aronchick)
- [Expanso](https://expanso.io)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON sentiment output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The sentiment result includes score, label, confidence, and metadata fields.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
