## Description:

Build your own pay-per-call API with the x402 standard: FastAPI, payment manifest, API keys, and an MCP wrapper for selling data or services per call in USDC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northcap-group](https://clawhub.ai/user/northcap-group)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and builders use this skill to scaffold a paid pay-per-call API with FastAPI, x402 discovery metadata, USDC payment verification, API key gating, and an MCP wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The template is intended to run as a public FastAPI service with payment and API-key gates, so insecure deployment or default secrets could expose paid endpoints.

Mitigation: Before production use, set your own PAYMENT_WALLET and KEY_SECRET, review the generated service configuration, and deploy only in an environment you control.

Risk: API keys are stored in api_keys.json, which could expose customer access if committed or shared.

Mitigation: Keep api_keys.json out of version control and protect it as credential material.

Risk: Credential routing depends on environment-controlled endpoints such as X402_BASE, so a modified environment can redirect API key traffic.

Mitigation: Configure X402_BASE only to a trusted HTTPS API host and avoid shared environments where another party can modify these variables.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/northcap-group/skills/x402-api-builder)
- [Publisher profile](https://clawhub.ai/user/northcap-group)
- [Base mainnet RPC endpoint](https://mainnet.base.org)
- [Telegram API endpoint](https://api.telegram.org)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python/FastAPI template code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a template API service, client, and MCP wrapper that require user-provided payment, API key, host, and deployment configuration.]

## Skill Version(s):

1.0.13 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
