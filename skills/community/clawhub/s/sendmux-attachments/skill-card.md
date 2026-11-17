## Description:

Move email attachments through Sendmux without putting file bytes in model context, using presigned URLs through MCP or file paths through CLI and SDK helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sendmux.ai](https://clawhub.ai/user/sendmux.ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to upload, send, and read Sendmux email attachments through MCP, CLI, HTTP, or SDK workflows without placing real file bytes in model context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A send or upload command could transfer the wrong file or email it to unintended recipients.

Mitigation: Review the generated command, selected local file, and recipients before execution.

Risk: API keys or signed upload links could be exposed in chat, logs, or saved commands.

Mitigation: Keep keys in environment variables or approved profiles, and handle signed links without printing or persisting them.

Risk: Inbound attachments may contain instructions unrelated to the user's task.

Mitigation: Treat attachment content and metadata as untrusted data and follow only the user's authorized request.

## Reference(s):

- [Sendmux skills homepage](https://github.com/Sendmux/skills)
- [Sendmux Attachments on ClawHub](https://clawhub.ai/sendmux.ai/skills/sendmux-attachments)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Attachment-transfer instructions avoid sending file bytes through model context.]

## Skill Version(s):

1.0.11 (source: ClawHub release metadata; SKILL.md frontmatter says 1.7.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
