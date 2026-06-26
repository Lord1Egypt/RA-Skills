## Description: <br>
查询中国国内火烧云、晚霞和朝霞预报，并在达到阈值时通过飞书通知用户。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neverland83](https://clawhub.ai/user/neverland83) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and weather-monitoring agents use this skill to query China-focused sunsetbot.top sunrise and sunset forecast data, compare vividness scores against notification thresholds, and keep local forecast logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: City queries and forecast parameters are sent to sunsetbot.top. <br>
Mitigation: Use the skill only for cities and forecast lookups you are comfortable sharing with that service. <br>
Risk: Local forecast logs under data/ can reveal location-interest history. <br>
Mitigation: Limit retention, clear logs, or avoid shared machines when that history is sensitive. <br>
Risk: Feishu notifications require a user Open ID in local configuration. <br>
Mitigation: Store the Open ID only in config/config.json and avoid embedding it in skill text, payloads, or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neverland83/sunsetbot-monitor-cn) <br>
- [SunsetBot forecast service](https://sunsetbot.top/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown notifications and JSONL plus Markdown log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call sunsetbot.top with queried city and forecast parameters, may send Feishu notifications, and writes local forecast history under data/.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
