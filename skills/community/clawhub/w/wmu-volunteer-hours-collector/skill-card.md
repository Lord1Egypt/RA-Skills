## Description:

WMU志愿时长收集器 helps Wenzhou Medical University student-union practice departments consolidate volunteer signup spreadsheets into standardized monthly volunteer-hour workbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pkx07](https://clawhub.ai/user/pkx07)

### License/Terms of Use:

MIT-0

## Use Case:

Student-union practice department staff and agents use this skill to parse collected volunteer registration spreadsheets, confirm missing activity details, map college and major abbreviations, and produce a formatted monthly volunteer-hours workbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow bulk-processes student personal data including student IDs and phone numbers.

Mitigation: Use a dedicated folder containing only authorized volunteer-hour spreadsheets and confirm permission to handle the student data before running the workflow.

Risk: Generated workbooks may preserve formula-prefixed spreadsheet values that could be unsafe when opened or shared.

Mitigation: Review and sanitize formula-prefixed cell values before sharing generated workbooks.

Risk: Dependencies and a referenced template asset are required, and evidence notes the template asset is missing from this artifact.

Mitigation: Install dependencies in a virtual environment, prefer pinned hashes, and verify that assets/志愿服务.xlsx is present before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pkx07/skills/wmu-volunteer-hours-collector)
- [College and major mapping reference](artifact/references/mapping.md)
- [Merged-cell handling note](artifact/references/merged-cell-trap.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational guidance with Python and shell snippets, plus generated Excel workbook files during use]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local spreadsheet files and asks for user confirmation when activity details, source labels, college, major, or date choices are ambiguous.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
