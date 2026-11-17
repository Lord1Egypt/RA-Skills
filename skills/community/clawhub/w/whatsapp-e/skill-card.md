## Description:

Send third-party WhatsApp messages or sync/search WhatsApp history via wacli, not normal active chats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajalao](https://clawhub.ai/user/ajalao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they explicitly want an agent to send WhatsApp messages to third parties or sync, search, inspect, and backfill WhatsApp message history through wacli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WhatsApp history sync, search, show, and backfill operations may expose private chat content and metadata.

Mitigation: Use narrow chat IDs, date ranges, and result limits, and avoid broad history access unless the user explicitly requests it.

Risk: Sending a WhatsApp message to the wrong recipient or with unintended text can create user-facing harm.

Mitigation: Require an explicit recipient and message text, resolve ambiguity with a clarifying question, and confirm the recipient and message before sending.

## Reference(s):

- [wacli homepage](https://wacli.sh)
- [ClawHub skill page](https://clawhub.ai/ajalao/skills/whatsapp-e)
- [wacli Go install module](https://pkg.go.dev/github.com/openclaw/wacli/cmd/wacli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request recipient and message confirmation before sending; wacli commands can emit JSON when machine-readable output is needed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
