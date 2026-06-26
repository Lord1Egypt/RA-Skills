## Description: <br>
Quant Full Stack supports an A-share stock quantitative trading workflow covering data collection, factor analysis, strategy construction, backtesting, simulated trading, and risk management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhdhappy](https://clawhub.ai/user/yhdhappy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative trading practitioners use this skill to run a local A-share quant workflow for data acquisition, alpha factor work, strategy construction, backtesting, simulated execution, and risk iteration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute local quant-trading workflow scripts without clear per-task safeguards or confirmation. <br>
Mitigation: Review the local ~/quant_trading scripts before use and require explicit approval before running workflow tasks. <br>
Risk: The simulated trade execution workflow could reach live broker credentials or place live orders if the local project is configured that way. <br>
Mitigation: Use a sandbox or paper-trading account and confirm 05_trade_execution cannot access real broker credentials or place live orders without explicit approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yhdhappy/quant-full-stack) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON status objects with local script stdout or stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs mapped Python scripts from an existing ~/quant_trading project with a 120-second execution timeout.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, config.yaml, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
