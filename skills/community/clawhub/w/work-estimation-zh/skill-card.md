## Description:

Helps agents analyze Chinese software requirements, break work into modules, estimate effort, complexity, risk, dependencies, schedules, and costs, and produce multi-sheet Excel estimation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinqiu193](https://clawhub.ai/user/jinqiu193)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and project planners use this skill to turn Chinese software requirements or requirement documents into structured work breakdowns, effort estimates, schedules, risk notes, dependency notes, and cost estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated spreadsheets may carry unsafe formula-like values from untrusted requirement text.

Mitigation: Escape formula-leading characters before sharing or opening generated workbooks, and review generated cells when inputs came from untrusted sources.

Risk: The skill can work from user-supplied local requirement document paths and write report files.

Mitigation: Confirm the intended input path before reading local files and disclose the exact output path before writing reports.

## Reference(s):

- [Evaluation Guide](references/evaluation-guide.md)
- [ClawHub skill page](https://clawhub.ai/jinqiu193/skills/work-estimation-zh)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, files]

**Output Format:** [Chinese-language guidance plus generated .xlsx workbook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workbook sheets cover overview, dimension details, Gantt planning, key risks, coordination, and cost estimates.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
