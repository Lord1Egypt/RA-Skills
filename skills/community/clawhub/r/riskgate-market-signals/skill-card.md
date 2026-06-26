## Description: <br>
Real-time crypto market intelligence for autonomous agents. Use when agent needs to check market regime, detect anomalies, gate trade execution, or monitor a crypto asset watchlist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PaperBuddha](https://clawhub.ai/user/PaperBuddha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to query RiskGate market signals, monitor supported crypto assets, detect anomalies, and gate trading or significant execution decisions with human escalation rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RiskGate API keys or M2M credentials are sent to RiskGate for authentication. <br>
Mitigation: Use limited credentials, keep secrets out of logs and shared files, and prefer environment variables for paid keys. <br>
Risk: Market signals could be misused as the sole authorization for trades or other financial actions. <br>
Mitigation: Require separate trading limits and human approval rules before execution, especially for high-severity anomalies, downtrends, volatile regimes, or API failures. <br>
Risk: Demo-tier limits or API failures can leave the agent without fresh market-signal data. <br>
Mitigation: Treat exhausted credits, rate limits, and 5xx responses as reasons to halt or pause execution and notify a human instead of assuming conditions are safe. <br>


## Reference(s): <br>
- [RiskGate Market Signals Skill](https://clawhub.ai/PaperBuddha/riskgate-market-signals) <br>
- [RiskGate API Base](https://api.riskgate.xyz) <br>
- [RiskGate Full API Reference](api-reference.md) <br>
- [RiskGate Agent Gate Decision Logic](decision-logic.md) <br>
- [RiskGate Monitoring and Reporting Pattern](monitoring.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, shell commands, markdown, configuration] <br>
**Output Format:** [Markdown with API request examples and JSON response schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use RISKGATE_API_KEY or demo credentials to authenticate requests to RiskGate.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
