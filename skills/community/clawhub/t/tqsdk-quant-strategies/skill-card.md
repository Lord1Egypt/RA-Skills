## Description: <br>
Provides TqSdk-based quantitative trading strategy guidance, backtesting support, optimization suggestions, and code templates covering trend, arbitrage, hedging, multi-factor, and AI-assisted strategies. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[gaingush](https://clawhub.ai/user/gaingush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative trading researchers use this skill to select, inspect, adapt, and test TqSdk strategy templates for futures-oriented research, simulation, and strategy prototyping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Executable TqSdk strategy scripts can place or manage trades and may affect real accounts if connected to live credentials. <br>
Mitigation: Run only with TqSim or paper-trading accounts until the user has added explicit live-mode controls, position limits, and stop or kill-switch behavior. <br>
Risk: Security evidence reports embedded live-looking credentials in the trading scripts. <br>
Mitigation: Remove and rotate exposed credentials, then use environment variables or interactive prompts for authentication. <br>
Risk: Trading strategy templates may be mistaken for investment advice or production-ready systems. <br>
Mitigation: Treat outputs as research and development guidance, validate with simulation and backtesting, and require human review before any live deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaingush/tqsdk-quant-strategies) <br>
- [TqSdk official documentation](https://doc.shinnytech.com/tqsdk/latest/) <br>
- [TqSdk quickstart](https://doc.shinnytech.com/tqsdk/latest/quickstart.html) <br>
- [TqSdk API reference](https://doc.shinnytech.com/tqsdk/latest/reference/index.html) <br>
- [TqSdk GitHub repository](https://github.com/shinnytech/tqsdk-python) <br>
- [ShinnyTech](https://www.shinnytech.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown explanations with Python code references, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include trading-strategy recommendations, code-level debugging notes, TqSdk usage guidance, and risk reminders for simulation-first validation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
