## Description:

Helps developers create and manage OpenClaw subagents by setting up independent workspaces, local skill directories, Feishu channel integration, and message-prefix conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[google-q-dot](https://clawhub.ai/user/google-q-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create OpenClaw subagents with dedicated workspaces, local skill copies, configuration files, and Feishu bot/channel bindings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Created subagents may forward every message to a Feishu group without filtering.

Mitigation: Use only controlled Feishu destinations and limit syncing to explicit, sanitized status updates.

Risk: Session data or secrets may be stored in plaintext MEMORY.md files.

Mitigation: Do not store sessions, app secrets, or credentials in memory files; use a secret manager or protected runtime configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/google-q-dot/skills/subagent-creator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, shell, Python, and filesystem examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes example OpenClaw directory structures and Feishu configuration snippets.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
