## Description:

Manage received inbound emails, attachments, and configured domains through the Resend API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjrussell](https://clawhub.ai/user/mjrussell)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent inspect received Resend emails, retrieve attachment metadata, and check configured domains using the Resend CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned third-party global CLI that handles the Resend API key.

Mitigation: Review the CLI before installing and prefer a pinned, verified version.

Risk: The skill can retrieve private inbound email content and attachment information.

Mitigation: Use a dedicated read-only Resend API key with the narrowest available scope and avoid displaying full message content unless needed.

## Reference(s):

- [ClawHub Resend skill page](https://clawhub.ai/mjrussell/skills/resend)
- [Resend homepage](https://resend.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the resend CLI and RESEND_API_KEY; CLI commands may return JSON when called with --json.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
