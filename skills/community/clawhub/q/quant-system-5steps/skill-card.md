## Description: <br>
5-Step Quant Trading System with multi-source data, enhanced ML models, and 15+ strategy templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pikachu022700](https://clawhub.ai/user/pikachu022700) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and quantitative analysts use this skill to run a five-step crypto market analysis pipeline that collects market data, calculates indicators, trains a model, generates strategy code, and backtests the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried trading symbols and request timing may be sent to Binance and Hyperliquid market-data APIs. <br>
Mitigation: Run only when that disclosure is acceptable for the intended workflow. <br>
Risk: The skill can fall back to synthetic market history if live historical data is unavailable. <br>
Mitigation: Check whether outputs used real market history or synthetic fallback data before relying on backtest metrics. <br>
Risk: Trading signals, backtests, and optimization suggestions may be mistaken for financial advice. <br>
Mitigation: Treat results as research output and independently validate them before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pikachu022700/quant-system-5steps) <br>
- [ClawHub metadata homepage](https://clawhub.com/quant-system-5steps) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Python return dictionary with console text and embedded strategy code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes market indicators, model signal, strategy template, backtest metrics, and optimization suggestions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
