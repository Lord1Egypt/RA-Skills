## Description: <br>
Automated trading assistant for cryptocurrency market analysis, technical signal detection, position sizing, risk management, and performance reporting using RSI, moving averages, support, and resistance strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rioo-maker](https://clawhub.ai/user/rioo-maker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze crypto market conditions, apply rule-based technical trading criteria, calculate position sizes, and produce trading performance reports. It is best suited for analysis and paper trading unless live trades are manually approved and account limits are enforced. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live trading or position-closing guidance may create financial loss if executed without oversight. <br>
Mitigation: Use the skill for analysis or paper trading unless every live order is manually approved with strict account and position-size limits. <br>
Risk: Trading signals may be incorrect, stale, or unsuitable for current market conditions. <br>
Mitigation: Validate signals against current market data, enforce the documented stop-loss and take-profit rules, and avoid trading during low volatility, high spread, or consolidation periods. <br>
Risk: Connection errors or exchange API failures can leave trades unmanaged. <br>
Mitigation: Define clear fail-safe behavior before use, including stopping new trades or closing open positions when connectivity or API errors occur. <br>


## Reference(s): <br>
- [Trading Strategies](references/trading_strategies.md) <br>
- [Performance Report Template](templates/performance_report.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance and reports with optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a position-sizing script that prints a numeric position size.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
