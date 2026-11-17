## Description:

Comprehensive stock decision analysis combining technical indicators, macro environment assessment, and historical backtesting to produce buy/sell recommendations with stop-loss and take-profit levels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pfbao](https://clawhub.ai/user/pfbao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze stock names or codes with technical indicators, macro context, backtesting, risk labels, and stop-loss/take-profit guidance. The artifact states that its output is for reference only and does not constitute investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal stock inputs can reach unsafe shell execution if a stock name or code contains shell syntax.

Mitigation: Before installation or use, change subprocess calls to argument-list execution and enforce strict stock-symbol validation.

Risk: Macro analysis performs external Bing searches and may disclose queried company, ticker, or industry terms.

Mitigation: Confirm that external search is acceptable for the operating environment and avoid sensitive watchlists or confidential investment workflows.

Risk: The financial-analysis scope is broad, and generated recommendations may be incorrect, stale, or misleading.

Mitigation: Treat outputs as decision support only, verify market data and source findings independently, and preserve the artifact's non-investment-advice disclaimer.

## Reference(s):

- [ClawHub Stock-Decision Skill Page](https://clawhub.ai/pfbao/skills/stock-decision)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with text sections, shell command examples, and JSON-like macro analysis output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes technical scores, buy/sell posture, risk level, stop-loss/take-profit levels, macro adjustment coefficients, and backtest summaries.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and changelog list 2.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
