## Description:

Pre-execution transaction safety check for autonomous AI agents that calls the SENTINEL trust oracle on Base before signing and returns a SAFE, UNSAFE, or UNKNOWN verdict, a 0-100 score, and an ed25519-signed receipt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teodorofodocrispin-cmyk](https://clawhub.ai/user/teodorofodocrispin-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and autonomous-agent operators use this skill to request a paid pre-signing safety verdict for Base transactions before funds move. It is suited for agents that can transmit unsigned transaction details to a third-party service and sign x402 EIP-3009 USDC payment authorizations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to make autonomous USDC payments for guard checks.

Mitigation: Use a dedicated low-balance Base USDC wallet and enforce local per-call, session, daily, and retry budgets before signing payment authorizations.

Risk: Unsigned transaction payloads, including calldata, are sent to a third-party service for evaluation.

Mitigation: Do not use the service for sensitive calldata that cannot leave the local environment, and review data handling requirements before deployment.

Risk: Incorrect payment destination, network, asset, tier, nonce, or expiry checks could cause unintended authorization behavior.

Mitigation: Validate the HTTPS origin, Base network, USDC contract, expected payTo address, quoted tier, nonce, and authorization expiry before signing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/teodorofodocrispin-cmyk/skills/sentinel-public)
- [Project homepage](https://github.com/teodorofodocrispin-cmyk/sentinel-public)
- [SENTINEL guard API](https://sentinel-agent.dev/v1/guard)
- [Health endpoint and receipt signer](https://sentinel-agent.dev/health)
- [Pricing](https://sentinel-agent.dev/pricing)
- [LLM-readable documentation](https://sentinel-agent.dev/llms.txt)
- [MCP server](https://sentinel-agent.dev/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on HTTP POST requests, x402 payment handling, verdict interpretation, and signed receipt verification.]

## Skill Version(s):

1.1.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
