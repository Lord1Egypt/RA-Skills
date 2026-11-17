## Description:

Plans commute route options that detour through vehicle inspection stations by using AMap driving routes, live traffic estimates, and candidate station data to produce Top N itinerary plans with timelines and turn-by-turn details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shengbinxu](https://clawhub.ai/user/shengbinxu)

### License/Terms of Use:

MIT-0

## Use Case:

Drivers and personal-assistant agents use this skill to compare vehicle inspection stops along a home-to-work route and generate a concise ranked travel plan. It is most relevant when the user has a fixed origin, destination, departure time, expected inspection duration, and candidate station list.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Home and workplace addresses, route destinations, and the AMap API key are sent to AMap for route calculation.

Mitigation: Review data-sharing expectations before using real addresses, use a restricted and rotatable API key, and avoid command-line key entry when possible.

Risk: The README claims the tool does not upload user data, which conflicts with the security evidence for AMap API calls.

Mitigation: Treat the no-upload claim as inaccurate and disclose the external AMap requests before installation or use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shengbinxu/skills/vehicle-inspection-route-planner)
- [AMap Open Platform Web Service key setup](https://console.amap.com/dev/key/app)
- [Traffic Safety Integrated Service Management Platform](https://122.gov.cn/)
- [Traffic Management 12123 app](https://122.gov.cn/#/app)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with ranked tables, itinerary timelines, and route instruction code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-supplied AMap Web Service API key, origin and destination addresses, departure time, inspection duration, city, station CSV, and Top N count.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
