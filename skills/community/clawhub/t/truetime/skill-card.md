## Description: <br>
TrueTime helps agents calculate and verify time-sensitive schedules across UTC, server time, NTP-sourced time, user local time, arbitrary IANA time zones, and Chinese lunar date context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cccat6](https://clawhub.ai/user/cccat6) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use TrueTime for reminders, cron planning, calendar conversions, cross-timezone coordination, deadline calculations, and other time-sensitive workflows where exact duration and timezone handling matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional NTP mode sends a time query to the selected NTP server, which can observe that it was queried. <br>
Mitigation: Use server time by default, and use only default or otherwise trusted NTP servers when NTP synchronization is explicitly needed. <br>
Risk: Missing or ambiguous timezone context can change the target time, especially during DST transition windows. <br>
Mitigation: Require IANA timezone names or explicit offsets, and stop for clarification when ambiguity can materially affect the scheduled time. <br>
Risk: The bundled helper requires a Node.js runtime, which may not exist in every sandbox image. <br>
Mitigation: Run the skill in a sandbox with Node.js available or install Node.js before invoking the helper. <br>


## Reference(s): <br>
- [TrueTime ClawHub release page](https://clawhub.ai/cccat6/truetime) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON fields from the bundled Node helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Time calculation outputs include UTC, server timezone, optional user timezone, deltas, time source, optional NTP server, lunar calendar fields, and assumptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
