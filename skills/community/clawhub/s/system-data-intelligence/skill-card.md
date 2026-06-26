## Description: <br>
System Data Intelligence helps agents read common document and data files, analyze datasets, create visual reports, connect to databases and APIs, and handle sensitive data with masking workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaojie911272507](https://clawhub.ai/user/zhaojie911272507) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to automate file ingestion, data profiling, database or API retrieval, chart generation, and concise reporting across Windows, macOS, Linux, and Docker environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can activate broadly on common file, analysis, database, API, and sensitive-data tasks. <br>
Mitigation: Review the skill before installation and invoke it only for tasks where this broad data access is intended. <br>
Risk: The skill can use high-impact local OS automation, database connections, API tokens, and file paths. <br>
Mitigation: Run it in a contained workspace, grant OS automation permissions cautiously, and provide only credentials and paths needed for the current task. <br>
Risk: The skill may persist extracted data in JSON, HTML, PNG, CSV, or markdown report files. <br>
Mitigation: Use it only with data suitable for local report files and clean generated outputs after the task, especially when sensitive data is involved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaojie911272507/system-data-intelligence) <br>
- [File formats reference](references/file-formats.md) <br>
- [Windows API reference](references/windows-api.md) <br>
- [macOS API reference](references/macos-api.md) <br>
- [Linux API reference](references/linux-api.md) <br>
- [Visualization patterns reference](references/viz-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and shell command blocks; generated artifacts may include JSON analysis results, HTML reports, PNG charts, and markdown summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write report, chart, JSON, and summary files under an outputs directory when the skill's scripts are used.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
