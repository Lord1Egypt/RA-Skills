## Description:

Generates ZenTao task analytics reports covering task counts, hours, difficulty, efficiency, and workload saturation from the included analyzer and export scripts.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[jiaolongxue](https://clawhub.ai/user/jiaolongxue)

### License/Terms of Use:


## Use Case:

Developers, project leads, and team operations users can use this skill to inspect ZenTao task workload and efficiency metrics for team performance review, workload analysis, resource planning, and project monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The current analyzer is early-stage demo/mock code and may overstate real ZenTao API or database access.

Mitigation: Review the scripts before relying on the reports, verify any ZenTao integration against a non-production environment, and treat outputs as advisory until real data access is implemented and tested.

Risk: Generated CSV files may carry report-opening risk in spreadsheet software until CSV escaping and formula neutralization are fixed.

Mitigation: Open CSV exports only after reviewing or neutralizing spreadsheet formulas, or prefer JSON output for inspection workflows.

Risk: ZenTao credentials and employee task data may expose sensitive operational or personal information.

Mitigation: Use read-only ZenTao credentials, avoid broad database accounts, keep secrets out of version control, and limit analysis to authorized internal users.

## Reference(s):

- [ZenTao connection configuration](artifact/references/zentao-config.md)
- [Metrics definitions and calculation logic](artifact/references/metrics-definition.md)
- [ClawHub skill page](https://clawhub.ai/jiaolongxue/skills/zentao-analytics)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON reports, CSV exports, and console summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports may include employee task metrics, workload saturation labels, rankings, warnings, and resource allocation suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
