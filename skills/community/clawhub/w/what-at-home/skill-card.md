## Description:

What At Home helps users record, search, move, back up, restore, and export household inventory organized by suite, room, furniture, and item.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yixj](https://clawhub.ai/user/yixj)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to maintain a local household inventory and find where items are stored. It supports inventory setup, item tracking, fuzzy search, storage recommendations, backup, restore, and export workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Household item names and storage locations are kept as plaintext local inventory data.

Mitigation: Install only if plaintext local storage is acceptable, keep the OpenClaw workspace private, and avoid placing exported inventory files in shared or synced folders without review.

Risk: Delete and restore commands can remove or replace inventory records.

Mitigation: Use explicit inventory wording for destructive commands and review available backups before restoring data.

Risk: Backup and export files can expose the same household inventory details as the primary data file.

Mitigation: Keep backups private and review exported JSON files before sharing or moving them outside the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yixj/skills/what-at-home)
- [Publisher profile](https://clawhub.ai/user/yixj)

## Skill Output:

**Output Type(s):** [text, JSON, files, guidance]

**Output Format:** [Plain text responses with optional JSON inventory, backup, and export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists local household inventory data under the OpenClaw workspace data directory.]

## Skill Version(s):

1.0.3 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
