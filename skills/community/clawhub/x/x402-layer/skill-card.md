## Description:

Helps AI agents pay for API access with USDC, manage monetized endpoints and credits, handle payment webhooks, and register or manage agents across supported networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivaavimusic](https://clawhub.ai/user/ivaavimusic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to discover paid services, pay for API access, build and manage monetized endpoints, and handle related agent registration and reputation workflows. Some tasks require signing or account credentials, while read-only discovery does not.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet signing and payment actions can move funds or change on-chain state.

Mitigation: Review the destination, amount, and requested action before signing; use a dedicated low-balance or delegated wallet and never place a long-lived private key in chats, logs, or shared terminals.

Risk: The skill includes an install command that downloads and runs a remote script, and the security review reports that install path as unverified.

Mitigation: Independently review the installation source and command before running it, and avoid using valuable credentials until the installation has been reviewed.

Risk: The security review says some components were only partially inspected, including an opaque XMTP script.

Mitigation: Treat the install as high risk; inspect the partially reviewed components and address the reported transaction, payment, installation, and file-handling risks before using funded wallets or valuable credentials.

## Reference(s):

- [x402 Layer agent documentation](https://docs.x402layer.cc/agentic-access/openclaw-skill)
- [x402 Layer Studio](https://studio.x402layer.cc)
- [Pay-per-request guide](references/pay-per-request.md)
- [Endpoint management guide](references/agentic-endpoints.md)
- [Webhook verification guide](references/webhooks-verification.md)
- [Agent registry and reputation guide](references/agent-registry-reputation.md)
- [Staking guide](references/staking.md)
- [ClawHub skill release](https://clawhub.ai/ivaavimusic/skills/x402-layer)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown runbooks with Python and JavaScript examples, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No fixed output shape; examples and returned service data depend on the selected workflow.]

## Skill Version(s):

1.17.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
