## Description: <br>
Interact with Notion using the unofficial private API - pages, databases, blocks, search, users, comments <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devxoul](https://clawhub.ai/user/devxoul) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to read, search, create, update, and organize Notion pages, databases, blocks, comments, users, and workspace content through the vibe-notion CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI uses the user's Notion desktop session token and acts as the user in accessible workspaces. <br>
Mitigation: Install only when this access model is acceptable, prefer the official Notion integration for sensitive workspaces, and remove ~/.config/vibe-notion/credentials.json when finished. <br>
Risk: Write, delete, and batch operations can make broad workspace changes without strong confirmation boundaries. <br>
Mitigation: Review all write, delete, and batch operations before execution, and do not blindly apply $hints fixes. <br>
Risk: Persistent memory may retain workspace IDs, page IDs, database IDs, and user preferences. <br>
Mitigation: Do not store credentials, tokens, full page content, or sensitive data in memory, and remove ~/.config/vibe-notion/MEMORY.md when the skill is no longer used. <br>


## Reference(s): <br>
- [Vibe Notion ClawHub release](https://clawhub.ai/devxoul/vibe-notion) <br>
- [Batch Operations](references/batch-operations.md) <br>
- [Block Types Reference](references/block-types.md) <br>
- [Common Patterns for Vibe Notion](references/common-patterns.md) <br>
- [Output Format](references/output-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands generally return JSON by default, with human-readable output available through --pretty.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
