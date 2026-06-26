## Description: <br>
Monitors Smart Money Concepts trading signals using 1H trend direction, 15M entry checks, and ATR-based stop-loss and take-profit levels for configured market symbols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zt6558609-cpu](https://clawhub.ai/user/zt6558609-cpu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and traders use this skill to run a local market-monitoring assistant that emits informational SMC trading-signal reports and risk levels for configured instruments. It is not an automatic trading system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitor contacts public market-data providers and can be scheduled hourly, so outages, stale data, or provider changes can affect signal quality. <br>
Mitigation: Review the configured symbols and data sources before enabling cron, and independently validate market data before acting on a signal. <br>
Risk: The security guidance flags code-quality and data-integrity issues, including exec() usage and disabled TLS verification in the current monitoring path. <br>
Mitigation: Prefer a fixed version that removes exec(), keeps TLS verification enabled, and review monitor_v2.py before scheduled use. <br>
Risk: The skill produces trading signals that could be mistaken for financial advice. <br>
Mitigation: Treat all outputs as informational, test with a simulated or low-risk workflow first, and apply independent risk controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zt6558609-cpu/smc-trading-signal-cn) <br>
- [Sina Finance market-data endpoint](https://hq.sinajs.cn/list=hf_GC) <br>
- [Yahoo Finance chart endpoint](https://query1.finance.yahoo.com/v8/finance/chart/GC=F) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, Markdown trading-signal reports, and JSON configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write timestamped signal Markdown files under scripts/output when signals are found.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
