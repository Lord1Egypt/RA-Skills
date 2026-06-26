## Description: <br>
UP 简历 AI 求职助手。创建专业简历、搜索校招/社招/实习岗位、JD 对照优化、简历诊断、每日求职监控、智能投递指导。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HelloSanshi](https://clawhub.ai/user/HelloSanshi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and job seekers use this skill to create and improve resumes, search campus, internship, and social hiring roles, monitor new openings, and prepare job application materials with an agent connected to the UPCV MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitoring workflow can create persistent scheduled agent runs and local job-search reports. <br>
Mitigation: Review the generated monitor.sh file and any launchd or cron entry before enabling it; confirm the schedule and removal steps. <br>
Risk: Resume, job-search, and ATS workflow data can include personal information. <br>
Mitigation: Install only if comfortable granting the UPCV MCP server access to resume and job-search data, and avoid storing government IDs or highly sensitive values in ATS records or local reports. <br>
Risk: Local ATS records and reports can persist after they are no longer needed. <br>
Mitigation: Periodically delete stale ~/.jobsclaw/reports entries and ats-records files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HelloSanshi/upcv-clawjob) <br>
- [UP 简历官网](https://upcv.tech) <br>
- [Clawjob OpenClaw 版](https://clawjob.upcv.tech) <br>
- [UPCV MCP Server](https://github.com/HireTechUpUp/upcv-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, structured resume and job-search content, and generated local file instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate resume content, job search summaries, PDF export links, ATS field mappings, monitor.sh scripts, cron or launchd setup guidance, and local Markdown reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
