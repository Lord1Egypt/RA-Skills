## Description:

Fetch productivity analytics from the RescueTime API for screen time, productivity score, app usage, time tracking, and daily or weekly activity reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rusynandriy](https://clawhub.ai/user/rusynandriy)

### License/Terms of Use:


## Use Case:

External users use this skill to ask an agent for RescueTime productivity analytics, including activity rankings, category breakdowns, hourly productivity, and daily summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The RescueTime API key could be exposed through shared files, repositories, or logs.

Mitigation: Store the API key in a protected environment variable or secret manager and keep it out of shared repositories and logs.

Risk: Detailed app, site, and activity reports can reveal private work patterns and browsing activity.

Mitigation: Ask the agent to confirm before fetching detailed app or site-level reports for broad or ambiguous requests.

## Reference(s):

- [ClawHub RescueTime skill page](https://clawhub.ai/rusynandriy/skills/rescuetime)
- [RescueTime API key management](https://www.rescuetime.com/anapi/manage)
- [RescueTime analytic data endpoint](https://www.rescuetime.com/anapi/data?key=API_KEY&format=json&perspective=rank&restrict_kind=activity)
- [RescueTime daily summary feed endpoint](https://www.rescuetime.com/anapi/daily_summary_feed?key=API_KEY)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include RescueTime API responses and converted time totals; users should treat returned activity data as private.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
