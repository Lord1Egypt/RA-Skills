## Description:

Fetches Feishu approval data for Xihu Hiring and generates a recruitment progress Excel workbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tyqqj0](https://clawhub.ai/user/tyqqj0)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting operators and authorized HR users use this skill to refresh Xihu Hiring candidate progress from Feishu approvals, apply manual corrections, and produce a three-sheet Excel report without exposing full candidate PII in chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Candidate personal data and Feishu approval contents may be exposed through temporary payload files or generated workbooks.

Mitigation: Run the skill only in a controlled workspace, restrict access to Feishu credentials and generated files, and store temporary payloads in a private per-run directory with cleanup.

Risk: Spreadsheet formula injection may occur if untrusted form fields are written directly into Excel cells.

Mitigation: Sanitize workbook text values that begin with spreadsheet formula markers before report generation or distribution.

Risk: Unpinned dependencies may change behavior across runs.

Mitigation: Pin runtime dependencies such as openpyxl before routine operational use.

## Reference(s):

- [Fetch Feishu Approvals](references/fetch-approvals.md)
- [Position Normalization Rules](references/normalization-rules.md)
- [Excel Report Builder](references/build-excel.md)
- [ClawHub Skill Page](https://clawhub.ai/tyqqj0/skills/xihu-hiring)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python snippets; generated runtime artifacts include JSON payloads and an Excel workbook.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses lark-cli and openpyxl; the final workbook is written as 西湖数智-招聘进度.xlsx in the active workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
