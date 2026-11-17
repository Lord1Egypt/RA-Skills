## Description:

Indexes a local Markdown lore vault and answers world-building continuity questions with sourced excerpts while tracking expiring canon and retained retcons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paradoxfuzzle](https://clawhub.ai/user/paradoxfuzzle)

### License/Terms of Use:

MIT-0

## Use Case:

World-builders and roleplay server maintainers use this skill to find cited canon in a local Markdown vault, monitor expiring lore, and preserve intentional retcons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The add --file option can write outside the configured lore vault, despite the vault-only documentation.

Mitigation: Use a dedicated vault with backups; do not allow agents to call add --file until absolute paths and traversal are rejected and writes are confined to the vault.

Risk: Adding or replacing entries can overwrite files, and the documentation understates vault-writing behavior.

Mitigation: Review writes and require confirmation or containment for overwrites; align the documentation with the actual behavior before installation.

## Reference(s):

- [Void Lore Index on ClawHub](https://clawhub.ai/paradoxfuzzle/skills/void-lore-index)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Cited lore excerpts and status reports in text or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Markdown vault; lexical matching rather than semantic search; excerpts limited by a configurable character budget. Requires Python 3.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
