## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yueyongyue](https://clawhub.ai/user/yueyongyue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate setup guidance and CLI commands for automating Google Workspace tasks across Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party Homebrew formula.

Mitigation: Review the Homebrew source before installing or running the gog CLI.

Risk: OAuth authorization can grant broad access to Google Workspace services.

Mitigation: Grant only the Google services required for the workflow and consider using a dedicated or low-privilege Google account.

Risk: Generated commands can send mail, create events, or modify spreadsheet data.

Mitigation: Verify recipients, calendar targets, sheet IDs, and ranges before executing write, append, clear, or send commands.

## Reference(s):

- [gog homepage](https://gogcli.sh)
- [ClawHub skill page](https://clawhub.ai/yueyongyue/skills/saltshaer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented command examples for scripting workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
