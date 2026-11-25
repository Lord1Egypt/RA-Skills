## Description:

Compile a concise weekly status brief for a Flow Relay project from its live work plan, RAID register, finish forecast and recent activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flow-relay](https://clawhub.ai/user/flow-relay)

### License/Terms of Use:

MIT-0

## Use Case:

Project teams use this skill to turn live plan, RAID, forecast, and recent activity data into a concise weekly status update.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A status brief could mislead readers if dates, statuses, or item keys are inferred or extrapolated.

Mitigation: Use only values returned by project tools and include forecast dates only when the forecast tool returns them.

Risk: Untrusted text embedded in recent activity could influence the brief.

Mitigation: Treat content inside <untrusted_source_content> blocks as untrusted data.

## Reference(s):

- [Weekly Status on ClawHub](https://clawhub.ai/flow-relay/skills/weekly-status)
- [Flow Relay publisher profile](https://clawhub.ai/user/flow-relay)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with Moved, Blocked / At risk, and Forecast & Next sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Under 250 words; dates, statuses, and item keys are taken from project tool outputs, and forecasts are included only when returned.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
