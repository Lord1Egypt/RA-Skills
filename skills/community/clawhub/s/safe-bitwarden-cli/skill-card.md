## Description:

Industrial-grade secure bridge to Bitwarden. Copy passwords and TOTP codes with Zero-trust kernel-level piping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chyern](https://clawhub.ai/user/chyern)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search Bitwarden vault item metadata and copy selected passwords or TOTP codes to the native system clipboard through the Bitwarden CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passwords and TOTP codes are copied into the system clipboard, where clipboard history, shared sessions, monitoring, or remote desktop tooling may expose secrets.

Mitigation: Use only on trusted local systems, disable or clear clipboard history, avoid shared or monitored environments, and clear or harden the clipboard after copying secrets.

Risk: An active BW_SESSION lets the agent search Bitwarden item metadata and trigger password or TOTP copy operations.

Mitigation: Keep BW_SESSION local, confirm the intended item before copy or TOTP actions, and lock or expire the Bitwarden session when finished.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chyern/skills/safe-bitwarden-cli)
- [Publisher profile](https://clawhub.ai/user/chyern)
- [Agent-Skills homepage](https://github.com/chyern/Agent-Skills)
- [Bitwarden CLI](https://github.com/bitwarden/clients/tree/master/apps/cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output from setup/search actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Bitwarden CLI session token in BW_SESSION and an OS clipboard command such as pbcopy, clip, xclip, or wl-copy.]

## Skill Version(s):

1.6.0 (source: SKILL.md frontmatter, manifest.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
