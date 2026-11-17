## Description:

WeChat AI assistant that sends messages to contacts and auto-replies based on visible chat context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cool131219](https://clawhub.ai/user/cool131219)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to send WeChat messages or read visible WeChat chat context and prepare auto-replies for a selected contact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read visible WeChat conversations and may expose chat content to an external OCR service.

Mitigation: Use it only for non-sensitive chats unless explicit OCR consent, local OCR, or clear external OCR disclosure is added.

Risk: The skill can send WeChat messages automatically as the user.

Mitigation: Require a human preview and confirmation step before any outbound message is sent.

Risk: Security evidence reports unsafe shell examples and missing bundled scripts.

Mitigation: Review the supplied scripts before installation and replace unsafe shell usage with safer subprocess or input handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cool131219/skills/reply-wechat-message)
- [Server-resolved GitHub source](https://github.com/cool131219/WeChat-Butler/tree/main/reply-wechat-message)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown instructions with inline shell commands and structured conversation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read visible WeChat chat context and send messages through bundled scripts when present.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
