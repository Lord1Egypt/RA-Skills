## Description:

Interact with Notion workspaces using the official API to manage pages, databases, blocks, users, and comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devxoul](https://clawhub.ai/user/devxoul)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and AI agents use this skill to inspect and update Notion workspaces through the vibe-notionbot CLI, including page, database, block, user, search, comment, and batch operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make broad Notion workspace changes, including archive, delete, database schema, upload, comment, and batch operations.

Mitigation: Use a narrowly scoped Notion integration token, share only the required pages and databases with the integration, and review write, delete, archive, database, and batch commands before execution.

Risk: The release installs an npm package without a pinned version in the provided install metadata.

Mitigation: Pin the vibe-notion package to a reviewed version where possible before installing or running the CLI.

Risk: The skill text points to a separate private-API desktop-token path that has broader credential behavior than the official API bot flow.

Mitigation: Prefer vibe-notionbot with NOTION_TOKEN for this skill and avoid the private-API desktop-token path unless the user intentionally accepts that broader credential behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/devxoul/skills/vibe-notionbot)
- [Notion Developer Portal](https://www.notion.so/my-integrations)
- [vibe-notion Feature Requests](https://github.com/devxoul/vibe-notion/issues)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Markdown, Guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require the vibe-notionbot binary and a NOTION_TOKEN integration token; batch operations use JSON payloads and fail fast on the first error.]

## Skill Version(s):

1.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
