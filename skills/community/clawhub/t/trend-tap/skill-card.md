## Description: <br>
Trend Tap fetches current trending topics from X/Twitter, Reddit, Google Trends, Hacker News, Zhihu, Bilibili, and Weibo, then presents an overview or expanded platform-specific results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XiaoYiWeio](https://clawhub.ai/user/XiaoYiWeio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent what is currently trending across several public platforms, then expand individual sources for ranked links and lightweight metrics. It can also create a local daily briefing schedule when the user explicitly requests recurring trend collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create a persistent recurring cron job for daily briefings. <br>
Mitigation: Review the scheduler behavior before enabling it, list existing Trend Tap schedules after setup, and remove the schedule when recurring collection is no longer needed. <br>
Risk: The Weibo fallback includes a hardcoded session-style cookie despite the no-auth claim. <br>
Mitigation: Review or disable the Weibo fallback before installation if hardcoded platform cookies are not acceptable in the deployment environment. <br>
Risk: The skill makes live requests to several public platforms and results can change or fail based on third-party availability. <br>
Mitigation: Treat fetched trend data as current but externally sourced, and verify important claims with source links or follow-up research before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/XiaoYiWeio/trend-tap) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Python 3](https://python.org) <br>
- [Trends24](https://trends24.in) <br>
- [TopHub Today](https://tophub.today) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown trend summaries with clickable links, optional JSON output, and optional saved daily JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python 3 standard-library scripts to make live requests to public trend sources; scheduled briefings modify the user's crontab.] <br>

## Skill Version(s): <br>
2.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
