## Description:

Automatically enforces workspace file size limits, archives stale or oversized files, and organizes root contents to keep AI agent context efficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casperzinou](https://clawhub.ai/user/casperzinou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep long-running AI workspaces lean by moving root-level clutter, trimming boot files, archiving stale memory notes, and logging cleanup results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically change agent memory and instruction files, which may alter future agent context.

Mitigation: Require explicit approval or protected-section parsing before changing AGENTS.md or MEMORY.md, and review resulting diffs before reuse.

Risk: The cleanup script can permanently delete very small Markdown files.

Mitigation: Replace deletion with quarantine or archive behavior and keep backups before scheduled runs.

Risk: A fixed workspace path and ordinary move operations can archive files from the wrong workspace or overwrite existing archive files.

Mitigation: Make the workspace path configurable and use collision-safe archive names before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/casperzinou/skills/talonforge-workspace-hygiene)
- [Publisher profile](https://clawhub.ai/user/casperzinou)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and a bash cleanup script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces cleanup reports and may write archive or log files when scheduled or invoked.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
