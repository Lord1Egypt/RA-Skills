## Description: <br>
Monitors sports betting odds movement across Asian handicap, European odds, and over/under markets, then reports changes and betting-risk signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to monitor sports match odds, compare line movement across markets, and receive concise reports on notable changes, anomalies, and follow-up posture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SkillPay billing can attempt a 0.01 USDT charge for the configured user identity. <br>
Mitigation: Confirm the SKILLPAY_USER_ID before use and require explicit host approval before each paid invocation. <br>
Risk: The artifact includes SkillPay credential material and requires sensitive payment configuration. <br>
Mitigation: Rotate or replace embedded billing credentials with platform-managed secrets before deployment. <br>
Risk: Betting-related reports may influence wagering decisions and can be incorrect or incomplete. <br>
Mitigation: Treat outputs as informational analysis, require human review, and follow applicable betting laws and internal policies. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/shenmeng/shenmeng-odds-movement-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/shenmeng) <br>
- [The Odds API endpoint](https://api.the-odds-api.com/v4) <br>
- [SkillPay billing provider](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain-text monitoring reports with odds changes, signal labels, and action guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid SkillPay billing may be required before use.] <br>

## Skill Version(s): <br>
2026.4.15-100 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
