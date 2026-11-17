## Description:

Monitors a selected Southwest Airlines flight segment for newly available preferred seats and alerts the agent without changing the reservation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdm0830](https://clawhub.ai/user/jdm0830)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and their agents use this skill to watch a particular Southwest flight for an open window, aisle, or exit-row seat and receive an alert when one appears. The traveler makes any seat change themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent logged-in Southwest browser profile gives the monitor access to account and reservation details.

Mitigation: Use a dedicated Southwest-only Chrome profile and grant access only if comfortable with an ongoing signed-in session.

Risk: Saved account credentials or an exposed browser debugging port can increase account-access risk.

Mitigation: Avoid saving the password unless you accept that risk, and keep the browser debugging port bound to localhost.

Risk: Optional background persistence could keep the logged-in browser and monitor running after reboot.

Mitigation: Review or disable any optional systemd persistence before enabling it.

## Reference(s):

- [Southwest Seat Monitor on ClawHub](https://clawhub.ai/jdm0830/skills/southwest-seat-monitor)
- [Patchright browser automation](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Agent alerts and JSON seat snapshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only seat-availability and session-health updates; no automatic seat changes.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
