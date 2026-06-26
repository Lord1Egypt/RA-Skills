## Description: <br>
Helps agents assess cryptocurrency social-media discussion, sentiment, trending topics, KOL activity, viral content, and FUD signals across platforms such as X/Twitter, Reddit, Telegram, and Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External crypto analysts, community managers, and developers use this skill to generate social sentiment summaries, detect emerging topics, monitor influential accounts, and prepare market sentiment reports. Evidence indicates it should be treated as a paid simulator/prototype rather than reliable live market intelligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release advertises live monitoring while security evidence says outputs should be treated as simulated prototype data. <br>
Mitigation: Do not rely on outputs for trading, incident response, or market decisions; validate findings against authoritative data sources before acting. <br>
Risk: The skill includes a paid billing path and may charge per invocation. <br>
Mitigation: Verify SkillPay charges, publisher identity, and the configured user identity before running the skill. <br>
Risk: The daemon mode can keep running and write local files. <br>
Mitigation: Start daemon mode only intentionally, review configuration first, and monitor local file output. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shenmeng/shenmeng-social-sentiment-monitor) <br>
- [API Configuration Guide](references/api-configuration.md) <br>
- [LunarCrush API](https://lunarcrush.com/api3) <br>
- [Santiment GraphQL API](https://api.santiment.net/graphql) <br>
- [SkillPay Billing Endpoint](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and console-oriented text with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local Python scripts, create local report/configuration files, and use paid billing flow when enabled.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
