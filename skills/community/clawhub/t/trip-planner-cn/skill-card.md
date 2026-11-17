## Description:

Plans one-way and round-trip travel in China using flights, trains, nearby airports, time constraints, and detailed itinerary timelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doushen-cloud](https://clawhub.ai/user/doushen-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to compare flight, train, airport-transfer, and driving options for one-way or round-trip itineraries in China under concrete timing constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trip locations, dates, timing constraints, and itinerary details may be shared with travel and map services used by the skill.

Mitigation: Provide only the trip details needed for planning, avoid unnecessary personal information, and configure the Baidu Maps API key only when driving-time lookups are desired.

Risk: Incomplete or stale travel results can lead to unsuitable itinerary recommendations.

Mitigation: Verify that flight and train results are complete before making decisions, and clearly label historical or estimated schedules when live data is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/doushen-cloud/skills/trip-planner-cn)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown itinerary summaries with comparison tables and timelines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include estimated driving times when the Baidu Maps API key is not configured.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
