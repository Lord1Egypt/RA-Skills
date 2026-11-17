## Description:

Exchange cryptocurrencies via kyc.rip aggregator API. Use when swapping, converting, or exchanging crypto assets. Supports 700+ coins, no KYC, best rates across 10+ providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xbtoshi](https://clawhub.ai/user/xbtoshi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to estimate, create, and monitor cryptocurrency swaps through the kyc.rip aggregator API, including address validation and supported-currency lookup. It is intended for workflows that need API guidance for comparing providers and preparing swap requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real-value cryptocurrency transfers where deposit instructions can be irreversible.

Mitigation: Require manual verification of destination addresses, deposit addresses, deposit amounts, memos, provider selection, and trade details before sending funds.

Risk: The skill may send wallet addresses, refund addresses, transaction amounts, provider choices, and status details to a third-party crypto API.

Mitigation: Use only when the user accepts disclosure of this wallet and transaction data to the third-party API.

Risk: The security evidence marks the release as suspicious because user-control safeguards and warnings are insufficient for financial actions.

Mitigation: Keep the agent in an advisory posture, estimate first, validate addresses, and ask for explicit user confirmation before creating trades or acting on deposit instructions.

## Reference(s):

- [KYC.RIP API](https://api.kyc.rip)
- [ClawHub skill page](https://clawhub.ai/xbtoshi/skills/swap-api)

## Skill Output:

**Output Type(s):** [guidance, API calls, JSON, markdown]

**Output Format:** [Markdown guidance with HTTP endpoint examples and JSON request/response bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes public API endpoints, query parameters, request fields, response examples, workflow steps, and error-handling notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
