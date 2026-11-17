## Description:

sheet-process helps agents guide users through filtering Tencent Docs smart sheets and exporting matching rows as JSON for workflows or HTML for interactive use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyi-arch](https://clawhub.ai/user/liuyi-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workflow builders who use WorkBuddy with Tencent Docs can select a smart sheet, define column and keyword filters, and export matching records for downstream AI nodes or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save filtered Tencent Docs sheet data as local output files.

Mitigation: Use it only with documents the user is authorized to process and keep exports in deliberate workspace folders with appropriate access controls.

Risk: HTML reports may embed unsafe spreadsheet content.

Mitigation: Prefer JSON output for automation and avoid opening or sharing generated HTML reports until the escaping issue is fixed.

Risk: The skill requires access to connected Tencent Docs sheets.

Mitigation: Install only if the publisher is trusted and review connector permissions before processing documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyi-arch/skills/sheet-process)

## Skill Output:

**Output Type(s):** [guidance, text, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python and shell snippets; generated filter results may be JSON or HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected WorkBuddy Tencent Docs connector and a referenced Tencent Docs smart sheet.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
