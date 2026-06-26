## Description: <br>
tqsdk helps agents use the TqSdk Python futures and options SDK for market data, backtesting, simulated trading, and live order examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coderwpf](https://clawhub.ai/user/coderwpf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-focused agents use this skill to draft Python TqSdk setup, market data, backtesting, simulated trading, and order-management examples for futures and options workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Order examples can affect a real futures or options account. <br>
Mitigation: Use TqSim or backtesting first, and require explicit human confirmation with strict symbol, volume, and loss limits before any live trading. <br>
Risk: Credentials can be exposed if account details are placed in prompts, logs, or source files. <br>
Mitigation: Use environment variables or secure secret storage, and keep TqAuth values out of prompts, logs, and committed files. <br>
Risk: Market data, strategy snippets, or generated examples can be stale, incomplete, or unsuitable for a specific account. <br>
Mitigation: Validate returned data, handle missing values and API errors, and require qualified human review before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coderwpf/tqsdk) <br>
- [TqSdk documentation](https://doc.shinnytech.com/tqsdk/latest/) <br>
- [TqSdk Python project](https://github.com/shinnytech/tqsdk-python) <br>
- [ShinnyTech website](https://www.shinnytech.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; examples may reference TQ_USERNAME and TQ_PASSWORD environment variables and TqSdk account credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
