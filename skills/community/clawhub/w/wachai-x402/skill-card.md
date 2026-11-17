## Description:

DeFi risk analysis toolkit powered by WACH.AI via x402 payments using AWAL wallet custody for token safety, honeypot, liquidity, holder distribution, and smart contract risk checks across Ethereum, Polygon, Base, BSC, and Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akshat-mishra101](https://clawhub.ai/user/akshat-mishra101)

### License/Terms of Use:

MIT

## Use Case:

Developers, agents, and DeFi users use this skill to request paid WACH.AI token risk reports, check wallet readiness through AWAL, and interpret analysis for supported EVM chains and Solana.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each token analysis is a paid request using AWAL/x402 custody and USDC on Base.

Mitigation: Keep the default 10,000 atomic USDC cap, verify AWAL authentication and balance before paid calls, and raise spend limits only after an explicit user decision.

Risk: Private key, seed phrase, or local wallet file handling could expose signing material.

Mitigation: Use the AWAL-only custody path and do not request, store, expose, or suggest private keys, seed phrases, wallet export files, or wallet.json flows.

Risk: Payment, parsing, or readiness failures can make a report incomplete or misleading.

Mitigation: Surface payment and AWAL errors clearly, retry transient failures at most once, and claim success only when the report payload is present.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/akshat-mishra101/skills/wachai-x402)
- [WACH.AI x402 verification endpoint](https://x402.wach.ai/verify-token)
- [TokenSense report pattern](https://tokensense.wach.ai/<chain>/<tokenAddress>)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Code]

**Output Format:** [Markdown guidance with shell commands and optional TypeScript usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful reports may include market data, risk scores, honeypot analysis, holder and liquidity signals, code analysis, social and community signals, source link, and timestamp.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
