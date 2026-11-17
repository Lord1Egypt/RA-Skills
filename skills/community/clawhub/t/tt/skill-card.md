## Description:

Send WhatsApp messages to other people or search/sync WhatsApp history via the wacli CLI (not for normal user chats).

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafay0313](https://clawhub.ai/user/rafay0313)

### License/Terms of Use:


## Use Case:

External users and developers use this skill when they explicitly need an agent to send WhatsApp messages to third parties, search chats, sync message history, or backfill WhatsApp history through wacli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send WhatsApp messages or files to individuals or groups through wacli.

Mitigation: Require an explicit recipient and message or file, ask for clarification when ambiguous, and confirm the recipient and content before sending.

Risk: Using wacli requires access to the user's WhatsApp account and local ~/.wacli store.

Mitigation: Install only from trusted upstream sources and use the skill only when comfortable granting that WhatsApp and local-store access.

## Reference(s):

- [wacli homepage](https://wacli.sh)
- [ClawHub skill page](https://clawhub.ai/rafay0313/skills/tt)
- [ClawHub publisher profile](https://clawhub.ai/user/rafay0313)

## Skill Output:

**Output Type(s):** [shell commands, guidance, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wacli command examples for authentication, sync, search, backfill, and sending messages or files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
