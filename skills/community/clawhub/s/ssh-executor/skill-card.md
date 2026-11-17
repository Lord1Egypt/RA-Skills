## Description:

Execute commands on remote hosts over SSH with structured discovery, pluggable credential backends, and safety guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rickkbarbosa](https://clawhub.ai/user/rickkbarbosa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and administer remote Linux servers over SSH, gather structured discovery results, and run approved maintenance commands with credential and host-key guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private-key and sudo-password handling can expose credentials.

Mitigation: Prefer the base key-only edition, avoid password and sudo modes unless necessary, and do not export private keys into environment variables.

Risk: Remote command execution and sudo paths can enable unintended or unsafe changes.

Mitigation: Review and harden the scripts before installation, require explicit approval for sudo or destructive commands, and start with read-only inspection.

Risk: Command injection issues are identified as unresolved in the authoritative security guidance.

Mitigation: Pin dependencies, review commands before execution, and treat vault-backed key storage and sudo execution as high-risk until the issues are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rickkbarbosa/skills/ssh-executor)
- [Safety notes](references/safety.md)
- [Vault backend integration](references/vault-backends.md)
- [Vaultwarden and SSH agent integration](references/vault-ssh-integration.md)
- [Multiplexing verification](references/multiplexing-verification.md)
- [Docker diagnostics without Docker CLI](references/docker-diagnostics-without-cli.md)
- [Remote backup cleanup via SSH](references/remote-backup-cleanup.md)
- [Security audit history](references/security-audit-2026-07-clawhub.md)
- [Testing pitfalls](references/testing-pitfalls-2026-07-23.md)
- [Troubleshooting field notes](references/troubleshooting-field-notes.md)
- [Vault key format](references/vault-key-format.md)
- [Server-to-server rsync](references/server-to-server-rsync.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON command-result contracts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote execution results are intended to separate exit status, stdout, stderr, confirmed facts, assumptions, open questions, and required approvals.]

## Skill Version(s):

2.4.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
