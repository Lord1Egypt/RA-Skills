## Description:

Use the `max` command-line tool to search and read messages in the owner's personal MAX Messenger account, answer questions from chat history, inspect attachments, and send messages when directly requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wirecat](https://clawhub.ai/user/wirecat)

### License/Terms of Use:

MIT-0

## Use Case:

The MAX account owner and their assistant use this skill to find chats, understand messages and agreements, review unread items or attachments, and respond to questions grounded in the owner's conversation history. It can also send messages or act through the owner's bots when the owner directly asks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill also documents group administration, task and contact management, and account changes, extending beyond its stated messaging purpose.

Mitigation: Keep those operations within the owner's requested task and require direct authorization before sending messages or changing account, group, contact, or task data.

Risk: The security scan had partial coverage because three local references were unresolved.

Mitigation: Review the unresolved reference material before enabling workflows that send messages or modify account data.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wirecat/skills/wirecat-max)
- [Publisher profile](https://clawhub.ai/user/wirecat)
- [Setup and sign-in](references/setup.md)
- [Search and local history](references/search.md)
- [Reading chats and unread messages](references/reading.md)
- [Sending and other changes](references/sending.md)
- [Groups and moderation](references/groups.md)
- [Contacts and notes](references/contacts.md)
- [Attachments and OCR](references/attachments.md)
- [Owner tasks](references/tasks.md)
- [Bot accounts](references/bot.md)
- [Machine output and CLI contract](references/machine.md)
- [Upstream CLI contract (linked by the skill)](https://github.com/WireCatLabs/max-cli/blob/main/docs/cli-contract.md)
- [Upstream reference guides (linked by the skill)](https://github.com/WireCatLabs/max-cli/tree/main/skills/max-cli/references)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language answers in Markdown, optionally with links to messages; command results may be JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should identify incomplete history or search coverage where relevant and distinguish unknown information from confirmed absence.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
