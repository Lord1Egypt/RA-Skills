## Description:

Executes remote SSH commands with structured discovery, pluggable credential backends, sudo and password-auth support, strict default host-key checks, and JSON command results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rickkbarbosa](https://clawhub.ai/user/rickkbarbosa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and operators use this skill to inspect and maintain Linux servers over SSH, starting with read-only discovery and escalating to mutating or sudo commands only with explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential exposure can occur through password authentication, sudo-password flows, private-key handling, or environment-variable secrets.

Mitigation: Prefer the base key-only edition unless sudo or password authentication is required; use dedicated least-privilege SSH accounts and single-purpose keys, avoid exporting private keys into environment variables, and avoid sudo-password or sensitive key-storage flows until the reported exposure issues are fixed.

Risk: Remote commands can mutate or damage systems, especially when sudo or destructive shell commands are allowed.

Mitigation: Start with read-only inspection, show the exact command before execution, and require explicit approval for every mutating or privileged command.

Risk: Host-key bypass or unverified first contact can expose SSH sessions to man-in-the-middle attacks.

Mitigation: Keep strict host-key verification enabled, manually verify host fingerprints before first connection, and avoid disabling host-key checks except with explicit user acceptance of the risk.

Risk: Local command-injection risk exists when command, host, user, or credential inputs are assembled for SSH execution.

Mitigation: Use narrow, single-purpose commands; validate target host and user values with the operator; and require review before running chained, privileged, or mutating commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rickkbarbosa/skills/ssh-full)
- [Publisher profile](https://clawhub.ai/user/rickkbarbosa)
- [SSH Executor Safety Notes](artifact/references/safety.md)
- [ClawHub Security Audit - July 2026](artifact/references/security-audit-2026-07-clawhub.md)
- [Vault Backend Integration](artifact/references/vault-backends.md)
- [Vaultwarden + SSH Agent Integration](artifact/references/vault-ssh-integration.md)
- [SSH Key Format in Vaultwarden](artifact/references/vault-key-format.md)
- [Multiplexing Verification](artifact/references/multiplexing-verification.md)
- [Server-to-Server rsync via Temporary Key](artifact/references/server-to-server-rsync.md)
- [Remote Backup Cleanup via SSH](artifact/references/remote-backup-cleanup.md)
- [Docker Diagnostics Without Docker CLI](artifact/references/docker-diagnostics-without-cli.md)
- [Testing Pitfalls - Discovered 2026-07-23](artifact/references/testing-pitfalls-2026-07-23.md)
- [Troubleshooting Field Notes](artifact/references/troubleshooting-field-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command-result stdout is intended to be parseable JSON; stderr carries status messages, warnings, and progress.]

## Skill Version(s):

2.4.2 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
