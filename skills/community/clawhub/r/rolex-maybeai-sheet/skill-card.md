## Description:

MaybeAI Sheet skill provides full Excel/spreadsheet lifecycle management via the MaybeAI platform, including upload, read, edit, analysis, formatting, worksheets, charts, formulas, export, and version operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ojbkxiongdei](https://clawhub.ai/user/ojbkxiongdei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and spreadsheet operators use this skill to guide agents through MaybeAI spreadsheet workflows, including upload, import, reading, editing, formatting, worksheet management, charts, formulas, export, and version-related operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ready-to-run examples can modify, overwrite, clear, delete, export, or otherwise change remote spreadsheets.

Mitigation: Use a MaybeAI token limited to intended spreadsheets, copy or back up spreadsheets first, and require explicit confirmation before destructive or write operations.

Risk: Running bundled scripts against production documents can apply multiple API operations without interactive review.

Mitigation: Read the full script before execution and run workflows on non-production documents until each operation is understood.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ojbkxiongdei/skills/rolex-maybeai-sheet)
- [MaybeAI Sheet Homepage](https://github.com/OmniMCP-AI/maybeai-uni)
- [MaybeAI Platform](https://maybe.ai)
- [MaybeAI API Token Page](https://maybe.ai/user/my-plan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl command examples and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce spreadsheet API calls and local exported .xlsx files; requires MAYBEAI_API_TOKEN, curl, and jq.]

## Skill Version(s):

0.1.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
