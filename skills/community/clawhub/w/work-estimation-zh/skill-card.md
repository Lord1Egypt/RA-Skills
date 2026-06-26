## Description: <br>
Chinese-language software work-estimation skill that analyzes requirements, breaks work into modules, estimates effort, risk, schedule, dependencies, and cost, and can generate a multi-sheet Excel report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinqiu193](https://clawhub.ai/user/jinqiu193) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering managers, and project leads use this skill to turn Chinese requirement descriptions or requirement documents into structured software effort estimates, including task breakdowns, effort ranges, risks, dependencies, schedules, and budget estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confidential requirements, credentials, or personal data could be exposed if supplied in an untrusted agent environment. <br>
Mitigation: Use the skill in a trusted local environment and avoid entering sensitive requirements, credentials, or personal data unless the environment is approved for that data. <br>
Risk: The bundled Excel generation script depends on openpyxl being available. <br>
Mitigation: Confirm the openpyxl dependency is installed before running the script. <br>


## Reference(s): <br>
- [Evaluation Guide](references/evaluation-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/jinqiu193/work-estimation-zh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance, files] <br>
**Output Format:** [Chinese prose and structured Markdown, with optional Python-generated Excel workbook files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Excel output is multi-sheet and may include overview, dimension detail, Gantt, risk, coordination, and cost sheets.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
