## Description:

纯离线的中文股市数据分析教学系统，使用模拟数据生成盘前市场分析示例，不调用外部网络服务。

This skill is for demonstration purposes and not for production usage.

## Publisher:

[luckjackyer](https://clawhub.ai/user/luckjackyer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and learners use this skill to study OpenClaw-style agent scripting and offline quantitative-analysis patterns. It generates Chinese-language simulated market briefings, stock-screening examples, technical levels, and local Markdown logs for educational review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated briefings may look like market guidance even though they are based on simulated data.

Mitigation: Treat all generated output as educational material only and do not use it for investment decisions.

Risk: The skill writes local configuration and Markdown report files.

Mitigation: Review config.json before running and periodically remove generated logs that are no longer needed.

Risk: The documentation includes an optional weekday cron schedule.

Mitigation: Enable the cron entry only when recurring local execution is intended, and remove that entry to stop scheduled runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luckjackyer/skills/stock-briefing)
- [OpenClaw](https://openclaw.ai)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Console text, JSON configuration, and Markdown briefing logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local logs/briefing-YYYY-MM-DD.md files and may create config.json with sample holdings if absent.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
