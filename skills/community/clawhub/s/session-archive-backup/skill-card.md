## Description:

Backup helps an OpenClaw agent set up a session archive and backup workflow for token-limit, idle-timeout, and manual reset events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nevereven619](https://clawhub.ai/user/nevereven619)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to configure session lifecycle archiving, long-term memory sync, reset logging, and GitHub or OneDrive backup behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retain full chat history, persistent memory, and agent configuration data for long-term storage.

Mitigation: Install only when long-term session retention is intended, disable raw transcript backup unless required, and avoid storing secrets in chats.

Risk: Backups may sync sensitive session and configuration data to GitHub or OneDrive without enough privacy controls.

Mitigation: Use private or encrypted backups, review sync destinations before enabling automation, and require manual review before cloud sync.

Risk: GitHub backup configuration may expose credentials if token-in-URL remotes are used.

Mitigation: Prefer SSH or a credential manager instead of embedding tokens in remote URLs.

Risk: Automatic long-term memory updates may preserve incorrect or sensitive information.

Mitigation: Require manual review before MEMORY.md updates are committed or synchronized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nevereven619/skills/session-archive-backup)
- [Workflow diagram](references/workflow-diagram.md)
- [Configuration templates](references/config-templates.md)
- [Troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with configuration templates, PowerShell and shell commands, and JSON or JSONL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local archive structure guidance and backup workflow instructions for OpenClaw sessions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
