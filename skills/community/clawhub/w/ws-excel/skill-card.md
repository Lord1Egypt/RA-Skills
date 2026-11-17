## Description:

Helps an agent handle Excel files for spreadsheet reading, writing, data cleaning, formula calculation, and multi-sheet operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fhbillwer](https://clawhub.ai/user/fhbillwer)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to ask an agent to inspect, clean, summarize, update, or calculate values in Excel workbooks and related tabular files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spreadsheet write operations could overwrite or change business or financial workbook data in place.

Mitigation: Give explicit instructions about whether workbook changes should be saved in place or written to a new file, and review important outputs before relying on them.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Code]

**Output Format:** [Markdown or text responses, with generated or modified spreadsheet files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write workbook data located under /workspace/data/analytics/.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
