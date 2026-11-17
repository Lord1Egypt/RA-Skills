## Description:

Human-readable on-chain transaction receipt that resolves transaction status, fees, and intent for transfers, swaps, approvals, DeFi-style calls, and NFT mint or transfer activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bevanding](https://clawhub.ai/user/bevanding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users can use this skill to turn a Bitcoin or EVM transaction hash into a concise, human-readable receipt with status, fees, fund flow, and a plain-language interpretation of common transaction intents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transaction hashes are sent to Tokenview and public blockchain endpoints.

Mitigation: Use the skill only when sharing transaction hashes with those services is acceptable for the use case.

Risk: The optional Tokenview API key is used in URL-based curl requests and may be visible in local process or URL logs.

Mitigation: Use a low-privilege API key, avoid pasting secrets into chat, and review local logging exposure before enabling the key.

Risk: A user-configured rate-limit file path can be rewritten by the skill.

Mitigation: Set TRANSACTION_RECEIPT_RATE_FILE only to a dedicated, non-critical state file path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bevanding/skills/transaction-receipt)
- [Source Repository](https://github.com/AntalphaAI/transaction-receipt)
- [Tokenview](https://tokenview.io)
- [Ethereum PublicNode](https://ethereum.publicnode.com)
- [Blockstream API](https://blockstream.info/api)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown transaction receipt or concise plain-text error guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transaction status, overview, interaction summary, fees, and a one-line takeaway; avoids raw upstream response bodies.]

## Skill Version(s):

1.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
