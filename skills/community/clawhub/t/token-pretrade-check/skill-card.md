## Description:

Guides agents through paid EVM token safety, liquidity, and optional market-timing checks before a trade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perria080925-bot](https://clawhub.ai/user/perria080925-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and users screen EVM tokens for safety, liquidity, and market-timing signals before deciding whether to trade. The checks provide heuristics, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token identifiers are sent to a third-party API.

Mitigation: Verify the endpoint and avoid sending identifiers you do not wish to disclose.

Risk: x402 calls can trigger USDC payments.

Mitigation: Check the quoted amount and wallet approval before authorizing each call.

Risk: Heuristic scores and market signals may be mistaken for financial advice.

Mitigation: Independently verify results and do not rely on the checklist alone for a trade.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/perria080925-bot/skills/token-pretrade-check)
- [Token check API endpoint](https://x402.bankr.bot/0xf436ca41bd0a236338bef57adeb4976677513010)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with API request examples and decision gates; API calls return JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Safety scores, liquidity metrics, and optional momentum signals; up to $0.0155 USDC per token in listed call fees.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
