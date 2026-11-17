## Description:

AI小红书信息源 scans AI-related Xiaohongshu posts by keyword, ranks them by engagement, clusters topics, and generates terminal summaries plus local HTML daily reports with optional daily subscription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators, Xiaohongshu creators, and industry analysts use this skill to monitor AI-related Xiaohongshu trends, review popular posts, and generate daily or historical reports for content planning and market observation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs a RedFox API key and makes outbound RedFox API calls.

Mitigation: Use a dedicated, revocable API key and install only when outbound RedFox requests are acceptable.

Risk: Subscription mode may store the API key in plaintext and install recurring execution with unsafe command handling.

Mitigation: Avoid --subscribe until credential storage and scheduled-task handling are fixed.

Risk: Generated HTML reports contain external data and may open automatically in a browser.

Mitigation: Use --no-open when reviewing reports from external data and open generated files only after inspection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/xiaohongshu-ai-feed)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFox API endpoint](https://redfox.hk/story/api/parseWork/queryXhsAiMsgs)

## Skill Output:

**Output Type(s):** [Text, HTML, Shell commands, Configuration]

**Output Format:** [Terminal text plus local HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reports under ~/Downloads/QoderReports by default and may open the generated report in a browser unless --no-open is used.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
