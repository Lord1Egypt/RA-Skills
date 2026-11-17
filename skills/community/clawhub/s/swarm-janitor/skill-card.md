## Description:

Enterprise-grade OpenClaw skill for cleaning up orphaned subagent processes, archiving transcripts to SuperMemory, and freeing disk space without losing work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvcidpsyche](https://clawhub.ai/user/lvcidpsyche)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to identify orphaned OpenClaw subagent sessions, preserve transcripts through archival, and clean old session files according to configurable retention policies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill promotes deleting OpenClaw session data, including force and no-archive usage patterns.

Mitigation: Run dry-run first, verify the session path and retention settings, keep separate backups, and avoid force or no-archive modes unless the data is already protected.

Risk: The reviewed package does not include the Python cleanup script referenced by the documentation.

Mitigation: Confirm the cleanup script source and behavior before deployment, and do not run substitute scripts without review.

Risk: Transcript archival may involve SuperMemory credentials or external storage destinations.

Mitigation: Protect SUPERMEMORY_API_KEY, choose an approved archive destination, and verify archived transcripts before deletion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lvcidpsyche/skills/swarm-janitor)
- [Configuration Reference](references/config.yaml)
- [Project Homepage](https://github.com/openclawdad/swarm-janitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; documented execution may produce cleanup reports, logs, archived transcripts, and deleted session files.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
