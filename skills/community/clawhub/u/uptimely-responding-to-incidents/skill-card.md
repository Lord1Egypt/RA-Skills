## Description:

Helps users respond to Uptimely incidents by declaring and updating incidents and alerts, and running on-demand monitor checks, with confirmation before each action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Incident responders and operators use this skill to investigate Uptimely monitors, incidents, and alerts, then confirm individual actions such as declaring or resolving an incident, raising an alert, or checking a monitor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confirmed incident or alert changes can notify people or change a public status page.

Mitigation: Review the affected project, target, proposed change, and recipients; require a separate explicit confirmation for each action.

Risk: On-demand monitor checks make real requests to monitored URLs.

Mitigation: Confirm the monitor and intended check before running a probe.

## Reference(s):

- [Responding To Incidents on ClawHub](https://clawhub.ai/devino/skills/uptimely-responding-to-incidents)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action confirmations and incident, alert, or monitor-check results.]

## Skill Version(s):

1.0.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
