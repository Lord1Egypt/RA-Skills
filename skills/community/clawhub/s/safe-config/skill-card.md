## Description:

Safely modifies OpenClaw configuration files by backing up the current config, previewing redacted changes, validating JSON, and requiring explicit user confirmation before edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justaboyhai-wq](https://clawhub.ai/user/justaboyhai-wq)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to review and safely modify persistent OpenClaw configuration for models, channels, tools, and skill settings. It is intended for workflows where configuration integrity and credential redaction matter before applying changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Redacted previews may expose secrets if string-based redaction misses a credential shape or nested field.

Mitigation: Use structural JSON redaction for known and user-defined secret fields, and avoid sharing preview output outside the local review session.

Risk: Writing replacement configuration through a shared /tmp path can allow race conditions or unintended file replacement.

Mitigation: Write temporary files in the same protected directory as the target config with restrictive permissions, then atomically rename after validation.

Risk: Configuration edits can break OpenClaw service behavior if applied without validation and rollback material.

Mitigation: Validate JSON before and after edits, create a timestamped backup before writing, and keep rollback instructions available.

## Reference(s):

- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw configuration examples](artifact/references/examples.md)
- [ClawHub skill page](https://clawhub.ai/justaboyhai-wq/skills/safe-config)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local file edits, redacted previews, validation steps, backups, and restart commands for OpenClaw configuration workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
