## Description: <br>
Excel工具(免费版) helps agents read, write, clean, calculate, and summarize xlsx spreadsheets with Python libraries such as openpyxl and pandas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals, independent developers, and agents use this skill to process single Excel files for statistics, data cleaning, report formatting, and basic formula work without Microsoft Excel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local Python and create or modify spreadsheet files. <br>
Mitigation: Review generated scripts before execution, provide explicit input paths, and prefer new output filenames instead of overwriting source files. <br>
Risk: Spreadsheet files may contain sensitive business or personal data. <br>
Mitigation: Use the skill only for intended Excel/xlsx processing, keep data local when possible, and inspect generated outputs before sharing them. <br>
Risk: Generated formulas may depend on Excel or another spreadsheet application to recalculate after the file is opened. <br>
Mitigation: For final numeric results, have the agent compute values directly in Python or verify formulas in the target spreadsheet application. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ws-excel-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python snippets, shell commands, and JSON-like structured status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local xlsx output files using user-provided paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
