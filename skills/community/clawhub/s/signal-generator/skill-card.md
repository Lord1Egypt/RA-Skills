## Description: <br>
Generates cryptocurrency trading signals from Bollinger Band Breakout or RSI Reversal strategies and records signal output for optional alerting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nititepfirm](https://clawhub.ai/user/nititepfirm) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and trading-bot operators use this skill to generate technical-analysis signals for configured crypto pairs and timeframes. The output can be reviewed directly, saved as JSON, or connected to a separate messaging wrapper for alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the local Python environment and a /root/quant-trading-bot path. <br>
Mitigation: Verify those local paths and dependencies are trusted before installing or scheduling the skill. <br>
Risk: Discord or Telegram alerts may not be sent by the skill alone. <br>
Mitigation: Add or verify a separate OpenClaw messaging wrapper before relying on external notifications. <br>
Risk: Scheduled execution can repeatedly fetch market data and update local signal output. <br>
Mitigation: Enable cron or other recurring execution only when repeated runs are intended. <br>
Risk: Generated trading signals may be mistaken for financial advice. <br>
Mitigation: Treat generated signals as informational technical-analysis output and review them before acting. <br>


## Reference(s): <br>
- [Signal Generator ClawHub Page](https://clawhub.ai/nititepfirm/signal-generator) <br>
- [README](artifact/README.md) <br>
- [Skill Documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration] <br>
**Output Format:** [Console text plus JSON signal records in last_signal.json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured symbol, strategy, intervals, targets, and filters; Discord or Telegram delivery requires a separate messaging wrapper.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
