## Description:

Undo gives AI coding agents local file-change snapshots, history listing, checkpoints, and restore commands so they can revert project files to earlier states.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-guang](https://clawhub.ai/user/x-guang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to track file edits during AI-assisted work, create checkpoints before risky changes, inspect history, and revert project files by step count, timestamp, or named checkpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initialization can make automatic host package changes.

Mitigation: Review initialization before use, remove or explicitly gate automatic package installation, and avoid privileged or production environments.

Risk: The skill persists broad local snapshots of project source files outside the project directory.

Mitigation: Use only in projects where persistent local snapshots are acceptable, avoid repositories containing secrets, and define cleanup expectations for snapshot storage.

Risk: Scanner guidance identifies local command-injection and symlink-copying risks.

Mitigation: Prefer a patched version that uses safe Git argument arrays, strict checkpoint-name validation, and avoids tracking untrusted symlinks.

Risk: Undo operations can overwrite working files while restoring an earlier state.

Mitigation: Require user confirmation before undo operations and preserve the pre-undo state through checkpoints.

## Reference(s):

- [Undo API Reference](artifact/references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/x-guang/skills/undo)
- [OpenClaw Skills Documentation](https://openclaws.io/docs/tools/skills/)
- [AgentSkills](https://agentskills.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and one-line JSON script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and Git; scripts operate on local project files and persistent local snapshot storage.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
