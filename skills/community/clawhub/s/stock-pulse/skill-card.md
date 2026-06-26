## Description: <br>
A-share stock analysis skill that accepts stock symbols and produces buy, sell, or hold signals, price levels, ASCII trend views, Monte Carlo price forecasts, and concise AI-assisted commentary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vineindalvik](https://clawhub.ai/user/vineindalvik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to inspect Chinese A-share symbols, generate stock dashboards, review intraday or daily trend summaries, and receive informational buy, sell, hold, and forecast analysis. Outputs are intended for decision support and should be reviewed before any financial action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected stock symbols, prompts, and generated analysis may be sent to the configured LLM provider. <br>
Mitigation: Use only an approved LLM endpoint and avoid entering symbols or prompts that should not be shared with that provider. <br>
Risk: Optional webhook delivery can share stock analysis with chat spaces. <br>
Mitigation: Configure webhook URLs only for destinations where recipients are authorized to see the generated analysis. <br>
Risk: Buy/sell signals, price targets, and forecasts may be inaccurate or unsuitable for a user's financial situation. <br>
Mitigation: Treat all outputs as informational decision support and review them independently before making investment decisions. <br>
Risk: Runtime dependencies and market-data packages execute in the user's Python environment. <br>
Mitigation: Install in an isolated environment and review dependency versions before deployment. <br>


## Reference(s): <br>
- [Stock Pulse ClawHub Page](https://clawhub.ai/vineindalvik/stock-pulse) <br>
- [baostock](http://baostock.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, analysis, guidance] <br>
**Output Format:** [Console text and Markdown-style reports with optional JSON-formatted analysis from the configured LLM] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include stock symbols, buy/sell/hold signals, entry and stop-loss levels, price targets, ASCII charts, Monte Carlo forecast ranges, and optional webhook messages.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
