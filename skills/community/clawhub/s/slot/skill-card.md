## Description:

Use when managing time slots, creating schedule blocks, detecting booking conflicts, exporting calendars, or applying scheduling templates for appointments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, list, check, and export local schedule blocks for appointments, work sessions, templates, and booking conflict checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores schedule details locally and can use a caller-provided SLOT_DATA_DIR.

Mitigation: Use a private, trusted data directory and avoid shared or attacker-writable SLOT_DATA_DIR locations.

Risk: CSV or iCalendar exports may carry labels or categories that originated from untrusted input.

Mitigation: Review exported files before opening or importing them into spreadsheet or calendar software.

Risk: Running the local shell script with elevated privileges could increase the impact of file-permission weaknesses.

Mitigation: Run the skill as a normal user and keep generated schedule files in user-owned storage.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xueyetianya/skills/slot)
- [Publisher Profile](https://clawhub.ai/user/xueyetianya)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and local CSV or iCalendar exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and reads local schedule data under ~/.slot-manager by default, or SLOT_DATA_DIR when configured.]

## Skill Version(s):

2.0.3 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
