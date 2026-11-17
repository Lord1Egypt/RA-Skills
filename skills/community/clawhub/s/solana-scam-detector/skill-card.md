## Description:

Detects potentially scam Solana tokens before trading by checking ticker patterns, token age signals, and known scam mints while remaining read-only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ammkode](https://clawhub.ai/user/ammkode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform a read-only pre-trade review of Solana token mints and symbols, returning safety issues that can inform further due diligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A safe result can be misleading because the token-age check may not prove token age and can fail open.

Mitigation: Do not rely on this skill as proof that a token is old or low-risk; independently verify creation age, liquidity, and market context before trading.

Risk: Public Solana RPC endpoints may expose IP addresses and query patterns.

Mitigation: Use a trusted private RPC endpoint when privacy or operational sensitivity matters.

Risk: The skill depends on Node.js and @solana/web3.js.

Mitigation: Use a pinned dependency install and review dependency updates before deploying the skill in a production agent.

## Reference(s):

- [Solana Scam Detector on ClawHub](https://clawhub.ai/ammkode/skills/solana-scam-detector)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript usage snippets and JSON-like safety results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Solana RPC checks; no wallet key, signing, Telegram ID, or trade history required.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
