## Description:

Worth It tracks per-project profitability for OpenClaw agents by logging money saved, money earned, time saved, and manual costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[storyscriptapp](https://clawhub.ai/user/storyscriptapp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to recognize explicit value logging commands and send saved, earned, time, and cost entries to a local Worth It service for project-level ROI tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Value-log descriptions may include sensitive client names, confidential project details, or private financial context.

Mitigation: Use generic descriptions or omit sensitive details unless storing them in the local Worth It dashboard is acceptable.

Risk: The skill sends value-log commands to a local Worth It API, so entries may fail or be incomplete if the local service or project configuration is unavailable.

Mitigation: Confirm the local Worth It service and project settings before relying on logged profitability totals.

## Reference(s):

- [ClawHub Worth It skill page](https://clawhub.ai/storyscriptapp/skills/worth-it)
- [ClawMart Worth It listing](https://www.shopclawmart.com/listings/worth-it-agent-profitability-tracker-961a92fb)

## Skill Output:

**Output Type(s):** [Guidance, Text, API Calls]

**Output Format:** [Markdown guidance with inline command examples and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends only explicit value-log commands to a local Worth It API when configured.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
