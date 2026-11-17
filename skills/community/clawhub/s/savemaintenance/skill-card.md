## Description:

Deterministic reconciliation of conversation-log.md, FTS5 index, and saved conversations for one-shot repair or maintenance runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirza42](https://clawhub.ai/user/mirza42)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to maintain saved-memory consistency by backing up memory files, reconciling conversation logs with saved markdown files, rebuilding the FTS5 index, and auditing the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rewrite saved-memory data during reconciliation.

Mitigation: Run dry mode first, keep generated backups, and review planned changes before a full repair run.

Risk: Custom snapshot tags may place sensitive memory copies outside the intended snapshot directory.

Mitigation: Use the default timestamped snapshot name or simple tags without slashes or absolute paths.

Risk: Backups and snapshots may contain sensitive saved-memory content.

Mitigation: Store the OpenClaw workspace securely and inspect generated backups or snapshots before sharing or moving them.

Risk: Server security evidence says this version needs review before relying on restore or full reconciliation.

Mitigation: Test in a disposable workspace and review the scripts before using them on important saved-memory data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirza42/skills/savemaintenance)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text, Configuration]

**Output Format:** [Markdown with inline bash commands and plaintext maintenance output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and an existing OpenClaw saved-memory workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
