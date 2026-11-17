## Description:

Creates, inspects, and edits Microsoft Excel XLSX workbooks, including workbook creation, data checks, formulas, dates, formatting, and change reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and automation teams use this skill to create, inspect, and update XLSX workbooks in agent workflows. It is intended for approved spreadsheet files and excludes encrypted-file cracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill asks for command execution, write access, API-key handling, and broad file-processing authority without tight scoping.

Mitigation: Review before installing, run in a sandbox or least-privilege workspace, and use only approved spreadsheet files or copies.

Risk: Command execution and broad file access can affect local files beyond the intended workbook task.

Mitigation: Review proposed commands before execution and restrict file permissions to the specific input and output paths needed for the workflow.

Risk: API-key handling is mentioned without a clearly named external service or documented data boundary.

Mitigation: Do not provide command execution authority or API credentials unless the publisher narrows the scope, names the external service, and documents exactly what data leaves the machine.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/xlsx-handler)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify XLSX files when the agent is granted file write access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
