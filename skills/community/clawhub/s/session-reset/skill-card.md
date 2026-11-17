## Description:

Session Reset helps manage OpenClaw agent session files through preview, backup, restore, cleanup, and scoped reset workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[traceless929](https://clawhub.ai/user/traceless929)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw developers and operators use this skill to preview and reset stale or targeted agent sessions, apply updated agent configuration, free disk space, and restore backups after accidental deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reset and restore operations may delete or overwrite files outside intended OpenClaw session directories when crafted scope or restore inputs are accepted.

Mitigation: Use the skill only after strict scope and restore-input validation, path containment checks, and review of backup manifests; pass only known agent names or valid backup timestamps.

Risk: The --force option bypasses confirmation on destructive reset operations.

Mitigation: Avoid --force on important environments; use --dry-run first and require clear human confirmation before deleting session files.

Risk: Untrusted backup manifests can influence restore destinations and overwrite existing session files.

Mitigation: Restore only from trusted backups and inspect the manifest contents before running restore commands.

## Reference(s):

- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw Skill development guide](https://docs.openclaw.ai/skills)
- [OpenClaw Session management](https://docs.openclaw.ai/sessions)
- [Artifact reference README](artifact/references/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference destructive reset, restore, and cleanup commands that should be previewed and confirmed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
