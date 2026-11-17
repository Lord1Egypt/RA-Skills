## Description:

Intelligent work report generator that collects activity from project history, task managers, and calendars to produce professional daily or weekly reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yqghlx](https://clawhub.ai/user/yqghlx)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and team contributors use this skill to turn project history, task-manager items, calendar events, and manual notes into daily reports, weekly reports, standup notes, sprint reviews, and other status updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect broad local folders while looking for project activity.

Mitigation: Specify the exact repository or folder to analyze and avoid broad home or desktop scans.

Risk: The skill may use local repository history and optional task or calendar data that could contain sensitive work information.

Mitigation: Use it only when those data sources are appropriate for the report, and review the generated report before sharing.

Risk: The skill can export reports to Feishu or files when configured.

Mitigation: Confirm the Feishu document or file destination before writing the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yqghlx/skills/yqg-smart-daily-report)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with optional inline commands and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally write reports to chat, a file path, clipboard, or Feishu document when the destination is confirmed.]

## Skill Version(s):

3.0.2 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
