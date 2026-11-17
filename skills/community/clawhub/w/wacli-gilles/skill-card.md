## Description:

Send WhatsApp messages to other people or search/sync WhatsApp history via the wacli CLI (not for normal user chats).

This skill is ready for commercial/non-commercial use.

## Publisher:

[gillescv](https://clawhub.ai/user/gillescv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when a user explicitly asks to contact someone on WhatsApp, or when they need to sync, search, or backfill WhatsApp history through the wacli CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wacli CLI can access WhatsApp login state and message history.

Mitigation: Review the CLI before installing, prefer a pinned and reviewed version, and protect or remove local WhatsApp data when it is no longer needed.

Risk: The skill can send outbound WhatsApp messages.

Mitigation: Require an explicit recipient and message text, then confirm both before sending.

Risk: Continuous sync can keep local WhatsApp history available to the CLI.

Mitigation: Run continuous sync only when intentionally needed and stop it after the requested task is complete.

## Reference(s):

- [wacli homepage](https://wacli.sh)
- [ClawHub skill page](https://clawhub.ai/gillescv/skills/wacli-gilles)
- [ClawHub publisher profile](https://clawhub.ai/user/gillescv)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use JSON output from wacli when parsing CLI results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
