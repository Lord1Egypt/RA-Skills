## Description:

Zoom API integration for meetings, calendar, chat, and user management. Use when the user asks to schedule meetings, check Zoom calendar, list recordings, send Zoom chat messages, manage contacts, or interact with any Zoom Workplace feature. Supports Server-to-Server OAuth and OAuth apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanchunsiong](https://clawhub.ai/user/tanchunsiong)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and agent users can use this skill to manage Zoom meetings, recordings, summaries, chat, users, contacts, and phone call logs through a Python CLI backed by Zoom OAuth credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use broad Zoom account-level API privileges.

Mitigation: Create a dedicated Zoom app and grant only the scopes needed for the commands you plan to use.

Risk: Zoom credentials and cached access tokens are sensitive.

Mitigation: Protect the local `.env` file and `/tmp/zoom_token.json`, and remove cached tokens when the workspace is shared or no longer trusted.

Risk: Some commands can delete meetings or recordings, send chat messages, or change meeting settings.

Mitigation: Review destructive and posting commands before allowing an agent to execute them.

Risk: The documented install command uses a system-wide pip override.

Mitigation: Prefer a virtual environment or another isolated Python environment instead of system-wide installation.

## Reference(s):

- [Zoom Authentication Setup](references/AUTH.md)
- [ClawHub Skill Page](https://clawhub.ai/tanchunsiong/skills/zoom-unofficial-community-skill)
- [Zoom Marketplace](https://marketplace.zoom.us/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance, shell command examples, terminal text, JSON responses, and downloaded files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands create, update, delete, post, or download Zoom resources using account-scoped OAuth access.]

## Skill Version(s):

0.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
