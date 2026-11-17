## Description:

Ensure real-time accurate scheduling and planning across UTC, server time, NTP-sourced time, user local time, and arbitrary time zones.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cccat6](https://clawhub.ai/user/cccat6)

### License/Terms of Use:


## Use Case:

Developers and agent operators use TrueTime to compute UTC-first target times for reminders, cron planning, calendar coordination, deadlines, and cross-timezone scheduling. It helps agents preserve the user's exact requested duration, handle DST and timezone ambiguity, and report both relative and absolute interpretations before time-sensitive execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional NTP mode can depend on a network path and public NTP server that the installer may not control.

Mitigation: Use server-clock mode for normal calculations, or enable NTP only when the network path and selected NTP server are trusted; avoid NTP mode for security-critical scheduling unless that trust is established.

Risk: Time-sensitive execution can be wrong when timezone context, DST overlap, or local-time assumptions are ambiguous.

Mitigation: Compute the canonical target in UTC first, use IANA timezone names, ask for clarification when timezone context can change the result, and verify the requested delta before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON helper-script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports UTC, user timezone, server timezone, delta, time source, optional NTP server, Chinese lunar fields, and assumptions for time-sensitive actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
