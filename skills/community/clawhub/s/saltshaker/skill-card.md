## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yueyongyue](https://clawhub.ai/user/yueyongyue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up and run the gog CLI for Google Workspace tasks across Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Google Workspace OAuth access, which can expose account data or enable account actions if granted too broadly.

Mitigation: Use the narrowest Google account and service scopes needed for the task.

Risk: Commands can send email, create calendar events, or modify and clear spreadsheet ranges.

Mitigation: Confirm intent and target resources before running write actions, especially mail, calendar, and Sheets update, append, or clear commands.

Risk: The skill depends on an external Homebrew formula for the gog CLI.

Mitigation: Install only after reviewing and trusting the gog Homebrew formula and the CLI source.

## Reference(s):

- [GOG CLI homepage](https://gogcli.sh)
- [ClawHub skill page](https://clawhub.ai/yueyongyue/skills/saltshaker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OAuth setup steps, Google Workspace command examples, account-selection tips, JSON output guidance, and confirmation guidance for sensitive operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
