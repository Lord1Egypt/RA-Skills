## Description:

禅道(Zentao)用户工作内容分析工具。通过数据库只读查询分析指定用户在指定时间段内的需求、任务、Bug、工时日志，生成 Markdown 格式的工作报告。仅支持 SQL SELECT 查询，不修改任何数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[endcy](https://clawhub.ai/user/endcy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and authorized operations or management users use this skill to generate Markdown work-analysis reports from Zentao records for a specified employee and date range. It is intended for authorized reporting over requirements, tasks, bugs, effort logs, and monthly activity trends using read-only database queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive employee work records and generate reports containing personal activity, effort, and performance-related information.

Mitigation: Use it only with explicit authorization for the target employee and report period, and restrict report storage and sharing according to organizational privacy policy.

Risk: The database queries may load broader employee and project metadata than a single-user report requires.

Mitigation: Use a dedicated read-only database account limited to the minimum required tables and columns, and narrow mapping queries where possible.

Risk: Database connection settings may expose sensitive deployment details if configuration files are shared broadly.

Mitigation: Keep configuration files access-controlled and use environment variables or managed configuration for credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/endcy/skills/zentao-work-stats)
- [Report template](artifact/references/report-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with SQL query guidance and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local work-analysis report and summary statistics for the requested user and time range.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
