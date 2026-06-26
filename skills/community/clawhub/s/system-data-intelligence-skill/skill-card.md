## Description: <br>
System Data Intelligence helps agents read and manipulate office or text files, perform multi-level data analysis, and generate charts, dashboards, and data reports across Windows, macOS, and Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaojie911272507](https://clawhub.ai/user/zhaojie911272507) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and agent builders use this skill to automate document and spreadsheet extraction, inspect data quality, run descriptive through predictive analysis, and produce reusable visual reports. It is most relevant when a task needs cross-application data flow or local file handling before analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports broad activation scope and capabilities to read local files, automate desktop applications, and create derived files containing source data. <br>
Mitigation: Use the skill first on non-sensitive data, review generated reports and logs before sharing, and only grant desktop automation permissions when the publisher and task justify that access. <br>
Risk: The security scan notes under-disclosed local persistence and raw macOS automation helpers. <br>
Mitigation: Run in a constrained workspace where practical, inspect generated files, and avoid broad macOS accessibility or automation permissions unless they are required for the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaojie911272507/system-data-intelligence-skill) <br>
- [Publisher profile](https://clawhub.ai/user/zhaojie911272507) <br>
- [Windows API Reference](references/windows-api.md) <br>
- [macOS API Reference](references/macos-api.md) <br>
- [Linux API Reference](references/linux-api.md) <br>
- [File Formats Reference](references/file-formats.md) <br>
- [Visualization Patterns Reference](references/viz-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; generated artifacts may include JSON, CSV, HTML reports, and PNG charts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local output directories containing analysis_result.json, summary.md, report HTML, PNG charts, and operation logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
