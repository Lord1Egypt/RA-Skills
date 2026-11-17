## Description:

自动监控关键词相关 YouTube 新视频，获取字幕并生成中文摘要，然后将报告推送到 Telegram。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huxiaoqiao](https://clawhub.ai/user/huxiaoqiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor YouTube for keyword-related videos, collect transcripts, summarize them in Chinese, and receive scheduled Telegram reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to run a script that is not included in the artifact on a schedule.

Mitigation: Inspect or obtain the missing script before enabling cron or any unattended execution.

Risk: The workflow installs an unpinned npm dependency.

Mitigation: Pin and review npm dependencies before installation.

Risk: The workflow may send transcripts, summaries, video metadata, and credentials to external services such as Telegram and transcriptapi.com.

Mitigation: Confirm the exact data shared with each external service and protect API keys and Telegram identifiers before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huxiaoqiao/skills/youtube-openclaw-monitor)
- [Publisher profile](https://clawhub.ai/user/huxiaoqiao)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and generated summary/report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces dated transcript/summary files and a latest-report markdown file when the referenced workflow is available and configured.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
