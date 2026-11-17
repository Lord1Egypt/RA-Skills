## Description:

Read data from two tabs in a Google Sheet to compare and identify differences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, analysts, and workflow builders use this recipe to have an agent read two Google Sheets tabs and compare the ranges for differences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spreadsheet contents may be sensitive when the agent reads user-provided sheet ranges.

Mitigation: Review the spreadsheet ID and tab ranges before running commands, and only provide ranges the agent is authorized to read.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/googleworkspace-bot/skills/recipe-compare-sheet-tabs)
- [Publisher Profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses gws and the gws-sheets skill to read user-provided spreadsheet IDs and ranges.]

## Skill Version(s):

0.22.5 (source: frontmatter); ClawHub release 1.0.14

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
