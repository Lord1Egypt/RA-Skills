## Description:

Use Wiz for current market prices, macro mood, Market Track, movers, global TradingWizard bots, ranked opportunities, Bot Fund performance, and optional private account tools through OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hugors00](https://clawhub.ai/user/hugors00)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use Wiz to retrieve live market context, TradingWizard bot signals, Bot Fund performance, and optional private TradingWizard workspace information. It supports market research and paper-trading workflows, not real-money trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market data, bot signals, and Bot Fund performance may be mistaken for personalized financial advice or guaranteed returns.

Mitigation: Present market information as educational context, separate observed data from interpretation, and avoid promises about future returns.

Risk: Optional OAuth can expose private TradingWizard workspace data and supported paper-trading controls.

Mitigation: Request OAuth only for private account features, do not request or expose credentials in chat, and require clear confirmation before any paper control.

Risk: Users may confuse paper-trading controls with real-money trading.

Mitigation: State that Wiz supports paper trading only and never claim that it places real-money trades.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hugors00/skills/wiz-by-tradingwizard)
- [TradingWizard MCP connection page](https://www.tradingwizard.ai/mcp?client=openclaw#connect)
- [TradingWizard MCP documentation](https://www.tradingwizard.ai/docs/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with market summaries, evidence notes, and setup command blocks when connection guidance is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public read-only market tools when available; optional private workspace and paper-trading controls require TradingWizard OAuth and clear user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
