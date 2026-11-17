## Description:

RiskOfficer helps agents manage virtual portfolios, calculate VaR, Monte Carlo, and stress-test risk metrics, run pre-trade checks, analyze portfolio correlations, and optimize allocations through the RiskOfficer API.

This skill is for research and development only.

## Publisher:

[mib424242](https://clawhub.ai/user/mib424242)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to inspect RiskOfficer portfolios, run risk analytics, compare portfolio states, perform virtual portfolio optimization, and prepare pre-trade checks before making decisions outside the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an account-level RiskOfficer token that can access portfolio data and broker-synced positions for analysis.

Mitigation: Install only when the publisher is trusted, prefer RISK_OFFICER_TOKEN as a session environment variable, and revoke or rotate the token when access is no longer needed.

Risk: Portfolio deletion, broker snapshot deletion, optimization apply, and broker disconnect actions can materially change RiskOfficer-side records or require reconnection.

Mitigation: Review the proposed change and require explicit user confirmation before allowing those API calls.

Risk: Portfolio operations are virtual and analytical; users could mistake optimization or pre-trade output for executed broker activity.

Mitigation: Keep broker sync read-only, state that no real broker orders are placed by the skill, and require users to execute real trades outside the agent.

Risk: Currency and data-history constraints can make risk calculations incomplete or unavailable.

Mitigation: Validate tickers and currency before portfolio changes, keep single-currency portfolios, and explain insufficient-history errors before suggesting alternate methods.

## Reference(s):

- [RiskOfficer ClawHub Page](https://clawhub.ai/mib424242/skills/riskofficer)
- [RiskOfficer Homepage](https://riskofficer.tech)
- [Academic and Technical References](references/academic-references.md)
- [VaR and CVaR Methodology](references/methodology-var.md)
- [Risk Parity Methodology](references/methodology-risk-parity.md)
- [Black-Litterman Optimization Methodology](references/methodology-black-litterman.md)
- [Pre-Trade Check Methodology](references/methodology-pre-trade.md)
- [Cross-Portfolio PnL Correlation Methodology](references/methodology-correlation.md)
- [Monte Carlo Simulation Methodology](references/methodology-monte-carlo.md)
- [Stress Test Methodology](references/methodology-stress-test.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl command examples and JSON request and response snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a RiskOfficer account token in RISK_OFFICER_TOKEN for live API requests]

## Skill Version(s):

4.3.0 (source: ClawHub release evidence and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
