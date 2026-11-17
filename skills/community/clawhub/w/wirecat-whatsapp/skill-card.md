## Description:

Read, search and send in the owner's personal WhatsApp through wa, and link it. Use when a question could be answered from the owner's WhatsApp chats (what someone said, agreed, promised or sent, a document, a date, who owes a reply), when asked to find a WhatsApp chat, person or group, read or summarise a conversation, prepare for a meeting from chats, draft or send a reply, or link or connect WhatsApp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wirecat](https://clawhub.ai/user/wirecat)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to answer questions from the owner's WhatsApp chats, find and summarize conversations, and prepare meeting context. It can also draft or send a reply or help link the account when asked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account and chat administration and message writes may be available without explicit owner approval; the security review was incomplete for one component.

Mitigation: Review command and MCP permissions before installation, enable only needed capabilities, and confirm writes through a trusted approval process.

Risk: Use of the unofficial client or bulk and unsolicited messages may put the owner's WhatsApp account at risk.

Mitigation: Avoid bulk or unsolicited messages and send only the exact content to the exact recipient the owner requested.

## Reference(s):

- [Commands reference](references/commands.md)
- [Connection reference](references/connection.md)
- [Groups reference](references/groups.md)
- [History reference](references/history.md)
- [Local store reference](references/local-store.md)
- [Search reference](references/search.md)
- [Sending reference](references/sending.md)
- [Setup reference](references/setup.md)
- [ClawHub release page](https://clawhub.ai/wirecat/skills/wirecat-whatsapp)
- [CLI contract documentation](https://github.com/WireCatLabs/whatsapp-cli/blob/main/docs/cli-contract.md)
- [Search documentation](https://github.com/WireCatLabs/whatsapp-cli/blob/main/docs/search.md)
- [Query language documentation](https://github.com/WireCatLabs/whatsapp-cli/blob/main/docs/query-language.md)
- [MCP documentation](https://github.com/WireCatLabs/whatsapp-cli/blob/main/docs/mcp.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language answers, conversation summaries, and reply drafts with message locators when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers may contain sensitive chat details, and completeness depends on the account's locally stored history.]

## Skill Version(s):

1.0.5 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
