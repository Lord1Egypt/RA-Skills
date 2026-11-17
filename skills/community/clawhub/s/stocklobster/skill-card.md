## Description:

Monitor StockLobster webhook alerts through OpenClaw and route screened stock signals to chat channels such as Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[l3g](https://clawhub.ai/user/l3g)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure, document, test, and troubleshoot StockLobster webhook ingestion through OpenClaw, including hook mappings, payload templates, and outbound delivery to Telegram or another supported channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents routing raw webhook text into the main OpenClaw agent through a bearer-token HTTP endpoint.

Mitigation: Restrict the hook to trusted senders, use HTTPS or a private tunnel, rotate a dedicated hooks token, and avoid exposing the endpoint directly on an untrusted network.

Risk: The documented mapping does not clearly validate structured fields or isolate webhook handling from the main agent.

Mitigation: Prefer structured field validation and a dedicated low-privilege notification agent before production deployment.

## Reference(s):

- [StockLobster Payload Format](references/payload-format.md)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OpenClaw hook mapping guidance, payload examples, curl test commands, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
