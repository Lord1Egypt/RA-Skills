## Description:

Reads Raspberry Pi boot logs through JishuBuddy UART sessions and helps diagnose wiring, permissions, baud mismatches, and disconnects while requiring approval for writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-aijishu](https://clawhub.ai/user/bowen-aijishu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and device operators use this skill when network or SSH access to a Raspberry Pi is unavailable and they need a bounded serial boot transcript with diagnosis of connection, permission, baud, encoding, or transport issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing JishuBuddy changes the operator machine by writing to the npm global prefix.

Mitigation: Run the check mode first, show the exact detected target version and install command, and install only the approved version after explicit approval.

Risk: Opening a serial port or sending serial input can affect the attached device or expose device output.

Mitigation: Treat port access, bounded reads, and writes as separate approvals; start with read-only capture and require approval before any write.

Risk: Incorrect voltage, wiring, permissions, or baud settings can produce misleading results or hardware risk.

Mitigation: Verify board revision, voltage level, ground, adapter path, owning group, and baud/framing before diagnosis; do not guess pinouts or bypass access controls.

Risk: JishuBuddy telemetry may send activation or heartbeat events by default.

Mitigation: Set JISHUBUDDY_TELEMETRY_DISABLED=true before launch when the user does not want telemetry.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bowen-aijishu/skills/raspberry-pi-serial-rescue)
- [Source homepage from metadata](https://github.com/x-aijishu/jishubuddy-skills/tree/main/raspberry-pi-serial-rescue)
- [JishuBuddy npm package](https://www.npmjs.com/package/jishubuddy)
- [Installation helper](scripts/install-jishubuddy.sh)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and structured diagnostic findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bounded serial-capture guidance, connection settings, sanitized evidence summaries, and confirmed, unconfirmed, or blocked finding statuses.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
