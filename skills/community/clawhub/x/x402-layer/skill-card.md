## Description:

x402 Layer helps developers and agents pay for APIs with USDC, create and manage monetized endpoints and marketplace services, handle credits and payment webhooks, and perform wallet-based agent registration, reputation, and staking workflows on supported networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivaavimusic](https://clawhub.ai/user/ivaavimusic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate USDC payments into APIs and applications, discover and consume paid services, and manage endpoints, credits, webhooks, and agent-registry workflows. Some operations sign wallet messages or submit on-chain transactions, so select a runbook and credentials appropriate to the requested action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signing tools may authorize excessive payments or unintended wallet transactions.

Mitigation: Begin with secret-free discovery; use a dedicated low-balance wallet, enforce spending limits, validate transactions, and avoid unattended direct-key operations.

Risk: Privileged credentials may grant broader access than a specific task requires.

Mitigation: Use task-specific, least-privilege credentials and approved HTTPS hosts; only enable credentials required by the chosen runbook.

Risk: Repeated or stale webhook events could trigger duplicate payment-related grants.

Mitigation: Check event freshness and implement duplicate-event protection before granting goods or credits.

## Reference(s):

- [Agent Registry and Reputation (ERC-8004 / Solana-8004)](references/agent-registry-reputation.md)
- [Agentic Endpoint Creation](references/agentic-endpoints.md)
- [World AgentKit Benefits](references/agentkit-benefits.md)
- [Credit-Based Access](references/credit-based.md)
- [Marketplace Discovery](references/marketplace.md)
- [Singularity MCP Control Plane](references/mcp-control-plane.md)
- [OpenWallet / OWS](references/openwallet-ows.md)
- [Pay-Per-Request](references/pay-per-request.md)
- [Payment Signing Reference](references/payment-signing.md)
- [Integrating Payments Into Your App](references/payments-integration.md)
- [$SGL Staking](references/staking.md)
- [Webhooks and Payment Verification](references/webhooks-verification.md)
- [XMTP Support in Studio](references/xmtp-support.md)
- [x402 Layer Documentation](https://docs.x402layer.cc/agentic-access/openclaw-skill)
- [x402 Layer Studio](https://studio.x402layer.cc)
- [ClawHub Release](https://clawhub.ai/ivaavimusic/skills/x402-layer)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, API results]

**Output Format:** [Markdown guidance with shell commands, code and configuration examples, and JSON/API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected workflow and may involve external API calls, payments, or signed on-chain transactions.]

## Skill Version(s):

1.15.0 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
