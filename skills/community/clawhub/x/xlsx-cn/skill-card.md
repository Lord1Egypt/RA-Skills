## Description: <br>
Excel spreadsheet processing for creating, reading, and editing Excel files with support for formulas, charts, and data analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>
Anthropic Consumer or Commercial Terms of Service <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to create, edit, analyze, format, and recalculate .xlsx workbooks while checking for formula errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recalculation helper can persistently change LibreOffice settings and load a compiled native compatibility shim. <br>
Mitigation: Review before installation, run in a disposable or isolated environment, and avoid using a primary user profile for evaluation. <br>
Risk: The skill may modify local Excel files during recalculation. <br>
Mitigation: Work on copies of important spreadsheets and review recalculation results before relying on the workbook. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guohongbin-git/xlsx-cn) <br>
- [OpenClaw fork source](https://github.com/anthropics/skills) <br>
- [OpenClaw metadata homepage](https://clawhub.com/skills/xlsx-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell commands; generated or modified XLSX files may be produced when the agent follows the skill.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return JSON formula-error details from the recalculation helper.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
