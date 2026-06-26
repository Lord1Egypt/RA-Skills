## Description: <br>
A 股智能盯盘与选股系统，基于 QVeris AI 数据源，提供持仓监控、实时预警、午盘/尾盘复盘和趋势选股功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seedew](https://clawhub.ai/user/seedew) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and investors use this skill to monitor A-share holdings, generate market review reports, receive portfolio alerts, and screen candidate stocks through QVeris-backed data workflows. Developers can also use the bundled scripts and dashboard files to configure local monitoring and review automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe credential handling may expose a QVeris API key, including bundled or inline secret examples. <br>
Mitigation: Do not use the bundled key; require a fixed release with that key removed and rotated, and provide QVERIS_API_KEY through a safer secret mechanism. <br>
Risk: Local holdings and alert files can persist sensitive portfolio information. <br>
Mitigation: Protect local stock data files with appropriate filesystem permissions and delete them when the skill is no longer used. <br>
Risk: Scheduled jobs can repeatedly run scripts that call external data services and update local files. <br>
Mitigation: Inspect and explicitly opt into any cron jobs or scheduled automation before enabling them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/seedew/stock-master-pro) <br>
- [QVeris AI data source](https://qveris.ai/?ref=y9d7PKgdPcPC-A) <br>
- [QVeris skill dependency](https://clawhub.com/skills/qveris?ref=stock-master-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown and text reports with shell commands plus JSON-backed local dashboard data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses QVERIS_API_KEY and local holdings, alert, review, and dashboard JSON files.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
