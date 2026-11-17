## Description:

Generates quality daily, weekly, or monthly reports from key figures and events, with Excel and PPT output or content ready for both.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lams001](https://clawhub.ai/user/lams001)

### License/Terms of Use:

MIT-0

## Use Case:

Quality teams, production quality staff, and managers use this skill to generate daily, weekly, or monthly quality reports with KPIs, issue/action tracking, charts, and Excel/PPT-ready outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may contain realistic sample business metrics when the user does not provide actual data.

Mitigation: Label sample figures as placeholders and require users to replace them with verified operational data before sharing reports.

Risk: The skill may save Excel or PowerPoint report files locally as intended outputs.

Mitigation: Review generated files before distribution and store them only in approved workspaces.

Risk: Generic report requests may activate the skill unintentionally.

Mitigation: Use specific prompts such as quality KPI report, quality weekly report, or 品质周报 when invoking the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lams001/skills/quality-report)
- [README](artifact/README.md)
- [Quality report reference](artifact/reference.md)
- [Template choices](artifact/examples/template-choices-zh.md)
- [Full process weekly example](artifact/examples/sample-full-process-weekly.md)
- [Multi-site weekly example](artifact/examples/sample-san-di-weekly.md)
- [First-inspection/submission/process weekly example](artifact/examples/sample-shoujian-songjian-weekly.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, files, guidance]

**Output Format:** [Markdown report content, optional CSV tables, Mermaid/chart specifications, and local .xlsx/.pptx files when the runtime supports file generation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate realistic sample business metrics when the user has no data; sample data should be clearly marked and replaced before operational use.]

## Skill Version(s):

1.4.0 (source: ClawHub release metadata and artifact clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
