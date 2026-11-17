## Description:

Query UK National Rail live boards, delays, cancellations, platforms, and service details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonjohnedwards-hub](https://clawhub.ai/user/simonjohnedwards-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and agents checking UK rail journeys use this skill to find live station departures and arrivals, platforms, delays, cancellations, and disruption notices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live board queries require an API key and send requests to the Rail Data service.

Mitigation: Provide a scoped key through the environment, keep it private, and allow outbound requests to api1.raildata.org.uk only when live data is needed.

## Reference(s):

- [Rail Live Boards on ClawHub](https://clawhub.ai/simonjohnedwards-hub/skills/rail-live-boards)
- [Rail Data live arrival and departure board API](https://api1.raildata.org.uk/1010-live-arrival-and-departure-boards-arr-and-dep1_1/LDBWS/api/20220120/GetArrDepBoardWithDetails/{crs})

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Live board JSON or a concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes service times, platforms, disruption notices, and cancellation or delay details when available.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
