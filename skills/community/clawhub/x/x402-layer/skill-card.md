## Description: <br>
x402-layer helps agents pay for APIs with USDC, deploy monetized endpoints, manage credits, webhooks, marketplace listings, wallet-first ERC-8004 registration and reputation, support flows, and $SGL staking across Base, Ethereum, Polygon, BSC, Monad, and Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivaavimusic](https://clawhub.ai/user/ivaavimusic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let agents discover, pay for, create, list, and manage x402 monetized endpoints, products, credits, webhooks, and marketplace resources. It also supports wallet-based agent registration, reputation feedback, support messaging, and Solana $SGL staking when the user explicitly authorizes signing or owner-scoped actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend funds and submit blockchain transactions. <br>
Mitigation: Use low-balance or delegated wallets and inspect every payment, staking, registration, or reputation action before execution. <br>
Risk: Owner-scoped credentials can manage or remove account resources such as endpoints, webhooks, campaigns, or support access. <br>
Mitigation: Use scoped API keys or PATs only for the selected runbook and confirm delete, revoke, webhook, and campaign operations before allowing the agent to run them. <br>
Risk: Wallet keys and service tokens grant sensitive authority when exposed to the agent runtime. <br>
Mitigation: Prefer AWAL, OWS, endpoint-scoped keys, or ephemeral wallets, and avoid loading credentials that are not needed for the current task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivaavimusic/x402-layer) <br>
- [x402 Layer Studio](https://studio.x402layer.cc) <br>
- [OpenClaw Skill Documentation](https://docs.x402layer.cc/agentic-access/openclaw-skill) <br>
- [Agentic Endpoint Creation](references/agentic-endpoints.md) <br>
- [Integrating Payments Into Your App](references/payments-integration.md) <br>
- [Webhooks and Payment Genuineness Verification](references/webhooks-verification.md) <br>
- [Agent Registry and Reputation](references/agent-registry-reputation.md) <br>
- [$SGL Staking](references/staking.md) <br>
- [Payment Signing Reference](references/payment-signing.md) <br>
- [OpenWallet / OWS](references/openwallet-ows.md) <br>
- [Singularity MCP Control Plane](references/mcp-control-plane.md) <br>
- [XMTP Support in Studio](references/xmtp-support.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, API calls, Markdown] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include wallet, payment, endpoint, webhook, marketplace, support, or staking runbooks; signing and write actions require explicit user-selected credentials.] <br>

## Skill Version(s): <br>
1.14.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
