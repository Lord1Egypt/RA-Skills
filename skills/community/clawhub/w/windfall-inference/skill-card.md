## Description:

Windfall Inference provides an OpenAI-compatible, spatially routed LLM inference gateway that routes requests by cost and carbon intensity, supports 200+ models, and records EAS attestations on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[papa-raw](https://clawhub.ai/user/papa-raw)

### License/Terms of Use:

Business Source License 1.1

## Use Case:

Developers and external agent builders use this skill to configure agents to send OpenAI-compatible chat completion requests through Windfall for model routing, caching, payment, and energy/carbon attestations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Windfall is a third-party inference proxy that can see prompts and route them to OpenRouter.

Mitigation: Avoid production secrets and confidential prompts until the proxy handling and downstream routing risks have been reviewed.

Risk: The security evidence flags review-worthy issues around wallet-linked accounts, dashboard XSS, and browser credential storage.

Mitigation: Review wallet authentication and dashboard flows before using sensitive wallets, accounts, or API keys.

Risk: The security evidence flags payment/proxy trust, dependency, and deployment-script concerns.

Mitigation: Address those issues and deploy in a controlled environment before relying on the service for sensitive or production workloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/papa-raw/skills/windfall-inference)
- [Publisher profile](https://clawhub.ai/user/papa-raw)
- [Windfall homepage](https://windfall.ecofrontiers.xyz)
- [Windfall chat completions endpoint](https://windfall.ecofrontiers.xyz/v1/chat/completions)
- [Testing guide](testing-guide.md)
- [License](LICENSE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, environment variables, and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WINDFALL_API_KEY for API-key use; x402 payment is also described for wallet-based requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
