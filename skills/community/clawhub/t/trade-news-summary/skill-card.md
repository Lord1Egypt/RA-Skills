## Description:

Automatically collects trade-related RSS news, translates headlines into Chinese, generates Markdown reports, and can push updates to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joewangup](https://clawhub.ai/user/joewangup)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and trade teams use this skill to collect trade-related news, translate headlines into Chinese, classify items by business topic, and optionally send daily and weekly summaries to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected news topics, titles, translations, summaries, and error details may be sent to configured third-party services.

Mitigation: Install only when that data sharing is acceptable, and use a dedicated low-privilege Feishu bot for notifications.

Risk: The artifact gives weak guidance for storing API secrets in shell startup files or crontab.

Mitigation: Store Baidu and Feishu credentials in a managed secret store or tightly scoped environment injection instead of persistent shell files.

Risk: Untrusted RSS content and links are incorporated into Markdown and webhook messages.

Mitigation: Use trusted RSS feeds and consider validating URLs and escaping Markdown before scheduled operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joewangup/skills/trade-news-summary)
- [Baidu Translate Open Platform](https://fanyi-api.baidu.com/)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report, Feishu message payloads, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local trade-news report and can post selected summaries to a configured Feishu webhook.]

## Skill Version(s):

2.3.3 (source: server release evidence and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
