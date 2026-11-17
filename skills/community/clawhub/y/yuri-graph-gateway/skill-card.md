## Description:

A transparent proxy usage guide for calling Facebook Graph API endpoints through Yuri Graph Gateway with a Yuri API token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuriskills](https://clawhub.ai/user/yuriskills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external API users use this skill to configure calls to Facebook Graph API endpoints through the Yuri Graph Gateway by replacing the Graph API domain and using a Yuri platform token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The proxy can route high-impact Facebook Graph API actions through a third-party provider.

Mitigation: Use least-privilege test or sandbox Facebook resources until provider authorization isolation, token storage, log redaction, and deletion controls are verified.

Risk: Yuri tokens may be exposed when passed in URLs, shell history, browser history, or logs.

Mitigation: Prefer body-based secret handling where available, keep tokens in a secret manager or environment variable, and rotate or revoke any token that may have been exposed.

## Reference(s):

- [Baiz AI Homepage](https://baiz.ai)
- [Yuri Graph Gateway on ClawHub](https://clawhub.ai/yuriskills/skills/yuri-graph-gateway)
- [Yuri Graph Gateway Endpoint](https://facebook-graph.baiz.ai)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with curl examples and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a sensitive YURI_TOKEN credential.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
