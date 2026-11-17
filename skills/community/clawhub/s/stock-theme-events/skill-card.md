## Description:

Stock Theme Events analyzes leading A-share stocks, clusters related market themes, searches recent finance and news sources, and generates a theme-to-event report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shinelp100](https://clawhub.ai/user/shinelp100)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, developers, and agent workflows use this skill to connect A-share market themes with recent news events and produce daily review reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled stock-code text is delegated to a spawned OpenClaw subagent without clear validation or permission limits.

Mitigation: Validate stock lists before use and constrain or review subagent permissions before processing untrusted inputs.

Risk: Network-based finance and news sources can be unavailable, stale, rate-limited, or misleading.

Mitigation: Review generated reports against the cited source links, keep request rates conservative, and avoid treating results as trading advice.

Risk: Dependencies and model downloads can change behavior if installed without pinning.

Mitigation: Install in an isolated environment and pin package versions before production use.

Risk: Artifact documentation includes a destructive repository reset command.

Mitigation: Do not run destructive Git commands from documentation unless working in a backed-up or disposable clone.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shinelp100/skills/stock-theme-events)
- [Jin10 news search](https://xnews.jin10.com/search?keyword={theme})
- [Eastmoney news search](https://so.eastmoney.com/news.aspx?q={keyword})
- [CLS news search](https://www.cls.cn/search?keyword={keyword})

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown reports with JSON intermediate data and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes stock theme clusters, related news items, source names, timestamps, and report-level risk notes when data is available.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
