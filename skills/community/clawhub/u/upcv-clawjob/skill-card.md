## Description:

UP 简历 AI 求职助手可帮助用户创建和编辑简历、搜索校招/社招/实习岗位、按 JD 优化简历、生成求职监控简报并准备投递材料。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellosanshi](https://clawhub.ai/user/hellosanshi)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers and students use this skill to manage resume creation and editing, discover job or campus recruiting opportunities, generate daily job-search summaries, and prepare application materials. The skill depends on the UPCV MCP service and an API key for resume and job-search operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume and job-search activity is connected to the UPCV MCP service.

Mitigation: Install only if this data sharing is acceptable, use a scoped API key where available, and pin the MCP package version when possible.

Risk: The daily monitoring workflow creates persistent launchd or cron scheduled tasks.

Mitigation: Review the generated monitoring script and scheduled task entry before enabling it, and remove only the specific job when disabling monitoring.

Risk: The security guidance flags unsafe cron cleanup guidance.

Mitigation: Avoid `crontab -r`; use `crontab -e` or another targeted method to remove only the monitor entry.

Risk: Generated reports and ATS records can retain job-search and application details on disk.

Mitigation: Periodically delete reports or ATS records that are no longer needed and avoid storing sensitive identifiers in reusable records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hellosanshi/skills/upcv-clawjob)
- [UP 简历](https://upcv.tech)
- [Clawjob OpenClaw edition](https://clawjob.upcv.tech)
- [UPCV MCP Server](https://github.com/HireTechUpUp/upcv-mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and conversational text with optional shell commands, configuration snippets, HTML resume content, and generated report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local monitoring scripts, scheduled task configuration, daily Markdown reports, ATS records, and PDF export links through the UPCV MCP service.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
