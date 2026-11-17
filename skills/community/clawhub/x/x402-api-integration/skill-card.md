## Description:

Turn any function into a revenue-generating API endpoint using x402 HTTP-native payments with zero dependencies and Node 16 standard library only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiny-coder-2104](https://clawhub.ai/user/tiny-coder-2104)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create pay-per-call Node.js API endpoints with x402 payment headers, service-function examples, deployment commands, and payment verification guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default payment-gated API example can be deployed publicly while accepting forged or unverified payments.

Mitigation: Implement fail-closed facilitator verification before public deployment, await verification before service work runs, and reject access when verification fails or is unavailable.

Risk: A public paid API endpoint can be abused if exposed without normal production controls.

Mitigation: Add appropriate authentication where needed, rate limits, input limits, logging, and monitoring before exposing the service.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/tiny-coder-2104/toolbox/tree/master/clawhub-skills/x402-api-integration)
- [ClawHub skill page](https://clawhub.ai/tiny-coder-2104/skills/x402-api-integration)
- [Publisher homepage](https://tinycoderstudio.gumroad.com/l/7-agent-skills-pack)
- [x402 facilitator verification endpoint](https://x402.org/facilitator/verify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides a Node.js server template, deployment commands, pricing examples, and production payment verification guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
