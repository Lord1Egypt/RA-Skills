## Description:

Research websites, extract structured findings, and save clean rows into Google Sheets. Use when users want web research organized into a spreadsheet \u2014 competitor lists, pricing data, contact lists, or any structured table from the web.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn web research into normalized spreadsheet rows and write them to Google Sheets through ClawLink after preview and confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may collect personal data such as emails or LinkedIn profile details during research.

Mitigation: Collect only data the user is allowed to use, keep scope small, and avoid fabricating missing values.

Risk: The skill can append or otherwise write rows to Google Sheets through ClawLink.

Mitigation: Preview the target sheet or range and require explicit user confirmation before creating, appending, overwriting, or bulk updating spreadsheet data.

Risk: Using the skill requires installing and allowing the ClawLink plugin and connecting Google Sheets.

Mitigation: Have the user complete ClawLink pairing intentionally and verify the live Google Sheets tool catalog before attempting writes.

## Reference(s):

- [Research to Sheets on ClawHub](https://clawhub.ai/hith3sh/skills/research-to-sheets)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=research-to-sheets)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Google Sheets Skill](https://clawhub.ai/hith3sh/google-sheets-spreadsheets)
- [Firecrawl Skill](https://clawhub.ai/hith3sh/firecrawl-web-scraping)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and structured row previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide user-confirmed Google Sheets writes through ClawLink after normalizing web research into rows.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
