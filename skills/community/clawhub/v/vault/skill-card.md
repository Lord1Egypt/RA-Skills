## Description:

Secure local password storage tool with AES-256-GCM encryption. Store, retrieve, and manage passwords with CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuiho-kai](https://clawhub.ai/user/zuiho-kai)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to store, retrieve, list, and remove local passwords, API keys, and credentials from a CLI-backed encrypted vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-handling and local storage behavior require review before the skill is used for real passwords or API keys.

Mitigation: Review before installing, use a strong master key, keep the default vault path unless filesystem risks are understood, and set restrictive permissions on the vault file.

Risk: Secrets entered directly as CLI arguments may be exposed by logged shells or command capture.

Mitigation: Avoid typing secrets directly into logged shell sessions and use operational controls that prevent command history or terminal logging from recording credentials.

Risk: Stored entries can be lost if the master key is lost, entries are removed, or the local vault file is corrupted.

Mitigation: Back up the master key and vault data securely before relying on the vault for important credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zuiho-kai/skills/vault)
- [Project Repository](https://github.com/zuiho-kai/openclaw-vault)
- [Project Issues](https://github.com/zuiho-kai/openclaw-vault/issues)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text CLI responses and Markdown documentation with inline shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, and VAULT_MASTER_KEY; stores encrypted vault data locally by default.]

## Skill Version(s):

1.1.2 (source: frontmatter, CHANGELOG, package.json, openclaw.plugin.json; released 2026-02-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
