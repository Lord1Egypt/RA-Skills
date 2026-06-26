## Description: <br>
Real-time trending topics aggregator across 7 platforms: X/Twitter, Reddit, Google Trends, Hacker News, Zhihu, Bilibili, and Weibo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XiaoYiWeio](https://clawhub.ai/user/XiaoYiWeio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, developers, and agents use this skill to collect current trending topics across English and Chinese-language platforms, start with a concise overview, and expand selected sources on demand. It can also configure an optional daily briefing through cron when the user explicitly requests scheduled trend collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds a Weibo session cookie in its source behavior. <br>
Mitigation: Review or remove the hard-coded cookie before use, and avoid treating it as an approved credential. <br>
Risk: The optional scheduler can create recurring cron jobs for daily trend collection. <br>
Mitigation: Use scheduling only when persistent execution is intended, and verify that users know how to list or remove the created cron entry. <br>
Risk: The skill fetches live data from multiple external sites and APIs. <br>
Mitigation: Run it in an environment where outbound network access is acceptable and review trend outputs before relying on them for decisions. <br>


## Reference(s): <br>
- [Trend Radar ClawHub Page](https://clawhub.ai/XiaoYiWeio/trend-radar) <br>
- [Publisher Profile](https://clawhub.ai/user/XiaoYiWeio) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Python 3](https://python.org) <br>
- [trends24.in](https://trends24.in) <br>
- [tophub.today](https://tophub.today) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown trend summaries with clickable links, optional JSON output, and shell commands for expansion or scheduling.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches live external trend sources concurrently; scheduled mode can save daily results under the user home directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
