## Description:

Reads macOS Notification Center titles and bodies and writes notification exports and work summaries into OpenClaw memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gift-is-coding](https://clawhub.ai/user/gift-is-coding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to capture recent macOS notifications, store them as local memory, and generate work-focused summaries and action items for an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notification titles and bodies may contain sensitive messages, calendar details, approvals, or codes.

Mitigation: Install only when this local collection is acceptable, review generated memory regularly, and delete stored notification memory when it is no longer needed.

Risk: Recurring collection can retain sensitive notification content more broadly than a one-time run.

Mitigation: Prefer manual or narrowly filtered runs unless scheduled capture is necessary, and review any 30-minute cron setup before enabling it.

Risk: The skill requires macOS notification database access and may ask users to grant broad disk access to Python.

Mitigation: Grant the narrowest practical macOS permissions and avoid giving Full Disk Access to a general Python interpreter where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gift-is-coding/skills/temp-notification-reader)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text files with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include notification titles and bodies stored in local OpenClaw memory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
