## Description:

Read, search and send in the owner's personal WhatsApp through wa, and link it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wirecat](https://clawhub.ai/user/wirecat)

### License/Terms of Use:

MIT-0

## Use Case:

People using their own WhatsApp account can search and review stored chats, find messages and follow-ups, prepare summaries or replies, and connect the account when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is rated suspicious because administrative and destructive messaging commands were reported beyond the stated scope, and the sending guide was only partially inspected.

Mitigation: Review the complete sending guide and command permission list before installation; restrict administrative and destructive commands or require explicit owner approval.

Risk: The skill can read private chat content and perform external writes such as sending or deleting messages; its documentation also warns of account restriction or ban risk from unofficial or bulk use.

Mitigation: Use minimal permissions, require the owner's explicit request for each write, and avoid bulk or unsolicited messages.

## Reference(s):

- [Setup and installation](references/setup.md)
- [Command reference](references/commands.md)
- [Search and chat evidence](references/search.md)
- [History and coverage](references/history.md)
- [Sending safeguards](references/sending.md)
- [Connection lifecycle](references/connection.md)
- [Groups and account controls](references/groups.md)
- [CLI contract](https://github.com/WireCatLabs/whatsapp-cli/blob/main/docs/cli-contract.md)
- [Search guide](https://github.com/WireCatLabs/whatsapp-cli/blob/main/docs/search.md)
- [Query language](https://github.com/WireCatLabs/whatsapp-cli/blob/main/docs/query-language.md)
- [MCP guide](https://github.com/WireCatLabs/whatsapp-cli/blob/main/docs/mcp.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Text or Markdown, with shell command examples where useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chat answers reflect locally stored history and may be incomplete.]

## Skill Version(s):

1.0.6 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
