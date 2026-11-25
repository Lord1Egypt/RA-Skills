## Description:

Set up WhatsApp and read or send messages in the owner's personal account through wa.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wirecat](https://clawhub.ai/user/wirecat)

### License/Terms of Use:

MIT-0

## Use Case:

Assistants use this skill to set up and operate the owner's personal WhatsApp account: find chats, read or search conversations, and send messages the owner explicitly requests. It also documents account, contact, and group actions and the safeguards for using them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security evidence is incomplete and flags capabilities beyond WhatsApp messaging, including task tracking, local-note search, and account or group administration.

Mitigation: Review those capabilities against your needs before installing, as advised by the security evidence.

Risk: The skill operates on a real personal WhatsApp account; unsolicited or bulk messaging can lead to account restrictions or bans.

Mitigation: Send only messages the owner explicitly requested, avoid bulk sends and unfamiliar recipients, and stop after a rate-limit refusal.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wirecat/skills/whatsapp-cli)
- [CLI contract](https://github.com/WireCatLabs/whatsapp-cli/blob/main/docs/cli-contract.md)
- [Search guide](https://github.com/WireCatLabs/whatsapp-cli/blob/main/docs/search.md)
- [Query language guide](https://github.com/WireCatLabs/whatsapp-cli/blob/main/docs/query-language.md)
- [MCP guide](https://github.com/WireCatLabs/whatsapp-cli/blob/main/docs/mcp.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON CLI output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can read local conversation data and perform account or messaging actions when authorized.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
