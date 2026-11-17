## Description:

Send WhatsApp messages to other people or search/sync WhatsApp history via the wacli CLI (not for normal user chats).

This skill is ready for commercial/non-commercial use.

## Publisher:

[sieyer](https://clawhub.ai/user/sieyer)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to send WhatsApp messages to third parties when explicitly requested, and to sync or search WhatsApp history through wacli. It is not intended for routine chats with the user over WhatsApp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external wacli CLI can access WhatsApp login state and message history.

Mitigation: Install only when the wacli project is trusted, and use a separate store path when limiting where session data is kept.

Risk: The skill can send WhatsApp messages to direct or group recipients.

Mitigation: Require an explicit recipient and message text, confirm both before sending, and ask a clarifying question when anything is ambiguous.

Risk: History backfill depends on the user's phone being online and may return best-effort results.

Mitigation: Treat backfill results as incomplete unless verified by subsequent sync or search.

## Reference(s):

- [wacli homepage](https://wacli.sh)
- [ClawHub skill page](https://clawhub.ai/sieyer/skills/whats-1-0-0)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use machine-readable JSON from wacli when parsing command output is requested.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
