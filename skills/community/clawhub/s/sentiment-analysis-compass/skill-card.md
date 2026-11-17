## Description:

Sentiment Compass monitors keyword mentions across Xiaohongshu, Douyin, Weibo, and WeChat Official Accounts, classifies Chinese sentiment, generates reports, and sends Feishu or email alerts when negative thresholds are exceeded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffersplind92](https://clawhub.ai/user/jeffersplind92)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, operations, and brand-monitoring teams use this skill to track Chinese social media mentions, classify sentiment, generate keyword reports, and trigger notifications for negative sentiment thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store credentials and configuration under ~/.sentiment-compass.

Mitigation: Run it in an isolated environment, restrict access to ~/.sentiment-compass, and avoid entering real API keys or SMTP passwords on command lines.

Risk: Monitored posts, keywords, summaries, credentials, alerts, and subscription tokens may be sent to external services when integrations are enabled.

Mitigation: Configure only trusted GLM-4, Feishu, email, and subscription verification endpoints, and treat monitored content as data that may leave the local environment.

Risk: The server security verdict is suspicious and calls for review before installation.

Mitigation: Review the skill before deployment and install it only after validating the configured providers, data handling, and alert destinations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeffersplind92/skills/sentiment-analysis-compass)
- [Publisher profile](https://clawhub.ai/user/jeffersplind92)
- [YK-Global paid plans](https://yk-global.com)
- [GLM API endpoint](https://open.bigmodel.cn/api/paas/v4/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON, Markdown reports, shell command examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce sentiment classifications, score summaries, trend data, alert payloads, and local configuration updates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
