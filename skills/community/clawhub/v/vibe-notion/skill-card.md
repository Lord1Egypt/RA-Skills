## Description:

Interact with Notion using the unofficial private API for pages, databases, blocks, search, users, and comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devxoul](https://clawhub.ai/user/devxoul)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to inspect, search, and modify Notion workspaces through the vibe-notion CLI. It supports workspace discovery, page and database management, block and comment operations, and batch updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a full Notion user session credential through an unofficial private API.

Mitigation: Install only when full-user Notion automation is intended; prefer the official integration-token CLI for lower-risk work and clear or rotate the stored session token when finished.

Risk: The skill can perform broad write, archive, delete, upload, and batch operations across Notion workspaces.

Mitigation: Review every write, delete, archive, upload, and batch command before execution, especially operations generated from large JSON files.

Risk: Private API behavior may change outside the skill publisher's control.

Mitigation: Pin and verify the package version before use, and expect compatibility review after Notion client or API changes.

Risk: Schema $hints can recommend changes to a user's Notion database structure.

Mitigation: Treat $hints as advisory; confirm the suggested database fix with the user before running any modifying command.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/devxoul/skills/vibe-notion)
- [Publisher Profile](https://clawhub.ai/user/devxoul)
- [Batch Operations](references/batch-operations.md)
- [Block Types Reference](references/block-types.md)
- [Common Patterns for Vibe Notion](references/common-patterns.md)
- [Output Format](references/output-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return JSON by default; --pretty provides human-readable formatting.]

## Skill Version(s):

1.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
