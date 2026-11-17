## Description:

Tator Trader builds unsigned crypto trade transactions from natural-language prompts via Tator's AI trading API across supported chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azep-ninja](https://clawhub.ai/user/azep-ninja)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to prepare natural-language crypto trading, swapping, bridging, transfer, perpetuals, prediction-market, token-launch, naming, and yield requests. The skill returns unsigned transactions or guidance that users must review before signing and broadcasting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote-built transaction payloads may be unsafe if signed without independent review.

Mitigation: Require explicit user approval, decode and simulate each transaction, and verify chainId, to, value, calldata, spender approvals, and description before signing or broadcasting.

Risk: Wallet misuse or key exposure can lead to loss of funds.

Mitigation: Use a dedicated low-balance wallet, never paste seed phrases or private keys, prefer managed wallet integrations, and enforce spending limits.

Risk: One AgentWallet example can broadcast transactions returned by a remote builder.

Mitigation: Do not use the broadcast sample as-is; add a verification gate and user approval before any send-transaction call.

Risk: Unknown or newly launched tokens may be malicious or impossible to sell.

Mitigation: Scan unknown tokens before buying and treat scan results as point-in-time evidence that should be refreshed.

## Reference(s):

- [Tator x402 Payment & Integration Reference](references/REFERENCE.md)
- [Supported Chains Reference](references/chains.md)
- [Tator Docs](https://docs.quickintel.io/tator)
- [x402 Protocol](https://www.x402.org)
- [Tator Accepted Payments Discovery Endpoint](https://x402.quickintel.io/accepted)
- [ClawHub Skill Page](https://clawhub.ai/azep-ninja/skills/tator-trader)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, JavaScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces unsigned transaction details and wallet-integration guidance; x402 API requests cost $0.20 USDC or USDM.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
