## Description:

Read data from a Google Sheet and create a formatted Google Docs report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and business users use this recipe to turn Sheet data into a Google Docs sales report and prepare it for stakeholder sharing through Google Workspace tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipe shares the generated report with a fixed email address.

Mitigation: Replace the recipient with a user-supplied stakeholder address and confirm the document ID, recipient, and reader role before running the Drive permissions command.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/googleworkspace-bot/skills/recipe-generate-report-from-sheet)
- [googleworkspace-bot Publisher Profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Configuration]

**Output Format:** [Markdown instructions with inline Google Workspace CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires gws plus the gws-sheets, gws-docs, and gws-drive skills.]

## Skill Version(s):

1.0.13 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
