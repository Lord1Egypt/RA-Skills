## Description:

Timezone conversion, current time, date arithmetic, and epoch conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutthemustard](https://clawhub.ai/user/cutthemustard)

### License/Terms of Use:


## Use Case:

Developers and external agents use this skill to get current times, convert timestamps between time zones, perform date arithmetic, and convert between ISO 8601 dates and Unix epoch timestamps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests are sent to a third-party time API and may expose the user's IP address in rate-limited form.

Mitigation: Avoid sending sensitive event details in time strings and review the service privacy posture before production use.

Risk: Usage beyond the free tier may incur paid-tier charges.

Mitigation: Track expected request volume and confirm payment behavior before relying on the skill for high-volume workflows.

## Reference(s):

- [Time Convert ClawHub page](https://clawhub.ai/cutthemustard/skills/time-convert)
- [Time API homepage](https://time.agentutil.net)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with REST API examples and JSON response descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced API returns JSON containing ISO time, Unix time, timezone, day of week, DST status, request ID, and service URL.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
