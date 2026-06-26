## Description: <br>
在工作日检查日报是否已提交，未提交时提醒并@快腿鹿。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bounding-elk](https://clawhub.ai/user/bounding-elk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and team operators use this skill to check whether the current workday's daily report exists and contains meaningful content. When the report is missing or incomplete, it emits a reminder that mentions the designated teammate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate recurring reminders on a cron schedule. <br>
Mitigation: Review the schedule before enabling it and remove the cron entry when reminders are no longer needed. <br>
Risk: The disclosed daily-report path may not match every environment. <br>
Mitigation: Install only when /data/reports/daily/YYYY-MM-DD.md is the intended report location or adjust the deployment environment accordingly. <br>
Risk: The reminder mentions a specific teammate handle. <br>
Mitigation: Confirm that tagging 快腿鹿 is appropriate for the team before enabling automated reminders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bounding-elk/report-reminder) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text reminder responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May output a fixed reminder mention or a fixed confirmation message based on report-file checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
