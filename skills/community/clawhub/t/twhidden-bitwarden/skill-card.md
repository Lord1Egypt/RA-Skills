## Description:

Bitwarden & Vaultwarden password manager integration for storing, retrieving, generating, and managing credentials through the Bitwarden CLI with automatic session management for official Bitwarden and self-hosted Vaultwarden servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twhidden](https://clawhub.ai/user/twhidden)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to let an OpenClaw agent store, retrieve, generate, and manage Bitwarden or Vaultwarden credentials through the Bitwarden CLI. It is intended for workflows where the operator is comfortable granting the agent vault access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access an unlocked Bitwarden or Vaultwarden vault and retrieve, create, edit, or delete credentials.

Mitigation: Use a dedicated low-scope vault account where possible and require manual approval for retrieve, create, edit, delete, and register commands.

Risk: Master password and server credentials may be supplied through environment variables or a plaintext credential file.

Mitigation: Avoid plaintext master-password files where possible, keep credential files out of version control, and restrict credential file permissions to the current user.

Risk: Session tokens are cached locally at /tmp/.bw_session during use.

Mitigation: Lock or logout after use so the session file is removed, and avoid sharing systems where temporary files may be exposed.

Risk: Vault authentication and encrypted vault operations are sent to the configured BW_SERVER.

Mitigation: Use HTTPS for BW_SERVER and only configure trusted Bitwarden or Vaultwarden servers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/twhidden/skills/twhidden-bitwarden)
- [Bitwarden](https://bitwarden.com/)
- [Bitwarden CLI Documentation](https://bitwarden.com/help/cli/)
- [Vaultwarden](https://github.com/dani-garcia/vaultwarden)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command output from the Bitwarden CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May surface credential values or vault item JSON when retrieval commands are used.]

## Skill Version(s):

1.0.5 (source: server release metadata and CHANGELOG, released 2026-02-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
