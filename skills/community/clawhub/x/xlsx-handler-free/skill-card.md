## Description: <br>
Xlsx Handler Free helps agents safely inspect, read, and edit local XLSX workbooks while preserving formulas, dates, merged cells, styles, and long text identifiers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and spreadsheet-heavy teams use this skill to have an agent inspect a workbook, choose pandas or openpyxl appropriately, generate or run local Python steps, and produce checked XLSX edits or workbook structure reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create or modify spreadsheet files, including existing workbooks. <br>
Mitigation: Ask the agent to save write operations to a new filename, avoid overwriting originals, and confirm the target workbook and sheet before changes. <br>
Risk: Generated Python workbook operations may preserve or alter formulas, dates, merged cells, styles, and long identifiers depending on tool choice. <br>
Mitigation: Review the proposed pandas or openpyxl approach before execution and require a final workbook validation report. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/thcjp/skills/xlsx-handler-free) <br>
- [SkillHub homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python code blocks, shell commands, and JSON-style reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local XLSX files when the agent is instructed to perform write operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
