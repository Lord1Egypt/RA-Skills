## Description:

Monitors 21 Chinese securities-regulation pages across SZSE, SSE, BSE, NEEQ, ChinaClear, and SAC, then detects changes and prepares notification content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huifeideyua1231](https://clawhub.ai/user/huifeideyua1231)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to check or run an existing securities monitoring deployment, review pending update notifications, and prepare WeCom notifications about regulatory page changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release relies on recurring scripts under /root/monitoring/securities outside the reviewed package.

Mitigation: Confirm the deployment path, cron entry, script ownership, permissions, cleanup policy, and run account before enabling the skill.

Risk: WeCom notification instructions are under-scoped and could send updates to the wrong recipient.

Mitigation: Verify the WeCom recipient and notification content before any message is sent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huifeideyua1231/skills/securities-monitor)
- [API 说明](references/api.md)
- [配置说明](references/config.md)
- [XCrawl Scrape API endpoint](https://run.xcrawl.com/v1/scrape)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference generated notification and diff files from the managed monitoring deployment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
