## Description:

Tmeet Skill helps agents use the Tencent Meeting tmeet CLI for OAuth authentication, meeting lifecycle management, recordings and transcripts, meeting reports, contacts, in-meeting controls, and troubleshooting feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wemeeting](https://clawhub.ai/user/wemeeting)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage Tencent Meeting workflows from the command line, including authentication, meeting setup and updates, recordings, reports, contact lookup for meeting workflows, in-meeting controls, and troubleshooting reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically install a global tmeet CLI package at the latest available version.

Mitigation: Install a pinned, reviewed tmeet CLI version before use and avoid automatic global @latest installation in sensitive workspaces.

Risk: The skill can handle sensitive meeting, credential, contact, recording, and log data.

Mitigation: Avoid sharing auth status output, limit displayed results to necessary fields, and review logs or feedback content for private account, meeting, or business data before upload.

Risk: Some supported commands can change meetings, invitations, recording permission requests, or live participant state.

Mitigation: Require explicit user confirmation before meeting-changing actions and show the relevant operation details using user-facing meeting identifiers.

## Reference(s):

- [Tmeet Skill on ClawHub](https://clawhub.ai/wemeeting/skills/tmeet-skill)
- [tmeet auth](references/tmeet-auth.md)
- [tmeet meeting](references/tmeet-meeting.md)
- [tmeet record](references/tmeet-record.md)
- [tmeet report](references/tmeet-report.md)
- [tmeet contact](references/tmeet-contact.md)
- [tmeet control](references/tmeet-control.md)
- [tmeet troubleshooting](references/tmeet-tshoot.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command-output handling.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide execution of the tmeet CLI and summarize JSON responses while minimizing unnecessary disclosure of sensitive meeting, account, credential, contact, recording, and log data.]

## Skill Version(s):

1.0.6 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
