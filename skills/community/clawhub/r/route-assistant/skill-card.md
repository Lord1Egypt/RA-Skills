## Description:

Route Assistant helps agents plan travel routes with Amap by comparing driving, transit, taxi, and walking options, filtering infeasible choices, and warning about timing conflicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chandler0714](https://clawhub.ai/user/chandler0714)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to compare route options between locations, choose feasible transport modes, and surface timing reminders for trips that involve train or flight schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad route and location triggers may activate the skill on general travel or address queries.

Mitigation: Review generated route guidance before acting, especially when the query was not intended as a route-planning request.

Risk: Route planning can expose sensitive home, work, or travel locations through the disclosed map-provider workflow.

Mitigation: Avoid sharing sensitive locations unless that processing is acceptable for the deployment context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chandler0714/skills/route-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown tables with concise recommendations and reminders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include route distances, estimated durations, transport-mode filtering, and timing conflict warnings.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
