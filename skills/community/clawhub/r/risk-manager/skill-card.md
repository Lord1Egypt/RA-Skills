## Description:

Compute portfolio risk metrics including VaR, Sharpe ratio, and Kelly criterion using historical and real-time data from the Finskills API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finskills](https://clawhub.ai/user/finskills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and portfolio managers use this skill to estimate portfolio risk, position sizing, and hedging considerations from portfolio holdings and market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README install command points at a mutable repository URL.

Mitigation: Install from a pinned version or commit when deploying the skill.

Risk: Portfolio holdings and related questions may be sent to an external market-data provider.

Mitigation: Use a dedicated Finskills API key and avoid submitting portfolio details that should not be analyzed through third-party API queries.

Risk: Risk metrics and hedging suggestions can be wrong or incomplete because they rely on historical data and simplified assumptions.

Mitigation: Treat outputs as decision support and review calculations, assumptions, and recommendations before taking financial action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/finskills/skills/risk-manager)
- [Project homepage](https://github.com/finskills/risk-manager)
- [Finskills API](https://finskills.net)
- [Finskills API registration](https://finskills.net/register)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API calls]

**Output Format:** [Markdown risk dashboard with metrics, tables, risk flags, and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY; some historical market data may require a Finskills Pro plan.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter declares 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
