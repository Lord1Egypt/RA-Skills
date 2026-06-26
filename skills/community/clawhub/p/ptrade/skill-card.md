## Description: <br>
Ptrade helps agents reference and draft Python strategy work for the Ptrade quantitative trading platform, including A-share, futures, margin, ETF, market data, and broker-server execution workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coderwpf](https://clawhub.ai/user/coderwpf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading-strategy authors use this skill as a compact Ptrade API reference for drafting, reviewing, and adapting Python strategy code before broker-side backtesting, paper testing, or approved live deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copyable examples can submit live orders, margin trades, futures trades, ETF operations, IPO subscriptions, or cancellations against real brokerage accounts. <br>
Mitigation: Test generated strategies in backtest or paper mode first and require explicit human approval before any live broker-side action. <br>
Risk: Ptrade strategies run on broker intranet servers with no external network access and limited package installation. <br>
Mitigation: Keep generated code within the broker-provided Python runtime and APIs, and avoid dependencies that require pip or internet access. <br>
Risk: Some Ptrade market-data calls are documented as unsafe to call concurrently. <br>
Mitigation: Serialize those data calls and add result validation plus exception handling around data fetches. <br>


## Reference(s): <br>
- [ClawHub Ptrade Skill Page](https://clawhub.ai/coderwpf/ptrade) <br>
- [Ptrade API Homepage](https://ptradeapi.com) <br>
- [QMT Ptrade API Reference](http://qmt.ptradeapi.com) <br>
- [BossQuant Bilibili Profile](https://space.bilibili.com/48693330) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python code examples and concise reference guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include trading API examples that require human review before use with a brokerage account.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact files also mention 1.2.0 and 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
