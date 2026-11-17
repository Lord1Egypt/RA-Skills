## Description:

Web to Excel extracts structured data from user-supplied web pages and fills specified ranges in Excel workbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oreosofat](https://clawhub.ai/user/oreosofat)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scrape structured data from supplied web pages, review field mappings, and populate selected rows and columns in Excel files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install Python packages when dependencies are missing.

Mitigation: Review dependencies before use and run only in environments where package installation is controlled or dependencies are preinstalled and pinned.

Risk: The skill accesses a local browser session through CDP and opens or reuses tabs for user-supplied URLs.

Mitigation: Use only trusted URLs, avoid sensitive browser sessions, and prefer an isolated browser profile for scraping tasks.

Risk: The skill can mutate Excel workbooks and the security summary notes insufficient scoping and confirmation.

Mitigation: Keep a backup of the workbook, confirm the target sheet, range, and field mapping before saving, and avoid processing sensitive spreadsheets without review.

Risk: Scraped spreadsheet values may include formula-like content.

Mitigation: Sanitize formula-like values before writing them to workbooks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oreosofat/skills/web-to-excel)
- [Field mapping reference](references/field-mapping.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance, Python code and shell commands, Excel workbook updates, and a text completion report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-supplied URL, workbook path, sheet name, target row range, and field mapping confirmation; may mutate local Excel files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
