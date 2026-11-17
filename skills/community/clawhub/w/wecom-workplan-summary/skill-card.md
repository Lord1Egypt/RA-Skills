## Description:

Summarizes team work-plan records by week or month from pasted table data or a configured WeCom smart sheet, then helps the agent produce a concise management-facing report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangpengle](https://clawhub.ai/user/zhangpengle)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and team leads use this skill to turn team work-plan records into weekly or monthly natural-language summaries with per-person activity, goal alignment, suggestions, and missing-submission notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process sensitive team work-plan data from WeCom or pasted tables.

Mitigation: Use it only with authorized WeCom credentials and with work-plan data that is appropriate for the agent environment.

Risk: Pasted work-plan data may be written temporarily to /tmp/workplan_paste.tsv.

Mitigation: Avoid pasting highly sensitive plans unless local temporary storage is acceptable, and delete the temporary file after use.

Risk: Report inputs may contain inaccurate or untrusted content if multiple people can edit the source sheet.

Mitigation: Review generated summaries against the source records before sharing them with stakeholders.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with supporting shell command invocation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses structured work-plan records and produces one human-readable summary stream.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
