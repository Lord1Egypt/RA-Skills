## Description:

Send WhatsApp messages to other people or search/sync WhatsApp history via the wacli CLI (not for normal user chats).

This skill is ready for commercial/non-commercial use.

## Publisher:

[fianabates1](https://clawhub.ai/user/fianabates1)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to send WhatsApp messages to explicitly specified recipients and to sync, search, or backfill WhatsApp chat history through the wacli CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use wacli with access to WhatsApp login state and message history.

Mitigation: Install and authenticate wacli only when that level of WhatsApp access is acceptable for the user and environment.

Risk: The skill can send WhatsApp messages to direct chats or groups.

Mitigation: Require an explicit recipient and message text, and confirm both before sending.

Risk: The provided brew and go install methods can resolve to mutable wacli versions.

Mitigation: Review or pin the wacli version before deployment in environments that require reproducible dependencies.

## Reference(s):

- [wacli homepage](https://wacli.sh)
- [ClawHub skill page](https://clawhub.ai/fianabates1/skills/test-wa)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wacli commands, recipient confirmation guidance, sync/search commands, and JSON-output parsing guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
