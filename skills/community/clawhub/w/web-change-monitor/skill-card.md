## Description:

Web Change Monitor helps agents configure URL monitoring tasks, detect webpage changes by hash, keyword, CSS selector, or regex, and report changes through Feishu notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiji0802](https://clawhub.ai/user/qiji0802)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor public webpage changes such as product listings, prices, inventory, and content updates, then review stored change history or receive Feishu notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs from the agent runtime, which may expose internal dashboards, localhost services, cloud metadata endpoints, or other sensitive network resources.

Mitigation: Use it only for approved public pages, avoid internal or sensitive URLs, and run it with network egress isolation where possible.

Risk: Monitored page contents and change details may be stored locally or sent through Feishu notifications.

Mitigation: Confirm what will be stored and notified before enabling monitoring, and avoid pages containing sensitive business or personal data.

Risk: Authenticated pages are not supported in the current artifact, so monitoring pages that require login may fail or produce incomplete results.

Mitigation: Prefer public pages unless reviewed authentication and credential-handling controls are added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qiji0802/skills/web-change-monitor)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON CLI responses and Feishu notification text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local SQLite monitoring state under ~/.web-change-monitor/history.db when used.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact changelog lists v1.0.0 released 2026-04-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
