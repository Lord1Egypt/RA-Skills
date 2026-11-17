## Description:

Monitors sports betting odds movement across Asian handicap, European odds, and over/under markets, then reports notable line changes, abnormal fluctuations, and alert-worthy signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to monitor football, basketball, and other sports odds, compare market movement across sources, and generate concise risk-aware reports or alerts. It is intended for odds monitoring and analysis, not as guaranteed betting advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes real billing logic and can initiate a SkillPay charge for the configured user identifier.

Mitigation: Install only after confirming the paid workflow, publisher trust, price per call, and the user identifier that will be charged.

Risk: A SkillPay API key is exposed in source code.

Mitigation: Rotate or revoke exposed credentials and require secrets to be supplied through a controlled environment before operational use.

Risk: The skill can make outbound calls to odds and billing services and store local SQLite odds history.

Mitigation: Run it in an environment with reviewed network access, approved API keys, and an understood local data-retention policy.

Risk: Odds movement signals can be misread as betting guarantees.

Mitigation: Present outputs as monitoring and analysis only, and require human review before any betting or financial decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenmeng/skills/shenmeng-odds-monitor-v3)
- [Publisher profile](https://clawhub.ai/user/shenmeng)
- [The Odds API](https://the-odds-api.com/)
- [SkillPay](https://skillpay.me)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or console-style monitoring reports with setup commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include odds snapshots, change summaries, detected market signals, alert recommendations, and payment or API-key setup notes.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact config, package __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
