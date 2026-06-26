## Description: <br>
Stock Simulator helps users practice virtual stock investing, record simulated trades, review returns, and learn investment analysis across A-share, Hong Kong, and U.S. markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KingDevatil](https://clawhub.ai/user/KingDevatil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and learners use this skill to simulate buying stocks, track virtual holdings and returns, and review market-oriented recommendations without using real funds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evidence security guidance notes powerful workflow behavior and recommends attention before using sensitive commands. <br>
Mitigation: Review proposed commands and generated code before execution, especially when they can affect accounts, public project state, or external review tools. <br>
Risk: The skill uses free third-party market data APIs that may be delayed, unavailable, or rate limited. <br>
Mitigation: Treat outputs as educational simulation data, confirm market data independently, and avoid using the skill as financial advice. <br>


## Reference(s): <br>
- [Stock API Reference](references/stock_api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/KingDevatil/stock-simulator) <br>
- [East Money Market Data API](https://push2.eastmoney.com/) <br>
- [Yahoo Finance Chart API](https://query1.finance.yahoo.com/v8/finance/chart/) <br>
- [iTick Documentation](https://docs.itick.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference external market-data APIs and local workspace files for simulated portfolio state.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
