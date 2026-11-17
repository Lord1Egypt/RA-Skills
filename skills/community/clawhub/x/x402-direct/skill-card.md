## Description:

Discover and search x402-enabled services via the x402.direct directory API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jovannyespinal](https://clawhub.ai/user/jovannyespinal)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to discover x402-enabled API services, compare trust scores and pricing, retrieve service payment details, and choose endpoints for agent-to-agent paid API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The paid search endpoint can trigger wallet-backed x402 payment flows.

Mitigation: Require explicit user approval, budget limits, and retry limits before using paid search or any wallet-backed x402 client.

Risk: Directory results may include third-party services with varying trust scores and payment terms.

Mitigation: Prefer free browse/detail endpoints first, review service details and trust scores, and use score or category filters before selecting a paid service.

## Reference(s):

- [x402.direct service directory](https://x402.direct)
- [x402.org facilitator](https://x402.org/facilitator)
- [ClawHub skill page](https://clawhub.ai/jovannyespinal/skills/x402-direct)
- [Publisher profile](https://clawhub.ai/user/jovannyespinal)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with API endpoint examples, JSON response shapes, and shell or TypeScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents toward free browse/detail endpoints or the paid x402 search endpoint.]

## Skill Version(s):

1.0.0 (source: evidence release, artifact metadata, CHANGELOG released 2025-05-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
