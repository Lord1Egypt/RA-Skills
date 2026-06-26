## Description: <br>
Generates professional HTML/PDF-ready data reports with KPI summaries, charts, tables, executive insights, and recommendations from CSV, Excel, or JSON data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plgonzalezrx8](https://clawhub.ai/user/plgonzalezrx8) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Business users, analysts, and developers use this skill to generate KPI dashboards, executive briefs, and structured analytical reports from CSV, Excel, JSON, or described datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Source data may be incomplete, dirty, or mapped to the wrong KPI fields. <br>
Mitigation: Validate inputs, flag missing or dirty data explicitly, and sanity-check metrics before relying on the report. <br>
Risk: Generated narratives or recommendations may overstate what the data supports. <br>
Mitigation: Review findings before sharing and avoid causal claims unless the provided data supports them. <br>
Risk: The helper script writes report and chart files to user-selected output paths. <br>
Mitigation: Run it from a trusted project folder, provide only intended data files, and choose output paths deliberately. <br>


## Reference(s): <br>
- [Report Templates](references/report-templates.md) <br>
- [Chart Guidelines](references/chart-guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, HTML files, Charts, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance and generated HTML reports with chart images] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports CSV, Excel, and JSON inputs; generated files are intended to stay within the current working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
