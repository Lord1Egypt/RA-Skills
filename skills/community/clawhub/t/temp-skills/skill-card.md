## Description:

Integrates the OKX API for spot and contract trading, asset management, risk control, and real-time market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danihe001](https://clawhub.ai/user/danihe001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-operations users can use this skill to guide OKX spot and derivatives trading workflows, including balances, order placement, transfers, risk checks, and market data retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published account and API-key material may allow unauthorized access or misuse if treated as live credentials.

Mitigation: Treat the key as exposed, revoke or rotate it, and move any credentials to secure runtime storage before use.

Risk: The skill is intended for real OKX trading and can guide asset-affecting order placement or funds movement.

Mitigation: Require explicit user approval for state-changing actions and clearly separate testnet from mainnet operation.

Risk: Trading guidance without clear operational safeguards can produce unintended financial exposure.

Mitigation: Use logging, pause-on-exception behavior, and pre-trade risk checks for drawdown, take-profit, stop-loss, and position controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danihe001/skills/temp-skills)
- [ClawHub publisher profile](https://clawhub.ai/user/danihe001)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with inline code-style function calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose live trading actions, credential configuration, risk checks, and logging expectations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
