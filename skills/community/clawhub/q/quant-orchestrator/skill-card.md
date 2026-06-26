## Description: <br>
Multi-Agent AI Quant System with multi-coin prediction, strategy templates, and automated backtesting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pikachu022700](https://clawhub.ai/user/pikachu022700) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and quantitative trading researchers use this skill to generate cryptocurrency market signals, strategy templates, automated backtests, and research reports. Outputs should be reviewed before use because the security evidence flags billing behavior and cautions that trading signals and backtests are research aids, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports under-explained billing code that can contact a payment service and attempt charges. <br>
Mitigation: Review the billing code before installation, require explicit user confirmation before any charge or payment-link creation, and ask the publisher to document pricing and minimum deposit terms. <br>
Risk: The artifact includes a hard-coded payment API key according to the security guidance. <br>
Mitigation: Require the publisher to move the API key out of source and rotate any exposed credential before deployment. <br>
Risk: Generated trading signals and backtests can be mistaken for investment advice. <br>
Mitigation: Treat generated predictions, strategies, and backtests as research-only outputs and require independent financial and operational review before any trading use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pikachu022700/quant-orchestrator) <br>
- [ClawDIS homepage metadata](https://clawhub.com/quant-orchestrator) <br>
- [Hyperliquid market data API endpoint referenced by artifact](https://api.hyperliquid.xyz/info) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Configuration, API Calls] <br>
**Output Format:** [Python dictionaries, markdown research reports, generated strategy code, and YAML workflow configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cryptocurrency signals, confidence scores, strategy templates, backtest metrics, payment-link responses, and saved markdown reports.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
