## Description:

Search, list, and manage Raindrop.io bookmarks via CLI, including reading bookmarks and collections as well as adding, deleting, moving, updating, and bulk-moving bookmarks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[velvet-shark](https://clawhub.ai/user/velvet-shark)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage a Raindrop.io bookmark library from an agent-accessible command-line workflow. It supports search, collection browsing, bookmark creation, tag and title updates, deletion, movement between collections, and bulk organization tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a Raindrop.io token to read and modify the user's bookmark account, including deletion and bulk movement.

Mitigation: Install only when that account access is acceptable, use the least exposed token handling available, and review destructive or bulk operations before execution.

Risk: Credential handling may expose a Raindrop.io token if it is passed on the command line or stored with weak file permissions.

Mitigation: Prefer a protected environment variable or secure credential store, avoid command-line tokens for regular use, and restrict permissions on any token file.

Risk: Delete and bulk operations execute immediately and can affect many bookmarks.

Mitigation: Require explicit confirmation or dry-run review in agent workflows before delete, move, update, or bulk-move commands are run.

## Reference(s):

- [Raindrop.io Developer Documentation](https://developer.raindrop.io/)
- [Raindrop.io Integrations Settings](https://app.raindrop.io/settings/integrations)
- [ClawHub Skill Page](https://clawhub.ai/velvet-shark/skills/raindrop)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke Raindrop.io API operations that read, write, delete, update, or bulk-move bookmarks when used with a valid RAINDROP_TOKEN.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
