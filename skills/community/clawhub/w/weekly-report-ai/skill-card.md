## Description: <br>
自动整理周报工具，支持从 GitHub、飞书文档和日历汇总工作内容，生成 Markdown 周报，并支持历史保存、HTML/PDF 导出、邮件发送和飞书文档写入。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Carson1012](https://clawhub.ai/user/Carson1012) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to collect weekly work activity from code repositories, documents, calendars, and manual notes, then turn it into a structured weekly report. It is intended for recurring work summaries that may be saved locally, exported, emailed, or published to Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles GitHub, Feishu, calendar, and SMTP credentials for work accounts. <br>
Mitigation: Use least-privilege tokens or app passwords, avoid passing secrets directly in shell commands, and rotate or revoke credentials after testing. <br>
Risk: Generated reports can be emailed or written to Feishu documents, which may expose sensitive work details. <br>
Mitigation: Preview report content, recipients, and destination documents before sending or publishing. <br>
Risk: History and export features write local files, and history management can delete saved reports. <br>
Mitigation: Restrict report output to expected directories, validate dates and paths, and review delete actions before execution. <br>
Risk: Scheduled unattended runs could publish or send incomplete or incorrect weekly reports. <br>
Mitigation: Avoid unattended cron runs until confirmation prompts and path validation are in place. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Carson1012/weekly-report-ai) <br>
- [Publisher profile](https://clawhub.ai/user/Carson1012) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, HTML/PDF files, JSON command results, and delivery guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save report history locally and send or publish generated report content through configured services.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
