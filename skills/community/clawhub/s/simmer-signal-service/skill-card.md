## Description: <br>
Professional trading-signal service powered by Simmer and Binance that returns BUY, SELL, or HOLD recommendations with confidence scores for BTC, ETH, and SOL fast markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NickQi688](https://clawhub.ai/user/NickQi688) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to request paid crypto prediction-market signals, check billing balance, and configure recurring signal checks for BTC, ETH, or SOL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The advertised per-signal price conflicts with the actual charge observed in the evidence. <br>
Mitigation: Review billing details before installation and assume real non-demo signal calls may charge 0.01 USDT unless the publisher verifies otherwise. <br>
Risk: Recurring cron examples can trigger repeated paid calls. <br>
Mitigation: Enable scheduled execution only intentionally, and use spending limits or monitoring before running recurring paid signal checks. <br>
Risk: The skill depends on paid trading signals that may influence financial decisions. <br>
Mitigation: Treat outputs as informational signals, verify market context independently, and avoid automated trading without separate risk controls. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/NickQi688/simmer-signal-service) <br>
- [SkillPay](https://skillpay.me) <br>
- [Simmer Markets](https://simmer.markets) <br>
- [ClawHub](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance, Shell commands, Configuration] <br>
**Output Format:** [JSON trading-signal responses and Markdown instructions with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SkillPay and Simmer credentials; supports BTC, ETH, and SOL with a configurable minimum confidence threshold.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
