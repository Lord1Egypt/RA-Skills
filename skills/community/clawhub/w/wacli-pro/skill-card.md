## Description:

Professional WhatsApp messaging via the wacli CLI for searching chat history, drafting natural messages, managing follow-ups, and sending messages or files from a user's personal WhatsApp account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prantikmedhi](https://clawhub.ai/user/prantikmedhi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to draft, review, and send context-aware WhatsApp messages through a configured wacli session. It is intended for personal, professional, and follow-up messaging where recent chat history, recipient identity, tone, and explicit send confirmation matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can inspect relevant WhatsApp chat history through the user's configured wacli session.

Mitigation: Limit history lookup to the minimum context needed for the requested message and avoid unnecessary personal data exposure.

Risk: The agent can send WhatsApp messages or files on the user's behalf.

Mitigation: Review the recipient, message text, and attachment before confirming, especially for sensitive personal, financial, or professional conversations.

Risk: Recipient ambiguity could cause a message to be sent to the wrong chat.

Mitigation: Ask the user to choose when multiple chats match and do not guess recipients.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/prantikmedhi/skills/wacli-pro)
- [History workflow](references/history-workflow.md)
- [Message patterns](references/message-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline wacli shell commands and drafted message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recipient lookup steps, concise message drafts, confirmation prompts, send commands, and a post-send summary.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
