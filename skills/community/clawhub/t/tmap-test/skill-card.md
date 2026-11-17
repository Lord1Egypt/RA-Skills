## Description:

Tencent Maps location services skill for POI search, nearby search, route planning, travel planning, trail visualization, and map data visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qfish](https://clawhub.ai/user/qfish)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to answer map-related requests, generate Tencent Maps links, retrieve structured POI and route data, and visualize travel or trail data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Map searches, addresses, coordinates, travel plans, and trail data links may be sent to Tencent Maps during normal use.

Mitigation: Use the skill only when sharing that location or itinerary data with Tencent Maps is acceptable.

Risk: Returned URLs may contain Tencent Maps API keys, precise coordinates, or private itinerary data.

Mitigation: Avoid logging or sharing generated URLs, and redact key, coordinate, itinerary, and trail data parameters before redistribution.

Risk: Tencent Maps API keys used with this skill can be exposed through generated links or command output.

Mitigation: Use a restricted, temporary Tencent Maps API key with low quotas and rotate it after testing.

## Reference(s):

- [ClawHub tmap-test Skill Page](https://clawhub.ai/qfish/skills/tmap-test)
- [Tencent Location Services Web Service Overview](https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview)
- [Tencent Location Services](https://lbs.qq.com/)
- [Tencent Place Search API Documentation](https://lbs.qq.com/service/webService/webServiceGuide/webServiceSearch)
- [Keyword Search Scenario](references/scene1-keyword-search.md)
- [Nearby Search Scenario](references/scene2-nearby-search.md)
- [POI Search Scenario](references/scene3-poi-search.md)
- [Route Planning Scenario](references/scene4-route-planning.md)
- [Travel Planner Scenario](references/scene5-travel-planner.md)
- [Trail Map Scenario](references/scene7-trail-map.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, JSON, Guidance]

**Output Format:** [Markdown with Tencent Maps links, inline shell commands, and structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Tencent Maps URLs containing API keys, coordinates, addresses, itinerary details, or trail data links.]

## Skill Version(s):

1.0.12 (source: server release metadata; artifact frontmatter and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
