## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parker-xferops](https://clawhub.ai/user/parker-xferops)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to work with Google Workspace services through the gog CLI, including Gmail, Calendar, Drive, Contacts, Sheets, and Docs tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned third-party CLI.

Mitigation: Install a reviewed and pinned gogcli version before use.

Risk: Google Workspace OAuth authorization can expose sensitive mail, calendar, Drive, contacts, document, and sheet data.

Mitigation: Authorize only the Google services needed for the task.

Risk: Headless setup may encourage storing GOG_KEYRING_PASSWORD in shell profiles or service files.

Mitigation: Avoid storing GOG_KEYRING_PASSWORD directly in shell profiles or service files; prefer a safer keyring setup where possible.

Risk: The CLI can send email or modify calendars, sheets, and Drive content.

Mitigation: Confirm any email, calendar, sheet, or Drive-modifying action before running it.

## Reference(s):

- [gogcli homepage](https://gogcli.sh)
- [ClawHub skill page](https://clawhub.ai/parker-xferops/skills/xferops-gog)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog CLI and Google OAuth setup.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
