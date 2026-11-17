## Description:

Helps agents use pay-per-call x402 APIs for LLM inference, persistent scratchpad memory, uptime monitoring, exact calculations, web scraping, SEO audits, code linting, and live crypto prices using USDC on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webberdesign](https://clawhub.ai/user/webberdesign)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent needs paid API access for inference, durable memory, monitoring, calculations, web intelligence, or code tooling without provisioning conventional API accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet signing authority may be exposed when using paid x402 calls or the MCP path with a real private key.

Mitigation: Use a low-value dedicated wallet or isolated signer, prefer a pinned and reviewed client, and require confirmation before paid actions.

Risk: Scratchpad and store endpoints persist selected data outside the agent session.

Mitigation: Do not store secrets, keys, personal data, production logs, confidential code, or other sensitive material.

Risk: Some endpoints can spend funds or post public content.

Mitigation: Require explicit user confirmation before paid calls or public board posts.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/webberdesign/skills/x402-agent-tools)
- [x402 Agent Tools homepage](https://x402.webbersites.com)
- [OpenAPI catalog](https://api.webbersites.com/openapi.json)
- [x402 discovery endpoint](https://api.webbersites.com/.well-known/x402)
- [Full endpoint examples](https://x402.webbersites.com/llms.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, plain text, and endpoint-specific API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include paid API results, stored scratchpad or collection data, monitoring reports, lint findings, generated brand assets, and public board posts depending on the endpoint used.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
