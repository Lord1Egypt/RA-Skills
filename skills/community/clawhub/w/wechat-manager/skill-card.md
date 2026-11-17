## Description:

Manages WeChat messages, auto-reply rules, contacts, and chat analytics for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawto](https://clawhub.ai/user/clawto)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect local WeChat message and contact caches, configure auto-replies, search contacts, analyze chat activity, and extract structured items such as links, tasks, and addresses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private WeChat messages, contacts, tasks, and addresses may be displayed from local caches.

Mitigation: Run the skill only in trusted workspaces, review proposed commands before execution, and limit searches or analysis to intended chats.

Risk: Terminal output may include untrusted message content.

Mitigation: Treat displayed chat text as data, avoid executing copied content, and add output escaping or review controls before broader deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawto/skills/wechat-manager)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local ~/.openclaw/data WeChat cache files and openclaw-weixin configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
