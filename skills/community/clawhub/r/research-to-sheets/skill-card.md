## Description: <br>
Research websites, extract structured findings, and save clean rows into Google Sheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to turn web research into structured Google Sheets rows for competitor lists, pricing data, contact lists, and similar tabular research tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects Google Sheets through OAuth and requires sensitive credentials. <br>
Mitigation: Use it only with authorized accounts and data, and complete setup through the disclosed ClawLink flow. <br>
Risk: Research rows may contain personal or contact data such as names, roles, emails, phone numbers, or profile data. <br>
Mitigation: Collect and store only data the user is authorized to process, keep values structured, and avoid fabricating missing fields. <br>
Risk: Spreadsheet create, append, overwrite, or bulk-update actions can change user data. <br>
Mitigation: Preview the target sheet or range and obtain user confirmation before executing any write. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hith3sh/research-to-sheets) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=research-to-sheets) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>
- [Google Sheets API](https://developers.google.com/sheets/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, structured previews, and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include normalized spreadsheet rows, sheet or range summaries, skipped-row notes, and tool-call guidance.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
