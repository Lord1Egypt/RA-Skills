## Description: <br>
Quant Trading CN helps agents provide quantitative-trading guidance for Indian equity workflows, including strategy generation, backtesting, live-trading considerations, and Zerodha or A-share adaptation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and traders use this skill to design, review, and improve quantitative trading bots for Indian-market workflows, with attention to backtest-live parity, Zerodha integration, risk controls, and A-share adaptation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide users toward unreviewed trading scripts or live broker workflows that can affect real money. <br>
Mitigation: Inspect generated or referenced code before running it, test in paper or backtest mode, and require explicit confirmation before any live order placement. <br>
Risk: Broker credentials and account data could be exposed if copied into shared files or generated bot outputs. <br>
Mitigation: Keep broker credentials out of shared files and use local secret management or environment variables with least-privilege access. <br>
Risk: Trading strategies generated from guidance can lose capital if used without appropriate controls. <br>
Mitigation: Set strict capital, position-size, and risk limits before any live trading workflow is enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guohongbin-git/quant-trading-cn) <br>
- [COMPREHENSIVE TRADING LEARNINGS FROM CLAUDE CODE HISTORY](references/KNOWLEDGE_en.md) <br>
- [NUANCES: Token-Burning Gotchas & First-Time Precautions](references/NUANCES_en.md) <br>
- [AlgoTrader: Quantitative Trading Skill for Claude Code](references/README_en.md) <br>
- [Zerodha Kite Connect](https://kite.trade/) <br>
- [Zerodha instruments endpoint](https://api.kite.trade/instruments) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose trading-bot code, configuration steps, and review findings; generated trading workflows should be tested in paper or backtest mode before live use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
