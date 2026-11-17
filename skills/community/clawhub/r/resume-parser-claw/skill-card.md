## Description:

Parses non-standard resumes from PDF, Word, image, or text inputs into structured candidate data, with optional Feishu Bitable writing and Excel or JSON export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting, HR operations, and talent data teams use this skill to normalize individual or batch resumes into candidate records for review, database entry, Feishu Bitable workflows, and downstream screening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume text exported to CSV or XLSX can be interpreted as spreadsheet formulas.

Mitigation: Prefer JSON when preserving raw parsed data, treat exported spreadsheets as potentially unsafe, and sanitize formula-like cell values before opening or sharing spreadsheet exports.

Risk: Resume files contain personal candidate data and may be written to Feishu or local files.

Mitigation: Process only resumes the user is authorized to handle and confirm the destination before writing candidate data to Feishu or exported files.

## Reference(s):

- [Resume schema and Feishu table structure](references/resume-schema.md)
- [Skills normalization dictionary](references/skills-dictionary.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance, shell commands, structured JSON, and optional CSV/XLSX files or Feishu records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Candidate records include normalized fields, quality scores, confidence markers, deduplication signals, and source-file metadata.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
