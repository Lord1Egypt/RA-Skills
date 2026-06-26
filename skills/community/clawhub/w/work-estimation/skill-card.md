## Description: <br>
Software Development Work Estimation accepts requirements text or supported documents, breaks work into modules, estimates effort, and outputs structured Excel evaluation reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinqiu193](https://clawhub.ai/user/jinqiu193) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering managers, and project planners use this skill to turn software requirements into module breakdowns, effort estimates, risk notes, dependency information, schedules, and cost estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes requirement text or requirement documents that may contain sensitive project details. <br>
Mitigation: Use only requirement content approved for the agent session and review generated estimates before sharing them. <br>
Risk: The Excel generator writes local report files to the selected or default output path. <br>
Mitigation: Review output locations before generating reports and avoid writing reports into unintended shared directories. <br>
Risk: The bundled test script references a hard-coded local Windows import path. <br>
Mitigation: Do not run the test script unless the path is trusted or updated to import the packaged generator directly. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Software Development Work Estimation Guide](references/evaluation-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Files, Guidance] <br>
**Output Format:** [Markdown responses and multi-sheet Excel workbooks (.xlsx)] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated workbooks include overview, dimension details, Gantt chart, key risks, coordination relations, and cost estimation sheets.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
