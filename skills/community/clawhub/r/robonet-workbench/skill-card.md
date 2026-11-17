## Description:

Robonet's MCP server helps agents build, backtest, optimize, and deploy crypto and prediction-market trading strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickemmons](https://clawhub.ai/user/nickemmons)

### License/Terms of Use:


## Use Case:

External developers and traders use this skill to explore market data, generate and refine strategy code, backtest performance, manage credits, and deploy vetted strategies to Hyperliquid or Polymarket workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live deployment tools can affect real funds, including losses, fees, liquidation, and continued remote trading until stopped.

Mitigation: Before calling deployment_create or deployment_start, explicitly confirm the account, symbol, leverage, wallet or vault, capital at risk, and acceptance of possible losses.

Risk: Generated or refined trading strategies may be incorrect, overfit, or unsuitable for current market conditions.

Mitigation: Backtest every generated or modified strategy across adequate and varied historical periods before considering live deployment.

Risk: AI generation, optimization, and deployment tools can incur USDC credit costs.

Mitigation: Check credit balance and review tool pricing before running expensive generation, optimization, enhancement, or deployment operations.

## Reference(s):

- [Robonet Skill Page](https://clawhub.ai/nickemmons/skills/robonet-workbench)
- [Robonet Dashboard](https://robonet.finance)
- [Robonet MCP Tools Catalog](shared-references/tool-catalog.md)
- [Jesse Framework Docs](https://jesse.trade)
- [Allora Network](https://allora.network)
- [Hyperliquid](https://hyperliquid.xyz)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown guidance with MCP tool calls and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce strategy code, backtest results, deployment configuration, account information, and cost-related guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
