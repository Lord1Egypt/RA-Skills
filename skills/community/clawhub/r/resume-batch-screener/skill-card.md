## Description:

Batch resume screening skill that parses job descriptions, scores and ranks multiple candidates, and generates screening and interview invitation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suql82](https://clawhub.ai/user/suql82)

### License/Terms of Use:

MIT-0

## Use Case:

HR employees and recruiting teams use this skill to compare multiple resumes against a job description with consistent scoring, ranking, and interview recommendation outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Regeneration guidance includes broad wildcard deletion of prior HR report spreadsheets.

Mitigation: Confirm the exact output directory and target filenames before cleanup; prefer versioned report outputs over deletion.

Risk: Resume screening handles sensitive candidate and HR data.

Mitigation: Use only in an approved local HR workspace and avoid shared or synced folders unless that storage is intended.

Risk: Keyword-based scoring and weights may not match the actual role.

Mitigation: Verify the scoring keywords, dimensions, and thresholds against the job description before relying on rankings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suql82/skills/resume-batch-screener)

## Skill Output:

**Output Type(s):** [files, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with code and shell snippets; generated spreadsheet files are described as XLSX reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ranked screening reports, interview invitation lists, scoring templates, and candidate scoring details.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
