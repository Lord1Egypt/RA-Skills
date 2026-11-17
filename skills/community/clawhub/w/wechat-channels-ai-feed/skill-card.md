## Description:

AI视频号信息源 scans AI-related WeChat Channels content, ranks posts by engagement, clusters topics, and generates an HTML daily report with cover images, metrics, and subscription support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as content operators, AI creators, and industry analysts use this skill to track trending AI content on WeChat Channels, review historical daily reports, and generate local HTML summaries for a chosen keyword or date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subscription mode can create persistent scheduled execution and may expose credentials.

Mitigation: Prefer one-shot runs with --no-open, use a scoped and revocable RedFox API key, and enable --subscribe only after credential storage and scheduled execution are reviewed.

Risk: Generated HTML reports can include unsafe or misleading content from fetched data.

Mitigation: Review generated reports before sharing or relying on them, and avoid opening reports automatically in higher-risk environments.

Risk: Scheduler setup can be affected by paths with unusual shell characters.

Mitigation: Install and run the skill from simple trusted paths, and review subscription setup before enabling the daily scheduler.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/wechat-channels-ai-feed)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFoxHub](https://redfox.hk)

## Skill Output:

**Output Type(s):** [text, html, shell commands, configuration]

**Output Format:** [Terminal text plus local HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; supports keyword, page size, date/time window, output directory, browser-opening, and subscription options.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
