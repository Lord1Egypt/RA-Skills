## Description:

Marks OpenClaw sessions with visible sidebar unread or failure badges that include an attention icon and timestamp note, then clears them through OpenClaw's native read lifecycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pondsi](https://clawhub.ai/user/pondsi)

### License/Terms of Use:

MIT-style with mandatory attribution

## Use Case:

Developers and OpenClaw operators use this skill to set and renew visible unread or failure markers on OpenClaw session rows so completed or failed replies remain visible until read.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify OpenClaw session status badges and may renew those badges on a schedule.

Mitigation: Install it only where unread badge updates are desired, and schedule the keepalive job intentionally.

Risk: The skill writes local bookkeeping to unread-marks.json.

Mitigation: Use OPENCLAW_STATE_DIR to place the state file in an expected location and review local retention expectations.

Risk: The helper is designed to fail silently so notification failures do not interrupt the reported workflow.

Mitigation: When badge delivery is operationally important, verify session status with OpenClaw session listing or keepalive dry-run output.

Risk: The bundled license requires attribution even though registry metadata reports MIT-0.

Mitigation: Review the bundled LICENSE before redistribution and preserve Pondsi attribution as required.

## Reference(s):

- [UnreadBadgeOpenClaw ClawHub page](https://clawhub.ai/pondsi/skills/unreadbadgeopenclaw)
- [OpenClaw](https://openclaw.ai)
- [Internals: sidebar marks](references/internals.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell command examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Node command examples for marking sessions and scheduling keepalive renewal.]

## Skill Version(s):

1.1.4 (source: server release metadata and CHANGELOG, released 2026-09-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
