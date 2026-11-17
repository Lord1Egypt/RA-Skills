## Description:

Pay for AI-agent API calls in USDG on Robinhood Chain via the x402 protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to configure and safely execute USDG x402 payments for Spraay gateway API calls on Robinhood Chain, including 402 challenge validation, local EIP-712 signing, and confirmation thresholds for higher-risk payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An exposed EVM_PRIVATE_KEY could allow unauthorized spending from the configured wallet.

Mitigation: Use a dedicated low-balance wallet, keep the key out of logs and prompts, and use it only for local EIP-3009 signing.

Risk: A malformed or untrusted 402 challenge could request the wrong asset, amount, recipient, or signing domain.

Mitigation: Verify the gateway origin, USDG contract, amount, payTo value, and pinned EIP-712 domain before signing.

Risk: Higher-value payments or fund-moving endpoints can transfer real funds.

Mitigation: Auto-pay only at or below $0.10, reject single calls above $1.00, and require explicit user confirmation for larger or fund-moving operations.

Risk: Automatic payment retries can create unintended repeated payment attempts.

Mitigation: Make one payment attempt per request and do not auto-retry rejected payments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/plagtech/skills/usdg-x402-payments)
- [Spraay](https://spraay.app)
- [Spraay USDG rail docs](https://docs.spraay.app/#robinhood-usdg)
- [Spraay x402 live catalog](https://gateway.spraay.app/.well-known/x402.json)
- [Spraay free endpoint index](https://gateway.spraay.app/free)
- [Robinhood Chain explorer](https://robinhoodchain.blockscout.com)
- [Robinhood Chain RPC](https://rpc.mainnet.chain.robinhood.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and EVM_PRIVATE_KEY; uses local signing and payment confirmation thresholds.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
